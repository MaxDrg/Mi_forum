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

$(function(){
  $('.minimized').click(function(event) {
    var i_path = $(this).attr('src');
    $('body').append('<div id="overlay"><div id="magnify"><img src="'+i_path+'"><div id="close-popup"><i></i></div></div></div>');
    $('#magnify').css({
     left: ($(document).width() - $('#magnify').outerWidth())/2,
     // top: ($(document).height() - $('#magnify').outerHeight())/2 upd: 24.10.2016
            top: ($(window).height() - $('#magnify').outerHeight())/2
   });
    $('#overlay, #magnify').fadeIn('fast');
  });
  
  $('body').on('click', '#close-popup, #overlay', function(event) {
    event.preventDefault();
    $('#overlay, #magnify').fadeOut('fast', function() {
      $('#close-popup, #magnify, #overlay').remove();
    });
  });
});