from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from config import Config
from models import db, User, Donation
from forms import RegisterForm, LoginForm, DonationForm
import os

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Initialize database (run once)
with app.app_context():
    os.makedirs(os.path.join(app.root_path, 'database'), exist_ok=True)
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data)
        user = User(
            role=form.role.data,
            name=form.name.data,
            surname=form.surname.data,
            company_name=form.company_name.data,
            registration_number=form.registration_number.data,
            email=form.email.data,
            phone=form.phone.data,
            password_hash=hashed_pw
        )
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash('Welcome back!', 'success')
            if user.role == 'company':
                return redirect(url_for('dashboard_company'))
            else:
                return redirect(url_for('dashboard_volunteer'))
        flash('Invalid credentials.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You are now logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard_company')
@login_required
def dashboard_company():
    if current_user.role != 'company':
        return redirect(url_for('dashboard_volunteer'))
    donations = Donation.query.filter_by(company_id=current_user.id).all()
    return render_template('dashboard_company.html', donations=donations)

@app.route('/dashboard_volunteer')
@login_required
def dashboard_volunteer():
    if current_user.role != 'volunteer':
        return redirect(url_for('dashboard_company'))
    donations = Donation.query.filter_by(status='available').all()
    return render_template('dashboard_volunteer.html', donations=donations)

@app.route('/add_donation', methods=['GET', 'POST'])
@login_required
def add_donation():
    if current_user.role != 'company':
        return redirect(url_for('dashboard_volunteer'))
    form = DonationForm()
    if form.validate_on_submit():
        donation = Donation(
            item_name=form.item_name.data,
            expiry_date=form.expiry_date.data,
            quantity=form.quantity.data,
            company_id=current_user.id,
            latitude=current_user.latitude,
            longitude=current_user.longitude
        )
        db.session.add(donation)
        db.session.commit()
        flash('Donation added successfully!', 'success')
        return redirect(url_for('dashboard_company'))
    return render_template('add_donation.html', form=form)

@app.route('/set_location', methods=['POST'])
@login_required
def set_location():
    data = request.get_json()
    if data:
        current_user.latitude = data['lat']
        current_user.longitude = data['lng']
        db.session.commit()
        return {'message': 'Location saved!'}
    return {'error': 'Invalid data'}, 400

if __name__ == '__main__':
    app.run(debug=True)
