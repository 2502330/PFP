// Movie Carousel and Reviews functionality
class MovieCarousel {
    constructor() {
        this.movies = [];
        this.currentMovieIndex = 0;
        this.init();
    }

    async init() {
        await this.loadMovies();
        this.renderCarousel();
        this.setupEventListeners();
    }

    async loadMovies() {
        try {
            const response = await fetch('../results/results.json');
            const data = await response.json();
            
            // Convert object to array and take first 20 movies for performance
            this.movies = Object.entries(data)
                .slice(0, 20)
                .map(([id, movie]) => ({
                    id,
                    ...movie
                }));
            
            console.log(`Loaded ${this.movies.length} movies`);
        } catch (error) {
            console.error('Error loading movies:', error);
            // Fallback to empty array
            this.movies = [];
        }
    }

    renderCarousel() {
        const carouselInner = document.getElementById('carousel-inner');
        if (!carouselInner) return;

        carouselInner.innerHTML = '';

        if (this.movies.length === 0) {
            carouselInner.innerHTML = `
                <div class="carousel-item active">
                    <div class="row justify-content-center">
                        <div class="col-md-8 text-center text-white">
                            <h3>No movies available</h3>
                            <p>Unable to load movie data.</p>
                        </div>
                    </div>
                </div>
            `;
            return;
        }

        // Group movies in sets of 3 for each carousel slide
        const groupedMovies = this.groupMovies(this.movies, 3);

        groupedMovies.forEach((movieGroup, groupIndex) => {
            const isActive = groupIndex === 0 ? 'active' : '';
            const slide = document.createElement('div');
            slide.className = `carousel-item ${isActive}`;
            
            slide.innerHTML = `
                <div class="row justify-content-center px-4">
                    ${movieGroup.map(movie => this.createMovieCard(movie)).join('')}
                </div>
            `;
            
            carouselInner.appendChild(slide);
        });
    }

    groupMovies(movies, size) {
        const groups = [];
        for (let i = 0; i < movies.length; i += size) {
            groups.push(movies.slice(i, i + size));
        }
        return groups;
    }

    createMovieCard(movie) {
        const genres = movie.genres ? movie.genres.slice(0, 2).join(', ') : 'N/A';
        const rating = movie.rating || 'N/A';
        const poster = movie.poster || 'assets/img/placeholder-movie.jpg';
        const reviewCount = movie.reviews ? movie.reviews.length : 0;
        
        return `
            <div class="col-md-4 mb-4">
                <div class="card bg-dark text-white h-100">
                    <img src="${poster}" class="card-img-top" alt="${movie.name}" 
                         onerror="this.src='assets/img/placeholder-movie.jpg'">
                    <div class="card-body d-flex flex-column">
                        <h5 class="card-title">${movie.name || 'Unknown Title'}</h5>
                        <p class="card-text">
                            <strong>Rating:</strong> ${rating}/10<br>
                            <strong>Genres:</strong> ${genres}<br>
                            <strong>Reviews:</strong> ${reviewCount}
                        </p>
                        <button class="btn btn-primary mt-auto" 
                                onclick="movieCarousel.showReviews('${movie.id}')">
                            View Reviews & Analysis
                        </button>
                    </div>
                </div>
            </div>
        `;
    }

