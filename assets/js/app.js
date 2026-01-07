/**
 * if(塾) Instagram風ブログ - メインアプリケーション
 * 依存ライブラリなし（Vanilla JS）
 */

(function() {
  'use strict';

  // ========================================
  // State
  // ========================================
  const state = {
    config: null,
    posts: [],
    stories: [],
    highlights: [],
    currentPost: null,
    currentSlide: 0,
    currentStory: 0,
    storyTimer: null,
    storyProgress: 0,
    filteredStories: []
  };

  // ========================================
  // DOM Elements
  // ========================================
  const elements = {
    storiesContainer: null,
    highlightsContainer: null,
    postsGrid: null,
    modal: null,
    storyViewer: null
  };

  // ========================================
  // Data Loading
  // ========================================
  async function loadData() {
    try {
      const [configRes, postsRes, storiesRes, highlightsRes] = await Promise.all([
        fetch('data/config.json'),
        fetch('data/posts.json'),
        fetch('data/stories.json'),
        fetch('data/highlights.json')
      ]);

      state.config = await configRes.json();
      const postsData = await postsRes.json();
      const storiesData = await storiesRes.json();
      const highlightsData = await highlightsRes.json();

      state.posts = postsData.posts || [];
      state.stories = storiesData.stories || [];
      state.highlights = highlightsData.highlights || [];

      return true;
    } catch (error) {
      console.error('Failed to load data:', error);
      return false;
    }
  }

  // ========================================
  // Rendering
  // ========================================
  function renderStories() {
    const container = elements.storiesContainer;
    if (!container || state.stories.length === 0) return;

    const html = state.stories.map((story, index) => `
      <button class="story-item" data-index="${index}" aria-label="${story.alt}">
        <div class="story-item__ring">
          <img
            src="${story.src}"
            alt="${story.alt}"
            class="story-item__avatar"
            onerror="this.src='data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><rect fill=%22%23f5f5f5%22 width=%22100%22 height=%22100%22/><text x=%2250%22 y=%2255%22 text-anchor=%22middle%22 fill=%22%23999%22 font-size=%2212%22>Story</text></svg>'"
          >
        </div>
        <span class="story-item__name">${story.highlight || 'Story'}</span>
      </button>
    `).join('');

    container.innerHTML = html;

    // Add click handlers
    container.querySelectorAll('.story-item').forEach(item => {
      item.addEventListener('click', () => {
        const index = parseInt(item.dataset.index, 10);
        state.filteredStories = state.stories;
        openStoryViewer(index);
      });
    });
  }

  function renderHighlights() {
    const container = elements.highlightsContainer;
    if (!container || state.highlights.length === 0) return;

    const html = state.highlights.map(highlight => `
      <button class="highlight-item" data-category="${highlight.name}" aria-label="${highlight.description}">
        <div class="highlight-item__ring">
          <img
            src="${highlight.icon}"
            alt="${highlight.name}"
            class="highlight-item__icon"
            onerror="this.src='data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><rect fill=%22%23f5f5f5%22 width=%22100%22 height=%22100%22/><text x=%2250%22 y=%2255%22 text-anchor=%22middle%22 fill=%22%23999%22 font-size=%2210%22>${encodeURIComponent(highlight.name)}</text></svg>'"
          >
        </div>
        <span class="highlight-item__name">${highlight.name}</span>
      </button>
    `).join('');

    container.innerHTML = html;

    // Add click handlers
    container.querySelectorAll('.highlight-item').forEach(item => {
      item.addEventListener('click', () => {
        const category = item.dataset.category;
        const filtered = state.stories.filter(s => s.highlight === category);
        if (filtered.length > 0) {
          state.filteredStories = filtered;
          openStoryViewer(0);
        }
      });
    });
  }

  function renderPosts() {
    const container = elements.postsGrid;
    if (!container || state.posts.length === 0) {
      if (container) {
        container.innerHTML = `
          <div class="empty" style="grid-column: 1 / -1;">
            <div class="empty__icon">📷</div>
            <p>投稿がありません</p>
          </div>
        `;
      }
      return;
    }

    const html = state.posts.map((post, index) => {
      const firstMedia = post.media && post.media[0];
      const imageSrc = firstMedia ? firstMedia.src : '';
      const imageAlt = firstMedia ? firstMedia.alt : post.title;
      const typeIcon = post.type === 'carousel' ? '◫' : (post.type === 'reel' ? '▶' : '');

      return `
        <article class="post-card" data-index="${index}" tabindex="0" role="button" aria-label="${post.title}">
          <img
            src="${imageSrc}"
            alt="${imageAlt}"
            class="post-card__image"
            loading="lazy"
            onerror="this.src='data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><rect fill=%22%23f5f5f5%22 width=%22100%22 height=%22100%22/><text x=%2250%22 y=%2250%22 text-anchor=%22middle%22 fill=%22%23999%22 font-size=%228%22>${encodeURIComponent(post.title.substring(0, 10))}</text></svg>'"
          >
          <div class="post-card__overlay">
            <span class="sr-only">詳細を見る</span>
          </div>
          ${typeIcon ? `<span class="post-card__type-badge" aria-hidden="true">${typeIcon}</span>` : ''}
        </article>
      `;
    }).join('');

    container.innerHTML = html;

    // Add click handlers
    container.querySelectorAll('.post-card').forEach(card => {
      card.addEventListener('click', () => {
        const index = parseInt(card.dataset.index, 10);
        openPostModal(index);
      });
      card.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          const index = parseInt(card.dataset.index, 10);
          openPostModal(index);
        }
      });
    });
  }

  // ========================================
  // Post Modal
  // ========================================
  function openPostModal(index) {
    const post = state.posts[index];
    if (!post) return;

    state.currentPost = post;
    state.currentSlide = 0;

    const modal = elements.modal;
    updateModalContent(post);
    modal.classList.add('is-open');
    document.body.style.overflow = 'hidden';

    // Focus management
    modal.querySelector('.modal__close').focus();
  }

  function closePostModal() {
    const modal = elements.modal;
    modal.classList.remove('is-open');
    document.body.style.overflow = '';
    state.currentPost = null;
  }

  function updateModalContent(post) {
    const modal = elements.modal;

    // Carousel
    const carouselTrack = modal.querySelector('.carousel__track');
    const carouselDots = modal.querySelector('.carousel__dots');

    const slidesHtml = post.media.map((media, i) => `
      <div class="carousel__slide">
        <img
          src="${media.src}"
          alt="${media.alt}"
          class="carousel__image"
          onerror="this.src='data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 400 400%22><rect fill=%22%23f5f5f5%22 width=%22400%22 height=%22400%22/><text x=%22200%22 y=%22200%22 text-anchor=%22middle%22 fill=%22%23999%22 font-size=%2216%22>画像 ${i + 1}</text></svg>'"
        >
      </div>
    `).join('');

    const dotsHtml = post.media.map((_, i) => `
      <span class="carousel__dot ${i === 0 ? 'is-active' : ''}" data-index="${i}"></span>
    `).join('');

    carouselTrack.innerHTML = slidesHtml;
    carouselDots.innerHTML = dotsHtml;

    // Post details
    modal.querySelector('.post-details__username').textContent = 'if_juku';
    modal.querySelector('.post-details__caption').textContent = post.caption.replace(/\n\n.*#/s, '\n\n');
    modal.querySelector('.post-details__hashtags').textContent = post.hashtags.join(' ');

    const datetime = new Date(post.datetime);
    modal.querySelector('.post-details__datetime').textContent = datetime.toLocaleDateString('ja-JP', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });

    modal.querySelector('.post-details__cta-button').href = post.cta_url;

    // Update carousel navigation state
    updateCarouselNav();
  }

  function updateCarouselNav() {
    const modal = elements.modal;
    const prevBtn = modal.querySelector('.carousel__nav--prev');
    const nextBtn = modal.querySelector('.carousel__nav--next');
    const dots = modal.querySelectorAll('.carousel__dot');
    const track = modal.querySelector('.carousel__track');

    const totalSlides = state.currentPost.media.length;

    prevBtn.disabled = state.currentSlide === 0;
    nextBtn.disabled = state.currentSlide === totalSlides - 1;

    track.style.transform = `translateX(-${state.currentSlide * 100}%)`;

    dots.forEach((dot, i) => {
      dot.classList.toggle('is-active', i === state.currentSlide);
    });
  }

  function navigateCarousel(direction) {
    const totalSlides = state.currentPost.media.length;
    const newSlide = state.currentSlide + direction;

    if (newSlide >= 0 && newSlide < totalSlides) {
      state.currentSlide = newSlide;
      updateCarouselNav();
    }
  }

  // ========================================
  // Story Viewer
  // ========================================
  function openStoryViewer(index) {
    const stories = state.filteredStories;
    if (!stories || stories.length === 0) return;

    state.currentStory = index;
    const viewer = elements.storyViewer;

    updateStoryContent();
    viewer.classList.add('is-open');
    document.body.style.overflow = 'hidden';

    startStoryTimer();
  }

  function closeStoryViewer() {
    const viewer = elements.storyViewer;
    viewer.classList.remove('is-open');
    document.body.style.overflow = '';
    stopStoryTimer();
  }

  function updateStoryContent() {
    const stories = state.filteredStories;
    const story = stories[state.currentStory];
    if (!story) return;

    const viewer = elements.storyViewer;

    // Progress bars
    const progressHtml = stories.map((_, i) => `
      <div class="story-viewer__progress-bar">
        <div class="story-viewer__progress-fill" data-index="${i}" style="width: ${i < state.currentStory ? '100%' : '0%'}"></div>
      </div>
    `).join('');
    viewer.querySelector('.story-viewer__progress').innerHTML = progressHtml;

    // Content
    viewer.querySelector('.story-viewer__image').src = story.src;
    viewer.querySelector('.story-viewer__image').alt = story.alt;
    viewer.querySelector('.story-viewer__text').textContent = story.text_overlay || '';

    // Link
    const linkEl = viewer.querySelector('.story-viewer__link');
    if (story.link) {
      linkEl.href = story.link.url;
      linkEl.textContent = story.link.label;
      linkEl.style.display = 'flex';
    } else {
      linkEl.style.display = 'none';
    }

    // Name
    viewer.querySelector('.story-viewer__name').textContent = story.highlight || 'if(塾)';
  }

  function startStoryTimer() {
    stopStoryTimer();

    const stories = state.filteredStories;
    const story = stories[state.currentStory];
    const duration = (story && story.duration) || 4;

    state.storyProgress = 0;
    const interval = 50; // 50ms updates
    const increment = (interval / (duration * 1000)) * 100;

    const progressBar = elements.storyViewer.querySelector(
      `.story-viewer__progress-fill[data-index="${state.currentStory}"]`
    );

    state.storyTimer = setInterval(() => {
      state.storyProgress += increment;

      if (progressBar) {
        progressBar.style.width = `${Math.min(state.storyProgress, 100)}%`;
      }

      if (state.storyProgress >= 100) {
        navigateStory(1);
      }
    }, interval);
  }

  function stopStoryTimer() {
    if (state.storyTimer) {
      clearInterval(state.storyTimer);
      state.storyTimer = null;
    }
  }

  function navigateStory(direction) {
    const stories = state.filteredStories;
    const newIndex = state.currentStory + direction;

    if (newIndex < 0 || newIndex >= stories.length) {
      closeStoryViewer();
      return;
    }

    state.currentStory = newIndex;
    updateStoryContent();
    startStoryTimer();
  }

  // ========================================
  // Swipe Support
  // ========================================
  function initSwipeSupport() {
    // Carousel swipe
    const carousel = elements.modal.querySelector('.carousel');
    let startX = 0;
    let isDragging = false;

    carousel.addEventListener('touchstart', (e) => {
      startX = e.touches[0].clientX;
      isDragging = true;
    }, { passive: true });

    carousel.addEventListener('touchmove', (e) => {
      if (!isDragging) return;
    }, { passive: true });

    carousel.addEventListener('touchend', (e) => {
      if (!isDragging) return;
      isDragging = false;

      const endX = e.changedTouches[0].clientX;
      const diff = startX - endX;

      if (Math.abs(diff) > 50) {
        navigateCarousel(diff > 0 ? 1 : -1);
      }
    });

    // Story viewer navigation zones
    const storyViewer = elements.storyViewer;
    storyViewer.querySelector('.story-viewer__nav--prev').addEventListener('click', () => {
      navigateStory(-1);
    });
    storyViewer.querySelector('.story-viewer__nav--next').addEventListener('click', () => {
      navigateStory(1);
    });
  }

  // ========================================
  // Event Listeners
  // ========================================
  function initEventListeners() {
    const modal = elements.modal;
    const storyViewer = elements.storyViewer;

    // Modal
    modal.querySelector('.modal__close').addEventListener('click', closePostModal);
    modal.querySelector('.modal__backdrop').addEventListener('click', closePostModal);
    modal.querySelector('.carousel__nav--prev').addEventListener('click', () => navigateCarousel(-1));
    modal.querySelector('.carousel__nav--next').addEventListener('click', () => navigateCarousel(1));

    // Carousel dots
    modal.querySelector('.carousel__dots').addEventListener('click', (e) => {
      if (e.target.classList.contains('carousel__dot')) {
        state.currentSlide = parseInt(e.target.dataset.index, 10);
        updateCarouselNav();
      }
    });

    // Story viewer
    storyViewer.querySelector('.story-viewer__close').addEventListener('click', closeStoryViewer);

    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
      if (modal.classList.contains('is-open')) {
        if (e.key === 'Escape') closePostModal();
        if (e.key === 'ArrowLeft') navigateCarousel(-1);
        if (e.key === 'ArrowRight') navigateCarousel(1);
      }

      if (storyViewer.classList.contains('is-open')) {
        if (e.key === 'Escape') closeStoryViewer();
        if (e.key === 'ArrowLeft') navigateStory(-1);
        if (e.key === 'ArrowRight') navigateStory(1);
      }
    });

    // Swipe
    initSwipeSupport();
  }

  // ========================================
  // Initialize
  // ========================================
  async function init() {
    // Cache DOM elements
    elements.storiesContainer = document.getElementById('stories-container');
    elements.highlightsContainer = document.getElementById('highlights-container');
    elements.postsGrid = document.getElementById('posts-grid');
    elements.modal = document.getElementById('post-modal');
    elements.storyViewer = document.getElementById('story-viewer');

    // Show loading state
    if (elements.postsGrid) {
      elements.postsGrid.innerHTML = `
        <div class="loading" style="grid-column: 1 / -1;">
          <div class="loading__spinner"></div>
        </div>
      `;
    }

    // Load data
    const success = await loadData();
    if (!success) {
      if (elements.postsGrid) {
        elements.postsGrid.innerHTML = `
          <div class="empty" style="grid-column: 1 / -1;">
            <div class="empty__icon">⚠️</div>
            <p>データの読み込みに失敗しました</p>
          </div>
        `;
      }
      return;
    }

    // Render
    renderStories();
    renderHighlights();
    renderPosts();

    // Event listeners
    initEventListeners();

    console.log('if(塾) Instagram風ブログ initialized');
  }

  // Run when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
