"""
Forms for Food Rescue App
"""
from flask_wtf import FlaskForm
from wtforms import (
    StringField, 
    PasswordField, 
    SubmitField, 
    SelectField, 
    IntegerField, 
    DateField,
    TextAreaField,
    BooleanField
)
from wtforms.validators import (
    DataRequired, 
    Email, 
    Length, 
    EqualTo, 
    Optional,
    ValidationError,
    NumberRange
)
from datetime import datetime

class RegisterForm(FlaskForm):
    """Registration form for new users"""
    
    role = SelectField(
        'I am a',
        choices=[('company', 'Food Company/Store'), ('volunteer', 'Volunteer')],
        validators=[DataRequired()]
    )
    
    # Personal information
    name = StringField(
        'First Name',
        validators=[DataRequired(), Length(min=2, max=100)]
    )
    
    surname = StringField(
        'Last Name',
        validators=[Optional(), Length(max=100)]
    )
    
    email = StringField(
        'Email',
        validators=[DataRequired(), Email(), Length(max=120)]
    )
    
    phone = StringField(
        'Phone Number',
        validators=[Optional(), Length(max=20)]
    )
    
    # Company-specific fields
    company_name = StringField(
        'Company Name',
        validators=[Optional(), Length(max=150)]
    )
    
    registration_number = StringField(
        'Registration Number',
        validators=[Optional(), Length(max=50)]
    )
    
    # Password
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=8, message='Password must be at least 8 characters long')
        ]
    )
    
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match')
        ]
    )
    
    submit = SubmitField('Create Account')
    
    def validate_company_name(self, field):
        """Validate that company name is provided for company role"""
        if self.role.data == 'company' and not field.data:
            raise ValidationError('Company name is required for companies')
    
    def validate_registration_number(self, field):
        """Validate that registration number is provided for company role"""
        if self.role.data == 'company' and not field.data:
            raise ValidationError('Registration number is required for companies')


class LoginForm(FlaskForm):
    """Login form"""
    
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()]
    )
    
    password = PasswordField(
        'Password',
        validators=[DataRequired()]
    )
    
    remember_me = BooleanField('Remember Me')
    
    submit = SubmitField('Login')


class DonationForm(FlaskForm):
    """Form for adding donations"""
    
    CATEGORIES = [
        ('', 'Select a category'),
        ('dairy', 'Dairy Products'),
        ('vegetables', 'Vegetables'),
        ('fruits', 'Fruits'),
        ('bakery', 'Bakery Items'),
        ('meat', 'Meat & Poultry'),
        ('seafood', 'Seafood'),
        ('grains', 'Grains & Cereals'),
        ('canned', 'Canned Goods'),
        ('frozen', 'Frozen Foods'),
        ('beverages', 'Beverages'),
        ('snacks', 'Snacks'),
        ('other', 'Other')
    ]
    
    item_name = StringField(
        'Item Name',
        validators=[DataRequired(), Length(min=2, max=100)],
        render_kw={'placeholder': 'e.g., Fresh Tomatoes'}
    )
    
    category = SelectField(
        'Category',
        choices=CATEGORIES,
        validators=[DataRequired()]
    )
    
    description = TextAreaField(
        'Description',
        validators=[Optional(), Length(max=500)],
        render_kw={
            'placeholder': 'Additional details about the item (optional)',
            'rows': 3
        }
    )
    
    expiry_date = DateField(
        'Expiry Date',
        validators=[DataRequired()],
        format='%Y-%m-%d'
    )
    
    quantity = IntegerField(
        'Quantity',
        validators=[
            DataRequired(),
            NumberRange(min=1, max=10000, message='Quantity must be between 1 and 10000')
        ],
        render_kw={'placeholder': 'Number of items'}
    )
    
    submit = SubmitField('Add Donation')
    
    def validate_expiry_date(self, field):
        """Validate that expiry date is in the future"""
        if field.data < datetime.now().date():
            raise ValidationError('Expiry date must be in the future')


class UpdateProfileForm(FlaskForm):
    """Form for updating user profile"""
    
    name = StringField(
        'First Name',
        validators=[DataRequired(), Length(min=2, max=100)]
    )
    
    surname = StringField(
        'Last Name',
        validators=[Optional(), Length(max=100)]
    )
    
    email = StringField(
        'Email',
        validators=[DataRequired(), Email(), Length(max=120)]
    )
    
    phone = StringField(
        'Phone Number',
        validators=[Optional(), Length(max=20)]
    )
    
    company_name = StringField(
        'Company Name',
        validators=[Optional(), Length(max=150)]
    )
    
    address = StringField(
        'Address',
        validators=[Optional(), Length(max=255)]
    )
    
    submit = SubmitField('Update Profile')


class ChangePasswordForm(FlaskForm):
    """Form for changing password"""
    
    current_password = PasswordField(
        'Current Password',
        validators=[DataRequired()]
    )
    
    new_password = PasswordField(
        'New Password',
        validators=[
            DataRequired(),
            Length(min=8, message='Password must be at least 8 characters long')
        ]
    )
    
    confirm_password = PasswordField(
        'Confirm New Password',
        validators=[
            DataRequired(),
            EqualTo('new_password', message='Passwords must match')
        ]
    )
    
    submit = SubmitField('Change Password')