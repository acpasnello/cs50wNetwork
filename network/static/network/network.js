document.addEventListener('DOMContentLoaded', function() {

  document.querySelectorAll(".likeicon").forEach(function(icon) {
    icon.onclick = function() {
      // Update like count, based on current like status of post by user
      // is this post liked by this user?
      iconinner = icon.firstElementChild;
      let status = (iconinner.dataset.liked === 'true');
      // Update displayed like # accordingly
      let postid = icon.dataset.postid;
      // Combine string for getting post count element
      let getlikecount = `#post${postid}likes`;
      // Get post like count value
      let likecount = document.querySelector(getlikecount);
      // console.log(likecount.innerHTML);
      // Update displayed like count
      if (status == true) {
        likecount.innerHTML = parseInt(likecount.innerHTML) - 1;
        iconinner.className = "fa-regular fa-heart";
        icon.style.color = "#A9A9A9";
        iconinner.dataset.liked = "false";

      }
      else {
        likecount.innerHTML = parseInt(likecount.innerHTML) + 1;
        iconinner.className = "fa-solid fa-heart";
        icon.style.color = "#FF0000";
        iconinner.dataset.liked = "true";
      }
      postid = parseInt(postid)
      update_like(postid, status)
    }
    // addEventListener("click", update_like)
  });
});

function update_like(postid, status) {
  // likecount = document.querySelector("")
  if (status) {
    // Fetch request to call view
    fetch(`/unlike/${postid}`)
    .then((response) => response.text())
    //.then((data) => console.log(data))
    .catch(function (error) {
      console.error('Error:', error);
    });
  }
  else {
    fetch(`/like/${postid}`)
    .then((response) => response.text())
    //.then((data) => console.log(data))
    .catch(function (error) {
      console.error('Error:', error);
    });
  }
}
