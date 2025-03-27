// Global object
const doc = document;
const mainSection = doc.getElementById("main_section");

// Navbar objects
const navbar = doc.getElementById("main-nav");
const accountButton = doc.getElementById("account_button");
const logoutButton = doc.getElementById("logout_menu_button");

const headerNavButtons = doc.getElementsByClassName("header_nav_btn");
const scrollUpButton = doc.getElementById("scroll_up_button");

// Profile objects
const textAreas = doc.getElementsByClassName("text_area");

// Create post objects
const createPostMenu = doc.getElementById("create-post-container");
const contentArea = doc.getElementById("content-area");
const contentCounter = doc.getElementById("char-counter");



// Event listeners
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

if (textAreas) {
  for (let i = 0; i < textAreas.length; i++) {
    textAreas[i].addEventListener("input", function () {
      this.style.height = "auto";
      this.style.height = this.scrollHeight + "px";
    });
  }
}

contentArea.addEventListener("input", function () {
  contentArea.scrollTop = contentArea.scrollHeight;
  const rows = Math.ceil(this.scrollHeight / parseFloat(getComputedStyle(this).lineHeight));
  if (rows > 15)
    this.value = this.value.slice(0, -1);

  // Update the counter
  const content = this.value;
  const contentLength = content.length;
  contentCounter.innerText = contentLength;


  if (contentLength > 980) {
    contentCounter.style.color = "#ff4d4d";
    contentCounter.style.fontWeight = "bold";
  } else if (contentLength > 900) {
    contentCounter.style.color = "#ff8888";
    contentCounter.style.fontWeight = "800";
  } else {
    contentCounter.style.color = "snow";
    contentCounter.style.fontWeight = "600";
  }
});

doc.addEventListener("mouseover", function (event) {
  if (
    !logoutButton.contains(event.target) &&
    !accountButton.contains(event.target)
  ) {
    accountButton.classList.remove("active");
  }
});


// Extra functions
function copyShareLinkToClipboard(accountName, postID) {
  const url = `/users/@${accountName}/${postID}`;
  navigator.clipboard.writeText(url);

  const share_button = doc.getElementById(
    `share_button_${accountName}_${postID}`
  );
  share_button.className += " active";
  setTimeout(() => {
    share_button.className = share_button.className.replace(" active", "");
  }, 1200);
}


// Button Functions
function showLogout() { accountButton.classList.toggle("active"); }

function goToPage(location) {
  if (window.location.href === `${location}`) return;
  window.location.href = `${location}`;
}

function showPassword() {
  const passwordInput = doc.getElementById("password-input");
  if (passwordInput.type === "password") {
    passwordInput.type = "text";
  } else {
    passwordInput.type = "password";
  }
}

function toggleCreatePost() {
  createPostMenu.classList.toggle("hide-menu");
  contentArea.focus();
}