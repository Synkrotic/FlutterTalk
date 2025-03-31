const postsContainer = document.getElementById('main_post_section');
const postLoadingIcon = document.getElementById('posts_loading_spinner');
let lastTime = new Date().getTime();

function loadNewPostsEvent() {
  if (!postsContainer || !postLoadingIcon) { 
    console.error('Post container or loading icon not found');
    return;
  }

  postsContainer.addEventListener('scroll', loadNewPosts);
}

async function loadNewPosts(recursionLevel = 0) {  
  if (postsContainer.scrollTop + postsContainer.clientHeight < postsContainer.scrollHeight * 0.9) return;
  if (recursionLevel > 5) { console.log(recursionLevel); addPopup(false, "Unable to load more posts!"); return; }

  const now = new Date().getTime();
  const timeDelta = now - lastTime;
  if (timeDelta < 100) return;
  lastTime = now;

  const url = `/getPosts/10`;
  const posts = await fetch(url).then((response) => {
    if (response.ok) { return response; }
    else return null;
  });
  if (!posts || posts.length == 0) {
    addPopup(false, 'Failed to load posts');
    setTimeout(() => loadNewPosts(recursionLevel + 1), 1000);
    return;
  }

  const postHTML = await fetch(`/getHTMLFile/post.html`, { method: "POST" }).then((response) => {
    if (response.ok) { return response; }
    else return null;
  });
  if (!postHTML) {
    addPopup(false, 'Failed to load posts');
    setTimeout(() => loadNewPosts(recursionLevel + 1), 1000);
    return;
  }

  const postHTMLText = await postHTML.text();
  const postsList = await posts.json();

  for (let postObject of postsList) {
    if (!postObject) continue;

    console.log(postHTMLText);
    const likeablePost = postHTMLText.replace(`{% if post.liked %}
        <i class="bi bi-heart-fill" id="like_icon_{{ post.postID }}"></i>
        {% else %}
        <i class="bi bi-heart" id="like_icon_{{ post.postID }}"></i>
        {% endif %}`,
    `<i class='bi bi-heart${postObject.liked ? "-fill" : ""}' id='like_icon_{{ post.postID }}'></i>`);

    let updatedPostHTML = fillJinjaVars(likeablePost, postObject);
    if (!updatedPostHTML) {
      setTimeout(() => loadNewPosts(recursionLevel + 1), 1000);
      return false;
    }

    postsContainer.insertAdjacentHTML('beforeend', updatedPostHTML);
    postsContainer.insertBefore(postLoadingIcon, postsContainer.lastChild);
  }
}

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

loadNewPostsEvent();