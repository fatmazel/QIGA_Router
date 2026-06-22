import { MapContainer, TileLayer, CircleMarker, Polyline, Tooltip } from 'react-leaflet'
import styles from './MapView.module.css'

// [0,100] sanal koordinatlarını Türkiye coğrafi sınırlarına ölçekle
// lat: 36–42 (6°), lng: 26–45 (19°)
function toLatLng([x, y]) {
  return [36 + (y / 100) * 6, 26 + (x / 100) * 19]
}

const OSM_URL = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
const OSM_ATTRIBUTION = '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'

// Türkiye merkezi
const CENTER = [39, 35.5]

export default function MapView({ cities, route }) {
  const hasData = cities && cities.length > 0

  // Rota: [c0,c1,...,c_{n-1}] → c0→c1→...→c0 (kapalı döngü)
  const routePositions = route
    ? [...route, route[0]].map((i) => toLatLng(cities[i]))
    : []

  return (
    <div className={styles.wrapper}>
      <h2 className={styles.title}>Rota Haritası</h2>

      {!hasData && (
        <div className={styles.placeholder}>
          Parametreleri ayarlayıp <strong>Çöz</strong> butonuna bas.
        </div>
      )}

      {hasData && (
        <MapContainer
          center={CENTER}
          zoom={5}
          style={{ height: '380px', width: '100%', borderRadius: '8px' }}
          zoomControl={true}
        >
          <TileLayer url={OSM_URL} attribution={OSM_ATTRIBUTION} />

          {/* En iyi rota — mavi çizgi */}
          {routePositions.length > 0 && (
            <Polyline positions={routePositions} color="#4a6fa5" weight={2.5} />
          )}

          {/* Şehir noktaları */}
          {cities.map((city, i) => (
            <CircleMarker
              key={i}
              center={toLatLng(city)}
              radius={6}
              pathOptions={{ color: '#2d3748', fillColor: '#f6ad55', fillOpacity: 1, weight: 1.5 }}
            >
              <Tooltip permanent direction="top" offset={[0, -8]}>
                <span style={{ fontSize: '11px', fontWeight: 600 }}>{i}</span>
              </Tooltip>
            </CircleMarker>
          ))}

          {/* Başlangıç şehri (route[0]) yeşil */}
          {route && (
            <CircleMarker
              center={toLatLng(cities[route[0]])}
              radius={8}
              pathOptions={{ color: '#276749', fillColor: '#48bb78', fillOpacity: 1, weight: 2 }}
            />
          )}
        </MapContainer>
      )}
    </div>
  )
}
