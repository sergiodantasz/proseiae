const theme = localStorage.getItem("theme") || "emerald";
document.documentElement.setAttribute("data-theme", theme);
document.cookie = `theme=${theme}; path=/; max-age=${31536000}; SameSite=Lax`;

document.addEventListener("DOMContentLoaded", () => {
  const themeControllers = document.querySelectorAll(".theme-controller");
  themeControllers.forEach((radio) => {
    if (radio.value === theme) {
      radio.checked = true;
    }
  });
});
