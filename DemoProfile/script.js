const yearElement = document.getElementById('year');
if (yearElement) {
  yearElement.textContent = new Date().getFullYear();
}

const sections = document.querySelectorAll('main section');
const navLinks = document.querySelectorAll('.nav-links a');

const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        navLinks.forEach((link) => {
          const targetId = link.getAttribute('href')?.replace('#', '');
          link.classList.toggle('active', targetId === entry.target.id);
        });
      }
    });
  },
  { threshold: 0.35 }
);

sections.forEach((section) => observer.observe(section));
