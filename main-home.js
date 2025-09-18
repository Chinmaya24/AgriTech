// main-home.js
// Simple animation and interactivity for AgriAI Dashboard

document.addEventListener('DOMContentLoaded', function() {
  // Language selector demo
  const langSelector = document.getElementById('language-selector');
  langSelector.addEventListener('change', function() {
    alert('Language switched to: ' + langSelector.options[langSelector.selectedIndex].text);
    // Integrate real i18n here
  });

  // Animate stat cards on scroll
  const statCards = document.querySelectorAll('.stat-card');
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.animation = 'fadeInUp 1s';
        entry.target.style.opacity = 1;
      }
    });
  }, { threshold: 0.5 });
  statCards.forEach(card => {
    card.style.opacity = 0;
    observer.observe(card);
  });

  // Hero animation (extra effect)
  const heroAnim = document.querySelector('.hero-animation');
  if (heroAnim) {
    heroAnim.addEventListener('mouseenter', () => {
      heroAnim.style.animationDuration = '2s';
    });
    heroAnim.addEventListener('mouseleave', () => {
      heroAnim.style.animationDuration = '4s';
    });
  }

  // Sidebar toggle for mobile
  const sidebarToggle = document.querySelector('.sidebar-toggle');
  const sidebar = document.querySelector('.sidebar');
  sidebarToggle.addEventListener('click', function() {
    sidebar.classList.toggle('active');
    sidebarToggle.classList.toggle('active');
  });

  // Welcome animation (user friendly)
  setTimeout(() => {
    const heroTitle = document.querySelector('.hero-title-gradient');
    if (heroTitle) {
      heroTitle.style.transition = 'text-shadow 0.7s';
      heroTitle.style.textShadow = '0 0 18px #b2f7ef';
      setTimeout(() => {
        heroTitle.style.textShadow = '';
      }, 1200);
    }
  }, 600);
});
