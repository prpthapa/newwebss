// ===================================
// PAGE LOADER
// ===================================
window.addEventListener('load', () => {
    const loader = document.getElementById('pageLoader');
    if (loader) {
        setTimeout(() => {
            loader.classList.add('hidden');
        }, 1000);
    }
});

// ===================================
// SMOOTH SCROLL & HEADER BEHAVIOR
// ===================================
const header = document.getElementById('header');
const navLinks = document.querySelectorAll('.nav-link');
const mobileToggle = document.getElementById('mobileToggle');
const navbar = document.getElementById('navbar');

// Header scroll effect
window.addEventListener('scroll', () => {
    if (header) {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    }
    
    // Update back to top button
    updateBackToTop();
    
    // Update active navigation
    updateActiveNav();
});

// Mobile menu toggle
if (mobileToggle && navbar) {
    mobileToggle.addEventListener('click', () => {
        mobileToggle.classList.toggle('active');
        navbar.classList.toggle('active');
    });
}

// Close mobile menu when clicking on a link
navLinks.forEach(link => {
    link.addEventListener('click', () => {
        if (mobileToggle && navbar) {
            mobileToggle.classList.remove('active');
            navbar.classList.remove('active');
        }
    });
});

// Active navigation link on scroll
const sections = document.querySelectorAll('section[id]');

function updateActiveNav() {
    const scrollPosition = window.scrollY + 100;
    
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.offsetHeight;
        const sectionId = section.getAttribute('id');
        
        if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
            navLinks.forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href') === `#${sectionId}`) {
                    link.classList.add('active');
                }
            });
        }
    });
}

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href !== '#' && href !== '') {
            e.preventDefault();
            const target = document.querySelector(href);
            if (target && header) {
                const headerHeight = header.offsetHeight;
                const targetPosition = target.offsetTop - headerHeight;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        }
    });
});

// ===================================
// SCROLL ANIMATIONS
// ===================================
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const elementObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe all elements with data-aos attribute
document.querySelectorAll('[data-aos]').forEach(element => {
    element.style.opacity = '0';
    element.style.transform = 'translateY(30px)';
    element.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    
    const delay = element.getAttribute('data-aos-delay');
    if (delay) {
        element.style.transitionDelay = `${delay}ms`;
    }
    
    elementObserver.observe(element);
});

// ===================================
// BACK TO TOP BUTTON
// ===================================
const backToTopBtn = document.getElementById('backToTop');

function updateBackToTop() {
    if (backToTopBtn) {
        if (window.scrollY > 500) {
            backToTopBtn.classList.add('visible');
        } else {
            backToTopBtn.classList.remove('visible');
        }
    }
}

if (backToTopBtn) {
    backToTopBtn.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// ===================================
// CONTACT FORM HANDLING
// ===================================
const contactForm = document.getElementById('contactForm');
const formMessage = document.getElementById('formMessage');

if (contactForm) {
    contactForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Get form data
        const formData = new FormData(contactForm);
        
        // Validate form
        const data = {
            name: formData.get('name'),
            email: formData.get('email'),
            subject: formData.get('subject'),
            message: formData.get('message')
        };
        
        if (!validateForm(data)) {
            return;
        }
        
        // Show loading state
        const submitBtn = contactForm.querySelector('.submit-btn');
        const btnText = submitBtn.querySelector('.btn-text');
        const btnLoading = submitBtn.querySelector('.btn-loading');
        
        if (btnText && btnLoading) {
            btnText.style.display = 'none';
            btnLoading.style.display = 'inline-flex';
        }
        submitBtn.disabled = true;
        
        try {
            // Get CSRF token
            const csrfToken = formData.get('csrfmiddlewaretoken');
            
            // Send data to backend
            const response = await fetch('/api/contact/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken
                },
                body: formData
            });
            
            const result = await response.json();
            
            if (response.ok && result.success) {
                showFormMessage('success', result.message || 'Thank you! Your message has been sent successfully.');
                contactForm.reset();
            } else {
                showFormMessage('error', result.message || 'Something went wrong. Please try again.');
            }
            
        } catch (error) {
            console.error('Error:', error);
            showFormMessage('error', 'Network error. Please check your connection and try again.');
        } finally {
            // Reset button state
            if (btnText && btnLoading) {
                btnText.style.display = 'inline';
                btnLoading.style.display = 'none';
            }
            submitBtn.disabled = false;
        }
    });
}

