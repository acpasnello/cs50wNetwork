document.addEventListener('DOMContentLoaded', function() {
  document.querySelector("#profileview").style.display = 'block';
  document.querySelector("#listview").style.display = 'none';

  // document.querySelector(".listlink").addEventListener('click', get_list(this))
});

function get_list(submittedlist) {
  // Trim number from front of string
  submittedlist = submittedlist.innerText
  console.log(submittedlist);
  let cut = submittedlist.lastIndexOf(" ");
  console.log(cut, typeof(cut))
  desiredlist = submittedlist.slice(parseInt(cut));
  console.log(desiredlist)
  fetch(`/userlist/${desiredlist}`)
}
