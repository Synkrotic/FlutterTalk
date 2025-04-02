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

// Search objects
const searchBar = document.getElementById("main_search_bar");



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

if (searchBar) {
  searchBar.addEventListener("input", function () {
    const searchValue = this.value;
    if (searchValue.length < 1) return;

    setTimeout(async () => {
      const searchValue2 = this.value;
      if (searchValue !== searchValue2) return;

      const postsContainer = document.getElementById("search_results_container");
      if (!postsContainer) return;

      postsContainer.removeEventListener("scroll", loadNewPosts);
      console.log(postsContainer.children.length);
      for (let childIndex = 0; childIndex < postsContainer.children.length; childIndex++) {
        let child = postsContainer.children[childIndex];
        console.log(childIndex, child);
        if (!child) continue;

        if (child.classList.contains("loading_spinner_container")) continue;
        postsContainer.removeChild(child);
      }

      loadNewPosts(0, searchValue, postsContainer);
      const status = await fetch(`/getPosts/10?query=${searchValue}`).then((response) => {
        if (response.ok) { return response.json(); }
        return false;
      });
      console.log(status)
      if (status.length > 0) addInfiniteScrollToContainer(postsContainer);
      else {
        const noResults = document.createElement("div");
        noResults.className = "no_results";
        noResults.innerText = "No results found!";
        postsContainer.appendChild(noResults);
      }
    }, 1000);
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


// General functions
function fillJinjaVars(html, object) {
  if (!object || !html) {
    console.error('Post object or html is null or undefined');
    return false;
  }

  const regex = /{{\s*post\.(\w+)\s*}}/g;
  return html.replace(regex, (match, p1) => {
    if (object[p1] !== undefined) {
      return object[p1];
    } else {
      console.warn(`Property ${p1} not found in object`);
      return match;
    }
  });
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