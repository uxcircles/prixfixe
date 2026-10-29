// Prix Fixe Brasserie — nav, scroll reveal, menu tabs, booking form

(function () {
  const body = document.body;

  // Mobile nav
  const toggle = document.querySelector(".nav-toggle");
  if (toggle) {
    toggle.addEventListener("click", () => {
      // The concept strip can push the header down, so start the overlay at its real bottom edge
      const header = document.querySelector(".site-header");
      body.style.setProperty("--nav-top", header.getBoundingClientRect().bottom + "px");
      const open = body.classList.toggle("nav-open");
      toggle.setAttribute("aria-expanded", open);
    });
    document.querySelectorAll(".nav a").forEach((a) =>
      a.addEventListener("click", () => body.classList.remove("nav-open"))
    );
  }

  // Reveal on scroll
  const reveals = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver(
      (entries) => entries.forEach((e) => {
        if (e.isIntersecting) { e.target.classList.add("is-in"); io.unobserve(e.target); }
      }),
      { rootMargin: "0px 0px -8% 0px" }
    );
    reveals.forEach((el) => io.observe(el));
  } else {
    reveals.forEach((el) => el.classList.add("is-in"));
  }

  // Menu tabs: highlight the section in view
  const tabs = document.querySelectorAll(".tabs a");
  if (tabs.length && "IntersectionObserver" in window) {
    const byId = {};
    tabs.forEach((t) => (byId[t.getAttribute("href").slice(1)] = t));
    const spy = new IntersectionObserver(
      (entries) => entries.forEach((e) => {
        if (!e.isIntersecting) return;
        tabs.forEach((t) => t.classList.remove("is-active"));
        byId[e.target.id]?.classList.add("is-active");
      }),
      { rootMargin: "-40% 0px -55% 0px" }
    );
    document.querySelectorAll(".menu-block").forEach((s) => spy.observe(s));
  }

  // Booking form (concept only, no backend)
  const form = document.querySelector("#booking-form");
  if (form) {
    const date = form.querySelector("#date");
    const today = new Date();
    const iso = new Date(today.getTime() - today.getTimezoneOffset() * 60000).toISOString().slice(0, 10);
    date.min = iso;
    date.value = iso;

    form.addEventListener("submit", (e) => {
      e.preventDefault();
      if (!form.reportValidity()) return;
      const data = new FormData(form);
      const when = new Date(data.get("date") + "T00:00").toLocaleDateString("en-GB", {
        weekday: "long", day: "numeric", month: "long",
      });
      document.querySelector("#confirm-text").textContent =
        `A table for ${data.get("guests")} on ${when} at ${data.get("time")}. ` +
        `We'll send confirmation to ${data.get("email")}.`;
      form.closest(".card").classList.add("is-sent");
    });
  }

  // Reviews strip arrows
  const strip = document.querySelector(".reviews");
  if (strip) {
    const step = () => strip.querySelector(".review").offsetWidth + 20;
    document.querySelector(".rv-prev")?.addEventListener("click", () => strip.scrollBy({ left: -step(), behavior: "smooth" }));
    document.querySelector(".rv-next")?.addEventListener("click", () => strip.scrollBy({ left: step(), behavior: "smooth" }));
  }

  const year = document.querySelector("#year");
  if (year) year.textContent = new Date().getFullYear();
})();
