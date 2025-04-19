/****************************
* Map Initialization
****************************/
const uwibounds = [selectedCampus.sw, selectedCampus.ne];

const map = L.map('map', {
    center: [10.642, -61.400],
    zoom: 18,
    minZoom: 17,
    maxZoom: 19,
    maxBounds: uwibounds,
    maxBoundsViscosity: 0.9,
    attributionControl: false,
    zoomControl: false
});

// Map Tile Layers
const satelliteLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    attribution: '&copy; Esri & OpenStreetMap contributors',
    maxZoom: 19
});

const defaultLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors',
    maxZoom: 19
}).addTo(map);

function toggleMapTiles() {
    if (map.hasLayer(defaultLayer)) {
        map.removeLayer(defaultLayer);
        map.addLayer(satelliteLayer);
    } else {
        map.removeLayer(satelliteLayer);
        map.addLayer(defaultLayer);
    }
}

/****************************
 * Map Controls
 ****************************/
L.Control.MapButtons = L.Control.extend({
    onAdd: function (map) {
        const container = L.DomUtil.create('div', 'leaflet-bar leaflet-control leaflet-control-custom');

        // Satellite toggle button
        const toggleButton = L.DomUtil.create('button', 'map-button material-icon-btn', container);
        toggleButton.innerHTML = '<i class="material-icons">satellite_alt</i>';
        toggleButton.onclick = toggleMapTiles;

        // Locate user button
        const locateButton = L.DomUtil.create('button', 'map-button material-icon-btn', container);
        locateButton.innerHTML = '<i class="material-icons">my_location</i>';
        locateButton.onclick = () => {
        map.locate({ setView: true, maxZoom: 20 });
        };

        return container;
    }
});

map.addControl(new L.Control.MapButtons({ position: 'bottomright' }));
L.control.zoom({ position: 'bottomleft' }).addTo(map);


/****************************
* User Location Handling
****************************/
map.on('locationfound', (e) => {
    L.marker(e.latlng).addTo(map).bindPopup("You are here!").openPopup();
});

map.on('locationerror', () => {
    alert("Location access denied or unavailable.");
});


/****************************
* Marker Logic
****************************/
let activeLocationMarker = null;
let clickedMarker = false;

function lightenHex(hex, percent) {
    hex = hex.replace('#', '');
    if (hex.length === 3) {
        hex = hex.split('').map(c => c + c).join('');
    }

    const num = parseInt(hex, 16);
    let r = (num >> 16) + Math.round(255 * (percent / 100));
    let g = ((num >> 8) & 0x00FF) + Math.round(255 * (percent / 100));
    let b = (num & 0x0000FF) + Math.round(255 * (percent / 100));

    r = r > 255 ? 255 : r;
    g = g > 255 ? 255 : g;
    b = b > 255 ? 255 : b;

    return '#' + (1 << 24 | (r << 16) | (g << 8) | b).toString(16).slice(1);
}
  
function loadMarkers() {
    markers.forEach(marker => {
        const latlng = [marker.latitude, marker.longitude];

        // Category color based on 2nd category (fallback to default if missing)
        const categoryColor = marker.category.color;

        const circle = L.circleMarker(latlng, {
            radius: 8,
            color: categoryColor,
            fillColor: categoryColor,
            fillOpacity: 0.9,
            className: 'custom-circle'
        }).on('click', function (e) {
            clickedMarker = true;
            e.originalEvent.stopPropagation(); // Prevent map from triggering click

            // Remove previous pointer
            if (activeLocationMarker) {
                map.removeLayer(activeLocationMarker);
            }

           // Fetch and inject custom SVG as drop marker
           fetch('/static/images/marker-pointer.svg')
           .then(res => res.text())
           .then(svg => {
               // customize SVG color by replacing fill
               const coloredSvg = svg.replace(/fill=".*?"/g, `fill="${lightenHex(categoryColor, 20)}"`);

               const dropIcon = L.divIcon({
                   className: 'custom-drop-icon',
                   html: `<div class="custom-drop-icon">${coloredSvg}</div>`,
                   iconSize: [50, 50],
                   iconAnchor: [25, 50]
               });

               activeLocationMarker = L.marker(latlng, {
                   icon: dropIcon
               }).addTo(map);
           });

            showMarkerDetails(marker);
        });

        circle.addTo(map);
    });
}

loadMarkers();


/****************************
* Map Click to Close Panel
****************************/
function closePanel() {
    if (clickedMarker) {
        clickedMarker = false;
        return;
    }
    
    // Close side panel
    document.getElementById('marker-info-panel').classList.remove('show');
    
    // Remove pointer marker
    if (activeLocationMarker) {
        map.removeLayer(activeLocationMarker);
        activeLocationMarker = null;
    }
}

map.on('click', function () {
    closePanel()
});

document.getElementById('close-panel').onclick = () => {
    closePanel()
};

/****************************
* Marker Info Panel Handler
****************************/
function showMarkerDetails(marker) {
    // Get all the target elements inside the info panel
    document.getElementById('marker-name').textContent = marker.name || 'Unnamed Marker';
    document.getElementById('marker-description').textContent = marker.description || 'No description available.';
    document.getElementById('marker-coordinates').textContent = `${marker.latitude.toFixed(5)}, ${marker.longitude.toFixed(5)}`;
    document.getElementById('marker-category').textContent = marker.category.name || 'Uncategorized';

    const imageEl = document.getElementById('marker-image');
    if (marker.image) {
        imageEl.src = marker.image;
        imageEl.alt = marker.name;
        imageEl.style.display = 'block';
    } else {
        imageEl.style.display = 'none';
    }

    // Show the panel
    document.getElementById('marker-info-panel').classList.add('show');
}
