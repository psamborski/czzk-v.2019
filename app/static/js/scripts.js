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