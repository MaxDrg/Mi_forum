// nav
$('.navToggle').click(function () {
  $('body').toggleClass('navActive');
});

function showArea(block_id) {
  let textareas = document.getElementsByClassName('textareas');
  for (var i = 0; i < textareas.length; i++) {
      var current_text = textareas[i];
      current_text.style.display = 'none';
  }
  let text = document.getElementById('block_' + block_id);
  text.style.display = 'block';
};

function search_info(class_name) {
  let input = document.getElementById('searchbar').value
  input=input.toLowerCase(); 

  let x = document.getElementsByClassName(class_name);
  for (i = 0; i < x.length; i++) {
      if (!x[i].innerHTML.toLowerCase().includes(input)) { 
          x[i].style.display="none";
      }
      else if (class_name === 'forumItem'){
          x[i].style.display="flex";
      }
      else {
          x[i].style.display="block";
      } 
  } 
} 