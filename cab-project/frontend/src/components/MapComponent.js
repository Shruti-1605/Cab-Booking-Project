import React, { useEffect, useRef } from 'react';

const MapComponent = ({ pickup, destination, onLocationSelect }) => {
  const mapRef = useRef(null);
  const mapInstance = useRef(null);

  useEffect(() => {
    // Load Leaflet CSS and JS
    if (!window.L) {
      const link = document.createElement('link');
      link.rel = 'stylesheet';
      link.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css';
      document.head.appendChild(link);

      const script = document.createElement('script');
      script.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js';
      script.onload = initializeMap;
      document.head.appendChild(script);
    } else {
      initializeMap();
    }
  }, []);

  const initializeMap = () => {
    if (mapInstance.current) return;

    const map = window.L.map(mapRef.current).setView([28.6139, 77.2090], 13);
    
    window.L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    mapInstance.current = map;

    // Add click handler
    map.on('click', (e) => {
      if (onLocationSelect) {
        onLocationSelect(e.latlng.lat, e.latlng.lng);
      }
    });
  };

  useEffect(() => {
    if (mapInstance.current && pickup.lat) {
      const pickupMarker = window.L.marker([pickup.lat, pickup.lng])
        .addTo(mapInstance.current)
        .bindPopup('Pickup Location');
    }
  }, [pickup]);

  useEffect(() => {
    if (mapInstance.current && destination.lat) {
      const destMarker = window.L.marker([destination.lat, destination.lng])
        .addTo(mapInstance.current)
        .bindPopup('Destination');
    }
  }, [destination]);

  return (
    <div 
      ref={mapRef} 
      style={{ height: '400px', width: '100%' }}
      className="rounded-lg border"
    />
  );
};

export default MapComponent;