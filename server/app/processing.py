import numpy as np
from obspy import read
from io import BytesIO
from .utils import envelope, pick_arrival_by_envelope
from .triangulation import locate_epicenter_grid

def load_trace_from_bytes(b: bytes):
    try:
        st = read(BytesIO(b))
        tr = st[0]
        data = tr.data.astype(float)
        sr = tr.stats.sampling_rate
        return data, float(sr)
    except Exception:
        arr = np.loadtxt(BytesIO(b))
        return arr.astype(float), 100.0

def process_three_stations(stations_meta, files_bytes, velocity_km_s=6.0, fft_max_freq=10.0):
    traces = []
    for b in files_bytes:
        data, sr = load_trace_from_bytes(b)

        N = len(data)
        yf = np.fft.rfft(data)
        xf = np.fft.rfftfreq(N, d=1/sr)
        mask = xf <= fft_max_freq
        yf_filtered = np.zeros_like(yf)
        yf_filtered[mask] = yf[mask]
        data_filtered = np.fft.irfft(yf_filtered, n=N)

        traces.append({'data': data_filtered, 'sr': sr})

    picks = []
    for tr in traces:
        env = envelope(tr['data'], tr['sr'])
        pick_time = pick_arrival_by_envelope(env, tr['sr'])
        picks.append(pick_time)

    epicenter = locate_epicenter_grid(stations_meta, picks, velocity_km_s)

    return {
        'stations': stations_meta,
        'picks_seconds_from_start': picks,
        'velocity_km_s': velocity_km_s,
        'epicenter': epicenter
    }
