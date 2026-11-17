// Live Preview, Debounced Scam Check, and Autosave Draft
document.addEventListener("DOMContentLoaded", function () {
  const titleInput = document.getElementById("job-title");
  const categorySelect = document.getElementById("job-category");
  const dayRadios = document.querySelectorAll('input[name="day_option"]');
  const timeInput = document.getElementById("job-time");
  const payInput = document.getElementById("job-pay");
  const payTypeSelect = document.getElementById("job-pay-type");
  const peopleInput = document.getElementById("job-people");
  const addressInput = document.getElementById("job-address");
  const detailsInput = document.getElementById("job-details");
  const publishBtn = document.getElementById("btn-publish-job");

  // Preview elements
  const prevTitle = document.getElementById("prev-title");
  const prevCategory = document.getElementById("prev-category");
  const prevPeople = document.getElementById("prev-people");
  const prevPay = document.getElementById("prev-pay");
  const prevTime = document.getElementById("prev-time");
  const prevAddress = document.getElementById("prev-address");

  // Safety status alert
  const safetyBanner = document.getElementById("scam-safety-status");

  function updatePreview() {
    if (prevTitle && titleInput) {
      prevTitle.textContent = titleInput.value || "Job Title";
    }
    if (prevPeople && peopleInput) {
      const p = peopleInput.value || "1";
      prevPeople.textContent = `${p} needed`;
    }
    if (prevPay && payInput && payTypeSelect) {
      const amount = payInput.value || "100";
      const ptype = payTypeSelect.value === "day" ? "/day" : "/hr";
      prevPay.textContent = `₹${amount}${ptype}`;
    }
    if (prevTime && timeInput) {
      let dayVal = "Today";
      dayRadios.forEach(r => { if (r.checked) dayVal = r.value.charAt(0).toUpperCase() + r.value.slice(1); });
      prevTime.textContent = `${dayVal} ${timeInput.value || "5:00 pm to 9:00 pm"}`;
    }
    if (prevAddress && addressInput) {
      prevAddress.textContent = addressInput.value || "Shop address";
    }
  }

  // Debounce helper
  let scamCheckTimeout = null;
  function triggerScamCheck() {
    clearTimeout(scamCheckTimeout);
    scamCheckTimeout = setTimeout(function () {
      const title = titleInput ? titleInput.value : "";
      const details = detailsInput ? detailsInput.value : "";

      fetch("/api/scam-check", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title: title, details: details })
      })
      .then(res => res.json())
      .then(data => {
        if (!data.ok) {
          // Blocked
          if (safetyBanner) {
            safetyBanner.className = "alert alert-danger mb-3";
            safetyBanner.innerHTML = '<strong>Safety check: blocked.</strong> Remove the fee or advance to publish.';
          }
          if (publishBtn) {
            publishBtn.disabled = true;
            publishBtn.className = "btn btn-secondary w-100 py-2 fw-bold";
            publishBtn.textContent = "Publish (locked)";
          }
          if (detailsInput) detailsInput.classList.add("is-invalid");
        } else {
          // Passed
          if (safetyBanner) {
            safetyBanner.className = "alert alert-success mb-3";
            safetyBanner.innerHTML = '<strong>Safety check passed.</strong> No fee or advance mentioned.';
          }
          if (publishBtn) {
            publishBtn.disabled = false;
            publishBtn.className = "btn btn-lv-primary w-100 py-2 fw-bold";
            publishBtn.textContent = "Publish job";
          }
          if (detailsInput) detailsInput.classList.remove("is-invalid");
        }
      })
      .catch(err => console.error("Scam check error:", err));
    }, 400);
  }

  // Draft autosave
  let draftTimeout = null;
  function autosaveDraft() {
    clearTimeout(draftTimeout);
    draftTimeout = setTimeout(function () {
      const payload = {
        title: titleInput ? titleInput.value : "",
        category: categorySelect ? categorySelect.value : "shop_helper",
        pay_amount: payInput ? payInput.value : "",
        pay_type: payTypeSelect ? payTypeSelect.value : "hour",
        time_range: timeInput ? timeInput.value : "",
        people_needed: peopleInput ? peopleInput.value : 1,
        address: addressInput ? addressInput.value : "",
        details: detailsInput ? detailsInput.value : ""
      };
      fetch("/api/draft", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      }).catch(err => console.log("Draft autosave:", err));
    }, 3000);
  }

  // Attach event listeners
  [titleInput, payInput, timeInput, peopleInput, addressInput, detailsInput].forEach(el => {
    if (el) {
      el.addEventListener("input", function () {
        updatePreview();
        triggerScamCheck();
        autosaveDraft();
      });
    }
  });

  if (categorySelect) categorySelect.addEventListener("change", updatePreview);
  if (payTypeSelect) payTypeSelect.addEventListener("change", updatePreview);
  dayRadios.forEach(r => r.addEventListener("change", updatePreview));

  // "Use my shop address" helper button
  const useShopAddrBtn = document.getElementById("btn-use-shop-address");
  if (useShopAddrBtn && addressInput) {
    useShopAddrBtn.addEventListener("click", function (e) {
      e.preventDefault();
      const shopAddr = this.getAttribute("data-address");
      if (shopAddr) {
        addressInput.value = shopAddr;
        updatePreview();
      }
    });
  }

  updatePreview();
});
