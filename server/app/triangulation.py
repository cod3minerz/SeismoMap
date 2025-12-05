import numpy as np

# функция для расчета расстояния между двумя точками по координатам (км)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # радиус Земли в км
    phi1 = np.radians(lat1)
    phi2 = np.radians(lat2)
    dphi = np.radians(lat2 - lat1)
    dlambda = np.radians(lon2 - lon1)

    a = np.sin(dphi/2)**2 + np.cos(phi1) * np.cos(phi2) * np.sin(dlambda/2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    return R * c

def locate_epicenter_grid(stations, picks, velocity_km_s, lat_step=0.01, lon_step=0.01):
    """
    stations: list of dicts with lat, lon
    picks: list of arrival times (seconds) на каждой станции
    velocity_km_s: скорость P-волны
    lat_step, lon_step: шаг сетки поиска
    """
    # Ограничиваем сетку на район реального эпицентра
    lat_min, lat_max = 66.0, 69.0     # ~ район суши вокруг 67.653N
    lon_min, lon_max = 140.0, 145.0   # ~ район суши вокруг 142.772E

    lat_grid = np.arange(lat_min, lat_max, lat_step)
    lon_grid = np.arange(lon_min, lon_max, lon_step)

    best_residual = float('inf')
    best_point = None

    for lat in lat_grid:
        for lon in lon_grid:
            residuals = []
            for i, s in enumerate(stations):
                d = haversine(lat, lon, s['lat'], s['lon'])
                t_expected = d / velocity_km_s
                residuals.append((picks[i] - t_expected)**2)
            total_residual = sum(residuals)
            if total_residual < best_residual:
                best_residual = total_residual
                # предполагаемое время события = минимальный pick минус расстояние/скорость
                origin_time = min(picks[i] - haversine(lat, lon, s['lat'], s['lon'])/velocity_km_s for i, s in enumerate(stations))
                best_point = {'lat': lat, 'lon': lon, 'origin_time': origin_time, 'residual': best_residual}

    return best_point
