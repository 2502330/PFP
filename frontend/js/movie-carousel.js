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

    console.log('Movie analysis structure:', movie.analysis); // Debug log

    const reviewsHtml = movie.reviews.slice(0, 100).map((review, index) => {
        // Try to get individual review score from analysis if available
        let reviewScore = 'N/A';
        let scoreClass = 'text-muted';
        
        // Check if there's an analysis array with individual scores for each review
        if (movie.analysis && movie.analysis[index] && movie.analysis[index].total_score !== undefined) {
            reviewScore = movie.analysis[index].total_score.toFixed(2);
            scoreClass = reviewScore >= 0 ? 'text-success' : 'text-danger';
            console.log(`Review ${index} has individual score: ${reviewScore}`); // Debug log
        } else if (movie.analysis && movie.analysis[0] && movie.analysis[0].review_scores && movie.analysis[0].review_scores[index] !== undefined) {
            reviewScore = movie.analysis[0].review_scores[index].toFixed(2);
            scoreClass = reviewScore >= 0 ? 'text-success' : 'text-danger';
        } else if (movie.analysis && movie.analysis[0] && movie.analysis[0].total_score !== undefined) {
            // Fallback: show overall score for each review
            reviewScore = movie.analysis[0].total_score.toFixed(2);
            scoreClass = reviewScore >= 0 ? 'text-success' : 'text-danger';
        }

        // Escape the movie name for onclick
        const escapedMovieName = movie.name.replace(/'/g, "\\'").replace(/"/g, '\\"');

        return `
            <div class="review-item mb-3 p-3 border rounded" style="cursor: pointer;" onclick="movieCarousel.updateAnalysisForReview('${escapedMovieName}', ${index});">
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <h6 class="text-info mb-0">Review ${index + 1} <small class="text-muted">(Click to view analysis)</small></h6>
                    <span class="badge bg-dark ${scoreClass}">
                        <i class="fas fa-chart-line me-1"></i>Score: ${reviewScore}
                    </span>
                </div>
                <p class="mb-0">${review.length > 10000 ? review.substring(0, 10000) + '...' : review}</p>
            </div>
        `;
    }).join('');

    const escapedMovieNameForButton = movie.name.replace(/'/g, "\\'").replace(/"/g, '\\"');

    return `
        <div class="reviews-section">
            <h5><i class="fas fa-comments me-2"></i>Reviews (Showing ${Math.min(100, movie.reviews.length)} of ${movie.reviews.length})</h5>
            <div class="btn-group mb-3" role="group">
                <button type="button" class="btn btn-outline-info btn-sm" onclick="movieCarousel.updateAnalysisForReview('${escapedMovieNameForButton}', -1);">
                    <i class="fas fa-chart-bar me-1"></i>Show Overall Analysis
                </button>
            </div>
            <div class="reviews-container" style="max-height: 400px; overflow-y: auto;">
                ${reviewsHtml}
            </div>
        </div>
    `;
}

