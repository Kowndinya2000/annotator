/*
#---------------------------------------------------
# @author: DANDE TEJA         <cs17b010@iittp.ac.in>
# @date: 21/05/2021
#---------------------------------------------------
*/


document.querySelector('.button').addEventListener('click',function() {
  var child = document.getElementById('clonemother');
  var clone = child.cloneNode(true);
  var node = document.getElementById("toasts").appendChild(clone);
  console.log(node.childNodes);
  setTimeout(function() {
    if(node) {
      document.getElementById('msg').innerHTML = "You just clicked the toast button, this toast will be closed in 1s.."
    }
  },1000);
})
function show_notification_red() {
  var child = document.getElementById('clone_red');
  var clone = child.cloneNode(true);
  var node = document.getElementById("toasts_red").appendChild(clone);
  console.log(node.childNodes);
}
function show_notification_green() {
  var child = document.getElementById('clone_success');
  var clone = child.cloneNode(true);
  var node = document.getElementById("toasts_success").appendChild(clone);
  console.log(node.childNodes);
}

function deletethis() {
  var e = window.event;
  var grand = e.target.parentNode.parentNode;
  grand.style.animation = "toast .5s ease-out forwards";
  setTimeout(() => {grand.remove();} ,500);
}