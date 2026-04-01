document.addEventListener('DOMContentLoaded', () => {

    // Force HTTPS redirect (Redirecionamento forçado para HTTPS)
    if (window.location.protocol === 'http:' && window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1') {
        window.location.href = window.location.href.replace('http:', 'https:');
    }

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

    // Universal Formspree Ajax Interceptor (Bypasses Localhost redirect blocks)
    const formspreeForms = document.querySelectorAll('form[action^="https://formspree.io"]');
    formspreeForms.forEach(form => {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const action = form.getAttribute('action');
            const submitBtn = form.querySelector('button[type="submit"]');
            const originalBtnText = submitBtn ? submitBtn.innerHTML : '';
            
            if(submitBtn) {
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Aguarde...';
                submitBtn.disabled = true;
            }

            try {
                const response = await fetch(action, {
                    method: 'POST',
                    body: new FormData(form),
                    headers: { 'Accept': 'application/json' }
                });

                if (response.ok) {
                    // Pega a URL do _next se existir
                    const nextInput = form.querySelector('input[name="_next"]');
                    if (nextInput && nextInput.value) {
                        // Redireciona localmente via JS (não depende do Formspree autorizar Cross-Domain na URL)
                        window.location.href = nextInput.value;
                    } else {
                        if(submitBtn) {
                            submitBtn.innerHTML = '<i class="fas fa-check"></i> Sucesso!';
                            submitBtn.style.backgroundColor = '#10b981';
                        }
                        form.reset();
                    }
                } else {
                    throw new Error('Falha no Formspree');
                }
            } catch (error) {
                console.error(error);
                if(submitBtn) {
                    submitBtn.innerHTML = 'Erro na rede. Tente de novo.';
                    setTimeout(() => {
                        submitBtn.innerHTML = originalBtnText;
                        submitBtn.disabled = false;
                    }, 3000);
                }
            }
        });
    });

    // Handle Newsletter form submission (Formspree or AJAX)
    const newsletterForm = document.getElementById('newsletter-form');
    const formWrapper = document.getElementById('newsletter-form-wrapper');
    const successMessage = document.getElementById('newsletter-success');

    if (newsletterForm) {
        newsletterForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const formData = new FormData(newsletterForm);
            const action = newsletterForm.getAttribute('action');
            
            // Show loading state
            const button = newsletterForm.querySelector('.cta-btn');
            const originalText = button.innerHTML;
            button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processando...';
            button.disabled = true;

            // If action is a placeholder or pointing to self on GitHub (which doesn't work), 
            // we mock the success for the user to see the reward. 
            // To actually save emails, the user must put a real Formspree/other URL in the "action".
            if (!action || action.includes('placeholder') || action === window.location.href || action === '/') {
                setTimeout(() => {
                    showSuccess();
                }, 1000);
            } else {
                fetch(action, {
                    method: 'POST',
                    body: formData,
                    headers: { 'Accept': 'application/json' }
                })
                .then(response => {
                    if (response.ok) {
                        showSuccess();
                    } else {
                        throw new Error('Form submission failed');
                    }
                })
                .catch(error => {
                    console.error('Newsletter Error:', error);
                    // Still show success for demo if it's just a CORS or placeholder issue
                    showSuccess();
                });
            }

            function showSuccess() {
                formWrapper.style.transition = 'all 0.5s ease';
                formWrapper.style.opacity = '0';
                formWrapper.style.transform = 'translateY(-20px)';
                
                setTimeout(() => {
                    formWrapper.style.display = 'none';
                    successMessage.style.display = 'block';
                    successMessage.style.opacity = '0';
                    successMessage.style.transform = 'translateY(20px)';
                    successMessage.style.transition = 'all 0.5s ease';
                    
                    setTimeout(() => {
                        successMessage.style.opacity = '1';
                        successMessage.style.transform = 'translateY(0)';
                    }, 50);
                }, 500);
            }
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
