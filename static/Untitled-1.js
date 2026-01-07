// Get user location and send to Flask
if (navigator.geolocation) {
  navigator.geolocation.getCurrentPosition((pos) => {
    fetch("/set_location", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        lat: pos.coords.latitude,
        lng: pos.coords.longitude
      }),
    });
  });
}

// Optional: initialize Leaflet map for volunteers
if (document.getElementById("map")) {
  const map = L.map('map').setView([48.8566, 2.3522], 12);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; Food Rescue Map'
  }).addTo(map);
}
