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
  content_ul = document.getElementsByClassName("asoZakaz__item__list");
  descs = document.getElementsByClassName("asoZakaz__item__desc");

  content_android = [
    [
      'Анализ ниши для определения необходимости ASO', 
      "Сбор семантического ядра", 
      "Название", 
      'Краткое описание', 
      'Описание'
    ],
    [
      'Анализ ниши для определения необходимости ASO', 
      "Сбор семантического ядра", 
      "Название", 
      'Краткое описание', 
      "Описание", 
      "Анализ графики", 
      'помощь с А/В-тестами'
    ],
    [
      "Сопровождение проекта",
      'Расширение списка локализаций',
      "Повторные итерации текстового ASO",
      'Непрерывное отслеживание позиций',
      'Продвижение по позициям',
      "Работа с рейтингом и отзывами",
      "Проведение сплит-тестов графики",
      "Отчёт о выполненной работе"
    ]
  ]

  content_ios = [
    [
      'Анализ ниши для определения необходимости ASO', 
      "Сбор семантического ядра", 
      "Название", 
      'Подзаголовок', 
      'Поле для ключевых слов'
    ],
    [
      'Анализ ниши для определения необходимости ASO', 
      "Сбор семантического ядра", 
      "Составление названия, подзаголовка", 
      'Заполнение поля для ключевых слов',
      "Анализ графики, помощь с А/В-тестами"
    ],
    [
      "Сопровождение проекта",
      'Расширение списка локализаций',
      "Повторные итерации текстового ASO",
      'Непрерывное отслеживание позиций',
      'Работа с мотивированным трафиком',
      "Работа с рейтингом и отзывами",
      "Проведение сплит-тестов графики",
      "Отчёт о выполненной работе"
    ]
  ]

  android_descs = [
    'Локаль “под ключ”', 
    '7 локалей “под ключ”', 
    'Всё то же, что и в ASO-Оптимизация PLUS , а так же:'
  ];

  ios_descs = [
    '1 локаль “под ключ”', 
    '3 страны с основной локалью + дополнительные', 
    'Всё то же, что и в ASO-Оптимизация PLUS , а так же:'
  ];

  android_prices = ['80 $', '460 $', 'от 520 $'];
  ios_prices = ['120 $', '540 $', 'от 620 $'];

  for (let i = 0; i < prices.length; i++) {
    if (radio_android.checked) {
      prices[i].innerHTML = android_prices[i];
      descs[i].innerHTML = android_descs[i];
      for (let j = 0; j < content_android[i].length; j++) {
        var li = document.createElement("li");
        li.appendChild(document.createTextNode(content_android[i][j]));
        content_ul[i].appendChild(li);
      }
    } else {
      prices[i].innerHTML = ios_prices[i];
      descs[i].innerHTML = ios_descs[i];
      for (let j = 0; j < content_ios[i].length; j++) {
        var li = document.createElement("li");
        li.appendChild(document.createTextNode(content_ios[i][j]));
        content_ul[i].appendChild(li);
      }
    }
  }
}

$(function(){
  $('.minimized').click(function(event) {
    var i_path = $(this).attr('src');
    $('body').append('<div style="display: flex;" id="overlay"><div style="display: flex;" id="magnify"><img src="'+i_path+'"><div id="close-popup"><i></i></div></div></div>');
    $('#overlay, #magnify').fadeIn('fast');
  });
  
  $('body').on('click', '#close-popup, #overlay', function(event) {
    event.preventDefault();
    $('#overlay, #magnify').fadeOut('fast', function() {
      $('#close-popup, #magnify, #overlay').remove();
    });
  });
});