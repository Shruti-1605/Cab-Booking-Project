import React, { useEffect, useRef, useState } from 'react';

const MapComponent = ({ 
  pickup, 
  dropoff, 
  driverLocation, 
  onLocationSelect, 
  showRoute = false,
  height = "400px" 
}) => {
  const mapRef = useRef(null);
  const [map, setMap] = useState(null);
  const [directionsService, setDirectionsService] = useState(null);
  const [directionsRenderer, setDirectionsRenderer] = useState(null);

  useEffect(() => {
    // Load Google Maps script
    if (!window.google) {
      const script = document.createElement('script');
      script.src = `https://maps.googleapis.com/maps/api/js?key=${import.meta.env.VITE_GOOGLE_MAPS_API_KEY}&libraries=places`;
      script.async = true;
      script.onload = initMap;
      document.head.appendChild(script);
    } else {
      initMap();
    }
  }, []);

  const initMap = () => {
    const mapInstance = new window.google.maps.Map(mapRef.current, {
      center: { lat: 28.6139, lng: 77.2090 }, // Delhi center
      zoom: 12,
      styles: [
        {
          featureType: "poi",
          elementType: "labels",
          stylers: [{ visibility: "off" }]
        }
      ]
    });

    const directionsServiceInstance = new window.google.maps.DirectionsService();
    const directionsRendererInstance = new window.google.maps.DirectionsRenderer({
      suppressMarkers: false,
      polylineOptions: {
        strokeColor: "#4F46E5",
        strokeWeight: 4
      }
    });

    directionsRendererInstance.setMap(mapInstance);

    setMap(mapInstance);
    setDirectionsService(directionsServiceInstance);
    setDirectionsRenderer(directionsRendererInstance);

    // Add click listener for location selection
    if (onLocationSelect) {
      mapInstance.addListener('click', (event) => {
        onLocationSelect({
          lat: event.latLng.lat(),
          lng: event.latLng.lng()
        });
      });
    }
  };

  // Update route when pickup/dropoff changes
  useEffect(() => {
    if (map && directionsService && directionsRenderer && pickup && dropoff && showRoute) {
      const request = {
        origin: pickup,
        destination: dropoff,
        travelMode: window.google.maps.TravelMode.DRIVING,
      };

      directionsService.route(request, (result, status) => {
        if (status === 'OK') {
          directionsRenderer.setDirections(result);
        }
      });
    }
  }, [pickup, dropoff, map, directionsService, directionsRenderer, showRoute]);

  // Add markers for pickup, dropoff, and driver
  useEffect(() => {
    if (!map) return;

    // Clear existing markers
    if (window.currentMarkers) {
      window.currentMarkers.forEach(marker => marker.setMap(null));
    }
    window.currentMarkers = [];

    // Pickup marker
    if (pickup) {
      const pickupMarker = new window.google.maps.Marker({
        position: pickup,
        map: map,
        title: "Pickup Location",
        icon: {
          url: "data:image/svg+xml;charset=UTF-8," + encodeURIComponent(`
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z" fill="#10B981"/>
              <circle cx="12" cy="9" r="2.5" fill="white"/>
            </svg>
          `),
          scaledSize: new window.google.maps.Size(32, 32)
        }
      });
      window.currentMarkers.push(pickupMarker);
    }

    // Dropoff marker
    if (dropoff) {
      const dropoffMarker = new window.google.maps.Marker({
        position: dropoff,
        map: map,
        title: "Drop Location",
        icon: {
          url: "data:image/svg+xml;charset=UTF-8," + encodeURIComponent(`
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z" fill="#EF4444"/>
              <circle cx="12" cy="9" r="2.5" fill="white"/>
            </svg>
          `),
          scaledSize: new window.google.maps.Size(32, 32)
        }
      });
      window.currentMarkers.push(dropoffMarker);
    }

    // Driver marker
    if (driverLocation) {
      const driverMarker = new window.google.maps.Marker({
        position: driverLocation,
        map: map,
        title: "Driver Location",
        icon: {
          url: "data:image/svg+xml;charset=UTF-8," + encodeURIComponent(`
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="12" cy="12" r="8" fill="#3B82F6"/>
              <path d="M8 12h8M12 8v8" stroke="white" stroke-width="2"/>
            </svg>
          `),
          scaledSize: new window.google.maps.Size(32, 32)
        }
      });
      window.currentMarkers.push(driverMarker);
    }
  }, [pickup, dropoff, driverLocation, map]);

  return (
    <div 
      ref={mapRef} 
      style={{ width: '100%', height }}
      className="rounded-lg border border-gray-200"
    />
  );
};

export default MapComponent;