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
  });

  document.querySelectorAll(".editpost").forEach((item) => {
    item.onclick = function() {
      // Get parent and post's current content
      let parent = item.parentElement;
      let currentContent = parent.getElementsByClassName("postcontent")[0].innerText;
      // Get post id
      let postid = parseInt(parent.getElementsByClassName("likeicon")[0].dataset.postid);
      // let token = "{% csrf_token %}";
      // console.log(typeof(postid))
      // Hide all of parent's children
      for (let i = 0; i < parent.children.length; i++) {
        parent.children[i].style.display = "none";
      }
      // Create new elements for editing
      let newDiv = document.createElement("div")
      newDiv.innerHTML =
      `<form>
        <input type="hidden" id="postid" name="postid" value="${postid}">
        <label for="updatepost">Edit Post:</label>
        <textarea id="updatepost" autofocus>${currentContent}</textarea>
        <button id="submitedit" class="btn btn-outline-warning">Submit</button>
      </form>`;
      // Append editing elements to parent
      parent.appendChild(newDiv);
      // Move cursor to end of text
      const textarea = newDiv.querySelector("#updatepost");
      const end = textarea.value.length;
      textarea.setSelectionRange(end,end);
      textarea.focus();
      // Add Event Listener on Button
      let submitbutton = newDiv.querySelector("#submitedit");
      if (submitbutton != undefined) {
        console.log(newDiv.querySelector("#updatepost").value)
      }
      else {
        console.log('fail')
      }

      submitbutton.addEventListener("click", function(event) {
        event.preventDefault()
        console.log(newDiv.querySelector("#updatepost").value)
        var response = editpost(newDiv);
        var updatedpost = response.then(data => {
          console.log(data.content);
          parent.getElementsByClassName("postcontent")[0].innerText = data.content;
          return data;
        })
        for (let i = 0; i < parent.children.length; i++) {
          console.log(parent.children[i])
          let node = parent.children[i];
          // console.log(node)
          if (node.attributes.getNamedItem("style")) {
            node.attributes.removeNamedItem("style");
          }
        }
        newDiv.style.display = "none";
        newDiv.remove();
      });

    }
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

async function editpost(editDiv) {
  let newContent = editDiv.querySelector("#updatepost").value;
  console.log(newContent)
  let postid = editDiv.querySelector("#postid").value;
  let csrftoken = getCookie('csrftoken');
  let body = {
    postid: postid,
    newContent: newContent
  };
  let response = await fetch('/editpost', {
    method: "POST",
    mode: "no-cors",
    headers: {"X-CSRFToken": csrftoken,
      'Content-Type': 'application/json:charset=utf-8'
    },
    body: JSON.stringify(body)
  });
  // .then(response => response.json())
  // .then(data => {
  //   post = data;
  //   console.log(post)
  //   return post;
  // })
  // .catch(function (error) {
  //   console.error('Error: ', error);
  // });
  let result = await response.json();
  console.log(result)
  return await result;
  // if (response.ok) {
  //   let result = await response.json();
  //   console.log(result.state)
  //   post = await result;
  //   return post;
  // }
  // else {
  //   console.log("HTTP-Error: ", response.status);
  // }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
