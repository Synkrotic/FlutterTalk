// Global object
const mainSection = document.getElementById("main_post_section");
let eventListener = false;

// Navbar objects
const navbar = document.getElementById("main-nav");
const accountButton = document.getElementById("account_button");
const accountActionButtons = document.getElementsByClassName("account_button_actions");

const headerNavButtons = document.getElementsByClassName("header_nav_btn");
const scrollUpButton = document.getElementById("scroll_up_button");

// Profile objects
const textAreas = document.getElementsByClassName("text_area");
const pfpInput = document.getElementById("pfp-input");

// Create post objects
const dialog_inputs = document.getElementsByClassName("dialog_textarea");

// Popup objects
const popupContainer = document.getElementById("popups-container");

// Search objects
const searchBar = document.getElementById("main_search_bar");

// Account objects
const accountPosts = document.getElementById("main_post_section");



// Event listeners
if (scrollUpButton && mainSection) {
  scrollUpButton.addEventListener("click", function () {
    mainSection.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  });
}

if (pfpInput) {
  pfpInput.addEventListener("change", function () {
    const file = this.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = function (e) {
      const image = document.getElementById("pfp-preview");
      if (image) {
        image.src = e.target.result;
      }
    };
    reader.readAsDataURL(file);
  });
}

// if (accountPosts) {
//   if (window.location.href.includes("/users/@")) {
//     document.cookie = "current_post=0; expires=Thu, 1 jan 2000 12:00:00 UTC;  path=/;";
//     const user = window.location.href.split("/").pop();
//     accountPosts.innerHTML = "";
//     loadNewPosts(0, user, accountPosts);
//     if (!eventListener) {
//       accountPosts.addEventListener("scroll", function () {
//         eventListener = true;
//         loadNewPosts(0, user, accountPosts);
//       });
//     }
//   }
// }

if (searchBar) {
  searchBar.addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
      event.preventDefault();
      const searchValue = this.value.trim();
      if (searchValue.length < 1) return;
      
      const postsContainer = document.getElementById("main_post_section");
      if (!postsContainer) return;
      if (!searchListener) {
        document.cookie = "current_post=0; expires=Thu, 1 jan 2000 12:00:00 UTC;  path=/;";
        postsContainer.innerHTML = "";
      }

      loadNewPosts(0, searchValue, postsContainer);
      fetch(`/getPosts/10?query=${encodeURIComponent(searchValue)}`)
        .then(response => {
          if (response.ok) return response.json();
          return false;
        })
        .then(status => {
          if (status && status.length > 0) {
            searchListener = true;
            if (searchListener)
              postsContainer.removeEventListener("scroll", loadNewPosts);
            postsContainer.addEventListener("scroll", function () {
              console.log("test");
              loadNewPosts(0, searchValue, postsContainer);
            });
          } else {
            const noResults = document.createElement("div");
            noResults.className = "no_results";
            noResults.innerText = "No results found!";
            postsContainer.appendChild(noResults);
          }
        });
    }
  });
  // searchBar.addEventListener("input", function () {
  //   const searchValue = this.value;
  //   if (searchValue.length < 1) return;

  //   setTimeout(async () => {
  //     const searchValue2 = this.value;
  //     if (searchValue !== searchValue2) return;

  //     document.cookie = "current_post=0; expires=Thu, 1 jan 2000 12:00:00 UTC;  path=/;"
  //     const postsContainer = document.getElementById("search_results_container");
  //     if (!postsContainer) return;

  //     // postsContainer.removeEventListener("scroll", loadNewPosts);
  //     postsContainer.innerHTML = "";

  //     loadNewPosts(0, searchValue, postsContainer);
  //     const status = await fetch(`/getPosts/10?query=${searchValue}`).then((response) => {
  //       if (response.ok) { return response.json(); }
  //       return false;
  //     });
  //     console.log(status, status.length)
  //     if (status.length > 0) {
  //       addInfiniteScrollToContainer(postsContainer, searchValue);
  //     }
  //     else {
  //       const noResults = document.createElement("div");
  //       noResults.className = "no_results";
  //       noResults.innerText = "No results found!";
  //       postsContainer.appendChild(noResults);
  //     }
  //   }, 1000);
  // });
}

if (textAreas) {
  for (let i = 0; i < textAreas.length; i++) {
    textAreas[i].addEventListener("input", function () {
      this.style.height = "auto";
      this.style.height = this.scrollHeight + "px";
    });
  }
}

for (let i = 0; i < dialog_inputs.length; i++) {
  let input = dialog_inputs[i];
  if (input) {
    input.addEventListener("input", function () {
      input.scrollTop = input.scrollHeight;
      const rows = Math.ceil(this.scrollHeight / parseFloat(getComputedStyle(this).lineHeight));
      maxChars = 999;
      if (rows > 16) {
        input.value = this.value.slice(0, -1);
        maxChars = this.value.length;
      }

      // Update the counter
      const content = this.value;
      const contentLength = content.length;
      const dialog_counter = input.nextElementSibling;

      if (!dialog_counter) return;
      dialog_counter.innerText = `${contentLength.toString()}/${maxChars}`;


      if (contentLength > (maxChars - 20)) {
        dialog_counter.style.color = "#ff4d4d";
        dialog_counter.style.fontWeight = "bold";
      } else if (contentLength > (maxChars - 100)) {
        dialog_counter.style.color = "#ff8888";
        dialog_counter.style.fontWeight = "800";
      } else {
        dialog_counter.style.color = "snow";
        dialog_counter.style.fontWeight = "600";
      }
    });
  }
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

async function goToUserPage() {
  const isLoggedIn =  await fetch('/users/isLoggedIn').then((response) => { return response.json(); });
  console.log(isLoggedIn);

  goToPage(`/${isLoggedIn.logged_in ? `users/@${isLoggedIn.username}` : 'profile'}`);    
}
