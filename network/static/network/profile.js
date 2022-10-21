document.addEventListener('DOMContentLoaded', function() {
  document.querySelector("#profileview").style.display = 'block';
  document.querySelector("#listview").style.display = 'none';
  document.querySelector("#postsdisplay").addEventListener('click', display_posts)
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
    display_list(list);
    console.log(list);
  })
  // .catch( error => {
  //   console.error('Error: ', error);
  // });
}

function display_list(list) {
  for (let i = 0; i < list.length; i++) {
    let itemDiv = document.createElement('div');
    itemDiv.className = "itemDiv";
    itemDiv.innerHTML =
    `<a class="postposter" href="/profile/${list[i].id}">${list[i].username}</a>`
    document.querySelector('#listview').appendChild(itemDiv)
  }
  document.querySelector("#postview").style.display = 'none';
}

function display_posts() {
  document.querySelector("#listview").style.display = 'none';
  document.querySelector("#listview").innerHTML = "";
  document.querySelector("#postview").style.display = 'block';
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
