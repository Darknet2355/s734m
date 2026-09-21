// FutureForge Labs — main.js
document.addEventListener('DOMContentLoaded', function () {

  /* ---------- Mobile navigation toggle ---------- */
  const hamburger = document.querySelector('.hamburger');
  const navbar = document.querySelector('.navbar');
  if (hamburger && navbar) {
    hamburger.addEventListener('click', function () {
      navbar.classList.toggle('open');
    });
    // Close menu when a nav link is tapped (mobile UX)
    document.querySelectorAll('.nav-links a').forEach(function (link) {
      link.addEventListener('click', function () {
        navbar.classList.remove('open');
      });
    });
  }

  /* ---------- "More" nav dropdown ---------- */
  document.querySelectorAll('.nav-dropdown-toggle').forEach(function (toggle) {
    const dropdown = toggle.closest('.nav-dropdown');
    toggle.addEventListener('click', function (e) {
      e.stopPropagation();
      const willOpen = !dropdown.classList.contains('open');
      document.querySelectorAll('.nav-dropdown.open').forEach(function (d) {
        d.classList.remove('open');
        d.querySelector('.nav-dropdown-toggle').setAttribute('aria-expanded', 'false');
      });
      if (willOpen) {
        dropdown.classList.add('open');
        toggle.setAttribute('aria-expanded', 'true');
      }
    });
  });
  document.addEventListener('click', function (e) {
    document.querySelectorAll('.nav-dropdown.open').forEach(function (dropdown) {
      if (!dropdown.contains(e.target)) {
        dropdown.classList.remove('open');
        dropdown.querySelector('.nav-dropdown-toggle').setAttribute('aria-expanded', 'false');
      }
    });
  });

  /* ---------- Animated stat counters ---------- */
  const counters = document.querySelectorAll('[data-counter]');
  if (counters.length) {
    const animateCounter = (el) => {
      const target = parseInt(el.getAttribute('data-counter'), 10) || 0;
      const duration = 1500;
      const startTime = performance.now();

      const step = (now) => {
        const progress = Math.min((now - startTime) / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
        el.textContent = Math.floor(eased * target).toLocaleString();
        if (progress < 1) {
          requestAnimationFrame(step);
        } else {
          el.textContent = target.toLocaleString() + (el.getAttribute('data-suffix') || '');
        }
      };
      requestAnimationFrame(step);
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          animateCounter(entry.target);
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.4 });

    counters.forEach((el) => observer.observe(el));
  }

  /* ---------- Image preview before upload (dashboard forms) ---------- */
  document.querySelectorAll('input[type="file"][data-preview]').forEach(function (input) {
    input.addEventListener('change', function () {
      const previewId = input.getAttribute('data-preview');
      const previewEl = document.getElementById(previewId);
      if (!previewEl || !input.files || !input.files[0]) return;
      const reader = new FileReader();
      reader.onload = function (e) {
        previewEl.src = e.target.result;
        previewEl.style.display = 'block';
      };
      reader.readAsDataURL(input.files[0]);
    });
  });

  /* ---------- Confirm before delete ---------- */
  document.querySelectorAll('[data-confirm]').forEach(function (el) {
    el.addEventListener('click', function (e) {
      const message = el.getAttribute('data-confirm') || 'Are you sure you want to delete this item?';
      if (!confirm(message)) {
        e.preventDefault();
      }
    });
  });

  /* ---------- Auto-dismiss alerts ---------- */
  document.querySelectorAll('.alert').forEach(function (alertEl) {
    setTimeout(function () {
      alertEl.style.transition = 'opacity 0.5s ease';
      alertEl.style.opacity = '0';
      setTimeout(() => alertEl.remove(), 500);
    }, 6000);
  });

  /* ---------- Navbar shadow on scroll ---------- */
  const nav = document.querySelector('.navbar');
  if (nav) {
    window.addEventListener('scroll', function () {
      if (window.scrollY > 10) {
        nav.style.boxShadow = '0 8px 24px rgba(5,11,31,0.35)';
      } else {
        nav.style.boxShadow = '';
      }
    });
  }
});
