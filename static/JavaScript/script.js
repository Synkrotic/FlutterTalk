// Global object
const mainSection = document.getElementById("main_post_section");

// Navbar objects
const navbar = document.getElementById("main-nav");
const accountButton = document.getElementById("account_button");
const accountActionButtons = document.getElementsByClassName("account_button_actions");

const headerNavButtons = document.getElementsByClassName("header_nav_btn");
const scrollUpButton = document.getElementById("scroll_up_button");

// Profile objects
const textAreas = document.getElementsByClassName("text_area");

// Create post objects
const createPostMenu = document.getElementById("create-post-container");
const contentArea = document.getElementById("content-area");
const contentCounter = document.getElementById("char-counter");

// Popup objects
const popupContainer = document.getElementById("popups-container");



// Event listeners
for (let i = 0; i < headerNavButtons.length; i++) {
  headerNavButtons[i].addEventListener("click", function () {
    if (this.className.includes(" active_page")) return;
    this.className = this.className.replace(" deactive_page", "");
    const current = document.getElementsByClassName("active_page");
    current[0].className = current[0].className.replace(
      "active_page",
      "deactive_page"
    );
    this.className += " active_page";
  });
}

if (scrollUpButton && mainSection) {
  scrollUpButton.addEventListener("click", function () {
    mainSection.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  });
}

if (textAreas) {
  for (let i = 0; i < textAreas.length; i++) {
    textAreas[i].addEventListener("input", function () {
      this.style.height = "auto";
      this.style.height = this.scrollHeight + "px";
    });
  }
}

if (contentArea) {
  contentArea.addEventListener("input", function () {
    console.log(Math.ceil(this.scrollHeight / parseFloat(getComputedStyle(this).lineHeight)));
    contentArea.scrollTop = contentArea.scrollHeight;
    const rows = Math.ceil(this.scrollHeight / parseFloat(getComputedStyle(this).lineHeight));
    if (rows > 16) {
      contentArea.value = this.value.slice(0, -1);
    }

    // Update the counter
    const content = this.value;
    const contentLength = content.length;

    if (!contentCounter) return;
    contentCounter.innerText = `${contentLength.toString()}/1000`;


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
}

if (accountActionButtons && accountButton) {
  document.addEventListener("mouseover", function (event) {
    if (!event) return;
    if (
      !Array.from(accountActionButtons).some(el => el.contains(event.target)) &&
      !accountButton.contains(event.target)
    ) {
      accountButton.classList.remove("active");
    }
  });
}


// Extra functions
function copyShareLinkToClipboard(accountName, postID) {
  const url = `/users/@${accountName}/${postID}`;
  navigator.clipboard.writeText(url);

  const share_button = document.getElementById(
    `share_button_${accountName}_${postID}`
  );
  if (!share_button) return;
  share_button.className += " active";
  setTimeout(() => {
    share_button.className = share_button.className.replace(" active", "");
  }, 1200);
}


// Button Functions
function showLogout() { if (accountButton) accountButton.classList.toggle("active"); }

function goToPage(location) {
  if (window.location.href === `${location}`) return;
  window.location.href = `${location}`;
}

function showPassword() {
  const passwordInput = document.getElementById("password-input");
  if (!passwordInput) return;
  if (passwordInput.type === "password") {
    passwordInput.type = "text";
  } else {
    passwordInput.type = "password";
  }
}

function toggleCreatePost() {
  if (!createPostMenu || !contentArea) return;
  createPostMenu.classList.toggle("hide-menu");
  contentArea.focus();
}

async function goToUserPage() {
  const isLoggedIn =  await fetch('/users/isLoggedIn').then((response) => { return response.json(); });
  console.log(isLoggedIn);

  goToPage(`/${isLoggedIn.logged_in ? `users/@${isLoggedIn.username}` : 'profile'}`);    
}