updateAnalysisForReview(movieName, reviewIndex) {
    console.log('updateAnalysisForReview called with:', movieName, reviewIndex); // Debug log
    
    const movie = this.movies.find(m => m.name === movieName);
    if (!movie) {
        console.log('Movie not found:', movieName); // Debug log
        console.log('Available movies:', this.movies.map(m => m.name)); // Debug log
        return;
    }

    let analysisToShow;
    let titleSuffix = '';

    if (reviewIndex === -1) {
        // Show overall analysis
        analysisToShow = movie.analysis && movie.analysis[0] ? movie.analysis[0] : null;
        titleSuffix = ' - Overall Analysis';
        console.log('Showing overall analysis:', analysisToShow); // Debug log
    } else {
        // Show specific review analysis
        analysisToShow = movie.analysis && movie.analysis[reviewIndex] ? movie.analysis[reviewIndex] : null;
        titleSuffix = ` - Review ${reviewIndex + 1} Analysis`;
        console.log('Showing review analysis for index:', reviewIndex, analysisToShow); // Debug log
    }

    const analysisSection = document.querySelector('.analysis-section');
    console.log('Analysis section found:', !!analysisSection); // Debug log
    
    if (analysisSection && analysisToShow) {
        console.log('Updating analysis section with data:', analysisToShow); // Debug log
        // Update the analysis section with the selected review's data
        analysisSection.innerHTML = `
            <h5><i class="fas fa-chart-line me-2"></i>Sentiment Analysis${titleSuffix}</h5>
            
            <div class="row mb-4">
                <div class="col-12">
                    <div class="analysis-card p-3 border rounded text-center">
                        <h6 class="text-info">Sentiment Score</h6>
                        <h2 class="mb-0 ${analysisToShow.total_score >= 0 ? 'text-success' : 'text-danger'}">
                            ${analysisToShow.total_score.toFixed(2)}
                        </h2>
                        <small class="text-muted">
                            ${analysisToShow.total_score >= 0 ? 'Positive' : 'Negative'}
                        </small>
                    </div>
                </div>
            </div>

            <div class="row mb-4">
                <div class="col-md-6">
                    <div class="analysis-card p-3 border rounded h-100">
                        <h6 class="text-success"><i class="fas fa-smile me-2"></i>Most Positive Sentence</h6>
                        <p class="small mb-0 fst-italic">"${analysisToShow.most_pos_sentence || 'N/A'}"</p>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="analysis-card p-3 border rounded h-100">
                        <h6 class="text-danger"><i class="fas fa-frown me-2"></i>Most Negative Sentence</h6>
                        <p class="small mb-0 fst-italic">"${analysisToShow.most_neg_sentence || 'N/A'}"</p>
                    </div>
                </div>
            </div>

            <div class="row mb-4">
                <div class="col-md-6">
                    <div class="analysis-card p-3 border rounded h-100">
                        <h6 class="text-success"><i class="fas fa-paragraph me-2"></i>Most Positive Paragraph</h6>
                        <div class="small" style="max-height: 150px; overflow-y: auto;">
                            <p class="mb-0 fst-italic">"${analysisToShow.most_pos_paragraph ? (analysisToShow.most_pos_paragraph.length > 500 ? analysisToShow.most_pos_paragraph.substring(0, 500) + '...' : analysisToShow.most_pos_paragraph) : 'N/A'}"</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="analysis-card p-3 border rounded h-100">
                        <h6 class="text-danger"><i class="fas fa-paragraph me-2"></i>Most Negative Paragraph</h6>
                        <div class="small" style="max-height: 150px; overflow-y: auto;">
                            <p class="mb-0 fst-italic">"${analysisToShow.most_neg_paragraph ? (analysisToShow.most_neg_paragraph.length > 500 ? analysisToShow.most_neg_paragraph.substring(0, 500) + '...' : analysisToShow.most_neg_paragraph) : 'N/A'}"</p>
                        </div>
                    </div>
                </div>
            </div>

            <div class="row">
                <div class="col-md-6">
                    <div class="analysis-card p-3 border rounded h-100">
                        <h6 class="text-success"><i class="fas fa-align-left me-2"></i>Most Positive Segment</h6>
                        <div class="small" style="max-height: 200px; overflow-y: auto;">
                            <p class="mb-0 fst-italic">"${analysisToShow.most_pos_segment ? (analysisToShow.most_pos_segment.length > 800 ? analysisToShow.most_pos_segment.substring(0, 800) + '...' : analysisToShow.most_pos_segment) : 'N/A'}"</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="analysis-card p-3 border rounded h-100">
                        <h6 class="text-danger"><i class="fas fa-align-left me-2"></i>Most Negative Segment</h6>
                        <div class="small" style="max-height: 200px; overflow-y: auto;">
                            <p class="mb-0 fst-italic">"${analysisToShow.most_neg_segment ? (analysisToShow.most_neg_segment.length > 800 ? analysisToShow.most_neg_segment.substring(0, 800) + '...' : analysisToShow.most_neg_segment) : 'N/A'}"</p>
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Highlight the selected review
        document.querySelectorAll('.review-item').forEach((item, idx) => {
            if (idx === reviewIndex) {
                item.style.backgroundColor = 'rgba(13, 202, 240, 0.1)';
                item.style.borderColor = '#0dcaf0';
            } else {
                item.style.backgroundColor = 'rgba(255, 255, 255, 0.05)';
                item.style.borderColor = '#444';
            }
        });
    } else {
        console.log('Cannot update analysis - missing section or data:', {
            analysisSection: !!analysisSection,
            analysisToShow: !!analysisToShow
        });
    }
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