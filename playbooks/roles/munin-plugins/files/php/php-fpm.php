#!/usr/bin/php
<?php

/**
* @author realhidden
* @author Devlopnet
* @author MorbZ
* @fixed for fiaas.co :)
* @licence CC
*/

//grab all pools
exec('find /etc/php5/fpm/pool.d/*.conf -type f -printf "%f\n"',$allpool);
foreach($allpool as &$pool)
{
   $pool=substr($pool,0,-5);
   $pool=preg_replace('/\./', '_', $pool); // munin doesn't like dots in poolnames!
}

//grab processes
exec("ps -eo %cpu,etime,rss,command | grep php-fpm", $result);

//iterate through processes
$groups = array();
foreach ($result as $line) {
	//split fields
	$line = trim($line);
	$args = preg_split('/\s+/', $line);
    if (strpos($args[3], 'php-fpm') === false) {
        continue;
    }
    list($cpu, $time, $ram, $type, $poolWord, $poolName) = $args;
    $poolName = preg_replace('/\./', '_', $poolName); // munin doesn't like dots in poolnames!

	//which group
    if ($poolWord == 'master') {
    	continue;
    }
    $groupName = $poolName;

	//add group
    if (!isset($groups[$groupName])) {
        $groups[$groupName] = array(
        	'count' => 0,
        	'memory' => 0,
        	'cpu' => 0,
        	'time' => 0
        );
    }
	
	//add values
	$groups[$groupName]['count']++;
	$groups[$groupName]['cpu'] += $cpu;
	$groups[$groupName]['time'] += timeToSeconds($time);
	$groups[$groupName]['memory'] += $ram / 1024;
}

//add missing pools
foreach($allpool as $groupName)
{
	if (isset($groups[$groupName]))
		continue;

	$groups[$groupName] = array(
                'count' => 0,
                'memory' => 0,
                'cpu' => 0,
                'time' => 0
        );
}

//check args
if(!isset($argv) || !isset($argv[0])) {
	die("Error: No Plugin name provided\n");
}
$fileCalled = basename($argv[0]);
$isConfig = isset($argv[1]) && $argv[1] == 'config';

//which plugin?
switch ($fileCalled) {
// ------------------------------------------------------		
	case 'php-fpm-memory':
// ------------------------------------------------------
		$elements = array();
		foreach ($groups as $name=>$array) {
			if($array['count'] > 0) {
				$ramMb = $array['memory'] / $array['count'];
			} else {
				$ramMb = $array['memory'];
			}
			$label = 'Pool ' . $name;
			$elements[$name] = array(
				'label'	=>	$label,
				'type'	=>	'GAUGE',
				'value'	=>	$ramMb
			);
		}
		$config = array(
			'params' => array(
				'graph_title' => 'PHP-FPM Average Process Memory',
				'graph_vlabel' => 'MB'
			),
			'elements'	=>	$elements
		);	
		break;
// ------------------------------------------------------		
	case 'php-fpm-cpu':
// ------------------------------------------------------
		$elements = array();
		foreach ($groups as $name=>$array) {
			$cpu = $array['cpu'];
			$label = 'Pool ' . $name;
			$elements[$name] = array(
				'label'	=>	$label,
				'type'	=>	'GAUGE',
				'value'	=>	$cpu
			);
		}
		$config = array(
			'params' => array(
				'graph_title' => 'PHP-FPM CPU',
				'graph_vlabel' => '%',
				'graph_scale' => 'no'
			),
			'elements'	=>	$elements
		);	
		break;
// ------------------------------------------------------		
	case 'php-fpm-count':
// ------------------------------------------------------
		$elements = array();
		foreach ($groups as $name=>$array) {
			$label = 'Pool ' . $name;
			$elements[$name] = array(
				'label'	=>	$label,
				'type'	=>	'GAUGE',
				'value'	=>	$array['count']
			);
		}
		$config = array(
			'params' => array(
				'graph_title' => 'PHP-FPM Processes',
				'graph_vlabel' => 'processes'
			),
			'elements'	=>	$elements
		);	
		break;
// ------------------------------------------------------		
	case 'php-fpm-time':
// ------------------------------------------------------
		$elements = array();
		foreach ($groups as $name=>$array) {
			$time = round($array['time'] / $array['count']);
			$label = 'Pool ' . $name;
			$elements[$name] = array(
				'label'	=>	$label,
				'type'	=>	'GAUGE',
				'value'	=>	$time
			);
		}
		$config = array(
			'params' => array(
				'graph_title' => 'PHP-FPM Average Process Age',
				'graph_vlabel' => 'seconds',
				'graph_scale' => 'no'
			),
			'elements'	=>	$elements
		);	
		break;
// ------------------------------------------------------
	default:
		die("Error: Unrecognized Plugin name $fileCalled\n");
}

//output
ksort($config['elements']);
if ($isConfig) {
	//graph params
	echo "graph_category PHP-FPM\n";
	foreach($config['params'] as $key=>$value) {
		echo $key . ' ' . $value . "\n";
	}
	
	//element params
	foreach($config['elements'] as $element=>$data) {
		foreach ($data as $key=>$value) {
			if ($key == 'value') continue;
			echo $element . '.' . $key . ' ' . $value . "\n";
		}
	}
} else {
	//element values
	foreach ($config['elements'] as $pool=>$element) {
		echo $pool . '.value ' . $element['value'] . "\n";
	}
}

//functions
function timeToSeconds ($time) {
	$seconds = 0;
	
	//days
	$parts = explode('-', $time);
	if(count($parts) == 2) {
		$seconds += $parts[0] * 86400;
		$time = $parts[1];
	}
	
	//hours
	$parts = explode(':', $time);
	if(count($parts) == 3) {
		$seconds += array_shift($parts) * 3600;
	}
	
	//minutes/seconds
	$seconds += $parts[0] * 60 + $parts[1];
	return $seconds;
}
