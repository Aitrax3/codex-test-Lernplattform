(() => {
  const STORAGE_KEY = "loopwise_theme";
  const THEMES = ["dark", "light"];

  const getStoredTheme = () => {
    try {
      const value = window.localStorage.getItem(STORAGE_KEY);
      return THEMES.includes(value) ? value : null;
    } catch {
      return null;
    }
  };

  const setStoredTheme = (theme) => {
    try {
      window.localStorage.setItem(STORAGE_KEY, theme);
    } catch {
      // ignore
    }
  };

  const applyTheme = (theme) => {
    const root = document.documentElement;
    root.dataset.theme = theme;
    const toggle = document.querySelector("[data-theme-toggle]");
    if (toggle) {
      toggle.textContent = theme === "light" ? "Dark" : "Light";
      toggle.setAttribute(
        "aria-label",
        theme === "light" ? "Zu Dark Mode wechseln" : "Zu Light Mode wechseln",
      );
    }
  };

  const nextTheme = (current) => (current === "light" ? "dark" : "light");

  const init = () => {
    const stored = getStoredTheme();
    const initial = stored || "dark";
    applyTheme(initial);

    const toggle = document.querySelector("[data-theme-toggle]");
    if (!toggle) return;
    toggle.addEventListener("click", () => {
      const current = document.documentElement.dataset.theme || "dark";
      const updated = nextTheme(current);
      setStoredTheme(updated);
      applyTheme(updated);
    });
  };

  window.LoopwiseTheme = { init, applyTheme };
})();

