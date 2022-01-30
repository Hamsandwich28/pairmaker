let movieSelected = 0, litSelected = 0, hobbySelected = 0;
function selectMovieHandle(cb) {
    if (cb.checked) {
        if (movieSelected < 2) {
            movieSelected += 1;
        } else {
            cb.checked = false;
        }
    } else {
        movieSelected -= 1;
    }
}
function selectLitHandle(cb) {
    if (cb.checked) {
        if (litSelected < 2) {
            litSelected += 1;
        } else {
            cb.checked = false;
        }
    } else {
        litSelected -= 1;
    }
}
function selectHobbyHandle(cb) {
    if (cb.checked) {
        if (hobbySelected < 2) {
            hobbySelected += 1;
        } else {
            cb.checked = false;
        }
    } else {
        hobbySelected -= 1;
    }
}