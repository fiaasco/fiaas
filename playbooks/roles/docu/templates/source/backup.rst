Backup
======

Backup is automatically created on {{ groups.backupservers|join(',') }}.

The retentionsettings are:

* {{ retention.daily }} daily backups are kept
* {{ retention.weekly }} weekly backups are kept
* {{ retention.monthly }} monthly backups are kept
* {{ retention.yearly }} yearly backups are kept

