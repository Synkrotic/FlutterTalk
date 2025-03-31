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

async function loadNewPosts() {  
  if (postsContainer.scrollTop + postsContainer.clientHeight < postsContainer.scrollHeight * 0.9) {
    postLoadingIcon.classList.add('hidden');
    return;
  }

  const now = new Date().getTime();
  const timeDelta = now - lastTime;
  if (timeDelta < 100) return;
  lastTime = now;

  postLoadingIcon.classList.remove('hidden');
  const url = `/getPosts/1`;
  const posts = await fetch(url).then((response) => {
    if (response.ok) { return response; }
    else return null;
  });
  if (!posts) {
    addPopup(false, 'Failed to load posts');
    // console.error('Failed to load post object');
    postLoadingIcon.classList.add('hidden');
    setTimeout(loadNewPosts, 1000);
    return;
  }

  const postHTML = await fetch(`/getHTMLFile/post.html`, { method: "POST" }).then((response) => {
    if (response.ok) { return response; }
    else return null;
  });
  if (!postHTML) {
    addPopup(false, 'Failed to load posts');
    postLoadingIcon.classList.add('hidden');
    setTimeout(loadNewPosts, 1000);
    return;
  }

  const postHTMLText = await postHTML.text();
  const postsList = await posts.json();
  const postObject = postsList[0];
  const updatedPostHTML = fillJinjaVars(postHTMLText, postObject);
  if (!updatedPostHTML) {
    setTimeout(loadNewPosts, 1000);
    return false;
  }

  postsContainer.insertAdjacentHTML("beforeend", updatedPostHTML)
}

function fillJinjaVars(html, object) {
  if (!object || !html) {
    console.error('Post object or html is null or undefined');
    return false;
  }

  const html2 = html.replace(
    `{% if post.liked %}
        <i class="bi bi-heart-fill" id="like_icon_{{ post.postID }}"></i>
        {% else %}
        <i class="bi bi-heart" id="like_icon_{{ post.postID }}"></i>
        {% endif %}`,
    `<i class='bi bi-heart${object.liked ? "-fill" : ""}' id='like_icon_{{ post.postID }}'></i>`); 

  const regex = /{{\s*post\.(\w+)\s*}}/g;
  return html2.replace(regex, (match, p1) => {
    if (object[p1] !== undefined) {
      return object[p1];
    } else {
      console.warn(`Property ${p1} not found in object`);
      return match;
    }
  });
}

loadNewPostsEvent();