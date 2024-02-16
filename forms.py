from wtforms import (Form, StringField, RadioField, SelectField, TextAreaField,
                     validators, TelField, PasswordField, IntegerField)
from wtforms.fields import EmailField, DateField, SearchField
from datetime import datetime


class CreateLoginForm(Form):
    email = EmailField('Email:', [validators.Email(), validators.Length(min=1, max=150), validators.DataRequired()])
    password = PasswordField('Password:', [validators.Length(min=1, max=150), validators.DataRequired()])


class CreateMemberForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    birthdate = DateField('Birthdate', format='%Y-%m-%d', validators=[validators.DataRequired()])
    gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')],
                         validators=[validators.DataRequired()])
    email = EmailField('Email', [validators.Email(), validators.Length(min=1, max=150), validators.DataRequired()])
    phone = StringField('Phone Number', [validators.DataRequired()])
    password = PasswordField('Enter password',
                             [validators.DataRequired(), validators.Length(min=8, message='Too Short'),
                              validators.Regexp('^(?=.*[A-Z])(?=.*[0-9])',
                                                message='Password must contain at least one capital letter and one '
                                                        'number')])
    confirm = PasswordField('Confirm password:', [validators.DataRequired(),
                                                  validators.EqualTo('password', 'password does not match')])


class CreateProductForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    price = StringField('Price ($)', [validators.Length(min=1, max=10), validators.DataRequired()])
    category = SelectField('Category', [validators.Length(min=1, max=150), validators.DataRequired()],
                           choices=[('Basic', 'Basic'), ('Emo', 'Emo'), ('Grunge', 'Grunge'), ('Preppy', 'Preppy')],
                           default='')
    remarks = StringField('Remarks', [validators.Length(min=1, max=150), validators.Optional()])
    drinks = StringField('Drinks', [validators.Length(min=1, max=150), validators.DataRequired()])


class CreateQuestionForm(Form):  # inherit from Form
    title = StringField('Title', [validators.Length(min=1, max=150), validators.DataRequired()], )
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    date_posted = DateField('Date Posted', format='%Y-%m-%d')
    question = TextAreaField('Question(s) (if any)', [validators.Optional()])
    overall = RadioField('Overall Experience', choices=[('B', 'Bad 😡'), ('N', 'Neutral 😐'), ('E', 'Excellent 😁')],
                         default='N')
    feedback = TextAreaField('Feedback (if any)', [validators.Optional()])


class CreateReplyForm(Form):
    reply = TextAreaField('Reply from Admin', [validators.Optional()])


class CreateNewsForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=150), validators.DataRequired()])
    description = TextAreaField('Description of News', [validators.DataRequired()])

class CreateCommentForm(Form):
    comment = TextAreaField('Comment', [validators.DataRequired()])

class CreateCardForm(Form):
    name = StringField('Customer Name', [validators.length(min=1, max=100), validators.DataRequired("message")])
    address = StringField('Address', [validators.Length(min=1, max=100), validators.DataRequired("message")])
    postalcode = StringField('Postal Code', [validators.length(min=6, max=6), validators.DataRequired("message"), validators.Regexp('^\d+$', message='Postal must only contain digits')])
    card = StringField('Card Number', [validators.Length(min=16, max=16, message='Card number must be 16 digits'),
                                       validators.Regexp('^\d+$', message='Card number must only contain digits'),
                                       validators.DataRequired(message='Card number is required')])

    expdate = StringField('Expiry Date (MM/YY)',
                          [validators.Length(min=5, max=5, message='Expiry date must be in MM/YY format'),
                           validators.Regexp('^\d{2}/\d{2}$', message='Expiry date must be in MM/YY format'),
                           validators.DataRequired(message='Expiry date is required')])

    CVV = StringField('Security Code (CVV)', [validators.Length(min=3, max=3, message='Security code must be 3 digits'),
                                              validators.Regexp('^\d+$',
                                                                message='Security code must only contain digits'),
                                              validators.DataRequired(message='Security code is required')])

    def validate_expdate(form, field):
        try:
            # Split the expiry date into month and year components
            parts = field.data.split('/')


            # Ensure there are exactly two parts (month and year)
            if len(parts) != 2:
                raise ValueError('Invalid expiry date format. Must be in MM/YY format')

            # Convert month and year to integers
            month = int(parts[0])

            year = int("20" + parts[1])

            # Check if month is between 1 and 12 (valid month range)
            if not 1 <= month <= 12:
                raise ValueError('Invalid month')


            # Get the current date
            current_date = datetime.now()

            # Create a datetime object for the expiry date
            exp_date = datetime(year, month, 1)
            print(exp_date)
            print(current_date)
            # Check if expiry date is in the past
            if exp_date < current_date:
                raise ValueError('Expiry date cannot be in the past')
        except (ValueError, AttributeError):
            raise validators.ValidationError('Invalid expiry date format. Must be in MM/YY format')


