function sharePost(accountName, postID) {
  const url = `/posts/addShare/${postID}`;
  fetch(url, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  }).then(async (response) => {
    if (response.status === 200) {
      if (location.protocol !== 'https:') {
        addPopup(false, `You're not on https, no link copied to clipboard.\nLink to post is ${location.protocol}//${window.location.host}/users/@${accountName}/${postID}`)
      } else
        copyShareLinkToClipboard(accountName, postID);
      const share_button = document.getElementById(`share_button_${postID}`);
      if (!share_button) return;
      share_button.innerHTML = share_button.innerHTML.replace(
        /(\d+)/,
        (match) => (parseInt(match) + 1).toString()
      );
      share_button.classList.add("active")
      setTimeout(() => { share_button.classList.remove("active"); }, 2000);
    } else {
      const msg = await response.json();
      addPopup(false, `Failed to share post.${msg.error}`);
    }
  });
}


async function likePost(postID) {
  const url = `/users/like/${postID}`;

  const response = await fetch(url, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });

  let likedByUser;
  if (response.status === 200) {
    const data = await response.json();
    likedByUser = data.userLiked;
  }

  if (likedByUser) {
    removeLike(postID);
  } else {
    addLike(postID);
  }
}

async function addLike(postID) {
  const url = `/users/like/${postID}`;
  const likeText = document.getElementById(`like_amount_${postID}`);
  const icon = document.getElementById(`like_icon_${postID}`);

  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        'Accept': 'application/json',
      },
    });

    if (response.ok) {
      const data = await response.json();

      if (data && typeof data.likes !== 'undefined' && likeText) {
        likeText.innerHTML = data.likes;

        if (response.ok && icon) {
          icon.classList.remove("bi-heart");
          icon.classList.add("bi-heart-fill");
        }

        if (data.message) {
          console.log(`Like status for post ${postID}: ${data.message}`);
        }

      } else {
        console.error(`Received success status ${response.status}, but 'likes' key missing in response data for post ${postID}:`, data);
      }

    } else {
      console.error(`Failed to like post ${postID}. Status: ${response.status}`);
      try {
        const errorData = await response.json();
        console.error('Error details:', errorData);
        addPopup(false, `Failed to like post.\n
          ${errorData.error || response.statusText}`);
      } catch (e) {
        addPopup(false, `Failed to like post.\n
          ${response.statusText}`);
      }
    }
  } catch (error) {
    console.error(`Network error or other issue liking post ${postID}:`, error);
    alert("Could not connect to the server to like the post.");
  }
}

async function removeLike(postID) {
  const url = `/users/like/${postID}`;

  try {
    const response = await fetch(url, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
    });

    let likeData;

    if (response.status === 200) {
      likeData = await response.json();
    } else {
      console.error("Request did not return a 200 status");
      return;
    }

    const icon = document.getElementById(`like_icon_${postID}`);
    const likeButton = document.getElementById(`like_amount_${postID}`);

    if (likeButton) {
      likeButton.innerHTML = likeData;
    } else {
      console.warn(`like_button_${postID} not found`);
    }

    if (icon) {
      icon.classList.remove("bi-heart-fill");
      icon.classList.add("bi-heart");
    } else {
      console.warn(`like_icon_${postID} not found`);
    }
  } catch (error) {
    addPopup(false, `Failed to remove like.\n
      ${error.message}`);
    console.error("Error in removeLike:", error);
  }
}

async function followUser(accountName) {
  const url = `/users/follow/${accountName}`;
  response = await fetch(url)
  if (!response.ok) {
    if (response.status === 404) {
      msg = "You need to be logged in!";
    } else if (response.status === 403) {
      msg = "You cannot follow yourself!";
    } else if (response.status === 401) {
      msg = "Tried to follow a non existing user!";
    } else {
      msg = response.statusText;
    }
    addPopup(false, `Failed to follow user. ${msg}`);
    return;
  }

  followStatus = await response.json();

  if (followStatus) {
    removeFollow(accountName);
  } else {
    addFollow(accountName);
  }
}

async function addFollow(accountName) {
  const url = `/users/follow/${accountName}`;
  response = await fetch(url, {method: "POST"});
  if (!response.ok) {
    addPopup(false, `Failed to follow user. ${response.statusText}`);
    return;
  }

  addPopup(true, `You are now following ${accountName}`);
}

async function removeFollow(accountName) {
  const url = `/users/follow/${accountName}`;
  response = await fetch(url, {method: "DELETE"});
  if (!response.ok) {
    addPopup(false, `Failed to unfollow user. ${response.statusText}`);
    return;
  }

  addPopup(true, `You are no longer following ${accountName}`);
}

