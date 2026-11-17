// LocalVelai Main Utilities
document.addEventListener("DOMContentLoaded", function () {
  // Auto-dismiss alerts after 5 seconds
  const alerts = document.querySelectorAll(".alert-dismissible");
  alerts.forEach(function (alert) {
    setTimeout(function () {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      if (bsAlert) bsAlert.close();
    }, 5000);
  });

  // Browser Geolocation Helper
  const geoBtn = document.getElementById("btn-use-location");
  if (geoBtn) {
    geoBtn.addEventListener("click", function () {
      if (!navigator.geolocation) {
        alert("Geolocation is not supported by your browser. Please select an area from the list.");
        return;
      }
      geoBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span> Locating...';
      navigator.geolocation.getCurrentPosition(
        function (pos) {
          const lat = pos.coords.latitude;
          const lng = pos.coords.longitude;
          const latInput = document.getElementById("input-lat");
          const lngInput = document.getElementById("input-lng");
          if (latInput) latInput.value = lat;
          if (lngInput) lngInput.value = lng;
          geoBtn.innerHTML = '✓ Location set';
          geoBtn.classList.remove("btn-outline-primary");
          geoBtn.classList.add("btn-success");
        },
        function (err) {
          geoBtn.innerHTML = 'Use my location';
          alert("Location access denied or unavailable. Please pick an area from the dropdown.");
        },
        { timeout: 8000 }
      );
    });
  }

  // Prevent double form submissions on payment & publish
  const lockForms = document.querySelectorAll("form.prevent-double-submit");
  lockForms.forEach(function (form) {
    form.addEventListener("submit", function () {
      const btn = form.querySelector('button[type="submit"]');
      if (btn) {
        btn.disabled = true;
        btn.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span> Processing...';
      }
    });
  });
});
