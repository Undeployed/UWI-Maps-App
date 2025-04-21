// ==============================
// MarkerManager Object
// Handles all marker-related functionality: adding, editing, and form control
// ==============================
const MarkerManager = {
    state: {
      isAdding: false,
      tempMarker: null,
    },
  
    elements: {
      map: document.getElementById("map"),
      formWrapper: document.getElementById("add-marker-form-wrapper"),
      markerForm: document.getElementById("add-marker-form"),
      latInput: document.getElementById("marker-lat"),
      lngInput: document.getElementById("marker-lng"),
      coordLat: document.getElementById('coord-lat'),
      coordLng: document.getElementById('coord-lng'),
      notifBar: document.getElementById("notification-bar"),
      categorySelect: document.getElementById('marker-form-category'),
      nameInput: document.getElementById('marker-form-name'),
      descInput: document.getElementById('marker-form-description'),
      imgInput: document.getElementById('marker-form-image'),
      formBtn: document.getElementById('form-add-btn'),
      formTitle: document.getElementById('marker-form-title'),
    },
  
    // Start the process to add a new marker
    startAdding() {
      this.cancel(); // reset state first
      this.state.isAdding = true;
      this.elements.markerForm.action = `/marker/add/${selectedCampus.id}`;
      this.clearForm();
      this.updateCursor(true);
      this.toggleForm(false); // show form after clicking on map
      this.elements.notifBar.classList.remove("hidden");
    },
  
    // Cancel current marker actions
    cancel() {
      this.state.isAdding = false;
      this.elements.formWrapper.classList.add("hidden");
      this.elements.notifBar.classList.add("hidden");
      this.updateCursor(false);
  
      if (this.state.tempMarker) {
        map.removeLayer(this.state.tempMarker);
        this.state.tempMarker = null;
      }
    },
  
    // Begin editing an existing marker
    edit(markerId) {
      this.cancel();
      const marker = markers.find(m => m.id === +markerId);
      if (!marker) return;
  
      this.elements.markerForm.action = `/marker/update/${markerId}`;
      this.fillForm(marker);
      this.toggleForm(true);
    },
  
    // Fill form inputs with marker data
    fillForm(marker) {
      this.elements.latInput.value = marker.latitude;
      this.elements.lngInput.value = marker.longitude;
      this.elements.coordLat.textContent = +marker.latitude.toFixed(6);
      this.elements.coordLng.textContent = +marker.longitude.toFixed(6);
      this.elements.nameInput.value = marker.name;
      this.elements.descInput.value = marker.description;
      this.elements.imgInput.value = marker.image;
      this.elements.formBtn.textContent = "Update Marker";
      this.elements.formTitle.textContent = "Update Marker";
  
      this.elements.categorySelect.value = marker.category.id;
      M.FormSelect.init(this.elements.categorySelect); // re-init Materialize select
    },
  
    // Reset form inputs to blank/default values
    clearForm() {
      this.elements.latInput.value = "";
      this.elements.lngInput.value = "";
      this.elements.coordLat.textContent = "--";
      this.elements.coordLng.textContent = "--";
      this.elements.nameInput.value = "";
      this.elements.descInput.value = "";
      this.elements.imgInput.value = "";
      this.elements.categorySelect.value = 1;
      this.elements.formBtn.textContent = "Add Marker";
      this.elements.formTitle.textContent = "Add New Marker";
      M.FormSelect.init(this.elements.categorySelect);
    },
  
    // Show/hide the marker form
    toggleForm(show = true) {
      this.elements.formWrapper.classList.toggle("hidden", !show);
    },
  
    // Change the map cursor when in add mode
    updateCursor(active) {
      this.elements.map.classList.toggle("add-mode-cursor", active);
    },
  
    // Drop a temporary preview marker on the map
    async dropTempMarker(lat, lng) {
      try {
        const res = await fetch('/static/images/marker-pointer.svg');
        let svg = await res.text();
        svg = svg.replace(/fill=".*?"/g, `fill="#ff513d"`); // Recolor the SVG
  
        const dropIcon = L.divIcon({
          className: 'custom-drop-icon',
          html: `<div class="custom-drop-icon">${svg}</div>`,
          iconSize: [50, 50],
          iconAnchor: [25, 45],
        });
  
        if (this.state.tempMarker) map.removeLayer(this.state.tempMarker);
  
        this.state.tempMarker = L.marker({ lat, lng }, {
          icon: dropIcon,
          draggable: false,
        }).addTo(map);
      } catch (err) {
        console.error("Failed to load custom SVG marker", err);
      }
    }
  };
  
  
  // ==============================
  // Keyboard Shortcut Listener
  // ESC key cancels marker add mode
  // ==============================
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && MarkerManager.state.isAdding) {
      MarkerManager.cancel();
    }
  });
  
  
  // ==============================
  // Map Click Handler
  // Add new marker when in 'add mode' and within campus bounds
  // ==============================
  map.on("click", async (e) => {
    if (MarkerManager.state.isAdding) {
        const { lat, lng } = e.latlng;
    
        if (!isWithinCampusBounds(lat, lng)) {
          alert("Please click within the campus boundary.");
          return;
        }
    
        // Update form with new coords
        MarkerManager.elements.latInput.value = lat;
        MarkerManager.elements.lngInput.value = lng;
        MarkerManager.elements.coordLat.textContent = lat.toFixed(6);
        MarkerManager.elements.coordLng.textContent = lng.toFixed(6);
    
        MarkerManager.toggleForm(true);
        await MarkerManager.dropTempMarker(lat, lng);
      } else {
        // Not adding? Just close any open panels
        MarkerManager.toggleForm(false);
        closeInfoPanel();
      }
  });
  
  
  // ==============================
  // Helper: Check if coords are within current campus bounds
  // ==============================
  function isWithinCampusBounds(lat, lng) {
    const [south, west] = selectedCampus.sw;
    const [north, east] = selectedCampus.ne;
    return lat >= south && lat <= north && lng >= west && lng <= east;
  }
  
  
  // ==============================
  // Info Panel: Close the right panel
  // ==============================
  function closeInfoPanel() {
    document.getElementById('marker-info-panel').classList.add('hidden');
  }
  
  
  // ==============================
  // Info Panel: Show marker details on right panel
  // ==============================
  function infoMarker(markerId) {
    const marker = markers.find(m => m.id === markerId);
    if (!marker) return;
  
    document.getElementById('info-title').innerText = marker.name;
    document.getElementById('info-description').innerText = marker.description || 'No description.';
    document.getElementById('info-category').innerText = marker.category?.name || 'Uncategorized';
    document.getElementById('info-coords').innerText = `(${marker.latitude}, ${marker.longitude})`;
  
    const updateList = document.getElementById('info-updates');
    updateList.innerHTML = '';
  
    if (marker.updates?.length) {
      marker.updates.slice().reverse().forEach((u, i) => {
        const li = document.createElement('li');
        li.innerText = `[#${marker.updates.length - i}]\nAdmin: ${u.user.username}\nDate: ${u.date}\n[Overview]: ${u.description}`;
        updateList.appendChild(li);
      });
    } else {
      const li = document.createElement('li');
      li.innerText = 'No updates yet.';
      updateList.appendChild(li);
    }
  
    document.getElementById('marker-info-panel').classList.remove('hidden');
  }
  