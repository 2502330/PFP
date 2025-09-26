/*!
* Start Bootstrap - Clean Blog v6.0.9 (https://startbootstrap.com/theme/clean-blog)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-clean-blog/blob/master/LICENSE)
*/
window.addEventListener('DOMContentLoaded', () => {
    let scrollPos = 0;
    const mainNav = document.getElementById('mainNav');
    const headerHeight = mainNav.clientHeight;
    window.addEventListener('scroll', function() {
        const currentTop = document.body.getBoundingClientRect().top * -1;
        if ( currentTop < scrollPos) {
            // Scrolling Up
            if (currentTop > 0 && mainNav.classList.contains('is-fixed')) {
                mainNav.classList.add('is-visible');
            } else {
                console.log(123);
                mainNav.classList.remove('is-visible', 'is-fixed');
            }
        } else {
            // Scrolling Down
            mainNav.classList.remove(['is-visible']);
            if (currentTop > headerHeight && !mainNav.classList.contains('is-fixed')) {
                mainNav.classList.add('is-fixed');
            }
        }
        scrollPos = currentTop;
    });
})

let moviesGlobal = [];
// Populate year dropdowns
function populateYearDropdowns() {
    const currentYear = new Date().getFullYear();
    const minYearDropdown = document.getElementById('minYear');
    const maxYearDropdown = document.getElementById('maxYear');

    // Populate years from 1900 to the current year
    for (let year = currentYear; year >= 1900; year--) {
        const minOption = document.createElement('option');
        minOption.value = year;
        minOption.textContent = year;
        minYearDropdown.appendChild(minOption);

        const maxOption = document.createElement('option');
        maxOption.value = year;
        maxOption.textContent = year;
        maxYearDropdown.appendChild(maxOption);
    }
}

// Call the function to populate the dropdowns
populateYearDropdowns();