function validateForm(data) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    
    if (!data.name || data.name.trim().length < 2) {
        showFormMessage('error', 'Please enter a valid name (at least 2 characters).');
        return false;
    }
    
    if (!emailRegex.test(data.email)) {
        showFormMessage('error', 'Please enter a valid email address.');
        return false;
    }
    
    if (!data.subject || data.subject.trim().length < 3) {
        showFormMessage('error', 'Please enter a subject (at least 3 characters).');
        return false;
    }
    
    if (!data.message || data.message.trim().length < 10) {
        showFormMessage('error', 'Please enter a message (at least 10 characters).');
        return false;
    }
    
    return true;
}

function showFormMessage(type, message) {
    if (formMessage) {
        formMessage.textContent = message;
        formMessage.className = `form-message ${type}`;
        formMessage.style.display = 'block';
        
        // Auto-hide success messages after 5 seconds
        if (type === 'success') {
            setTimeout(() => {
                formMessage.style.display = 'none';
            }, 5000);
        }
    }
}

// ===================================
// SUBJECT CARD TRACKING
// ===================================
const subjectButtons = document.querySelectorAll('.subject-btn');

subjectButtons.forEach(btn => {
    btn.addEventListener('click', (e) => {
        const subject = e.currentTarget.getAttribute('data-subject');
        
        // Track analytics
        trackEvent('subject_click', {
            subject: subject,
            timestamp: new Date().toISOString()
        });
        
        // Add animation effect
        e.currentTarget.style.transform = 'scale(0.95)';
        setTimeout(() => {
            e.currentTarget.style.transform = '';
        }, 200);
    });
});

function trackEvent(eventName, eventData) {
    // Placeholder for analytics tracking
    console.log('Event tracked:', eventName, eventData);
}

// ===================================
// LAZY LOADING FOR IMAGES
// ===================================
if ('loading' in HTMLImageElement.prototype) {
    const images = document.querySelectorAll('img[loading="lazy"]');
    images.forEach(img => {
        img.src = img.src;
    });
} else {
    // Fallback for browsers that don't support lazy loading
    const script = document.createElement('script');
    script.src = 'https://cdnjs.cloudflare.com/ajax/libs/lazysizes/5.3.2/lazysizes.min.js';
    document.body.appendChild(script);
}

// ===================================
// COOKIE CONSENT
// ===================================
const cookieSettings = document.getElementById('cookieSettings');

if (cookieSettings) {
    cookieSettings.addEventListener('click', (e) => {
        e.preventDefault();
        showCookieConsent();
    });
}

function showCookieConsent() {
    alert('Cookie settings functionality - integrate with your cookie consent solution');
}

function checkCookieConsent() {
    const consent = localStorage.getItem('cookieConsent');
    if (!consent) {
        // Show cookie consent banner if needed
    }
}

checkCookieConsent();

// ===================================
// KEYBOARD NAVIGATION
// ===================================
document.addEventListener('keydown', (e) => {
    // Close mobile menu with Escape key
    if (e.key === 'Escape' && navbar && navbar.classList.contains('active')) {
        if (mobileToggle) mobileToggle.classList.remove('active');
        navbar.classList.remove('active');
    }
    
    // Scroll to top with Home key
    if (e.key === 'Home' && e.ctrlKey) {
        e.preventDefault();
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
    
    // Scroll to bottom with End key
    if (e.key === 'End' && e.ctrlKey) {
        e.preventDefault();
        window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
    }
});

// ===================================
// DEBOUNCE HELPER FUNCTION
// ===================================
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// ===================================
// LOCAL STORAGE HELPERS
// ===================================
const Storage = {
    set: (key, value) => {
        try {
            localStorage.setItem(key, JSON.stringify(value));
            return true;
        } catch (error) {
            console.error('Storage error:', error);
            return false;
        }
    },
    
    get: (key) => {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : null;
        } catch (error) {
            console.error('Storage error:', error);
            return null;
        }
    },
    
    remove: (key) => {
        try {
            localStorage.removeItem(key);
            return true;
        } catch (error) {
            console.error('Storage error:', error);
            return false;
        }
    },
    
    clear: () => {
        try {
            localStorage.clear();
            return true;
        } catch (error) {
            console.error('Storage error:', error);
            return false;
        }
    }
};

// ===================================
// SHARE FUNCTIONALITY
// ===================================
async function shareContent(title, text, url) {
    if (navigator.share) {
        try {
            await navigator.share({
                title: title,
                text: text,
                url: url
            });
            console.log('Content shared successfully');
        } catch (error) {
            console.error('Error sharing:', error);
        }
    } else {
        // Fallback: copy to clipboard
        const fullUrl = window.location.origin + url;
        copyToClipboard(fullUrl);
        alert('Link copied to clipboard!');
    }
}

function copyToClipboard(text) {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    textarea.style.opacity = '0';
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand('copy');
    document.body.removeChild(textarea);
}