function createPost(submitButton) {
  const header = submitButton.parentElement;
  const dialog = header.parentElement;
  const contentArea = header.nextElementSibling;
  if (!contentArea) return;
  const postContent = contentArea.value;
  if (contentArea.length < 1) return;

  const url = "/post";
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ content: postContent })
  }).then((response) => {
    if (response.status === 200) {
      contentArea.value = "";
      dialog.classList.add("closed_dialog");
      dialog.close();
      addPopup(true, "Post created successfully!");
    } else {
      response.json().then((data) => {
        addPopup(false, data.statusText);
      });
    }
  });
}

function addComment(submitButton) {
  const header = submitButton.parentElement;
  const dialog = header.parentElement;
  const contentArea = header.nextElementSibling;
  if (!contentArea) return;
  const commentContent = contentArea.value;
  if (commentContent.length < 1) return;

  const parentID = dialog.classList.value.split('=')[1];

  const url = `/post/${parentID}`;
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ content: commentContent })
  }).then((response) => {
    if (response.status === 200) {
      contentArea.value = "";
      let lastClass = dialog.classList[dialog.classList.length - 1];
      dialog.classList.replace(lastClass, 'closed_dialog');
      setTimeout(dialog.close(), 500)
      addPopup(true, "Comment added successfully!");
    } else {
      response.json().then((data) => {
        addPopup(false, data.statusText);
      });
    }
  });
}





function logout() {
  fetch("/logout", {
    method: "POST",
  }).then((res) => {
    if (res.status !== 200) {
      res.json().then((data) => {
        throw new Error(data.errorText);
      }).catch((error) => {
        addPopup(false, error.message);
      });
    } else {
      addPopup(true, "Logged out successfully!");
    }
  });
}


function addPopup(errorType, errorText) {
  url = "/getHTMLFile/popup.html";
  try {
    fetch(url, {
      method: "GET",
    }).then(async (res) => {
      if (res.ok && popupContainer) {
        const errorID = Math.floor(Math.random() * 1000000);
        document.cookie = `POPUP-${errorID}={"type": ${errorType}, "text": "${errorText}"}; path=/;`;

        let popupHTML = await res.text();
        popupHTML = popupHTML.replace("{{ popupType|lower }}", errorType ? "success" : "error");
        popupHTML = popupHTML.replace("{{ popupType|upper }}", errorType ? "SUCCESS" : "ERROR");
        popupHTML = popupHTML.replace("{{ errorID }}", errorID);
        popupHTML = popupHTML.replace("{{ errorID }}", errorID);
        popupHTML = popupHTML.replace("{{ errorText }}", errorText);
        popupContainer.insertAdjacentHTML("beforeend", popupHTML);
        setTimeout(() => {
          const popup = document.getElementById(`POPUP_CONTAINER_${errorID}`);
          if (popup)
            closePopup(`POPUP_${errorID}`);
        }, 20000)
      } else {
        throw new Error("Failed to add popup!");
      }
    });
  } catch (error) {
    console.error(error);
  }
}


function closePopup(id) {
  try {
    const popupIDArr = id.toString().split('_');
    const popupID = popupIDArr[popupIDArr.length - 1];
    if (!popupID) return;

    const popup = document.getElementById(`POPUP_CONTAINER_${popupID}`);
    if (!popup) return;
    
    const popupType = popup.classList[popup.classList.length - 1];
    const popupText = popup.querySelector(".popup-text").innerHTML;
    if (!popupText || !popupType) return;

    document.cookie = `POPUP-${popupID}={"type": ${popupType}, "text": "${popupText}"}; expires=Thu, 1 jan 2000 12:00:00 UTC;  path=/;`;
    popup.remove();
  } catch (error) {
    console.error("Error closing popup:", error);
  }
}

function loadPopups() {
  const allCookies = document.cookie.split("; ");
  allCookies.forEach(cookie => {
    if (cookie.startsWith("POPUP-")) {
      const cookieValue = cookie.split("=")[1];
      const popupData = JSON.parse(decodeURIComponent(cookieValue));
      const popupID = cookie.split("=")[0].split("-")[1];

      if (popupData) {
        addPopup(popupData.type, popupData.text);
        document.cookie = `POPUP-${popupID}={"type": ${popupData.type}, "text": "${popupData.text}"}; expires=Thu, 1 jan 2000 12:00:00 UTC; path=/;`;
      }
    }
  });
}

loadPopups();