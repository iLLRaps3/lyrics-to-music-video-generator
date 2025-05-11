// Mobile menu toggle functionality
document.addEventListener('DOMContentLoaded', function() {
  // Mobile menu toggle
  const mobileMenuButton = document.querySelector('.mobile-menu-button');
  const mobileMenu = document.querySelector('.mobile-menu');
  
  if (mobileMenuButton && mobileMenu) {
    mobileMenuButton.addEventListener('click', function() {
      mobileMenu.classList.toggle('hidden');
    });
  }

  // Close mobile menu when clicking on a link
  const mobileMenuLinks = document.querySelectorAll('.mobile-menu a');
  mobileMenuLinks.forEach(link => {
    link.addEventListener('click', function() {
      mobileMenu.classList.add('hidden');
    });
  });

  // Active link highlighting
  const currentPage = window.location.pathname.split('/').pop();
  const navLinks = document.querySelectorAll('nav a');
  
  navLinks.forEach(link => {
    const linkPage = link.getAttribute('href');
    if (linkPage === currentPage) {
      link.classList.add('text-blue-600', 'font-bold');
      link.classList.remove('text-gray-500');
    }
  });

  // Smooth scrolling for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth'
        });
      }
    });
  });
});

// Form validation for contact page
function validateForm() {
  const form = document.getElementById('contact-form');
  if (form) {
    form.addEventListener('submit', function(e) {
      let isValid = true;
      const nameInput = document.getElementById('name');
      const emailInput = document.getElementById('email');
      const serviceInput = document.getElementById('service');
      const messageInput = document.getElementById('message');
      const fileInput = document.getElementById('demo');
      
      // File validation
      if (fileInput.files.length > 0) {
        const file = fileInput.files[0];
        const validTypes = ['audio/mp3', 'audio/wav', 'audio/aiff'];
        const maxSize = 25 * 1024 * 1024; // 25MB
        
        if (!validTypes.includes(file.type)) {
          showError(fileInput, 'Please upload an MP3, WAV or AIFF file');
          isValid = false;
        } else if (file.size > maxSize) {
          showError(fileInput, 'File size must be less than 25MB');
          isValid = false;
        }
      }
      
      // Reset error states
      document.querySelectorAll('.error-message').forEach(el => el.remove());
      document.querySelectorAll('.border-red-500').forEach(el => el.classList.remove('border-red-500'));
      
      // Name validation
      if (!nameInput.value.trim()) {
        showError(nameInput, 'Name is required');
        isValid = false;
      }
      
      // Email validation
      if (!emailInput.value.trim()) {
        showError(emailInput, 'Email is required');
        isValid = false;
      } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailInput.value)) {
        showError(emailInput, 'Please enter a valid email');
        isValid = false;
      }
      
      // Service validation
      if (!serviceInput.value) {
        showError(serviceInput, 'Please select a service');
        isValid = false;
      }
      
      // Message validation
      if (!messageInput.value.trim()) {
        showError(messageInput, 'Please describe your project');
        isValid = false;
      } else if (messageInput.value.trim().length < 20) {
        showError(messageInput, 'Please provide more details (min 20 characters)');
        isValid = false;
      }
      
      if (!isValid) {
        e.preventDefault();
      }
    });
  }
}

function showError(input, message) {
  input.classList.add('border-red-500');
  const error = document.createElement('p');
  error.className = 'error-message text-red-500 text-xs mt-1';
  error.textContent = message;
  input.parentNode.appendChild(error);
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
  validateForm();
});