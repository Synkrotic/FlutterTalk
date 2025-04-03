function sharePost(accountName, postID) {
  const url = `/posts/addShare/${postID}`;
  fetch(url, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  }).then(async (response) => {
    if (response.status === 200) {
      if (location.protocol !== 'https:')
        addPopup(false, `You're not on https, no link copied to clipboard.\n
          Link to post is http://${window.location.host}/users/@${accountName}/${postID}`);
      else
        copyShareLinkToClipboard(accountName, postID);
      const share_button = document.getElementById(`share_button_${postID}`);
      if (!share_button) return;
      share_button.innerHTML = share_button.innerHTML.replace(
        /(\d+)/,
        (match) => (parseInt(match) + 1).toString()
      );
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

function createPost() {
  const contentArea = document.getElementById("content-area");
  if (!contentArea) return;
  const postContent = contentArea.value;

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
      addPopup(true, "Post created successfully!");
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
  try {
    fetch(`/addPopup/${errorType ? "success" : "error"}/${errorText}`, {
      method: "POST",
    }).then(async (res) => {
      if (res.ok && popupContainer) {
        const popupHTML = await res.text();
        popupContainer.insertAdjacentHTML("beforeend", popupHTML);
        setTimeout(() => {
          const popup = document.getElementById(`POPUP_CONTAINER_${errorID}`);
          if (popup)
            closePopup(errorID);
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
  const errorID = id.split("-")[1];
  try {
    fetch(`/closePopup/${errorID}`, {
      method: "POST",
    }).then((res) => {
      if (res.status === 200) {
        const popup = document.getElementById(`POPUP_CONTAINER_${errorID}`);
        if (popup)
          popup.remove();
        else
          console.error(`Popup with ID ${id} not found.`);
      } else {
        throw new Error("Failed to close popup!");
      }
    });
  } catch (error) {
    console.error(error);
  }
}