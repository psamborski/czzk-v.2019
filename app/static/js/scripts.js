/* MENU SHRINK */

let logo_container = document.getElementById("logo-container");
let page_title = document.getElementById("page-title");

window.addEventListener('scroll', function(){
  if(15 < window.pageYOffset) {
    logo_container.classList = 'logo-container-smaller';
    page_title.style.margin = '-200px 0 0 0';
    page_title.style.opacity = '0';
  } else {
    logo_container.classList = 'logo-container-normal';
    page_title.style.margin = '-5px 0 0 0';
    page_title.style.opacity = '1';
  }
});

/* MOBILE MENU TOGGLE */
let menu_about = document.getElementById("menu-list-about");
let menu_multimedia = document.getElementById("menu-list-media");
let arrows = document.getElementsByClassName("fa-angle-down");

menu_about.addEventListener('click', function(){
  if(screen.width < 1000 || window.innerWidth < 1000){
    menu_about.style.height = menu_about.style.height === '200px' ? '50px' : '200px';
    arrows[0].classList.toggle("rotate-arrow");
  }

});

menu_multimedia.addEventListener('click', function(){
  if(screen.width < 1000 || window.innerWidth < 1000) {
    menu_multimedia.style.height = menu_multimedia.style.height === '250px' ? '50px' : '250px';
    arrows[1].classList.toggle("rotate-arrow");
  }
});

/* POP UP = MODAL or FLASH MESSAGE */

let toggle_pop_up = function (pop_up_id, do_i_wanna_open) {
  let pop_up = document.getElementById(pop_up_id);
  if(do_i_wanna_open){
    pop_up.style.display = "block";
  } else {
    pop_up.style.display = "none";
  }
};

let pop_ups = document.getElementsByClassName("pop-up");
let modal_triggers = document.getElementsByClassName("modal-trigger"); // triggers are just for modals
let pop_up_close_buttons = document.getElementsByClassName("pop-up-close");

//open pop_up
for (let i = 0; i < modal_triggers.length; i++) {
  modal_triggers[i].addEventListener('click', function(){toggle_pop_up(this.hash.substr(1), true)}, false);
}

// close pop_up
for (let i = 0; i < pop_up_close_buttons.length; i++) {
  pop_up_close_buttons[i].addEventListener('click', function(){toggle_pop_up(this.parentElement.parentElement.id, false)}, false);
}

// when the user clicks anywhere outside of the pop_up, close it
for (let i = 0; i < pop_ups.length; i++) {
  pop_ups[i].addEventListener(
      'click',
      function(event){
          if (this !== event.target) return;
          toggle_pop_up(this.id, false)
      },
      false);
}