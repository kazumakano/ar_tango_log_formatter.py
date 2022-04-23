import csv
import os.path as path
import pickle
from datetime import datetime
from typing import Optional
import numpy as np
import yaml
from matplotlib import pyplot as plt
from scipy.interpolate import interp1d


def load_log(file: str) -> tuple[np.ndarray, np.ndarray]:
    data = np.loadtxt(file, dtype=np.float64, delimiter=",")[:, (0, 1, 3)]    # (timestamp, x, y)
    print(f"utility.py: {path.basename(file)} has been loaded")

    return data[:, 1:], data[:, 0]

def vis_on_map(map_img: np.ndarray, pos: np.ndarray) -> None:
    plt.figure(figsize=(20, 20))
    plt.imshow(map_img, cmap="gray")
    plt.scatter(pos[:, 0], pos[:, 1], s=1)

def _resample_log(freq: float, pos: np.ndarray, ts: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    resampled_ts = np.arange(ts[0], ts[-1], step=1/freq, dtype=np.float64)

    resampled_pos = np.empty((len(resampled_ts), 2), dtype=np.float32)
    for i in range(2):
        resampled_pos[:, i] = interp1d(ts, pos[:, i])(resampled_ts)

    return resampled_pos, resampled_ts

def _conv2datetime(ts: np.ndarray) -> np.ndarray:
    ts = ts.astype(object)

    for i, t in enumerate(ts):
        ts[i] = datetime.fromtimestamp(t)

    return ts.astype(datetime)

def format_log(file_name: str, pos: np.ndarray, ts: np.ndarray, freq: Optional[float] = None) -> None:
    if freq is not None:
        pos, ts = _resample_log(freq, pos, ts)
    ts = _conv2datetime(ts)

    tgt_file = path.join(path.dirname(__file__), "../formatted/", file_name + ".csv")
    with open(tgt_file, mode="w", newline="") as f:
        writer = csv.writer(f)
        t: datetime
        for i, t in enumerate(ts):
            writer.writerow((t.strftime("%Y-%m-%d %H:%M:%S.%f"), *pos[i]))

    print(f"written to {file_name}.csv")

    with open(path.splitext(tgt_file)[0] + ".pkl", mode="wb") as f:
        pickle.dump((ts, pos), f)

    print(f"written to {file_name}.pkl")

def write_conf(file_name: str, init_pos: tuple[int, int], mag: float) -> None:
    with open(path.join(path.dirname(__file__), "../formatted/", file_name + ".yaml"), mode="w") as f:
        yaml.safe_dump({
            "init_pos": init_pos,
            "mag": mag
        }, f)

    print(f"written to {file_name}.yaml")
