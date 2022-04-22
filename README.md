# tango_log_formatter.py
This is Python module to resample frequency and convert logs format from CSV exported by [Tango Logger](https://bitbucket.org/uclabnu/tangologger/src/master/) to CSV and pickle able to be interpreted by [particle_filter.py](https://github.com/kazumakano/particle_filter.py).

## Usage
### format_logs.py
You can run this formatter as following.
You can specify config file, source file or directory and target directory with flags.
`config/default.yaml` will be used if unspecified.
Default source and target directory are `raw/` and `formatted/`.
```sh
python script/format_logs.py [--conf_file PATH_TO_CONF_FILE] [--src_file PATH_TO_SRC_FILE] [--src_dir PATH_TO_SRC_DIR] [--tgt_dir PATH_TO_TGT_DIR]
```

### pull_logs.ps1
You can pull log files from your Android smartphone with this script.
You can filter datetime of log files and specify directory to put them.
Default directory is `raw/`.
```sh
.\pull_logs.ps1 -Datetime LOG_DATETIME [-Dir PATH_TO_DIR]
```
