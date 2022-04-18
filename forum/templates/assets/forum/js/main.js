// nav
$('.navToggle').click(function () {
  $('body').toggleClass('navActive');
});

// ding
var ding = document.getElementById('ding');
var body = document.getElementById("body");
ding.addEventListener('show.bs.dropdown', function () {
  body.classList.add('dingActive');
});
ding.addEventListener('hidden.bs.dropdown', function () {
  body.classList.remove('dingActive');
});

// modalZakaz
var exampleModal = document.getElementById('modalZakaz')
exampleModal.addEventListener('show.bs.modal', function (event) {
  var button = event.relatedTarget
  var recipient = button.getAttribute('data-bs-whatever')
  var modalTitle = exampleModal.querySelector('.modal-title')
  modalTitle.textContent = 'Оформить ' + '"' + recipient + '"'
})

function showArea(block_id) {
  let textareas = document.getElementsByClassName('comments_textareas');
  for (var i = 0; i < textareas.length; i++) {
      var current_text = textareas[i];
      current_text.style.display = 'none';
  }
  let text = document.getElementById('block_' + block_id);
  text.style.display = 'block';
};