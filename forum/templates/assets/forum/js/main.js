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
  input = input.toLowerCase();

  let x = document.getElementsByClassName(class_name);
  for (i = 0; i < x.length; i++) {
    if (!x[i].innerHTML.toLowerCase().includes(input)) {
      x[i].style.display = "none";
    }
    else if (class_name === 'forumItem') {
      x[i].style.display = "flex";
    }
    else {
      x[i].style.display = "block";
    }
  }
}

function change_price() {
  radio_android = document.getElementById('btnradio1');
  prices = document.getElementsByClassName("asoZakaz__item__price");

  ios_prices = ['120 $', '540 $', 'от 620 $'];
  android_prices = ['80 $', '460 $', 'от 520 $'];

  for (let i = 0; i < prices.length; i++) {
    if (radio_android.checked) {
      prices[i].innerHTML = android_prices[i];
    } else {
      prices[i].innerHTML = ios_prices[i];
    }
  }
}

function resizeImage(img) {
  var MAX_WIDTH = 300;
  var MAX_HEIGHT = 300;

  var width = img.width;
  var height = img.height;

  // Change the resizing logic
  if (width > height) {
    if (width > MAX_WIDTH) {
      height = height * (MAX_WIDTH / width);
      width = MAX_WIDTH;
    }
  } else {
    if (height > MAX_HEIGHT) {
      width = width * (MAX_HEIGHT / height);
      height = MAX_HEIGHT;
    }
  }

  var canvas = document.createElement("canvas");
  canvas.width = width;
  canvas.height = height;
  var ctx = canvas.getContext("2d");
  ctx.drawImage(img, 0, 0, width, height);
}