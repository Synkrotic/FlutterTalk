const doc = document;
const headerNavButtons = doc.getElementsByClassName("header_nav_btn");
const scrollUpButton = doc.getElementById("scroll_up_button");

const mainSection = doc.getElementById("main_section");

for (let i = 0; i < headerNavButtons.length; i++) {
  headerNavButtons[i].addEventListener("click", function () {
    if (this.className.includes(" active_page")) return;
    this.className = this.className.replace(" deactive_page", "");
    const current = doc.getElementsByClassName("active_page");
    current[0].className = current[0].className.replace(
      "active_page",
      "deactive_page"
    );
    this.className += " active_page";
  });
}

scrollUpButton.addEventListener("click", function () {
  mainSection.scrollTo({
    top: 0,
    behavior: "smooth",
  });
});

function goToPage(location) {
  if (window.location.href === `${location}`) return;
  window.location.href = `${location}`;
}

function showPassword() {
  const passwordInput = document.getElementById("password-input");
  if (passwordInput.type === "password") {
    passwordInput.type = "text";
  } else {
    passwordInput.type = "password";
  }
}