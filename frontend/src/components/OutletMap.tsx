import React, { useState, useEffect } from "react";
import { MapContainer, TileLayer, Marker, Circle, Popup } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { useQuery } from "@tanstack/react-query";
import type { LatLngExpression } from "leaflet";
import ChatSearchBox from "./ChatSearchBox";
import MapLegend from "./MapLegend";

const RADIUS_METERS = 5000;

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

export type Outlet = {
  id: number;
  name: string;
  address: string;
  operating_hours: string;
  waze_link: string;
  latitude: number;
  longitude: number;
  features: string[];
};

function haversineDistance(a: Outlet, b: Outlet): number {
  const toRad = (x: number) => (x * Math.PI) / 180;
  const R = 6371000;
  const dLat = toRad(b.latitude - a.latitude);
  const dLon = toRad(b.longitude - a.longitude);
  const lat1 = toRad(a.latitude);
  const lat2 = toRad(b.latitude);
  const c =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(lat1) * Math.cos(lat2) * Math.sin(dLon / 2) * Math.sin(dLon / 2);
  return R * 2 * Math.atan2(Math.sqrt(c), Math.sqrt(1 - c));
}

export default function OutletMap() {
  const [intersectingIds, setIntersectingIds] = useState<Set<number>>(
    new Set()
  );
  const [chatbotResults, setChatbotResults] = useState<Outlet[] | null>(null);
  const [chatbotLoading, setChatbotLoading] = useState(false);
  const [chatbotError, setChatbotError] = useState<string | null>(null);

  const { data: outlets = [] } = useQuery<Outlet[]>({
    queryKey: ["outlets"],
    queryFn: async () => {
      const res = await fetch(`${import.meta.env.VITE_API_URL}/outlets`);
      if (!res.ok) throw new Error("Failed to fetch outlets");
      return res.json();
    },
  });

  const currentOutlets: Outlet[] = chatbotResults ?? outlets;

  useEffect(() => {
    if (!currentOutlets.length) {
      setIntersectingIds(new Set());
      return;
    }
    const intersecting = new Set<number>();
    for (let i = 0; i < currentOutlets.length; i++) {
      for (let j = i + 1; j < currentOutlets.length; j++) {
        const a = currentOutlets[i],
          b = currentOutlets[j];
        if (
          a.latitude &&
          a.longitude &&
          b.latitude &&
          b.longitude &&
          haversineDistance(a, b) <= RADIUS_METERS * 2
        ) {
          intersecting.add(a.id);
          intersecting.add(b.id);
        }
      }
    }
    setIntersectingIds(intersecting);
  }, [currentOutlets]);

  const center: LatLngExpression = currentOutlets.length
    ? [currentOutlets[0].latitude, currentOutlets[0].longitude]
    : [3.139, 101.6869];

  return (
    <div className="h-screen w-full relative">
      <ChatSearchBox
        setChatbotResults={setChatbotResults}
        setChatbotError={setChatbotError}
        chatbotLoading={chatbotLoading}
        setChatbotLoading={setChatbotLoading}
        chatbotError={chatbotError}
      />
      <MapLegend />
      {chatbotError && (
        <div
          className="absolute left-1/2 -translate-x-1/2 z-[1000] bg-white p-2 rounded shadow text-red-700 font-medium mt-2"
          style={{ top: 70 }}
        >
          {chatbotError}
        </div>
      )}
      <MapContainer center={center} zoom={12} className="h-screen w-full">
        <TileLayer
          attribution='&copy; <a href="https://osm.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {currentOutlets.map((outlet: Outlet) =>
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
    </div>
  );
}