// ===================================
// NOTIFICATION SYSTEM
// ===================================
function showNotification(message, type = 'info', duration = 3000) {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    const bgColor = type === 'success' ? '#2ECC71' : type === 'error' ? '#E74C3C' : '#FF6B35';
    
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        background: ${bgColor};
        color: white;
        border-radius: 12px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.16);
        z-index: 10000;
        animation: slideInRight 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => {
            if (notification.parentNode) {
                document.body.removeChild(notification);
            }
        }, 300);
    }, duration);
}

// ===================================
// NOTES VIEWER FUNCTIONALITY (for topic_detail.html)
// ===================================
function initializeNotesViewer() {
    const notesContainer = document.querySelector('.note-container');
    if (!notesContainer) return; // Not on notes viewer page
    
    let currentPage = 1;
    const notes = document.querySelectorAll('.note-image-wrapper');
    const thumbnails = document.querySelectorAll('.thumbnail');
    const totalPages = notes.length;
    
    if (totalPages === 0) return;
    
    function updatePage(page) {
        if (page < 1 || page > totalPages) return;
        
        currentPage = page;
        const currentPageEl = document.getElementById('currentPage');
        if (currentPageEl) {
            currentPageEl.textContent = currentPage;
        }
        
        // Update notes visibility
        notes.forEach((note, index) => {
            note.classList.toggle('active', index + 1 === currentPage);
        });
        
        // Update thumbnail active state
        thumbnails.forEach((thumb, index) => {
            thumb.classList.toggle('active', index + 1 === currentPage);
        });
        
        // Scroll thumbnail into view
        const activeThumbnail = document.querySelector(`.thumbnail[data-page="${currentPage}"]`);
        if (activeThumbnail) {
            activeThumbnail.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
        }
        
        // Update button states
        const prevBtn = document.getElementById('prevNote');
        const nextBtn = document.getElementById('nextNote');
        if (prevBtn) prevBtn.disabled = currentPage === 1;
        if (nextBtn) nextBtn.disabled = currentPage === totalPages;
        
        // Reset zoom when changing pages
        const activeNote = document.querySelector('.note-image-wrapper.active .note-image');
        if (activeNote) {
            activeNote.style.transform = 'scale(1)';
        }
    }
    
    // Navigation buttons
    const prevBtn = document.getElementById('prevNote');
    const nextBtn = document.getElementById('nextNote');
    
    if (prevBtn) {
        prevBtn.addEventListener('click', () => {
            updatePage(currentPage - 1);
        });
    }
    
    if (nextBtn) {
        nextBtn.addEventListener('click', () => {
            updatePage(currentPage + 1);
        });
    }
    
    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowLeft') updatePage(currentPage - 1);
        if (e.key === 'ArrowRight') updatePage(currentPage + 1);
    });
    
    // Fullscreen toggle
    const fullscreenBtn = document.getElementById('toggleFullscreen');
    if (fullscreenBtn) {
        fullscreenBtn.addEventListener('click', () => {
            const viewer = document.getElementById('notesViewer');
            if (viewer) {
                viewer.classList.toggle('fullscreen');
                const icon = fullscreenBtn.querySelector('i');
                if (icon) {
                    icon.classList.toggle('fa-expand');
                    icon.classList.toggle('fa-compress');
                }
            }
        });
    }
    
    // Zoom controls
    let zoomLevel = 1;
    const zoomInBtn = document.getElementById('zoomIn');
    const zoomOutBtn = document.getElementById('zoomOut');
    
    if (zoomInBtn) {
        zoomInBtn.addEventListener('click', () => {
            zoomLevel = Math.min(zoomLevel + 0.2, 3);
            const activeImage = document.querySelector('.note-image-wrapper.active .note-image');
            if (activeImage) {
                activeImage.style.transform = `scale(${zoomLevel})`;
            }
        });
    }
    
    if (zoomOutBtn) {
        zoomOutBtn.addEventListener('click', () => {
            zoomLevel = Math.max(zoomLevel - 0.2, 0.5);
            const activeImage = document.querySelector('.note-image-wrapper.active .note-image');
            if (activeImage) {
                activeImage.style.transform = `scale(${zoomLevel})`;
            }
        });
    }
    
    // Thumbnail click handler
    thumbnails.forEach((thumbnail, index) => {
        thumbnail.addEventListener('click', () => {
            updatePage(index + 1);
        });
    });
    
    // Initialize first page
    updatePage(1);
}

