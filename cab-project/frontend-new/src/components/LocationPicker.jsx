import React, { useState, useRef, useEffect } from 'react';
import { MapPin, Search, X } from 'lucide-react';

const LocationPicker = ({ onLocationSelect, placeholder = "Enter location", value = "" }) => {
  const [query, setQuery] = useState(value);
  const [suggestions, setSuggestions] = useState([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const autocompleteService = useRef(null);
  const placesService = useRef(null);

  useEffect(() => {
    if (window.google && !autocompleteService.current) {
      autocompleteService.current = new window.google.maps.places.AutocompleteService();
      placesService.current = new window.google.maps.places.PlacesService(
        document.createElement('div')
      );
    }
  }, []);

  const handleInputChange = (e) => {
    const value = e.target.value;
    setQuery(value);

    if (value.length > 2 && autocompleteService.current) {
      autocompleteService.current.getPlacePredictions(
        {
          input: value,
          componentRestrictions: { country: 'in' }, // Restrict to India
          types: ['establishment', 'geocode']
        },
        (predictions, status) => {
          if (status === window.google.maps.places.PlacesServiceStatus.OK) {
            setSuggestions(predictions || []);
            setShowSuggestions(true);
          }
        }
      );
    } else {
      setSuggestions([]);
      setShowSuggestions(false);
    }
  };

  const handleSuggestionClick = (suggestion) => {
    setQuery(suggestion.description);
    setShowSuggestions(false);

    // Get place details
    if (placesService.current) {
      placesService.current.getDetails(
        { placeId: suggestion.place_id },
        (place, status) => {
          if (status === window.google.maps.places.PlacesServiceStatus.OK) {
            const location = {
              lat: place.geometry.location.lat(),
              lng: place.geometry.location.lng(),
              address: place.formatted_address
            };
            onLocationSelect(location);
          }
        }
      );
    }
  };

  const getCurrentLocation = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const location = {
            lat: position.coords.latitude,
            lng: position.coords.longitude,
            address: "Current Location"
          };
          setQuery("Current Location");
          onLocationSelect(location);
        },
        (error) => {
          console.error("Error getting location:", error);
          alert("Unable to get current location");
        }
      );
    }
  };

  const clearInput = () => {
    setQuery("");
    setSuggestions([]);
    setShowSuggestions(false);
  };

  return (
    <div className="relative">
      <div className="relative">
        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
        <input
          type="text"
          value={query}
          onChange={handleInputChange}
          placeholder={placeholder}
          className="w-full pl-10 pr-20 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
        <div className="absolute right-2 top-1/2 transform -translate-y-1/2 flex gap-1">
          {query && (
            <button
              onClick={clearInput}
              className="p-1 text-gray-400 hover:text-gray-600"
            >
              <X className="w-4 h-4" />
            </button>
          )}
          <button
            onClick={getCurrentLocation}
            className="p-1 text-blue-500 hover:text-blue-700"
            title="Use current location"
          >
            <MapPin className="w-4 h-4" />
          </button>
        </div>
      </div>

      {showSuggestions && suggestions.length > 0 && (
        <div className="absolute z-10 w-full mt-1 bg-white border border-gray-200 rounded-lg shadow-lg max-h-60 overflow-y-auto">
          {suggestions.map((suggestion) => (
            <div
              key={suggestion.place_id}
              onClick={() => handleSuggestionClick(suggestion)}
              className="px-4 py-3 hover:bg-gray-50 cursor-pointer border-b border-gray-100 last:border-b-0"
            >
              <div className="flex items-start gap-3">
                <MapPin className="w-4 h-4 text-gray-400 mt-0.5 flex-shrink-0" />
                <div>
                  <div className="font-medium text-gray-900">
                    {suggestion.structured_formatting.main_text}
                  </div>
                  <div className="text-sm text-gray-500">
                    {suggestion.structured_formatting.secondary_text}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default LocationPicker;