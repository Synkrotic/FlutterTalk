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
        alert(`You're not on https, no link copied to clipboard.\nLink to post is http://${window.location.host}/users/@${accountName}/${postID}`);
      else
        copyShareLinkToClipboard(accountName, postID);
      const share_button = doc.getElementById(`share_button_${postID}`);
      share_button.innerHTML = share_button.innerHTML.replace(
        /(\d+)/,
        (match) => parseInt(match) + 1
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

  console.log("test", likedByUser);

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

      if (data && typeof data.likes !== 'undefined') {
        likeText.innerHTML = data.likes;

        if (response.status === 201 || response.status === 200) {
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
        alert(`Error: ${errorData.error || response.statusText}`);
      } catch (e) {
        alert(`Error: ${response.statusText}`);
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
    // Make the fetch call
    const response = await fetch(url, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
    });

    // Only attempt to parse JSON if status is 200 (OK)
    let likeData;

    if (response.status === 200) {
      likeData = await response.json();
    } else {
      console.error("Request did not return a 200 status");
      return;
    }

    // Extract the like amount from the returned JSON
    // (Assuming the response has a property 'likes')
    const likeAmount = likeData;

    // Use the document object to select elements
    const icon = document.getElementById(`like_icon_${postID}`);
    const likeButton = document.getElementById(`like_amount_${postID}`);

    // Check if elements exist before modifying them
    if (likeButton) {
      likeButton.innerHTML = likeAmount;
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
    console.error("Error in removeLike:", error);
  }
}

function createPost() {
  const contentArea = doc.getElementById("content-area");
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
    }).then((res) => {
      if (res.status === 200) {
        window.location.reload();
      } else {
        throw new Error("Failed to add popup!");
      }
    });
  } catch (error) {
    console.error(error);
  }
}


function closePopup(id) {
  errorID = id.split("-")[1];
  try {
    fetch(`/closePopup/${errorID}`, {
      method: "POST",
    }).then((res) => {
      if (res.status === 200) {
        window.location.reload();
      } else {
        throw new Error("Failed to close popup!");
      }
    });
  } catch (error) {
    console.error(error);
  }
}