// Global function for thumbnail clicks (used in template)
function goToPage(page) {
    const notes = document.querySelectorAll('.note-image-wrapper');
    const thumbnails = document.querySelectorAll('.thumbnail');
    const totalPages = notes.length;
    
    if (page < 1 || page > totalPages) return;
    
    const currentPageEl = document.getElementById('currentPage');
    if (currentPageEl) {
        currentPageEl.textContent = page;
    }
    
    notes.forEach((note, index) => {
        note.classList.toggle('active', index + 1 === page);
    });
    
    thumbnails.forEach((thumb, index) => {
        thumb.classList.toggle('active', index + 1 === page);
    });
    
    const prevBtn = document.getElementById('prevNote');
    const nextBtn = document.getElementById('nextNote');
    if (prevBtn) prevBtn.disabled = page === 1;
    if (nextBtn) nextBtn.disabled = page === totalPages;
}

// ===================================
// SHOW MORE FUNCTIONALITY
// ===================================
function initializeShowMore() {
    // Show More Chapters
    const showMoreChaptersBtn = document.getElementById('showMoreChapters');
    if (showMoreChaptersBtn) {
        showMoreChaptersBtn.addEventListener('click', function() {
            const hiddenChapters = document.querySelectorAll('.hidden-chapter');
            const isShowing = this.classList.contains('showing');
            
            if (isShowing) {
                // Hide chapters
                hiddenChapters.forEach(chapter => {
                    chapter.style.display = 'none';
                });
                this.querySelector('.show-more-text').textContent = 'Show More Chapters';
                this.querySelector('i').classList.remove('fa-chevron-up');
                this.querySelector('i').classList.add('fa-chevron-down');
                this.classList.remove('showing');
            } else {
                // Show chapters
                hiddenChapters.forEach(chapter => {
                    chapter.style.display = 'block';
                });
                this.querySelector('.show-more-text').textContent = 'Show Less';
                this.querySelector('i').classList.remove('fa-chevron-down');
                this.querySelector('i').classList.add('fa-chevron-up');
                this.classList.add('showing');
            }
        });
    }
    
    // Show More Topics
    const showMoreTopicsBtn = document.getElementById('showMoreTopics');
    if (showMoreTopicsBtn) {
        showMoreTopicsBtn.addEventListener('click', function() {
            const hiddenTopics = document.querySelectorAll('.hidden-topic');
            const isShowing = this.classList.contains('showing');
            
            if (isShowing) {
                // Hide topics
                hiddenTopics.forEach(topic => {
                    topic.style.display = 'none';
                });
                this.querySelector('.show-more-text').textContent = 'Show More Topics';
                this.querySelector('i').classList.remove('fa-chevron-up');
                this.querySelector('i').classList.add('fa-chevron-down');
                this.classList.remove('showing');
            } else {
                // Show topics
                hiddenTopics.forEach(topic => {
                    topic.style.display = 'block';
                });
                this.querySelector('.show-more-text').textContent = 'Show Less';
                this.querySelector('i').classList.remove('fa-chevron-down');
                this.querySelector('i').classList.add('fa-chevron-up');
                this.classList.add('showing');
            }
        });
    }
    
    // Show More Thumbnails (Note Images)
    const showMoreThumbnailsBtn = document.getElementById('showMoreThumbnails');
    if (showMoreThumbnailsBtn) {
        showMoreThumbnailsBtn.addEventListener('click', function() {
            const hiddenThumbnails = document.querySelectorAll('.hidden-thumbnail');
            const isShowing = this.classList.contains('showing');
            
            if (isShowing) {
                // Hide thumbnails
                hiddenThumbnails.forEach(thumb => {
                    thumb.style.display = 'none';
                });
                const totalCount = document.querySelectorAll('.thumbnail').length;
                this.querySelector('.show-more-text').textContent = `Show All Pages (${totalCount})`;
                this.querySelector('i').classList.remove('fa-chevron-up');
                this.querySelector('i').classList.add('fa-chevron-down');
                this.classList.remove('showing');
            } else {
                // Show thumbnails
                hiddenThumbnails.forEach(thumb => {
                    thumb.style.display = 'block';
                });
                this.querySelector('.show-more-text').textContent = 'Show Less';
                this.querySelector('i').classList.remove('fa-chevron-down');
                this.querySelector('i').classList.add('fa-chevron-up');
                this.classList.add('showing');
            }
        });
    }
}

// ===================================
// INITIALIZE ON DOM READY
// ===================================
document.addEventListener('DOMContentLoaded', () => {
    initializeNotesViewer();
    initializeShowMore();
    console.log('Notes website initialized successfully! 🚀');
});

// ===================================
// CSS ANIMATIONS
// ===================================
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    .form-message {
        padding: 1rem;
        border-radius: 8px;
        margin-top: 1rem;
        font-weight: 600;
    }
    
    .form-message.success {
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    
    .form-message.error {
        background-color: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }
`;
document.head.appendChild(style);