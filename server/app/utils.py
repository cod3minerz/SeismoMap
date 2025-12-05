import numpy as np
from scipy.signal import hilbert, butter, filtfilt

def envelope(trace, sr):
    analytic_signal = hilbert(trace)
    return np.abs(analytic_signal)

def pick_arrival_by_envelope(env, sr, threshold_factor=5.0):
    threshold = np.mean(env) + threshold_factor * np.std(env)
    idx = np.argmax(env > threshold)
    return idx / sr

def bandpass_filter(data, sr, low=1.0, high=15.0, order=4):
    nyq = 0.5 * sr
    b, a = butter(order, [low/nyq, high/nyq], btype='band')
    return filtfilt(b, a, data)
