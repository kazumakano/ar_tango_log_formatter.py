import csv
import math
import os.path as path
import pickle
from datetime import datetime
from enum import Enum
from typing import Optional
import numpy as np
import yaml
from matplotlib import pyplot as plt
from scipy.interpolate import interp1d

class App(Enum):
    AR_APP = 0
    TANGO_APP = 1

def load_acc_log(file: str) -> tuple[np.ndarray, np.ndarray]:
    data = np.loadtxt(file, dtype=np.float64, delimiter=",")
    print(f"{path.basename(file)} has been loaded")

    return np.linalg.norm(data[:, 1:], axis=1), data[:, 0]

def load_ar_log(file: str) -> tuple[np.ndarray, np.ndarray]:
    pos = np.empty((0, 2), dtype=np.float64)
    ts = np.empty(0, dtype=datetime)

    with open(file) as f:
        for row in csv.reader(f):
            pos = np.vstack((pos, (-np.float64(row[1]), np.float64(row[3]))))
            ts = np.hstack((ts, datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S.%f")))

    return pos, ts

def load_pose_log(file: str) -> tuple[np.ndarray, np.ndarray]:
    data = np.loadtxt(file, dtype=np.float64, delimiter=",")[:, (0, 1, 3)]    # (timestamp, x, y)
    print(f"{path.basename(file)} has been loaded")

    return data[:, 1:], data[:, 0]

def rot(angle: float, pos: np.ndarray) -> np.ndarray:
    angle = math.radians(angle)
    return np.dot(np.array(((math.cos(angle), -math.sin(angle)), (math.sin(angle), math.cos(angle))), dtype=np.float64), pos.T).T

def loop_closure(pos: np.ndarray) -> np.ndarray:
    err = pos[-1] - pos[0]
    lc_pos = np.empty(pos.shape, dtype=np.float64)

    for i, p in enumerate(pos):
        lc_pos[i] = p - err * i / (len(pos) - 1)

    return lc_pos

def vis_pos_on_map(map_img: np.ndarray, pos: np.ndarray) -> None:
    plt.figure(figsize=(20, 20))
    plt.imshow(map_img, cmap="gray")
    plt.scatter(pos[:, 0], pos[:, 1], s=1)
    plt.scatter(pos[0, 0], pos[0, 1])

def _conv2datetime(ts: np.ndarray) -> np.ndarray:
    ts = ts.astype(object)

    for i, t in enumerate(ts):
        ts[i] = datetime.fromtimestamp(t)

    return ts.astype(datetime)

def vis_acc(acc: np.ndarray, ts: np.ndarray, begin: datetime, end: datetime) -> None:
    plt.figure(figsize=(16, 4))
    plt.xlim(left=begin, right=end)
    plt.plot(_conv2datetime(ts), acc)

def _resample_log(freq: float, pos: np.ndarray, ts: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    resampled_ts = np.arange(ts[0], ts[-1], step=1/freq, dtype=np.float64)

    resampled_pos = np.empty((len(resampled_ts), 2), dtype=np.float32)
    for i in range(2):
        resampled_pos[:, i] = interp1d(ts, pos[:, i])(resampled_ts)

    return resampled_pos, resampled_ts

def format_log(file_name: str, offset: float, pos: np.ndarray, ts: np.ndarray, freq: Optional[float] = None) -> None:
    if freq is not None:
        pos, ts = _resample_log(freq, pos, ts)
    ts = _conv2datetime(ts + offset)

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

def write_conf(angle: float, init_pos: tuple[int, int], mag: float, offset: float, app: App, file_name: str) -> None:
    with open(path.join(path.dirname(__file__), "../formatted/", file_name + ".yaml"), mode="w") as f:
        yaml.safe_dump({
            "angle": angle,
            "init_pos": init_pos,
            "mag": mag,
            "offset": offset,
            "app": app
        }, f)

    print(f"written to {file_name}.yaml")
