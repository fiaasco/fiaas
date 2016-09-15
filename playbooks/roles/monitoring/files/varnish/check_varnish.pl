#!/usr/bin/perl

# check_varnish.pl v1.0, 29/4/2011
# Written by Andy Sykes <andy@tinycat.co.uk>
#
# This plugin monitors the counters returned by varnishstat.
# It also returns perfdata for each of the counters it monitors.
# See the --help option for information on usage.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

use strict;
use warnings;

use Data::Dumper;
use Getopt::Long;

# Parse command line options
my @specs;
my ( $list, $help );
GetOptions(
    "spec|s=s" => \@specs,
    "list|l"   => \$list,
    "help|h"   => \$help
);

# Print help if they asked for it
if ($help) {
    print_help();
}

if ($list) {
    print_list();
}

# Global vars that hold the parsed varnishstat output
my %stats;
my %stats_help;

my @perfdata;         # Holds perfdata output blocks
my @nagios_output;    # Holds the text returned to Nagios
my $status_flag = 0
  ; # Nagios plugin return status (0 = OK, 1 = WARNING, 2 = CRITICAL, 3 = UNKNOWN)

if ( scalar(@specs) == 0 ) {
    print_help();
}

parse_varnishstat();

foreach (@specs) {

    my ( $counter, $warn, $crit, $direction ) = split( /,/, $_, 4 );
    my $has_ranges =
      0;  # Indicates if a given spec option has 'range' parameters (crit, warn)

    # Validate the spec option

# Must either have both warn and crit values, or leave the warn and crit specifications blank
    if ( defined($crit) and ( not defined($warn) ) ) {
        return_error(
"Spec option $_ is bad: you must specify either warn & crit values, or none at all"
        );
    }

    if ( defined($warn) and ( not defined($crit) ) ) {
        return_error(
"Spec option $_ is bad: you must specify either warn & crit values, or none at all"
        );
    }

    # Make sure the warn and crit values are numeric (and integer)
    # Check the spec option includes the direction to warn in
    if ( defined($crit) and defined($warn) ) {

        $direction = 'u' if not defined($direction);
        $direction =~ /^d$|^u$/
          or
          return_error("The last component of the spec option must be u or d");
        $warn =~ /\d+/
          or return_error(
            "Not a valid spec option for counter '$_' - warn is not a number");
        $crit =~ /\d+/
          or return_error(
            "Not a valid spec option for counter '$_' - crit is not a number");
        $has_ranges = 1;

    }

    # Make sure the counter they want to monitor actually exists
    return_error("Not a valid counter in spec option - $counter")
      if not defined( $stats{$counter} );

    # The spec option is valid - let's process it

    # Retrieve the counter's value
    my $value = $stats{$counter};

  # Generate perfdata output - include warn + crit values if they were specified
    my $perfdata_string;
    if ( defined($warn) and defined($crit) ) {
        $perfdata_string = "$counter=$value;$warn;$crit;;";
    }
    else {
        $perfdata_string = "$counter=$value;;;;";
    }

    # Store this perfdata output
    push @perfdata, $perfdata_string;

    # Produce text output if we're over warn or crit values
    my $nagios_text;
    if ($has_ranges) {
        if ( $direction eq 'u' ) {
            if ( ( $value > $warn ) and ( $value < $crit ) ) {
                push @nagios_output, "Counter '$counter' is over warn value";
                $status_flag = 1 if $status_flag < 1;
            }
        }
        elsif ( $direction eq 'd' ) {
            if ( ( $value < $warn ) and ( $value > $crit ) ) {
                push @nagios_output, "Counter '$counter' is under warn value";
                $status_flag = 1 if $status_flag < 1;
            }
        }

        if ( $direction eq 'u' ) {
            if ( $value > $crit ) {
                push @nagios_output, "Counter '$counter' is over crit value";
                $status_flag = 2 if $status_flag < 2;
            }
        }
        elsif ( $direction eq 'd' ) {
            if ( $value < $crit ) {
                push @nagios_output, "Counter '$counter' is under crit value";
                $status_flag = 2 if $status_flag < 2;
            }
        }
    }
}

return_output();

