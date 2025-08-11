function setTheme(theme) {
  localStorage.setItem("theme", theme);
  document.documentElement.setAttribute("data-theme", theme);
  document.cookie = `theme=${theme}; path=/; max-age=${31536000}; SameSite=Lax`;
}

document.addEventListener("DOMContentLoaded", () => {
  const theme = localStorage.getItem("theme") || "emerald";

  document.querySelectorAll(".theme-controller").forEach((radio) => {
    radio.checked = radio.value === theme;

    radio.addEventListener("change", () => {
      setTheme(radio.value);
      htmx.trigger(document.body, "themeChanged");
    });
  });
});
