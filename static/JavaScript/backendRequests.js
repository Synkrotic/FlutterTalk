ip = "localhost";

function sharePost(accountName, postID) {
  const url = `http:/${ip}:5500/users/@${accountName}/${postID}/addShare`;
  fetch(url, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  }).then((response) => {
    if (response.status === 200) {
      copyShareLinkToClipboard(accountName, postID);

      const share_button = doc.getElementById(
        `share_button_${accountName}_${postID}`
      );
      share_button.innerHTML = share_button.innerHTML.replace(
        /(\d+)/,
        (match) => parseInt(match) + 1
      );
    }
  });
}

function copyShareLinkToClipboard(accountName, postID) {
  const url = `http://${ip}:5500/users/@${accountName}/${postID}`;
  navigator.clipboard.writeText(url);

  const share_button = doc.getElementById(
    `share_button_${accountName}_${postID}`
  );
  share_button.className += " active";
  setTimeout(() => {
    share_button.className = share_button.className.replace(" active", "");
  }, 1200);
}
