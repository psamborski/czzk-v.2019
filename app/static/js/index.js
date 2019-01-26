/* BIG GALLERY AUTO SLIDE */
(function() { //something like document.ready
  let interval = setInterval( function(){ changeSlide(); }, 5000);
  window.addEventListener('load', resetLoader, false );

  let slides = document.getElementsByClassName("main-gallery-radio");
  let pause = document.getElementById("main-gallery-radio-pause");

  let i = 0;

  for (let i = 3; i < 6; i++) {
    slides[i%3].addEventListener('change', function(){
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
    for (i = 0; i < 3; i++) {
      if (slides[i].checked === true) {
        slides[i].checked = false;
        slides[(i + 1) % 3].checked = true;
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

  let gallery = document.getElementById("main-gallery");
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

      if ( xDiff > 4 ) { /* from right to left */
        for (i = 0; i < 3; i++){
          if ( slides[i].checked === true ) {
            slides[i].checked = false;
            slides[(i+1)%3].checked = true;
            clearInterval( interval );
            resetLoader();
            interval = setInterval( function(){ changeSlide(); }, 5000);
            break;
          }
        }
      } else if ( xDiff < -4 ) {
        for (i = 3; i < 6; i++){
          if ( slides[i%3].checked === true ) {
            slides[i%3].checked = false;
            slides[(i-1)%3].checked = true;
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



