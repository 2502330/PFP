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

// Fetch and display movies from imdb.json
function renderMovieCard(movie, idx) {
  return `
    <div class="col-md-4 mb-3">
      <div class="card h-100">
        <img src="${movie.poster || ''}" class="card-img-top" alt="${movie.name || 'No Title'}">
        <div class="card-body">
          <h5 class="card-title">${movie.name || 'No Title'}</h5>
          <p class="card-text"><strong>Genres:</strong> ${(movie.genres || []).join(', ')}</p>
          <p class="card-text"><strong>Release Date:</strong> ${movie.date_published || ''}</p>
          <p class="card-text"><strong>Rating:</strong> ${movie.rating || ''}</p>
          <button class="btn btn-primary mt-2" onclick="showReviewsByIndex(${idx})">Read Reviews</button>
        </div>
      </div>
    </div>
  `;
}

function renderCarouselSlides(movies, perSlide = 3) {
  const slides = [];
  for (let i = 0; i < movies.length; i += perSlide) {
    const group = movies.slice(i, i + perSlide);
    slides.push(`
      <div class="carousel-item${i === 0 ? ' active' : ''}">
        <div class="row">
          ${group.map((movie, idx) => renderMovieCard(movie, i + idx)).join('')}
        </div>
      </div>
    `);
  }
  return slides.join('');
}

let moviesGlobal = [];

fetch('assets/imdb.json')
  .then(res => res.json())
  .then(data => {
    moviesGlobal = Object.values(data).filter(m => m && m.name);
    const carouselInner = document.getElementById('carousel-inner');
    if (!carouselInner || moviesGlobal.length === 0) {
      carouselInner.innerHTML = '<div class="carousel-item active"><div class="post-preview text-center">No movies found.</div></div>';
      return;
    }
    carouselInner.innerHTML = renderCarouselSlides(moviesGlobal, 3);
  })
  .catch(() => {
    const carouselInner = document.getElementById('carousel-inner');
    if (carouselInner) {
      carouselInner.innerHTML = '<div class="carousel-item active"><div class="post-preview text-center">Failed to load movies.</div></div>';
    }
  });

  
function showReviews(reviews, movieName) {
    const modalLabel = document.getElementById('reviewsModalLabel');
    const modalBody = document.getElementById('reviewsModalBody');
    modalLabel.textContent = `Reviews for ${movieName}`;
    if (reviews && reviews.length > 0) {
        modalBody.innerHTML = `<ul>${reviews.map(r => `<li class="mb-3">${r}</li>`).join('')}</ul>`;
    } else {
        modalBody.innerHTML = '<p>No reviews available.</p>';
    }
    // Show the modal
    const modal = new bootstrap.Modal(document.getElementById('reviewsModal'));
    modal.show();
}

function showReviewsByIndex(idx) {
    const movie = moviesGlobal[idx];
    showReviews(movie.reviews || [], movie.name || 'No Title');
}

