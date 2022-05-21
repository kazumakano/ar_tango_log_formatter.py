# ar_tango_log_formatter.py
This is Python module to transform coordinate, resample frequency and convert logs format from CSV exported by [AR Logger](https://github.com/kazumakano/ARLogger) and [Tango Logger](https://bitbucket.org/uclabnu/tangologger/src/master/) to CSV and pickle able to be interpreted by [particle_filter.py](https://github.com/kazumakano/particle_filter.py).

## Usage
### pull_tango_logs.ps1
You can pull tango log files from your Android smartphone with this script.
You can filter datetime of log files and specify directory to put them.
Default directory is `raw/`.
```sh
.\pull_logs.ps1 -Datetime LOG_DATETIME [-Dir PATH_TO_DIR]
```
