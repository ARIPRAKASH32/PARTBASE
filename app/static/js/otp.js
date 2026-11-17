// 6-box OTP Auto-Advance and Countdown Timer
document.addEventListener("DOMContentLoaded", function () {
  const boxes = document.querySelectorAll(".otp-box");
  const fullInput = document.getElementById("otp-full-code");
  const resendBtn = document.getElementById("btn-resend-otp");
  const timerSpan = document.getElementById("otp-timer");

  if (boxes.length === 6) {
    boxes[0].focus();

    boxes.forEach((box, idx) => {
      box.addEventListener("input", function (e) {
        const val = this.value;
        if (val.length >= 1) {
          this.value = val.slice(-1); // Keep last char
          if (idx < 5) {
            boxes[idx + 1].focus();
          }
        }
        updateFullCode();
      });

      box.addEventListener("keydown", function (e) {
        if (e.key === "Backspace" && !this.value && idx > 0) {
          boxes[idx - 1].focus();
        }
      });

      box.addEventListener("paste", function (e) {
        e.preventDefault();
        const pasted = (e.clipboardData || window.clipboardData).getData("text").trim();
        if (/^\d{6}$/.test(pasted)) {
          pasted.split("").forEach((digit, i) => {
            if (boxes[i]) boxes[i].value = digit;
          });
          boxes[5].focus();
          updateFullCode();
        }
      });
    });

    function updateFullCode() {
      let code = "";
      boxes.forEach(b => code += b.value);
      if (fullInput) fullInput.value = code;
    }
  }

  // Resend Countdown Timer (30 seconds)
  let countdown = 30;
  if (timerSpan) {
    const interval = setInterval(function () {
      countdown--;
      const formatted = countdown < 10 ? `0:0${countdown}` : `0:${countdown}`;
      timerSpan.textContent = formatted;

      if (countdown <= 0) {
        clearInterval(interval);
        if (resendBtn) {
          resendBtn.disabled = false;
          resendBtn.classList.remove("text-muted");
          resendBtn.textContent = "Resend OTP now";
        }
      }
    }, 1000);
  }
});
