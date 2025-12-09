import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png'
import markerIcon from 'leaflet/dist/images/marker-icon.png'
import markerShadow from 'leaflet/dist/images/marker-shadow.png'

// Исправление путей для Next.js
L.Icon.Default.mergeOptions({
	iconRetinaUrl: markerIcon2x.src,
	iconUrl: markerIcon.src,
	shadowUrl: markerShadow.src,
})