# Turn the varnishstat output into a Perl hash
sub parse_varnishstat {

    open (VARNISHSTAT, "/usr/bin/varnishstat -1 |");

    while (<VARNISHSTAT>) {
        s/\s+/ /g;    # normalise spaces
        /(\S+) (\S+) \S+ (.*)/;
        $stats{$1}      = $2;
        $stats_help{$1} = $3;
    }

    # Add our special calculated counter 'cache_hit_percent'
    my $hit             = $stats{'cache_hit'};
    my $miss            = $stats{'cache_miss'};
    if ( ($hit + $miss) == 0 ) {
    	$stats{'cache_hit_percent'} = '-';
    }
    else {
		my $percent         = ( $hit / ( $hit + $miss ) ) * 100;
		my $rounded_percent = sprintf( "%.2f", $percent );
		$stats{'cache_hit_percent'} = $rounded_percent;
    }
}

sub return_error {
    my $error_msg = shift;
    print "UNKNOWN - $error_msg\n";
    exit 3;
}

sub return_output {

    my $output          = join( "; ", @nagios_output );
    my $perfdata_output = join( " ",  @perfdata );

    my $state;
    $state = "WARNING -"                   if $status_flag == 1;
    $state = "CRITICAL -"                  if $status_flag == 2;
    $state = "OK - all counters in range;" if $status_flag == 0;
    print "$state $output | $perfdata_output\n";
    exit $status_flag;

}

sub print_help {

    print <<EOF;

check_varnish.pl v1.0 - Nagios plugin for Varnish Cache monitoring

This Nagios plugin reads the output of 'varnishstat -1', which presents a one-shot
look at all the internal counters that Varnish has.

It can monitor any of these counters, and you can add warning & critical values for
each counter individually.

Additionally, there is one 'special' counter that doesn't exist in the varnishstat -1 output -
this is 'cache_hit_percent', which is calculated like this:
     
     cache_hit_percent = ( cache_hit / ( cache_hit + cache_miss ) ) * 100

Usage:

	check_varnish.pl --spec=[spec definition] --spec=[spec definition]
	check_varnish.pl --list
	check_varnish.pl --help

Options:

    --spec=[spec definition], -s [spec definition]
        Specifies which Varnish counter to monitor. A spec definition looks like this:
        
            --spec=counter_name,warnvalue,critvalue,[u|d]
        
        The "u" or "d" option at the end determines whether you want to consider the warn and crit values as met
        when the counter is above ('u' - up) or below ('d' - down) these values.
        e.g. for failed backend requests, you'd want to use the 'u' option (since more failed backend 
        requests is bad thing), but for the cache_hit_percent you'd want to use 'd', since you'll only
        warn when the cache isn't serving as many requests from memory as you'd expect. 
        
        If no 'u' or 'd' option is present, 'u' is assumed.
        
        If you don't want to set warn/crit values (i.e. just want perfdata output), then use this form:
        
            --spec=counter_name
        
        To monitor multiple counters, use multiple --spec options. e.g.
        
            --spec=counter_one --spec=counter_two,50,80 --spec=counter_three
        
        The plugin will return a WARNING state if any one counter is over its warn value, and no counters
        are over the critical value. Similarly, if any one counter is over its crit value, the plugin
        will return a CRITICAL state.
    
    --list
        This option prints a list of all the available Varnish counters available, and a brief
        description of what each one is for (taken from the varnishstat output).
    
    --help
        Displays this message.

check_varnish.pl comes with absolutely NO WARRANTY either implied or explicit
This program is licensed under the terms of the
GNU General Public License (check source code for details)

EOF

    exit 3;

}

sub print_list {

    # Print a list of all the varnishstat counters
    # and their (sometimes meaningless!) description
    parse_varnishstat();

    if ($list) {
        print "\nAvailable Varnish performance counters:\n\n";
        printf( "%-20s",   "Counter" );
        printf( "%-20s\n", "Description" );
        printf( "%-20s",   "---------------" );
        printf( "%-20s\n", "---------------" );

        # Print our special "cache_hit_ratio" counter info
        printf( "%-20s",   "cache_hit_percent" );
        printf( "%-20s\n", "Percent of requests served from cache" );

        foreach my $key ( keys %stats ) {
            next if $key eq "cache_hit_percent";
            my $info = $stats_help{$key};
            printf( "%-20s",   $key );
            printf( "%-20s\n", $info );
        }
        exit 3;
    }

}
