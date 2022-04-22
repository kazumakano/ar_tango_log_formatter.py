from __future__ import annotations
import csv
import os.path as path
import pickle
from datetime import datetime
from glob import iglob
from typing import Optional
import numpy as np
import yaml
from scipy.interpolate import interp1d


def _set_params(conf_file: str | None) -> None:
    global ROOT_DIR, FREQ

    ROOT_DIR = path.join(path.dirname(__file__), "../")

    if conf_file is None:
        conf_file = path.join(ROOT_DIR, "config/default.yaml")
    print(f"{path.basename(conf_file)} has been loaded")

    with open(conf_file) as f:
        FREQ = np.float32(yaml.safe_load(f)["freq"])

def _load_log(src_file: str) -> np.ndarray:
    return np.loadtxt(src_file, dtype=np.float64, delimiter=",")[:, (0, 1, 3)]    # (timestamp, x, y)

def _resample_log(data: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    resampled_ts = np.arange(data[0, 0], data[-1, 0] + 1/FREQ, step=1/FREQ, dtype=np.float64)

    resampled_pos = np.empty((len(resampled_ts), 2), dtype=np.float32)
    for i in range(2):
        resampled_pos[:, i] = interp1d(data[:, 0], data[:, i+1])(resampled_ts)

    return resampled_pos, resampled_ts

def _conv2datetime(ts: np.ndarray) -> np.ndarray:
    ts = ts.astype(object)

    for i, t in enumerate(ts):
        ts[i] = datetime.fromtimestamp(t)

    return ts.astype(datetime)

def _format_log(src_file: str, tgt_dir: str) -> None:
    data = _load_log(src_file)

    pos, ts = (data[:, 1:], data[:, 0]) if FREQ == 0 else _resample_log(data)
    ts = _conv2datetime(ts)

    tgt_file = path.join(tgt_dir, path.basename(src_file))
    with open(tgt_file, mode="w", newline="") as f:
        writer = csv.writer(f)
        t: datetime
        for i, t in enumerate(ts):
            writer.writerow((t.strftime("%Y-%m-%d %H:%M:%S.%f"), *pos[i]))

    print(f"written to inertial/{path.basename(tgt_file)}")

    tgt_file = path.splitext(tgt_file)[0] + ".pkl"
    with open(tgt_file, mode="wb") as f:
        pickle.dump((ts, pos), f)

    print(f"written to inertial/{path.basename(tgt_file)}")

def format_logs(src_file: Optional[str] = None, src_dir: Optional[str] = None, tgt_dir: Optional[str] = None) -> None:
    if tgt_dir is None:
        tgt_dir = path.join(ROOT_DIR, "formatted/")    # save to default target directory

    if src_file is None and src_dir is None:
        for src_file in iglob(path.join(ROOT_DIR, "raw/*.csv")):    # loop for default source directory
            _format_log(src_file, tgt_dir)

    elif src_file is None:
        for src_file in iglob(path.join(src_dir, "*.csv")):    # loop for specified source directory
            _format_log(src_file, tgt_dir)

    elif src_dir is None:
        _format_log(src_file, tgt_dir)

    else:
        raise Exception("'src_file' and 'src_dir' are specified at the same time")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--conf_file", help="specify config file", metavar="PATH_TO_CONF_FILE")
    parser.add_argument("--src_file", help="specify source file", metavar="PATH_TO_SRC_FILE")
    parser.add_argument("--src_dir", help="specify source directory", metavar="PATH_TO_SRC_DIR")
    parser.add_argument("--tgt_dir", help="specify target directory", metavar="PATH_TO_TGT_DIR")
    args = parser.parse_args()

    _set_params(args.conf_file)

    format_logs(args.src_file, args.src_dir, args.tgt_dir)
