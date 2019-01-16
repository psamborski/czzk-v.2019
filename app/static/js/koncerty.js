/* OLDER/NEWER */

let new_older = document.getElementById("new-older");
let new_newer = document.getElementById("new-newer");
let old_older = document.getElementById("old-older");
let old_newer = document.getElementById("old-newer");

let old_concerts = document.getElementById("old-concerts");
let new_concerts = document.getElementById("new-concerts");


old_older.addEventListener('click', function () {
    if (old_concerts.offsetWidth > 800) {
        let position = parseInt(window.getComputedStyle(old_concerts, null).getPropertyValue("top"));
        let height = old_concerts.offsetHeight;
        if (position + height > 600) {
            new_position = position - 600;
            old_concerts.style.top = new_position + "px";
        }
    }

}, false);

old_newer.addEventListener('click', function () {
    if (old_concerts.offsetWidth > 800) {
        let position = parseInt(window.getComputedStyle(old_concerts, null).getPropertyValue("top"));
        let height = old_concerts.offsetHeight;
        if (position < 0) {
            new_position = position + 600;
            old_concerts.style.top = new_position + "px";
        }
    }
}, false);

new_older.addEventListener('click', function () {
    if (old_concerts.offsetWidth > 800) {
        let position = parseInt(window.getComputedStyle(new_concerts, null).getPropertyValue("top"));
        let height = new_concerts.offsetHeight;
        if (position + height > 600) {
            new_position = position - 600;
            old_concerts.style.top = new_position + "px";
        }
    }
}, false);

new_newer.addEventListener('click', function () {
    if (old_concerts.offsetWidth > 800) {
        let position = parseInt(window.getComputedStyle(new_concerts, null).getPropertyValue("top"));
        let height = new_concerts.offsetHeight;
        if (position < 0) {
            new_position = position + 600;
            old_concerts.style.top = new_position + "px";
        }
    }
}, false);