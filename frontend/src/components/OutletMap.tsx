import React, { useEffect, useState } from "react";
import { MapContainer, TileLayer, Marker, Circle, Popup } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

interface Outlet {
  id: number;
  name: string;
  address: string;
  operating_hours: string;
  waze_link: string;
  latitude: number;
  longitude: number;
  features: string[];
}

const RADIUS_METERS = 5000;

// Custom marker icons
const blueIcon = new L.Icon({
  iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
  shadowSize: [41, 41],
});
const redIcon = new L.Icon({
  iconUrl:
    "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
  shadowSize: [41, 41],
});

function haversineDistance(
  lat1: number,
  lon1: number,
  lat2: number,
  lon2: number
) {
  const toRad = (x: number) => (x * Math.PI) / 180;
  const R = 6371000; // meters
  const dLat = toRad(lat2 - lat1);
  const dLon = toRad(lon2 - lon1);
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(toRad(lat1)) *
      Math.cos(toRad(lat2)) *
      Math.sin(dLon / 2) *
      Math.sin(dLon / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return R * c;
}

const OutletMap: React.FC = () => {
  const [outlets, setOutlets] = useState<Outlet[]>([]);
  const [intersectingIds, setIntersectingIds] = useState<Set<number>>(
    new Set()
  );

  useEffect(() => {
    fetch("http://localhost:8000/outlets")
      .then((res) => res.json())
      .then((data) => setOutlets(data));
  }, []);

  useEffect(() => {
    // Find intersecting outlets
    const intersecting = new Set<number>();
    for (let i = 0; i < outlets.length; i++) {
      for (let j = i + 1; j < outlets.length; j++) {
        const a = outlets[i];
        const b = outlets[j];
        if (
          a.latitude &&
          a.longitude &&
          b.latitude &&
          b.longitude &&
          haversineDistance(a.latitude, a.longitude, b.latitude, b.longitude) <=
            RADIUS_METERS * 2
        ) {
          intersecting.add(a.id);
          intersecting.add(b.id);
        }
      }
    }
    setIntersectingIds(intersecting);
  }, [outlets]);

  // Center map on KL if possible
  const center = outlets.length
    ? [outlets[0].latitude, outlets[0].longitude]
    : [3.139, 101.6869]; // Default: Kuala Lumpur

  return (
    <MapContainer
      center={center as [number, number]}
      zoom={12}
      style={{ height: "100vh", width: "100%" }}
    >
      <TileLayer
        attribution='&copy; <a href="https://osm.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {outlets.map((outlet) =>
        outlet.latitude && outlet.longitude ? (
          <React.Fragment key={outlet.id}>
            <Circle
              center={[outlet.latitude, outlet.longitude]}
              radius={RADIUS_METERS}
              pathOptions={{
                color: intersectingIds.has(outlet.id) ? "red" : "blue",
                fillOpacity: 0.075,
              }}
            />
            <Marker
              position={[outlet.latitude, outlet.longitude]}
              icon={intersectingIds.has(outlet.id) ? redIcon : blueIcon}
            >
              <Popup>
                <strong>{outlet.name}</strong>
                <br />
                {outlet.address}
                <br />
                {outlet.operating_hours}
                <br />
                <a
                  href={outlet.waze_link}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Waze
                </a>
              </Popup>
            </Marker>
          </React.Fragment>
        ) : null
      )}
    </MapContainer>
  );
};

export default OutletMap;
