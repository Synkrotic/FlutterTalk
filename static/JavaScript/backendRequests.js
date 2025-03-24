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
