document.addEventListener("DOMContentLoaded", () => {
  const cards = document.querySelectorAll(".card-animate, .info-box, .profile-card, .about-card, .stat-box, .mini-panel, .dashboard-card");

  cards.forEach((card, index) => {
    card.style.animationDelay = `${index * 0.12}s`;
  });

  const counters = document.querySelectorAll("[data-target]");
  counters.forEach((counter) => {
    const target = Number(counter.dataset.target || 0);
    const suffix = target >= 100 ? "%" : "+";
    let current = 0;
    const step = Math.max(1, Math.ceil(target / 30));

    const timer = setInterval(() => {
      current += step;
      if (current >= target) {
        current = target;
        clearInterval(timer);
      }
      counter.textContent = `${current}${suffix}`;
    }, 40);
  });

  const buttons = document.querySelectorAll(".btn");

  buttons.forEach((button) => {
    button.addEventListener("mouseenter", () => {
      button.style.transform = "translateY(-3px)";
    });

    button.addEventListener("mouseleave", () => {
      button.style.transform = "translateY(0)";
    });
  });

  const quickChoices = document.querySelectorAll(".quick-choice");
  const userTypeInput = document.querySelector("input[name='userType']");

  quickChoices.forEach((button) => {
    button.addEventListener("click", () => {
      quickChoices.forEach((item) => item.classList.remove("active"));
      button.classList.add("active");
      if (userTypeInput) {
        userTypeInput.value = button.dataset.choice || "New User";
      }
    });
  });

  const contactForm = document.querySelector(".contact-form");

  if (contactForm) {
    contactForm.addEventListener("submit", (event) => {
      event.preventDefault();

      const formData = new FormData(contactForm);
      const name = (formData.get("name") || "").toString().trim();
      const email = (formData.get("email") || "").toString().trim();
      const message = (formData.get("message") || "").toString().trim();
      const inquiryType = (formData.get("inquiryType") || "General Inquiry").toString().trim();
      const userType = (formData.get("userType") || "New User").toString().trim();

      const text = [
        "Hi Sachin,",
        `${userType}.`,
        name ? `My name is ${name}.` : "",
        email ? `Email: ${email}` : "",
        inquiryType ? `Inquiry type: ${inquiryType}` : "",
        message ? message : "I would like to connect with you.",
        ""
      ].filter(Boolean).join("\n");

      const whatsappUrl = `https://wa.me/919226313805?text=${encodeURIComponent(text)}`;
      window.open(whatsappUrl, "_blank", "noopener,noreferrer");
      contactForm.reset();
      if (userTypeInput) userTypeInput.value = "New User";
      quickChoices.forEach((item) => {
        item.classList.toggle("active", item.dataset.choice === "New User");
      });
    });
  }
});
