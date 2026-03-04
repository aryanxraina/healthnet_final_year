// Mobile menu toggle
// Mobile menu toggle
const mobileMenuBtn = document.getElementById('mobileMenuBtn');
if (mobileMenuBtn) {
    mobileMenuBtn.addEventListener('click', function () {
        const mobileMenu = document.getElementById('mobileMenu');
        if (mobileMenu) {
            mobileMenu.classList.toggle('hidden');
        }
    });
}

// Features dropdown (desktop)
const featuresBtn = document.getElementById('featuresDropdownBtn');
const featuresMenu = document.getElementById('featuresDropdown');
if (featuresBtn && featuresMenu) {
    featuresBtn.addEventListener('click', function (e) {
        e.preventDefault();
        featuresMenu.classList.toggle('hidden');
    });
    document.addEventListener('click', function (e) {
        if (!featuresBtn.contains(e.target) && !featuresMenu.contains(e.target)) {
            featuresMenu.classList.add('hidden');
        }
    });
}

// Profile dropdown
const profileDropdown = document.getElementById('profileDropdown');
if (profileDropdown) {
    profileDropdown.addEventListener('click', function () {
        // Add dropdown functionality here
        // For now, maybe just toggle a simple menu or log out
        console.log("Profile clicked");
    });
}

// Toast notification function
function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;

    const container = document.getElementById('toastContainer');
    if (container) {
        container.appendChild(toast);

        // Show toast
        setTimeout(() => toast.classList.add('show'), 100);

        // Hide and remove toast
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }
}

// Initialize page
document.addEventListener('DOMContentLoaded', function () {
    // Check if user is logged in
    const token = localStorage.getItem('healthnet_token');
    const profileDropdown = document.getElementById('profileDropdown');

    if (profileDropdown) {
        if (token) {
            // User is logged in, show profile section
            profileDropdown.style.display = 'flex';
        } else {
            // User is not logged in, hide profile
            // Ideally we should show a login button here
            profileDropdown.style.display = 'none';
        }
    }
});
