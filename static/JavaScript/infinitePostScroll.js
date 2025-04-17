let postsContainer = document.getElementById('main_post_section');
// if (document.getElementById('search_results_container')) postsContainer = document.getElementById('search_results_container');
const postLoadingIcon = document.getElementById('posts_loading_spinner');
let lastTime = new Date().getTime();

async function loadNewPosts(recursionLevel = 0, query = null, container=postsContainer) {
  if (!container || !postLoadingIcon) return false;

  if (container.scrollTop + container.clientHeight < container.scrollHeight * 0.9) return false;
  if (recursionLevel > 5) {
    addPopup(false, "Unable to load more posts!");
    return false;
  }

  const now = new Date().getTime();
  const timeDelta = now - lastTime;
  if (timeDelta < 500) return false;
  lastTime = now;

  let url = `/getPosts/10`;
  if (window.location.href.includes("?following=true")) url += `?following=true`;
  if (query) url += `?query=${query}`;
  const posts = await fetch(url).then((response) => {
    if (response.ok) { return response; }
    else return null;
  });
  if (!posts || posts.length == 0) {
    addPopup(false, 'Failed to load posts');
    setTimeout(() => loadNewPosts(recursionLevel + 1), 1000);
    return false;
  }

  const postHTML = await fetch(`/getHTMLFile/post.html`, { method: "GET" }).then((response) => {
    if (response.ok) { return response; }
    else return false;
  });
  if (!postHTML) {
    addPopup(false, 'Failed to load posts');
    setTimeout(() => loadNewPosts(recursionLevel + 1), 1000);
    return false;
  }

  const postHTMLText = await postHTML.text();
  const postsList = await posts.json();

  for (let postObject of postsList) {
    if (!postObject) continue;

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

    container.insertAdjacentHTML('beforeend', updatedPostHTML);
    container.insertBefore(postLoadingIcon, container.lastChild);
  } 
}

function addInfiniteScrollToContainer(container, query) {
  if (!container) container = postsContainer;
  if (!query) query = null;
  
  if (!container) return false
  container.addEventListener('scroll', function() { loadNewPosts(0, query, container); });
}

if (!window.location.href.includes("/search")) {
  console.log("test");
  window.addEventListener("load", loadNewPosts)
  addInfiniteScrollToContainer();
}