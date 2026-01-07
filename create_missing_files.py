"""
Generate Missing Files Script
This will create all the missing files in your project
"""
import os

def create_missing_files():
    print("=" * 60)
    print("CREATING MISSING FILES")
    print("=" * 60)
    print()
    
    # Create static folders
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    print("✅ Created static folders")
    
    # Create about.html
    about_html = '''{% extends 'base.html' %}

{% block title %}About Us{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-lg-10">
        <div class="text-center mb-5">
            <h1 class="display-4 text-success fw-bold mb-3">
                <i class="bi bi-basket3-fill"></i> About Food Rescue
            </h1>
            <p class="lead text-muted">Our mission to reduce food waste and support communities</p>
        </div>

        <div class="card shadow-sm mb-4">
            <div class="card-body p-5">
                <h2 class="text-success mb-4">Our Mission</h2>
                <p class="lead">
                    Food Rescue connects food companies and stores with volunteers to redistribute 
                    surplus food that would otherwise go to waste.
                </p>
            </div>
        </div>

        <div class="card shadow-sm border-success">
            <div class="card-body p-5 text-center">
                <h3 class="text-success mb-3">Join the Movement</h3>
                <p class="mb-4">Whether you're a business with surplus food or a volunteer ready to help, we need you!</p>
                {% if not current_user.is_authenticated %}
                <a href="{{ url_for('register') }}" class="btn btn-success btn-lg px-5">
                    <i class="bi bi-person-plus"></i> Get Started Today
                </a>
                {% endif %}
            </div>
        </div>
    </div>
</div>
{% endblock %}
'''
    
    with open('templates/about.html', 'w', encoding='utf-8') as f:
        f.write(about_html)
    print("✅ Created templates/about.html")
    
    # Create 404.html
    error_404 = '''{% extends 'base.html' %}

{% block title %}Page Not Found{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6 text-center">
        <div class="py-5">
            <i class="bi bi-exclamation-triangle text-warning" style="font-size: 6rem;"></i>
            <h1 class="display-1 fw-bold text-muted mt-4">404</h1>
            <h2 class="mb-3">Page Not Found</h2>
            <p class="lead text-muted mb-4">
                Oops! The page you're looking for doesn't exist.
            </p>
            <a href="{{ url_for('index') }}" class="btn btn-success btn-lg">
                <i class="bi bi-house"></i> Go Home
            </a>
        </div>
    </div>
</div>
{% endblock %}
'''
    
    with open('templates/404.html', 'w', encoding='utf-8') as f:
        f.write(error_404)
    print("✅ Created templates/404.html")
    
    # Create 500.html
    error_500 = '''{% extends 'base.html' %}

{% block title %}Server Error{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6 text-center">
        <div class="py-5">
            <i class="bi bi-exclamation-octagon text-danger" style="font-size: 6rem;"></i>
            <h1 class="display-1 fw-bold text-muted mt-4">500</h1>
            <h2 class="mb-3">Internal Server Error</h2>
            <p class="lead text-muted mb-4">
                Something went wrong. We're working to fix it!
            </p>
            <a href="{{ url_for('index') }}" class="btn btn-success btn-lg">
                <i class="bi bi-house"></i> Go Home
            </a>
        </div>
    </div>
</div>
{% endblock %}
'''
    
    with open('templates/500.html', 'w', encoding='utf-8') as f:
        f.write(error_500)
    print("✅ Created templates/500.html")
    
    # Create style.css
    style_css = '''/* Food Rescue App - Custom Styles */

:root {
    --primary-green: #198754;
    --light-green: #d4edda;
    --dark-green: #146c43;
}

body {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

main {
    flex: 1;
}

.navbar-brand {
    font-size: 1.5rem;
}

.card {
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    border-radius: 10px;
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 .5rem 1rem rgba(0, 0, 0, .15) !important;
}

.btn-success {
    background-color: var(--primary-green);
    border-color: var(--primary-green);
}

.btn-success:hover {
    background-color: var(--dark-green);
    border-color: var(--dark-green);
    transform: translateY(-2px);
}

.form-control:focus {
    border-color: var(--primary-green);
    box-shadow: 0 0 0 0.2rem rgba(25, 135, 84, 0.25);
}

#map {
    border-radius: 10px;
    z-index: 1;
}

footer {
    margin-top: auto;
}
'''
    
    with open('static/css/style.css', 'w', encoding='utf-8') as f:
        f.write(style_css)
    print("✅ Created static/css/style.css")
    
    # Create scripts.js
    scripts_js = '''// Food Rescue App - JavaScript

// Auto-dismiss alerts after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert:not(.alert-warning)');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
});

// Confirm before deleting
function confirmDelete(message) {
    return confirm(message || 'Are you sure you want to delete this item?');
}

// Initialize tooltips
function initTooltips() {
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
}

document.addEventListener('DOMContentLoaded', initTooltips);
'''
    
    with open('static/js/scripts.js', 'w', encoding='utf-8') as f:
        f.write(scripts_js)
    print("✅ Created static/js/scripts.js")
    
    print()
    print("=" * 60)
    print("✅ ALL MISSING FILES CREATED!")
    print("=" * 60)
    print()
    print("Now run: python app.py")
    print("Your app should work perfectly!")

if __name__ == '__main__':
    create_missing_files()
    input("\nPress Enter to exit...")