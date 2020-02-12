/* BIG GALLERY AUTO SLIDE */
(function() { //something like document.ready
  let interval = setInterval( function(){ changeSlide(); }, 5000);
  window.addEventListener('load', resetLoader, false );

  let gallery = document.getElementById("main-gallery");
  let slides = document.getElementsByClassName("main-gallery-radio");
  let pause = document.getElementById("main-gallery-radio-pause");

  gallery.style.left = "0%";

  let i = 0;

  for (let i = slides.length; i < slides.length * 2; i++) {
    slides[i%slides.length].addEventListener('change', function(){
      gallery.style.left = "-" + (100 * (i%slides.length)).toString() + "%";
      clearInterval( interval );
      if ( pause.checked === false ){
        resetLoader();
      }
      interval = setInterval( function(){ changeSlide(); }, 5000);
    }, false);
  }

  function changeSlide() {
    if (pause.checked !== false) {
      return;
    }
    resetLoader();
    for (i = 0; i < slides.length; i++) {
      if (slides[i].checked === true) {
        slides[i].checked = false;
        slides[(i + 1) % slides.length].checked = true;
        gallery.style.left = "-" + (100 * ((i + 1) % slides.length)).toString() + "%";

        break;
      }
    }
  }

  pause.addEventListener('click', function(){
      if ( pause.checked ){
        clearInterval( interval );
        clearLoader();
      } else {
        clearInterval( interval );
        interval = setInterval( function(){ changeSlide(); }, 5000);
        resetLoader();
      }
    }
  );

  function resetLoader(){
    let loader = document.querySelector(".main-gallery-radio:checked ~ .gallery-loader");
    loader.style.animation = "";
    void loader.offsetWidth;
    loader.style.animation = "loading 5s linear backwards";
  }

  function clearLoader(){
    let loader = document.querySelector(".main-gallery-radio:checked ~ .gallery-loader");
    loader.style.animation = "";
    void loader.offsetWidth;
  }



  /* BIG GALLERY SWIPE */

  gallery.addEventListener('touchstart', handleTouchStart, false);
  gallery.addEventListener('touchmove', handleTouchMove, false);

  let xDown = null;

  function handleTouchStart(evt) {
    xDown = evt.touches[0].clientX;
  }

  function handleTouchMove(evt) {
    let slides = document.getElementsByClassName("main-gallery-radio");
    let i = 0;

    if ( ! xDown ) {
      return;
    }

    let xUp = evt.touches[0].clientX;

    let xDiff = xDown - xUp;

      if ( xDiff > slides.length + 1 ) { /* from right to left */
        for (i = 0; i < slides.length; i++){
          if ( slides[i].checked === true ) {
            slides[i].checked = false;
            slides[(i+1)%slides.length].checked = true;
            gallery.style.left = "-" + (100 * ((i+1)%slides.length)).toString() + "%";
            clearInterval( interval );
            resetLoader();
            interval = setInterval( function(){ changeSlide(); }, 5000);
            break;
          }
        }
      } else if ( xDiff < -(slides.length + 1) ) {
        for (i = 3; i < 6; i++){
          if ( slides[i%slides.length].checked === true ) {
            slides[i%slides.length].checked = false;
            slides[(i-1)%slides.length].checked = true;
            gallery.style.left = "-" + (100 * ((i-1)%slides.length)).toString() + "%";
            clearInterval( interval );
            resetLoader();
            interval = setInterval( function(){ changeSlide(); }, 5000);
            break;
          }
        }
      }

    /* reset values */
    xDown = null;
  }
})();



