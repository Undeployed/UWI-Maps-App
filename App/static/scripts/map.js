/****************************
* Map Module
****************************/
const MapModule = (function() {
    // Private variables
    let map;
    let activeLocationMarker = null;
    let userLocationMarker = null;
    let clickedMarker = false;
    let selectedMarker = null;
    let toggleButton, locateButton;
    
    const satelliteLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
        attribution: '&copy; Esri & OpenStreetMap contributors',
        maxZoom: 19
    });

    const defaultLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors',
        maxZoom: 19
    });

    // Public API
    return {
        init(selectedCampus) {
            const uwibounds = [selectedCampus.sw, selectedCampus.ne];
            const centerLat = (selectedCampus.sw[0] + selectedCampus.ne[0]) / 2;
            const centerLng = (selectedCampus.sw[1] + selectedCampus.ne[1]) / 2;

            map = L.map('map', {
                center: [centerLat, centerLng],
                zoom: 18,
                minZoom: 17,
                maxZoom: 19,
                maxBounds: uwibounds,
                maxBoundsViscosity: 0.9,
                attributionControl: false,
                zoomControl: false
            }).fitBounds(uwibounds);

            defaultLayer.addTo(map);
            this.initControls();
            this.initEventHandlers();
            return map; // Return map instance for edit.js
        },

        initControls() {
            // Custom control buttons
            L.Control.MapButtons = L.Control.extend({
                onAdd: function() {
                    const container = L.DomUtil.create('div', 'leaflet-bar leaflet-control leaflet-control-custom');

                    // Satellite toggle button
                    toggleButton = L.DomUtil.create('button', 'map-button material-icon-btn', container);
                    toggleButton.innerHTML = '<i class="material-icons">satellite_alt</i>';
                    toggleButton.onclick = () => MapModule.toggleMapTiles();

                    // Locate user button
                    locateButton = L.DomUtil.create('button', 'map-button material-icon-btn', container);
                    locateButton.innerHTML = '<i class="material-icons">my_location</i>';
                    locateButton.onclick = () => map.locate({ setView: true, maxZoom: 20 });

                    return container;
                }
            });

            map.addControl(new L.Control.MapButtons({ position: 'bottomright' }));
            L.control.zoom({ position: 'bottomleft' }).addTo(map);
        },

        initEventHandlers() {
            map.on('locationfound', (e) => {
                if (userLocationMarker) map.removeLayer(userLocationMarker);
                userLocationMarker = L.circleMarker(e.latlng, {
                    radius: 12,
                    color: '#5bb7cf',
                    fillColor: '#5bb7cf',
                    fillOpacity: 0.7,
                    weight: 3
                }).addTo(map).bindPopup("You are here!").openPopup();
            });

            map.on('locationerror', () => {
                alert("Location access denied or unavailable.");
            });
        },

        toggleMapTiles() {
            if (map.hasLayer(defaultLayer)) {
                map.removeLayer(defaultLayer);
                map.addLayer(satelliteLayer);
            } else {
                map.removeLayer(satelliteLayer);
                map.addLayer(defaultLayer);
            }
        },

        loadMarkers(markers) {
            markers.forEach(marker => {
                const latlng = [marker.latitude, marker.longitude];
                const circle = L.circleMarker(latlng, {
                    radius: 8,
                    color: marker.category.color,
                    fillColor: marker.category.color,
                    fillOpacity: 0.9,
                    className: 'custom-circle'
                }).on('click', function(e) {
                    if (editing && MarkerManager.state.isAdding) return;
                    clickedMarker = true;
                    e.originalEvent.stopPropagation();
                    
                    if (activeLocationMarker) map.removeLayer(activeLocationMarker);
                    
                    this.showMarkerPointer(marker, latlng);
                    this.showMarkerDetails(marker);
                    
                    if (editing) this.updateEditUI(marker);
                }.bind(this));

                circle.addTo(map);
            });
        },

        async showMarkerPointer(marker, latlng) {
            const response = await fetch('/static/images/marker-pointer.svg');
            const svg = await response.text();
            const coloredSvg = svg.replace(/fill=".*?"/g, `fill="${this.lightenHex(marker.category?.color || '#999', 20)}"`);

            const dropIcon = L.divIcon({
                className: 'custom-drop-icon',
                html: `<div class="custom-drop-icon">${coloredSvg}</div>`,
                iconSize: [50, 50],
                iconAnchor: [25, 50]
            });

            activeLocationMarker = L.marker(latlng, { icon: dropIcon }).addTo(map);
        },

        lightenHex(hex, percent) {
            hex = hex.replace('#', '');
            if (hex.length === 3) hex = hex.split('').map(c => c + c).join('');

            const num = parseInt(hex, 16);
            const adjust = (c) => Math.min(c + Math.round(255 * (percent / 100)), 255);
            
            const r = adjust(num >> 16);
            const g = adjust((num >> 8) & 0x00FF);
            const b = adjust(num & 0x0000FF);

            return '#' + (1 << 24 | (r << 16) | (g << 8) | b).toString(16).slice(1);
        },

        updateEditUI(marker) {
            if (selectedMarker) this.removeHighlight(selectedMarker.id);
            selectedMarker = marker;
            
            const listItem = document.getElementById(`marker-${marker.id}`);
            if (listItem) {
                listItem.scrollIntoView({ behavior: 'smooth', block: 'center' });
                listItem.classList.add('highlight');
            }
        },

        removeHighlight(id) {
            const listItem = document.getElementById(`marker-${id}`);
            if (listItem) listItem.classList.remove('highlight');
            selectedMarker = null;
        },

        showMarkerDetails(marker) {
            if (editing) return;
            
            document.getElementById('marker-name').textContent = marker.name || 'Unnamed Marker';
            document.getElementById('marker-description').innerHTML = (marker.description || 'No description available.').replace(/\n/g, '<br>');
            document.getElementById('marker-coordinates').textContent = `${marker.latitude.toFixed(5)}, ${marker.longitude.toFixed(5)}`;
            document.getElementById('marker-campus').textContent = marker.campus || 'Unnamed Campus';
            document.getElementById('marker-category').textContent = marker.category.name || 'Uncategorized';

            const imageEl = document.getElementById('marker-image');
            if (marker.image) {
                imageEl.src = marker.image;
                imageEl.alt = marker.name;
                imageEl.style.display = 'block';
            } else {
                imageEl.style.display = 'none';
            }


            const faculty = document.getElementById('marker-faculty');
            if (marker.faculty) {
                faculty.textContent = marker.faculty.name || 'No Faculty'
            }

            const markerTime = document.getElementById('marker-time');
            const markerTimeP = document.getElementById('marker-time-p');
            if (marker.open_time) {
                let desc = marker.open_time;
                if (marker.close_time) desc += ` - ${marker.close_time}`;
                markerTime.textContent = desc;
                markerTimeP.style.display = 'inline-block';
            } else {
                markerTime.textContent = '';
                markerTimeP.style.display = 'none';
            }

            document.getElementById('marker-info-panel').classList.add('show');
        },

        closePanel() {
            if (clickedMarker) {
                clickedMarker = false;
                return;
            }

            if (selectedMarker && editing) this.removeHighlight(selectedMarker.id);
            if (!editing) document.getElementById('marker-info-panel').classList.remove('show');
            if (activeLocationMarker) {
                map.removeLayer(activeLocationMarker);
                activeLocationMarker = null;
            }
        }
    };
})();

// Initialize map and expose it to edit.js
const map = MapModule.init(selectedCampus);
map.on('click', () => MapModule.closePanel());

if (!editing) {
    document.getElementById('close-panel').onclick = () => MapModule.closePanel();
}

// Load markers
MapModule.loadMarkers(markers);