document.addEventListener('DOMContentLoaded', function() {
    initTooltips();
    initScrollAnimations();
    initToastNotifications();
    initBackToTop();
});

function initTooltips() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(el) {
        return new bootstrap.Tooltip(el);
    });
}

function initScrollAnimations() {
    var observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.stat-card, .feature-card, .falla-card').forEach(function(el) {
        observer.observe(el);
    });
}

function initToastNotifications() {
    var toasts = document.querySelectorAll('.toast');
    toasts.forEach(function(toast) {
        var bsToast = new bootstrap.Toast(toast, { delay: 5000 });
        bsToast.show();
    });
}

function initBackToTop() {
    var btn = document.createElement('button');
    btn.innerHTML = '<i class="fas fa-arrow-up"></i>';
    btn.className = 'back-to-top';
    btn.style.cssText = 'position:fixed;bottom:30px;right:30px;width:45px;height:45px;border-radius:50%;background:var(--unefa-primary);color:#fff;border:none;font-size:1.2rem;cursor:pointer;box-shadow:0 4px 15px rgba(0,0,0,0.2);display:none;z-index:999;transition:all 0.3s ease;';
    document.body.appendChild(btn);

    window.addEventListener('scroll', function() {
        btn.style.display = window.scrollY > 300 ? 'block' : 'none';
    });

    btn.addEventListener('click', function() {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}

function showToast(message, type) {
    type = type || 'info';
    var colors = { info: '#17a2b8', success: '#28a745', warning: '#ffc107', error: '#dc3545' };
    var toast = document.createElement('div');
    toast.className = 'toast-show';
    toast.style.cssText = 'position:fixed;top:20px;right:20px;background:' + (colors[type] || colors.info) + ';color:#fff;padding:12px 24px;border-radius:8px;z-index:9999;font-weight:500;box-shadow:0 4px 15px rgba(0,0,0,0.2);max-width:400px;';
    toast.innerHTML = '<i class="fas fa-' + (type === 'success' ? 'check-circle' : type === 'error' ? 'times-circle' : type === 'warning' ? 'exclamation-triangle' : 'info-circle') + '"></i> ' + message;
    document.body.appendChild(toast);
    setTimeout(function() {
        toast.className = 'toast-hide';
        setTimeout(function() { toast.remove(); }, 300);
    }, 4000);
}

function formatDate(dateStr) {
    if (!dateStr) return '-';
    var d = new Date(dateStr);
    return d.toLocaleDateString('es-ES', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' });
}

function getCSRFToken() {
    var name = 'csrftoken';
    var value = '; ' + document.cookie;
    var parts = value.split('; ' + name + '=');
    if (parts.length === 2) return parts.pop().split(';').shift();
    return document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
}
