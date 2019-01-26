/* OLDER/NEWER */

let planned_older = document.getElementById("planned-older");
let planned_newer = document.getElementById("planned-newer");
let past_older = document.getElementById("past-older");
let past_newer = document.getElementById("past-newer");

let past_concerts = document.getElementById("past-concerts");
let planned_concerts = document.getElementById("planned-concerts");
let past_flag = true;
let planned_flag = true;


past_older.addEventListener('click', function () {
  if (past_concerts.offsetWidth > 800 && past_flag) {
    let position = parseInt(window.getComputedStyle(past_concerts, null).getPropertyValue("top"));
    let height = past_concerts.offsetHeight;
    if (position + height > 600) {
      let new_position = position - 600;
      past_concerts.style.top = new_position + "px";
    }
    past_flag = false;
    setTimeout(function(){past_flag = true;}, 200);
  }

}, false);

past_newer.addEventListener('click', function () {
  if (past_concerts.offsetWidth > 800 && past_flag) {
    let position = parseInt(window.getComputedStyle(past_concerts, null).getPropertyValue("top"));
    // let height = past_concerts.offsetHeight;
    if (position < 0) {
      let new_position = position + 600;
      past_concerts.style.top = new_position + "px";
    }
    past_flag = false;
    setTimeout(function(){past_flag = true;}, 200);
  }
}, false);

planned_older.addEventListener('click', function () {
  if (past_concerts.offsetWidth > 800 && planned_flag) {
    let position = parseInt(window.getComputedStyle(planned_concerts, null).getPropertyValue("top"));
    let height = planned_concerts.offsetHeight;
    if (position + height > 600) {
      let new_position = position - 600;
      past_concerts.style.top = new_position + "px";
    }
    planned_flag = false;
    setTimeout(function(){planned_flag = true;}, 200);
  }
}, false);

planned_newer.addEventListener('click', function () {
  if (past_concerts.offsetWidth > 800 && planned_flag) {
    let position = parseInt(window.getComputedStyle(planned_concerts, null).getPropertyValue("top"));
    // let height = new_concerts.offsetHeight;
    if (position < 0) {
      let new_position = position + 600;
      past_concerts.style.top = new_position + "px";
    }
    planned_flag = false;
    setTimeout(function(){planned_flag = true;}, 200);
  }
}, false);