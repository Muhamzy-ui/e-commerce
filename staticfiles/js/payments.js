document.addEventListener("DOMContentLoaded", function () {
  // Select all payment option cards
  const cards = document.querySelectorAll(".payment-option-card");

  cards.forEach((card) => {
    card.addEventListener("click", function () {
      // Deselect all cards
      cards.forEach((c) => c.classList.remove("selected"));

      // Select clicked card
      card.classList.add("selected");

      // Check the corresponding radio input
      const radio = card.querySelector('input[type="radio"]');
      if (radio) {
        radio.checked = true;
      }
    });

    // Also allow keyboard accessibility
    card.addEventListener("keypress", function (e) {
      if (e.key === "Enter" || e.key === " ") {
        card.click();
      }
    });
  });
});
