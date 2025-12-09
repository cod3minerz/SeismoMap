'use client'

import { DefaultIcon } from '@/lib/customMarker'
import 'leaflet/dist/leaflet.css'
import { Circle, MapContainer, Marker, Popup, TileLayer } from 'react-leaflet'

type Station = {
	name: string
	lat: number
	lon: number
}

type Epicenter = {
	lat: number
	lon: number
	origin_time: number
	residual: number
}

type SeismoResult = {
	stations: Station[]
	picks_seconds_from_start: number[]
	velocity_km_s: number
	epicenter: Epicenter
}

export default function SeismoMap({ result }: { result: SeismoResult }) {
	const { epicenter, stations } = result

	const center: [number, number] = [epicenter.lat, epicenter.lon]

	return (
		<div className='w-full h-[800px] rounded-xl overflow-hidden border border-neutral-300'>
			<MapContainer
				center={center}
				zoom={7}
				scrollWheelZoom={true}
				style={{ width: '100%', height: '100%' }}
			>
				<TileLayer
					attribution='&copy; OpenStreetMap'
					url='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
				/>

				{/* Эпицентр */}
				<Marker position={[epicenter.lat, epicenter.lon]} icon={DefaultIcon}>
					<Popup>
						<b>Epicenter</b>
						<br />
						Lat: {epicenter.lat.toFixed(3)}
						<br />
						Lon: {epicenter.lon.toFixed(3)}
						<br />
						Origin time: {epicenter.origin_time.toFixed(3)}
						<br />
						Residual: {epicenter.residual.toExponential(3)}
					</Popup>
				</Marker>

				<Circle
					center={[epicenter.lat, epicenter.lon]}
					radius={30000} // 30 км
					pathOptions={{ color: 'red', opacity: 0.4 }}
				/>

				{/* Станции */}
				{stations.map((s, i) => (
					<Marker key={i} position={[s.lat, s.lon]} icon={DefaultIcon}>
						<Popup>
							<b>{s.name}</b>
							<br />
							Lat: {s.lat}
							<br />
							Lon: {s.lon}
							<br />
							Pick: {result.picks_seconds_from_start[i].toFixed(2)} s
						</Popup>
					</Marker>
				))}
			</MapContainer>
		</div>
	)
}
