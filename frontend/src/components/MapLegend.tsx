import React from "react";

export default function MapLegend() {
  return (
    <div className="absolute bottom-6 left-6 z-[1100] bg-white/95 rounded-lg shadow p-4 flex flex-col gap-2 min-w-[220px] border border-gray-200">
      <div className="font-semibold mb-1">Map Legend</div>
      <div className="flex items-center gap-2">
        <span className="inline-block w-4 h-4 rounded-full border-2 border-blue-600 bg-blue-200" />
        <span>Outlet (no other outlets detected within a 5km radius)</span>
      </div>
      <div className="flex items-center gap-2">
        <span className="inline-block w-4 h-4 rounded-full border-2 border-red-600 bg-red-200" />
        <span>
          Outlet (at least one other outlet found within a 5km radius)
        </span>
      </div>
    </div>
  );
}
