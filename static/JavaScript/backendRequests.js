function sharePost(accountName, postID) {
  if (location.protocol !== 'https:'){
    alert("You're not on https, no link copied to clipboard.");
    return;
  }
  const url = `/users/addShare/${postID}`;
  fetch(url, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  }).then((response) => {
    if (response.status === 200) {
      copyShareLinkToClipboard(accountName, postID);
      alert("Link copied to clipboard!");
      const share_button = doc.getElementById(`share_button_${postID}`);
      share_button.innerHTML = share_button.innerHTML.replace(
        /(\d+)/,
        (match) => parseInt(match) + 1
      );
    }
  });
}


async function likePost(postID) {
  const url = `/users/like/${postID}`;

  likedByUser = await fetch(url, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  }).then((response) => {
    if (response.status === 200) {
      return response.json().userLiked;
    }
  });

  if (likedByUser)
    removeLike(postID);
  else
    addLike(postID);

  //window.location.reload();
}

async function addLike(postID) {
  url = `/users/like/${postID}`;
  const likeAmount = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  }).then((response) => {
    if (response.status === 200) {
      return response.json();
    }
  });

  const likeText = doc.getElementById(`like_amount_${postID}`);
  const icon = doc.getElementById(`like_icon_${postID}`);
  likeText.value = likeAmount;
  icon.classList.remove("bi-heart");
  icon.classList.add("bi-heart-fill");
}

async function removeLike(postID) {
  url = `/users/like/${postID}`;
  const likeAmount = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  }).then((response) => {
    if (response.status === 200) {
      return response;
    }
  });

  const icon = doc.getElementById(`like_icon_${postID}`);
  likeButton.innerHTML = likeAmount;
  icon.classList.remove("bi-heart");
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