class CreateAddressForm(Form):
    address = StringField('Address', [validators.Length(min=1, max=100), validators.DataRequired("message")])
    postalcode = StringField('Postal Code', [validators.length(min=6, max=6), validators.DataRequired("message"), validators.Regexp('^\d+$', message='Postal must only contain digits')])

class CreateAdminForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = EmailField('email', [validators.Email(), validators.Length(min=1, max=150), validators.DataRequired()])
    password = PasswordField('Enter password',
                             [validators.DataRequired(), validators.Length(min=8, message='Too Short'),
                              validators.Regexp('^(?=.*[A-Z])(?=.*[0-9])',
                                                message='Password must contain at least one capital letter and one '
                                                        'number')])
    confirm = PasswordField('Confirm password:', [validators.DataRequired(),
                                                  validators.EqualTo('password', 'password does not match')])


class CreateVoucherForm(Form):
    voucher_id = StringField('ID code',
                             [validators.length(min=1, max=10),
                              validators.Regexp('^[a-zA-Z0-9_-]+$',
                                                message='Invalid characters in ID code, you can only use \"_\" and \"-\"'),
                              validators.DataRequired()])
    name = StringField('Voucher name', [validators.length(min=1, max=150), validators.DataRequired()])
    discount = StringField('Discount (%)',
                           [validators.length(min=1, max=3),
                            validators.Regexp('^[1-9]\d?$|^100$', message='Discount can only be from 1 to 100'),
                            validators.DataRequired()])


class VoucherForm(Form):
    voucher_id = StringField('Voucher Code', [validators.Length(min=1, max=10), validators.DataRequired()])
    email = EmailField('Recipient Email', [validators.Email(), validators.DataRequired()])


class CreateSearchForm(Form):
    search = SearchField('Search here:', [validators.Length(min=1, max=150), validators.DataRequired()])


class CreateSupplierForm(Form):
    company_name = StringField('Company name:', [validators.Length(min=1, max=150), validators.DataRequired()])
    company_email = EmailField('Company email:', [validators.Length(min=1, max=150), validators.DataRequired()])
    company_phone = StringField('Company phone:', [validators.Length(min=1, max=150), validators.DataRequired()])
    company_address = StringField('Company address:', [validators.Length(min=1, max=150), validators.DataRequired()])
    password = PasswordField('Enter password',
                             [validators.DataRequired(), validators.Length(min=8, message='Too Short'),
                              validators.Regexp('^(?=.*[A-Z])(?=.*[0-9])',
                                                message='Password must contain at least one capital letter and one '
                                                        'number')])
    confirm = PasswordField('Confirm password:', [validators.DataRequired(),
                                                  validators.EqualTo('password', 'password does not match')])


class CreateForgetPassword(Form):
    email = EmailField('Your email:',
                       [validators.Email(), validators.Length(min=1, max=150), validators.DataRequired()])


class VerifyOTPForm(Form):
    otp = StringField('OTP', [validators.Length(min=6, max=6), validators.DataRequired()])


class ResetPasswordForm(Form):
    new_password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.Length(min=8, message='Password must be at least 8 characters long'),
                              validators.Regexp('^(?=.*[A-Z])(?=.*[0-9])',
                                                message='Password must contain at least one capital letter and one '
                                                        'number')
    ])
    confirm_password = PasswordField('Confirm Password', [
        validators.DataRequired(),
        validators.EqualTo('new_password', message='Passwords must match')
    ])

