let theme = false;
const themeSwitch = document.getElementById("theme_switch");

function lightMode(root) {
  root.style.setProperty("--background", "var(--lightSurface)");
  root.style.setProperty("--secondaryBackground", "var(--lightBackground)");
  root.style.setProperty("--primaryColor", "var(--lightGray)");
  root.style.setProperty("--secondaryColor", "var(--cloudGray)");
  root.style.setProperty("--tertiaryColor", "var(--coolWhite)");
  root.style.setProperty("--quaternaryColor", "var(--softBlueGray)");
  root.style.setProperty("--quinaryColor", "var(--dustyBlue)");
  root.style.setProperty("--senaryColor", "var(--steelBlue)");
  root.style.setProperty("--septenaryColor", "var(--textBlue)");
  root.style.setProperty("--octonaryColor", "var(--bodyText)");
  root.style.setProperty("--nonaryColor", "var(--tealAccent)");
  root.style.setProperty("--ctaColor", "var(--primaryBlue)");
  root.style.setProperty("--textColor", "var(--headingText)");
}

function darkMode(root) {
  root.style.setProperty("--background", "var(--blackish)");
  root.style.setProperty("--secondaryBackground", "var(--darkblackish)");
  root.style.setProperty("--primaryColor", "var(--darkBlue)");
  root.style.setProperty("--secondaryColor", "var(--mediumBlue)");
  root.style.setProperty("--tertiaryColor", "var(--moderateBlue)");
  root.style.setProperty("--quaternaryColor", "var(--darkCyan)");
  root.style.setProperty("--quinaryColor", "var(--darkGrayBlue)");
  root.style.setProperty("--senaryColor", "var(--powderBlue)");
  root.style.setProperty("--septenaryColor", "var(--grayBlue)");
  root.style.setProperty("--octonaryColor", "var(--pickledBlueWood)");
  root.style.setProperty("--nonaryColor", "var(--eastBay)");
  root.style.setProperty("--ctaColor", "var(--attentionBlue)");
  root.style.setProperty("--textColor", "var(--whiteText)");
}

function switchTheme() {
  const root = document.querySelector(":root");

  if (theme) darkMode(root);
  else lightMode(root);
  
  theme = !theme;

  document.cookie = `theme=${theme}; path=/;`;
}

function getCookie(startsStr) {
  const allCookies = document.cookie.split("; ");
  let cookieName = null;
  let cookieValue = null;
  allCookies.forEach(cookie => {
    if (cookie.startsWith(`${startsStr}`)) {
      const cookieSplit = cookie.split("=");
      cookieName = cookieSplit[0];
      cookieValue = cookieSplit[1];
    }
  });
  const res = [cookieName, cookieValue];
  return res;
}

function checkUserTheme() {
  let cookieTheme = getCookie("theme=")[1];
  const root = document.querySelector(":root");
  if (cookieTheme === "true") {
    theme = true
    lightMode(root);
  } else if (cookieTheme === "false") {
    theme = false
    darkMode(root);
  } else {
    document.cookie = `theme=${theme}; path=/;`;
  }
}

if (themeSwitch) {
  themeSwitch.addEventListener("click", function () {
    switchTheme();
  });
}

checkUserTheme();
themeSwitch.checked = theme;