import numpy as np
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0 
    phi1 = np.radians(lat1)
    phi2 = np.radians(lat2)
    dphi = np.radians(lat2 - lat1)
    dlambda = np.radians(lon2 - lon1)

    a = np.sin(dphi/2)**2 + np.cos(phi1) * np.cos(phi2) * np.sin(dlambda/2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    return R * c

def locate_epicenter_grid(stations, picks, velocity_km_s, lat_step=0.05, lon_step=0.05):
    lats = [s['lat'] for s in stations]
    lons = [s['lon'] for s in stations]
    
    lat_min, lat_max = min(lats), max(lats)
    lon_min, lon_max = min(lons), max(lons)
    
    lat_min -= 2.0
    lat_max += 2.0
    lon_min -= 2.0
    lon_max += 2.0

    lat_grid = np.arange(lat_min, lat_max, lat_step)
    lon_grid = np.arange(lon_min, lon_max, lon_step)

    best_residual = float('inf')
    best_pfxpoint = None

    for lat in lat_grid:
        for lon in lon_grid:
            origin_times = []
            for i, s in enumerate(stations):
                d = haversine(lat, lon, s['lat'], s['lon'])
                origin_time_i = picks[i] - d / velocity_km_s
                origin_times.append(origin_time_i)
            origin_time = min(origin_times)
            

            residuals = []
            for i, s in enumerate(stations):
                d = haversine(lat, lon, s['lat'], s['lon'])
                t_expected = origin_time + d / velocity_km_s
                residuals.append((picks[i] - t_expected)**2)
            total_residual = sum(residuals)
            if total_residual < best_residual:
                best_residual = total_residual
                best_point = {'lat': lat, 'lon': lon, 'origin_time': origin_time, 'residual': best_residual}

    return best_point
