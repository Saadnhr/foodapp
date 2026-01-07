"""
Database models for Food Rescue App
"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    """User model for both companies and volunteers"""
    
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(20), nullable=False)  # 'company' or 'volunteer'
    
    # Personal information
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(20))
    password_hash = db.Column(db.String(200), nullable=False)
    
    # Company-specific fields
    company_name = db.Column(db.String(150))
    registration_number = db.Column(db.String(50))
    
    # Location data
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    address = db.Column(db.String(255))
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    company_donations = db.relationship(
        'Donation',
        backref='company',
        lazy=True,
        foreign_keys='Donation.company_id'
    )
    
    volunteer_donations = db.relationship(
        'Donation',
        backref='volunteer',
        lazy=True,
        foreign_keys='Donation.volunteer_id'
    )
    
    def __repr__(self):
        if self.role == 'company':
            return f'<Company {self.company_name}>'
        return f'<Volunteer {self.name} {self.surname}>'
    
    @property
    def display_name(self):
        """Return appropriate display name based on role"""
        if self.role == 'company':
            return self.company_name or self.name
        return f"{self.name} {self.surname}" if self.surname else self.name
    
    def update_last_login(self):
        """Update last login timestamp"""
        self.last_login = datetime.utcnow()
        db.session.commit()


class Donation(db.Model):
    """Donation model for food items"""
    
    __tablename__ = 'donation'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Item information
    item_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))  # e.g., 'dairy', 'vegetables', 'bakery'
    expiry_date = db.Column(db.Date, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    
    # Status tracking
    status = db.Column(
        db.String(20), 
        default='available'
    )  # 'available', 'claimed', 'completed', 'expired'
    
    # Location (copied from company at creation)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    claimed_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    
    # Foreign keys
    company_id = db.Column(
        db.Integer, 
        db.ForeignKey('user.id'), 
        nullable=False,
        index=True
    )
    volunteer_id = db.Column(
        db.Integer, 
        db.ForeignKey('user.id'), 
        nullable=True
    )
    
    def __repr__(self):
        return f'<Donation {self.item_name} - {self.status}>'
    
    @property
    def is_expired(self):
        """Check if donation has expired"""
        return self.expiry_date < datetime.now().date()
    
    @property
    def days_until_expiry(self):
        """Calculate days until expiry"""
        delta = self.expiry_date - datetime.now().date()
        return delta.days
    
    @property
    def urgency_level(self):
        """Return urgency level based on days until expiry"""
        days = self.days_until_expiry
        if days <= 0:
            return 'expired'
        elif days <= 1:
            return 'critical'
        elif days <= 3:
            return 'high'
        elif days <= 7:
            return 'medium'
        return 'low'
    
    def mark_as_expired(self):
        """Mark donation as expired"""
        if self.is_expired and self.status == 'available':
            self.status = 'expired'
            db.session.commit()