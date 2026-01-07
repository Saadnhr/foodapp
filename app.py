"""
Food Rescue App - Main Application
Connects food companies with volunteers to reduce food waste
"""
from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
from math import radians, cos, sin, asin, sqrt

from config import Config
from models import db, User, Donation
from forms import RegisterForm, LoginForm, DonationForm

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'warning'

@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login"""
    return User.query.get(int(user_id))

# Initialize database
with app.app_context():
    os.makedirs(os.path.join(app.root_path, 'database'), exist_ok=True)
    db.create_all()

def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate distance between two points using Haversine formula
    Returns distance in kilometers
    """
    if None in (lat1, lon1, lat2, lon2):
        return None
    
    # Convert to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    
    # Radius of earth in kilometers
    r = 6371
    return c * r

@app.route('/')
def index():
    """Home page"""
    stats = {
        'total_donations': Donation.query.count(),
        'available_donations': Donation.query.filter_by(status='available').count(),
        'companies': User.query.filter_by(role='company').count(),
        'volunteers': User.query.filter_by(role='volunteer').count()
    }
    return render_template('index.html', stats=stats)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        # Check if email already exists
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already registered. Please login instead.', 'danger')
            return redirect(url_for('login'))
        
        hashed_pw = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        user = User(
            role=form.role.data,
            name=form.name.data,
            surname=form.surname.data,
            company_name=form.company_name.data if form.role.data == 'company' else None,
            registration_number=form.registration_number.data if form.role.data == 'company' else None,
            email=form.email.data.lower(),
            phone=form.phone.data,
            password_hash=hashed_pw
        )
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred. Please try again.', 'danger')
            app.logger.error(f"Registration error: {str(e)}")
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        if current_user.role == 'company':
            return redirect(url_for('dashboard_company'))
        return redirect(url_for('dashboard_volunteer'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash(f'Welcome back, {user.name}!', 'success')
            
            # Redirect to next page or dashboard
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            
            if user.role == 'company':
                return redirect(url_for('dashboard_company'))
            return redirect(url_for('dashboard_volunteer'))
        
        flash('Invalid email or password.', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard/company')
@login_required
def dashboard_company():
    """Company dashboard - view and manage donations"""
    if current_user.role != 'company':
        flash('Access denied. Companies only.', 'danger')
        return redirect(url_for('dashboard_volunteer'))
    
    # Get company's donations with statistics
    donations = Donation.query.filter_by(company_id=current_user.id).order_by(
        Donation.created_at.desc()
    ).all()
    
    stats = {
        'total': len(donations),
        'available': len([d for d in donations if d.status == 'available']),
        'claimed': len([d for d in donations if d.status == 'claimed']),
        'completed': len([d for d in donations if d.status == 'completed'])
    }
    
    return render_template('dashboard_company.html', donations=donations, stats=stats)

@app.route('/dashboard/volunteer')
@login_required
def dashboard_volunteer():
    """Volunteer dashboard - view available donations with distance"""
    if current_user.role != 'volunteer':
        flash('Access denied. Volunteers only.', 'danger')
        return redirect(url_for('dashboard_company'))
    
    # Get available donations
    donations = Donation.query.filter_by(status='available').order_by(
        Donation.created_at.desc()
    ).all()
    
    # Calculate distances if volunteer has location
    if current_user.latitude and current_user.longitude:
        for donation in donations:
            if donation.latitude and donation.longitude:
                donation.distance = calculate_distance(
                    current_user.latitude,
                    current_user.longitude,
                    donation.latitude,
                    donation.longitude
                )
        # Sort by distance
        donations = sorted(donations, key=lambda x: x.distance if hasattr(x, 'distance') and x.distance else float('inf'))
    
    # Get volunteer's claimed donations
    my_claims = Donation.query.filter_by(
        volunteer_id=current_user.id
    ).order_by(Donation.created_at.desc()).all()
    
    return render_template('dashboard_volunteer.html', 
                          donations=donations, 
                          my_claims=my_claims)

@app.route('/donation/add', methods=['GET', 'POST'])
@login_required
def add_donation():
    """Add a new donation (companies only)"""
    if current_user.role != 'company':
        flash('Only companies can add donations.', 'danger')
        return redirect(url_for('dashboard_volunteer'))
    
    # Check if company has set location
    if not current_user.latitude or not current_user.longitude:
        flash('Please set your location first to add donations.', 'warning')
    
    form = DonationForm()
    if form.validate_on_submit():
        # Validate expiry date is in the future
        if form.expiry_date.data < datetime.now().date():
            flash('Expiry date must be in the future.', 'danger')
            return render_template('add_donation.html', form=form)
        
        donation = Donation(
            item_name=form.item_name.data,
            description=form.description.data,
            category=form.category.data,
            expiry_date=form.expiry_date.data,
            quantity=form.quantity.data,
            company_id=current_user.id,
            latitude=current_user.latitude,
            longitude=current_user.longitude
        )
        
        try:
            db.session.add(donation)
            db.session.commit()
            flash('Donation added successfully!', 'success')
            return redirect(url_for('dashboard_company'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred. Please try again.', 'danger')
            app.logger.error(f"Add donation error: {str(e)}")
    
    return render_template('add_donation.html', form=form)

@app.route('/donation/<int:donation_id>/claim', methods=['POST'])
@login_required
def claim_donation(donation_id):
    """Claim a donation (volunteers only)"""
    if current_user.role != 'volunteer':
        return jsonify({'error': 'Only volunteers can claim donations'}), 403
    
    donation = Donation.query.get_or_404(donation_id)
    
    if donation.status != 'available':
        return jsonify({'error': 'This donation is no longer available'}), 400
    
    donation.status = 'claimed'
    donation.volunteer_id = current_user.id
    donation.claimed_at = datetime.utcnow()
    
    try:
        db.session.commit()
        flash('Donation claimed successfully! Please pick it up before expiry.', 'success')
        return jsonify({'success': True, 'message': 'Donation claimed!'})
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Claim donation error: {str(e)}")
        return jsonify({'error': 'An error occurred'}), 500

@app.route('/donation/<int:donation_id>/complete', methods=['POST'])
@login_required
def complete_donation(donation_id):
    """Mark donation as completed"""
    donation = Donation.query.get_or_404(donation_id)
    
    # Check permissions
    if current_user.role == 'volunteer' and donation.volunteer_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    if current_user.role == 'company' and donation.company_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    donation.status = 'completed'
    donation.completed_at = datetime.utcnow()
    
    try:
        db.session.commit()
        flash('Donation marked as completed!', 'success')
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Complete donation error: {str(e)}")
        return jsonify({'error': 'An error occurred'}), 500

@app.route('/donation/<int:donation_id>/delete', methods=['POST'])
@login_required
def delete_donation(donation_id):
    """Delete a donation (company only, only if not claimed)"""
    donation = Donation.query.get_or_404(donation_id)
    
    if current_user.role != 'company' or donation.company_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    if donation.status == 'claimed':
        return jsonify({'error': 'Cannot delete claimed donation'}), 400
    
    try:
        db.session.delete(donation)
        db.session.commit()
        flash('Donation deleted successfully.', 'success')
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Delete donation error: {str(e)}")
        return jsonify({'error': 'An error occurred'}), 500

@app.route('/user/location', methods=['POST'])
@login_required
def set_location():
    """Save user's location"""
    data = request.get_json()
    
    if not data or 'lat' not in data or 'lng' not in data:
        return jsonify({'error': 'Invalid data'}), 400
    
    try:
        current_user.latitude = float(data['lat'])
        current_user.longitude = float(data['lng'])
        db.session.commit()
        return jsonify({'success': True, 'message': 'Location saved!'})
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Set location error: {str(e)}")
        return jsonify({'error': 'Failed to save location'}), 500

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    db.session.rollback()
    return render_template('500.html'), 500

# Context processors
@app.context_processor
def utility_processor():
    """Add utility functions to templates"""
    def format_date(date):
        if date:
            return date.strftime('%Y-%m-%d')
        return ''
    
    def days_until_expiry(expiry_date):
        if expiry_date:
            delta = expiry_date - datetime.now().date()
            return delta.days
        return None
    
    return dict(format_date=format_date, days_until_expiry=days_until_expiry)

if __name__ == '__main__':
    app.run(debug=True)