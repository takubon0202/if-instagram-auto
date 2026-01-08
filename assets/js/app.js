/**
 * if(塾) Instagram風ブログ - メインアプリケーション
 * 依存ライブラリなし（Vanilla JS）
 *
 * 機能:
 * - Grid/Feed表示切り替え
 * - 無限スクロール（12投稿ずつ読み込み）
 * - カテゴリフィルター
 * - 投稿カウント表示
 * - ローディング状態
 * - スクロール位置保持
 */

(function() {
  'use strict';

  // ========================================
  // Constants
  // ========================================
  const POSTS_PER_PAGE = 12;
  const SCROLL_THRESHOLD = 200; // px from bottom to trigger load

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
    filteredStories: [],
    // New state for infinite scroll and filtering
    displayedPosts: [],
    filteredPosts: [],
    currentPage: 0,
    isLoading: false,
    hasMorePosts: true,
    currentCategory: 'all',
    viewMode: 'grid', // 'grid' or 'feed'
    scrollPosition: 0,
    categories: []
  };

  // ========================================
  // DOM Elements
  // ========================================
  const elements = {
    storiesContainer: null,
    highlightsContainer: null,
    postsGrid: null,
    modal: null,
    storyViewer: null,
    // New elements
    postsSection: null,
    viewToggle: null,
    categoryFilter: null,
    postCount: null,
    loadingIndicator: null
  };

  // ========================================
  // Data Loading
  // ========================================
  async function loadData() {
    try {
      console.log('[if塾] Loading data...');

      const [configRes, postsRes, storiesRes, highlightsRes] = await Promise.all([
        fetch('data/config.json'),
        fetch('data/posts.json'),
        fetch('data/stories.json'),
        fetch('data/highlights.json')
      ]);

      // Check response status
      if (!postsRes.ok) {
        throw new Error(`Posts fetch failed: ${postsRes.status} ${postsRes.statusText}`);
      }

      state.config = await configRes.json();
      const postsData = await postsRes.json();
      const storiesData = await storiesRes.json();
      const highlightsData = await highlightsRes.json();

      state.posts = postsData.posts || [];
      state.stories = storiesData.stories || [];
      state.highlights = highlightsData.highlights || [];

      console.log(`[if塾] Loaded ${state.posts.length} posts, ${state.stories.length} stories, ${state.highlights.length} highlights`);

      // Extract unique categories from posts
      extractCategories();

      // Initialize filtered posts with all posts
      state.filteredPosts = [...state.posts];
      state.hasMorePosts = state.filteredPosts.length > 0;

      return true;
    } catch (error) {
      console.error('[if塾] Failed to load data:', error);
      return false;
    }
  }

  // ========================================
  // Category Management
  // ========================================
  function extractCategories() {
    const categorySet = new Set();

    state.posts.forEach(post => {
      // Check highlight field (most common category indicator)
      if (post.highlight) {
        categorySet.add(post.highlight);
      }
      // Also check track and category fields
      if (post.track) {
        categorySet.add(post.track);
      }
      if (post.category) {
        categorySet.add(post.category);
      }
    });

    state.categories = Array.from(categorySet).sort();
  }

  function filterByCategory(category) {
    state.currentCategory = category;
    state.currentPage = 0;
    state.displayedPosts = [];
    state.hasMorePosts = true;

    if (category === 'all') {
      state.filteredPosts = [...state.posts];
    } else {
      state.filteredPosts = state.posts.filter(post =>
        post.highlight === category ||
        post.track === category ||
        post.category === category
      );
    }

    // Re-render posts
    clearPostsGrid();
    loadMorePosts();
    updatePostCount();
    updateCategoryButtons();
  }

  function updateCategoryButtons() {
    if (!elements.categoryFilter) return;

    const buttons = elements.categoryFilter.querySelectorAll('.category-btn');
    buttons.forEach(btn => {
      const isActive = btn.dataset.category === state.currentCategory;
      btn.classList.toggle('is-active', isActive);
      btn.classList.toggle('category-btn--active', isActive);
    });
  }

  // ========================================
  // View Mode Toggle
  // ========================================
  function toggleViewMode() {
    state.viewMode = state.viewMode === 'grid' ? 'feed' : 'grid';

    if (elements.postsGrid) {
      elements.postsGrid.classList.toggle('posts-grid--feed', state.viewMode === 'feed');
      elements.postsGrid.classList.toggle('posts-grid--grid', state.viewMode === 'grid');
    }

    updateViewToggleButtons();

    // Re-render displayed posts in new mode
    rerenderDisplayedPosts();
  }

  function updateViewToggleButtons() {
    if (!elements.viewToggle) return;

    const gridBtn = elements.viewToggle.querySelector('[data-view="grid"]');
    const feedBtn = elements.viewToggle.querySelector('[data-view="feed"]');

    if (gridBtn) {
      gridBtn.classList.toggle('is-active', state.viewMode === 'grid');
      gridBtn.classList.toggle('view-tab--active', state.viewMode === 'grid');
    }
    if (feedBtn) {
      feedBtn.classList.toggle('is-active', state.viewMode === 'feed');
      feedBtn.classList.toggle('view-tab--active', state.viewMode === 'feed');
    }
  }

  // ========================================
  // Post Count
  // ========================================
  function updatePostCount() {
    if (!elements.postCount) return;

    const total = state.filteredPosts.length;

    // HTML structure is: <strong id="post-count">0</strong> 投稿
    // So we only set the number
    elements.postCount.textContent = total;
  }

  // ========================================
  // Infinite Scroll & Loading
  // ========================================
  function loadMorePosts() {
    if (state.isLoading || !state.hasMorePosts) {
      console.log(`[if塾] loadMorePosts skipped: isLoading=${state.isLoading}, hasMorePosts=${state.hasMorePosts}`);
      return;
    }

    console.log(`[if塾] loadMorePosts: loading page ${state.currentPage}`);

    state.isLoading = true;
    showLoading();

    // Simulate async loading with requestAnimationFrame for smooth UI
    requestAnimationFrame(() => {
      const start = state.currentPage * POSTS_PER_PAGE;
      const end = start + POSTS_PER_PAGE;
      const newPosts = state.filteredPosts.slice(start, end);

      console.log(`[if塾] Loading posts ${start} to ${end}, found ${newPosts.length} posts`);

      if (newPosts.length > 0) {
        state.displayedPosts = [...state.displayedPosts, ...newPosts];
        state.currentPage++;
        appendPosts(newPosts, start);
      }

      state.hasMorePosts = end < state.filteredPosts.length;
      state.isLoading = false;

      hideLoading();
      updatePostCount();

      console.log(`[if塾] After load: displayed=${state.displayedPosts.length}, hasMore=${state.hasMorePosts}`);
    });
  }

  function showLoading() {
    if (elements.loadingIndicator) {
      elements.loadingIndicator.classList.add('is-visible');
    }
  }

  function hideLoading() {
    if (elements.loadingIndicator) {
      elements.loadingIndicator.classList.remove('is-visible');
    }
  }

  function handleScroll() {
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    const windowHeight = window.innerHeight;
    const documentHeight = document.documentElement.scrollHeight;

    // Check if we're near the bottom
    if (documentHeight - (scrollTop + windowHeight) < SCROLL_THRESHOLD) {
      loadMorePosts();
    }
  }

  // ========================================
  // Scroll Position Management
  // ========================================
  function saveScrollPosition() {
    state.scrollPosition = window.pageYOffset || document.documentElement.scrollTop;
  }

  function restoreScrollPosition() {
    window.scrollTo(0, state.scrollPosition);
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

  function renderControlsUI() {
    // Use existing HTML elements instead of creating duplicates
    const postsGrid = elements.postsGrid;
    if (!postsGrid) return;

    // Cache existing elements from HTML
    elements.viewToggle = document.querySelector('.view-tabs');
    elements.categoryFilter = document.querySelector('.category-filter');
    elements.postCount = document.getElementById('post-count');
    elements.loadingIndicator = document.getElementById('load-more');

    // Add event listeners for existing controls
    initControlsListeners();
  }

  function initControlsListeners() {
    // View toggle
    if (elements.viewToggle) {
      elements.viewToggle.addEventListener('click', (e) => {
        const btn = e.target.closest('[data-view]');
        if (btn && btn.dataset.view !== state.viewMode) {
          toggleViewMode();
        }
      });
    }

    // Category filter
    if (elements.categoryFilter) {
      elements.categoryFilter.addEventListener('click', (e) => {
        const btn = e.target.closest('.category-btn');
        if (btn) {
          filterByCategory(btn.dataset.category);
        }
      });
    }
  }

  function clearPostsGrid() {
    if (elements.postsGrid) {
      elements.postsGrid.innerHTML = '';
    }
  }

  function renderPostCard(post, index) {
    const firstMedia = post.media && post.media[0];
    const imageSrc = firstMedia ? firstMedia.src : '';
    const imageAlt = firstMedia ? firstMedia.alt : post.title;
    const typeIcon = post.type === 'carousel' ? '&#9707;' : (post.type === 'reel' ? '&#9654;' : '');

    if (state.viewMode === 'feed') {
      // Feed view - larger card with more info
      const datetime = new Date(post.datetime);
      const dateStr = datetime.toLocaleDateString('ja-JP', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      });

      return `
        <article class="post-card post-card--feed" data-index="${index}" tabindex="0" role="button" aria-label="${post.title}">
          <div class="post-card__header">
            <div class="post-card__avatar">if</div>
            <div class="post-card__meta">
              <span class="post-card__username">if_juku</span>
              <time class="post-card__date">${dateStr}</time>
            </div>
            ${post.highlight ? `<span class="post-card__category">${post.highlight}</span>` : ''}
          </div>
          <div class="post-card__media">
            <img
              src="${imageSrc}"
              alt="${imageAlt}"
              class="post-card__image"
              loading="lazy"
              onerror="this.src='data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><rect fill=%22%23f5f5f5%22 width=%22100%22 height=%22100%22/><text x=%2250%22 y=%2250%22 text-anchor=%22middle%22 fill=%22%23999%22 font-size=%228%22>${encodeURIComponent(post.title.substring(0, 10))}</text></svg>'"
            >
            ${typeIcon ? `<span class="post-card__type-badge" aria-hidden="true">${typeIcon}</span>` : ''}
            ${post.media && post.media.length > 1 ? `<span class="post-card__media-count">${post.media.length}</span>` : ''}
          </div>
          <div class="post-card__body">
            <h3 class="post-card__title">${post.title}</h3>
            <p class="post-card__caption">${post.caption.split('\n')[0].substring(0, 100)}${post.caption.length > 100 ? '...' : ''}</p>
          </div>
        </article>
      `;
    } else {
      // Grid view - compact card
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
          ${post.media && post.media.length > 1 ? `<span class="post-card__multi-badge" aria-hidden="true">&#9707;</span>` : ''}
        </article>
      `;
    }
  }

  function appendPosts(posts, startIndex) {
    const container = elements.postsGrid;
    if (!container) return;

    const fragment = document.createDocumentFragment();

    posts.forEach((post, i) => {
      const wrapper = document.createElement('div');
      wrapper.innerHTML = renderPostCard(post, startIndex + i);
      const card = wrapper.firstElementChild;

      // Add click handler
      card.addEventListener('click', () => {
        saveScrollPosition();
        openPostModal(startIndex + i);
      });

      card.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          saveScrollPosition();
          openPostModal(startIndex + i);
        }
      });

      // Add animation class
      card.style.opacity = '0';
      card.style.transform = 'translateY(20px)';

      fragment.appendChild(card);
    });

    container.appendChild(fragment);

    // Animate new cards
    requestAnimationFrame(() => {
      const newCards = container.querySelectorAll('.post-card');
      newCards.forEach((card, i) => {
        if (i >= startIndex) {
          setTimeout(() => {
            card.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
          }, (i - startIndex) * 50);
        }
      });
    });
  }

  function rerenderDisplayedPosts() {
    clearPostsGrid();

    const container = elements.postsGrid;
    if (!container) return;

    state.displayedPosts.forEach((post, index) => {
      const wrapper = document.createElement('div');
      wrapper.innerHTML = renderPostCard(post, index);
      const card = wrapper.firstElementChild;

      card.addEventListener('click', () => {
        saveScrollPosition();
        openPostModal(index);
      });

      card.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          saveScrollPosition();
          openPostModal(index);
        }
      });

      container.appendChild(card);
    });
  }

  function renderPosts() {
    const container = elements.postsGrid;
    if (!container) {
      console.error('[if塾] Posts grid container not found!');
      return;
    }

    console.log(`[if塾] renderPosts called, posts count: ${state.posts.length}`);

    // Clear and show initial loading
    container.innerHTML = '';

    if (state.posts.length === 0) {
      console.log('[if塾] No posts to display');
      container.innerHTML = `
        <div class="empty" style="grid-column: 1 / -1;">
          <div class="empty__icon">📷</div>
          <p>投稿がありません</p>
        </div>
      `;
      return;
    }

    // Load first batch of posts
    loadMorePosts();
  }

  // ========================================
  // Post Modal
  // ========================================
  function openPostModal(index) {
    const post = state.displayedPosts[index];
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

    // Restore scroll position after modal closes
    requestAnimationFrame(() => {
      restoreScrollPosition();
    });
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

    // Infinite scroll
    let scrollTimeout;
    window.addEventListener('scroll', () => {
      if (scrollTimeout) {
        cancelAnimationFrame(scrollTimeout);
      }
      scrollTimeout = requestAnimationFrame(handleScroll);
    }, { passive: true });

    // Swipe
    initSwipeSupport();
  }

  // ========================================
  // Initialize
  // ========================================
  async function init() {
    console.log('[if塾] init() called');

    // Cache DOM elements
    elements.storiesContainer = document.getElementById('stories-container');
    elements.highlightsContainer = document.getElementById('highlights-container');
    elements.postsGrid = document.getElementById('posts-grid');
    elements.modal = document.getElementById('post-modal');
    elements.storyViewer = document.getElementById('story-viewer');

    console.log('[if塾] DOM elements cached:', {
      postsGrid: !!elements.postsGrid,
      modal: !!elements.modal,
      storyViewer: !!elements.storyViewer
    });

    // Show loading state
    if (elements.postsGrid) {
      elements.postsGrid.innerHTML = `
        <div class="loading" style="grid-column: 1 / -1;">
          <div class="loading__spinner"></div>
        </div>
      `;
    }

    // Load data
    console.log('[if塾] Starting loadData...');
    const success = await loadData();
    console.log('[if塾] loadData result:', success, 'posts:', state.posts.length);

    if (!success) {
      console.error('[if塾] loadData failed');
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

    // Render UI controls
    console.log('[if塾] Rendering UI controls...');
    renderControlsUI();

    // Add grid class for initial state
    if (elements.postsGrid) {
      elements.postsGrid.classList.add('posts-grid--grid');
    }

    // Render
    console.log('[if塾] Rendering components...');
    renderStories();
    renderHighlights();
    renderPosts();

    // Event listeners
    initEventListeners();

    console.log('[if塾] Instagram風ブログ initialized');
    console.log(`[if塾] Total posts: ${state.posts.length}`);
    console.log(`[if塾] Displayed posts: ${state.displayedPosts.length}`);
    console.log(`[if塾] Categories: ${state.categories.join(', ')}`);
    console.log(`[if塾] Posts grid element:`, elements.postsGrid);

    // Debug: Update post count element directly to verify
    const postCountEl = document.getElementById('post-count');
    if (postCountEl) {
      console.log('[if塾] Post count element found, updating to:', state.posts.length);
    }
  }

  // ========================================
  // Public API (for debugging)
  // ========================================
  window.ifJukuApp = {
    loadMorePosts,
    filterByCategory,
    toggleViewMode,
    updatePostCount,
    getState: () => ({ ...state })
  };

  // Run when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
