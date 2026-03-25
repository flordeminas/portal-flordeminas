document.addEventListener('DOMContentLoaded', () => {

    // Smooth scroll for nav links
    const navLinks = document.querySelectorAll('.nav-link, .header-cta, .btn');
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            const href = link.getAttribute('href');
            if (href.startsWith('#')) {
                e.preventDefault();
                const targetId = href.substring(1);
                const targetElement = document.getElementById(targetId);
                if (targetElement) {
                    window.scrollTo({
                        top: targetElement.offsetTop - 80, // subtract header height
                        behavior: 'smooth'
                    });
                }
            }
        });
    });

    // Handle Newsletter form submission (Netlify Forms AJAX)
    const newsletterForm = document.getElementById('newsletter-form');
    const formWrapper = document.getElementById('newsletter-form-wrapper');
    const successMessage = document.getElementById('newsletter-success');

    if (newsletterForm) {
        newsletterForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const formData = new FormData(newsletterForm);
            
            // Show loading state
            const button = newsletterForm.querySelector('.cta-btn');
            const originalText = button.innerHTML;
            button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processando...';
            button.disabled = true;

            fetch('/', {
                method: 'POST',
                headers: { "Content-Type": "application/x-www-form-urlencoded" },
                body: new URLSearchParams(formData).toString()
            })
            .then(() => {
                // Success Transition
                formWrapper.style.opacity = '0';
                setTimeout(() => {
                    formWrapper.style.display = 'none';
                    successMessage.style.display = 'block';
                    successMessage.style.opacity = '0';
                    setTimeout(() => {
                        successMessage.style.opacity = '1';
                        successMessage.style.transform = 'translateY(0)';
                    }, 50);
                }, 300);
            })
            .catch(error => {
                console.error('Newsletter Error:', error);
                alert('Ocorreu um erro ao processar sua inscrição. Por favor, tente novamente.');
                button.innerHTML = originalText;
                button.disabled = false;
            });
        });
    }

    // Intersection Observer for scroll animations
    const observerOptions = {
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Initial styles for animations
    const animatedElements = document.querySelectorAll('.service-card, .article-card, .cta-section');
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'all 0.6s ease-out';
        observer.observe(el);
    });

    // Mobile Menu Toggle
    const menuToggle = document.getElementById('menu-toggle');
    const navLinksList = document.querySelector('.nav-links');
    
    if (menuToggle && navLinksList) {
        menuToggle.addEventListener('click', () => {
            menuToggle.classList.toggle('active');
            navLinksList.classList.toggle('active');
        });

        // Close menu when clicking a link
        navLinksList.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                menuToggle.classList.remove('active');
                navLinksList.classList.remove('active');
            });
        });
    }

    // Theme Toggle Logic
    const themeToggle = document.getElementById('theme-toggle');
    const htmlElement = document.documentElement;
    
    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            const currentTheme = htmlElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';
            
            htmlElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
        });
    }

    // Change header appearance on scroll
    const header = document.querySelector('header');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });

    // Ensure all external links open in a new tab
    const allLinks = document.querySelectorAll('a');
    allLinks.forEach(link => {
        const href = link.getAttribute('href');
        // Check if the link is external (starts with http, https, mailto, tel, or is a WhatsApp link)
        if (href && (href.startsWith('http') || href.startsWith('mailto') || href.startsWith('tel') || href.includes('wa.me'))) {
            // Only set if not already set or specifically desired for all external
            link.setAttribute('target', '_blank');
            link.setAttribute('rel', 'noopener noreferrer');
        }
    });

});