    showReviews(movieId) {
        const movie = this.movies.find(m => m.id === movieId);
        if (!movie) return;

        const modal = document.getElementById('reviewsModal');
        const modalTitle = document.getElementById('reviewsModalLabel');
        const modalBody = document.getElementById('reviewsModalBody');

        if (!modal || !modalTitle || !modalBody) return;

        modalTitle.textContent = `Reviews & Analysis - ${movie.name}`;
        
        // Create reviews and analysis content
        const analysisContent = this.createAnalysisContent(movie);
        const reviewsContent = this.createReviewsContent(movie);
        
        modalBody.innerHTML = `
            ${analysisContent}
            <hr class="my-4">
            ${reviewsContent}
        `;

        // Show the modal
        const bootstrapModal = new bootstrap.Modal(modal);
        bootstrapModal.show();
    }


createAnalysisContent(movie) {
    if (!movie.analysis || movie.analysis.length === 0) {
        return `
            <div class="analysis-section mb-4">
                <h5>Sentiment Analysis</h5>
                <p class="text-muted">No analysis available for this movie.</p>
            </div>
        `;
    }

    // Use the first analysis result
    const analysis = movie.analysis[0];
    
    return `
        <div class="analysis-section mb-4">
            <h5><i class="fas fa-chart-line me-2"></i>Sentiment Analysis</h5>
            
            <!-- Total Score -->
            <div class="row mb-4">
                <div class="col-12">
                    <div class="analysis-card p-3 border rounded text-center">
                        <h6 class="text-info">Overall Sentiment Score</h6>
                        <h2 class="mb-0 ${analysis.total_score >= 0 ? 'text-success' : 'text-danger'}">
                            ${analysis.total_score}
                        </h2>
                        <small class="text-muted">
                            ${analysis.total_score >= 0 ? 'Positive Overall' : 'Negative Overall'}
                        </small>
                    </div>
                </div>
            </div>

            <!-- Sentences Analysis -->
            <div class="row mb-4">
                <div class="col-md-6">
                    <div class="analysis-card p-3 border rounded h-100">
                        <h6 class="text-success"><i class="fas fa-smile me-2"></i>Most Positive Sentence</h6>
                        <p class="small mb-0 fst-italic">"${analysis.most_pos_sentence || 'N/A'}"</p>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="analysis-card p-3 border rounded h-100">
                        <h6 class="text-danger"><i class="fas fa-frown me-2"></i>Most Negative Sentence</h6>
                        <p class="small mb-0 fst-italic">"${analysis.most_neg_sentence || 'N/A'}"</p>
                    </div>
                </div>
            </div>

            <!-- Paragraphs Analysis -->
            <div class="row mb-4">
                <div class="col-md-6">
                    <div class="analysis-card p-3 border rounded h-100">
                        <h6 class="text-success"><i class="fas fa-paragraph me-2"></i>Most Positive Paragraph</h6>
                        <div class="small" style="max-height: 150px; overflow-y: auto;">
                            <p class="mb-0 fst-italic">"${analysis.most_pos_paragraph ? (analysis.most_pos_paragraph.length > 500 ? analysis.most_pos_paragraph.substring(0, 500) + '...' : analysis.most_pos_paragraph) : 'N/A'}"</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="analysis-card p-3 border rounded h-100">
                        <h6 class="text-danger"><i class="fas fa-paragraph me-2"></i>Most Negative Paragraph</h6>
                        <div class="small" style="max-height: 150px; overflow-y: auto;">
                            <p class="mb-0 fst-italic">"${analysis.most_neg_paragraph ? (analysis.most_neg_paragraph.length > 500 ? analysis.most_neg_paragraph.substring(0, 500) + '...' : analysis.most_neg_paragraph) : 'N/A'}"</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Segments Analysis -->
            <div class="row">
                <div class="col-md-6">
                    <div class="analysis-card p-3 border rounded h-100">
                        <h6 class="text-success"><i class="fas fa-align-left me-2"></i>Most Positive Segment</h6>
                        <div class="small" style="max-height: 200px; overflow-y: auto;">
                            <p class="mb-0 fst-italic">"${analysis.most_pos_segment ? (analysis.most_pos_segment.length > 800 ? analysis.most_pos_segment.substring(0, 800) + '...' : analysis.most_pos_segment) : 'N/A'}"</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="analysis-card p-3 border rounded h-100">
                        <h6 class="text-danger"><i class="fas fa-align-left me-2"></i>Most Negative Segment</h6>
                        <div class="small" style="max-height: 200px; overflow-y: auto;">
                            <p class="mb-0 fst-italic">"${analysis.most_neg_segment ? (analysis.most_neg_segment.length > 800 ? analysis.most_neg_segment.substring(0, 800) + '...' : analysis.most_neg_segment) : 'N/A'}"</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

    createReviewsContent(movie) {
        if (!movie.reviews || movie.reviews.length === 0) {
            return `
                <div class="reviews-section">
                    <h5><i class="fas fa-comments me-2"></i>Reviews</h5>
                    <p class="text-muted">No reviews available for this movie.</p>
                </div>
            `;
        }

        const reviewsHtml = movie.reviews.slice(0, 100).map((review, index) => `
            <div class="review-item mb-3 p-3 border rounded">
                <h6 class="text-info">Review ${index + 1}</h6>
                <p class="mb-0">${review.length > 10000 ? review.substring(0, 10000) + '...' : review}</p>
            </div>
        `).join('');

        return `
            <div class="reviews-section">
                <h5><i class="fas fa-comments me-2"></i>Reviews (Showing all reviews of ${movie.reviews.length})</h5>
                <div class="reviews-container" style="max-height: 400px; overflow-y: auto;">
                    ${reviewsHtml}
                </div>
            </div>
        `;
    }

    setupEventListeners() {
        // Add any additional event listeners if needed
        console.log('Event listeners set up');
    }
}

// Initialize the carousel when the page loads
let movieCarousel;
document.addEventListener('DOMContentLoaded', () => {
    movieCarousel = new MovieCarousel();
});