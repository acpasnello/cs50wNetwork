document.addEventListener('DOMContentLoaded', function() {
  document.querySelector("#profileview").style.display = 'block';
  document.querySelector("#listview").style.display = 'none';
  document.querySelector("#postsdisplay").addEventListener('click', display_posts)
  if (document.querySelector("#followbutton")) {
    document.querySelector("#followbutton").addEventListener('click', updatefollow)
  }
  // document.querySelector(".listlink").addEventListener('click', get_list(this))
});

function get_list(submittedlist, userid) {
  // Clear previously displayed list
  document.querySelector("#listview").innerHTML = "";
  // Trim number from front of string
  submittedlist = submittedlist.innerText
  let cut = submittedlist.lastIndexOf(" ");
  let desiredlist = submittedlist.slice(parseInt(cut+1));
  // Get user id
  userid = userid
  // CSRFtoken
  const csrftoken = getCookie('csrftoken');
  document.querySelector("#listview").style.display = 'block'
  fetch(`/userlist/${desiredlist}`, {
    method: 'POST',
    headers: {'X-CSRFToken': csrftoken},
    body: JSON.stringify({
      'userid': userid
    })
  })
  .then( response => response.json())
  .then( list => {
    // console.log(list);
    display_list(list);
  })
  // .catch( error => {
  //   console.error('Error: ', error);
  // });
}

function display_list(list) {
  if (list.length > 0) {
    for (let i = 0; i < list.length; i++) {
      let itemDiv = document.createElement('div');
      itemDiv.className = "itemDiv";
      itemDiv.innerHTML =
      `<a class="postposter" href="/profile/${list[i].id}">${list[i].username}</a>`
      document.querySelector('#listview').appendChild(itemDiv)
    }
  }
  else {
      document.querySelector('#listview').innerHTML = "No users yet."
    }

  document.querySelector("#postview").style.display = 'none';
}

function display_posts() {
  document.querySelector("#listview").style.display = 'none';
  document.querySelector("#listview").innerHTML = "";
  document.querySelector("#postview").style.display = 'block';
}

function updatefollow() {
  // Get Button element and info it stores
  let button = document.querySelector("#followbutton");
  let currentState = button.dataset.follow;
  let profileUser = button.dataset.user;
  // Get Follower count info from profile page to update
  let profDiv = button.parentElement.parentElement;
  let followerCountText = profDiv.getElementsByClassName('listlink')[1].innerText;
  let followingCountText = profDiv.getElementsByClassName('listlink')[2].innerText;
  let cuts = [followerCountText.indexOf(" "), followingCountText.indexOf(" ")];
  let followerCount = followerCountText.slice(0, cuts[0]);
  let followingCount = followingCountText.slice(0, cuts[1]);
  // Send request to backend
  fetch("/follow", {
    method: "PUT",
    body: JSON.stringify({
      currentState: currentState,
      user: profileUser
    })
  })
  // Update Display of Page to reflect request
  if (currentState == "true") {
    // Unfollow
    button.dataset.follow = "false";
    button.className = "btn btn-outline-primary";
    button.innerText = "Follow";
    let followerCountUpdate = followerCount - 1;
    if (followerCountUpdate == 1) {
      profDiv.getElementsByClassName('listlink')[1].innerText = `${followerCountUpdate} Follower`
    }
    else{
      profDiv.getElementsByClassName('listlink')[1].innerText = `${followerCountUpdate} Followers`
    }
  }
  else if (currentState == "false") {
    // Follow
    button.dataset.follow = "true";
    button.className = "btn btn-outline-danger";
    button.innerText = "Unfollow";
    let followerCountUpdate = parseInt(followerCount) + 1;
    profDiv.getElementsByClassName('listlink')[1].innerText = `${followerCountUpdate} Followers`
  }
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
