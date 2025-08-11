const validThemes = ["emerald", "night"];

function setTheme(theme) {
  localStorage.setItem("theme", theme);
  document.documentElement.setAttribute("data-theme", theme);
  document.cookie = `theme=${theme}; path=/; max-age=${31536000}; SameSite=Lax`;
}

document.addEventListener("DOMContentLoaded", () => {
  let savedTheme = localStorage.getItem("theme") || "emerald";

  if (!validThemes.includes(savedTheme)) {
    savedTheme = "emerald";
  }

  setTheme(savedTheme);

  document.querySelectorAll(".theme-controller").forEach((radio) => {
    radio.checked = radio.value === savedTheme;

    radio.addEventListener("change", () => {
      setTheme(radio.value);
      htmx.trigger(document.body, "themeChanged");
    });
  });
});
