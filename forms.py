from wtforms import (Form, StringField, RadioField, SelectField, TextAreaField,
                     validators, TelField, PasswordField, IntegerField)
from wtforms.fields import EmailField, DateField, SearchField

# CAN YOU FUCKING WORK PLEASE I FUCKING HATE YOU PLEASE PLEASE PLEASE PLEASE PLEASE PLEASE PLEASE
class CreateLoginForm(Form):
    email = EmailField('Email:', [validators.Length(min=1, max=150), validators.DataRequired()])
    password = PasswordField('Password:', [validators.Length(min=1, max=150), validators.DataRequired()])


class CreateMemberForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = StringField('email', [validators.Length(min=1, max=150), validators.DataRequired()])
    phone = StringField('Phone Number', [validators.DataRequired()])
    password = PasswordField('Enter password', [validators.DataRequired(), validators.Length(min=8, message='Too Short')])
    confirm = PasswordField('Confirm password:', [validators.DataRequired(),
                                                  validators.EqualTo('password', 'password does not match')])


class CreateProductForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    price = StringField('Price ($)', [validators.Length(min=1, max=10), validators.DataRequired()])
    category = SelectField('Category', [validators.Length(min=1, max=150), validators.DataRequired()],
                           choices=[('Basic', 'Basic'), ('Emo', 'Emo'), ('Grunge', 'Grunge'), ('Preppy', 'Preppy')], default='')
    remarks = StringField('Remarks', [validators.Length(min=1, max=150), validators.Optional()])
    drinks = StringField('Drinks', [validators.Length(min=1, max=150), validators.DataRequired()])


class CreateQuestionForm(Form):  # inherit from Form
    title = StringField('Title',[validators.Length(min=1, max=150), validators.DataRequired()], )
    email = EmailField('Email', [validators.Email(), validators.Optional()])
    date_posted = DateField('Date Posted', format='%Y-%m-%d')
    question = TextAreaField('Question(s) (if any)', [validators.DataRequired()])
    overall = RadioField('Overall Experience', choices=[('B', 'Bad 😡'), ('N', 'Neutral 😐'), ('E', 'Excellent 😁')],
                     default='N')
    feedback = TextAreaField('Feedback (if any)', [validators.Optional()])


class CreateCardForm(Form):
    name = StringField('Customer Name', [validators.length(min=1, max=100), validators.DataRequired("message")])
    address = StringField('Address', [validators.Length(min=1, max=100), validators.DataRequired("message")])
    postalcode = StringField('Postal Code', [validators.length(min=6, max=6), validators.DataRequired("message")])
    card = StringField('Card Number', [validators.Length(min=16, max=16, message='Card number must be 16 digits'),
                                validators.Regexp('^\d+$', message='Card number must only contain digits'),
                                validators.DataRequired(message='Card number is required')])

    expdate = StringField('Expiry Date (MM/YY)', [validators.Length(min=5, max=5, message='Expiry date must be in MM/YY format'),
                                      validators.Regexp('^\d{2}/\d{2}$', message='Expiry date must be in MM/YY format'),
                                      validators.DataRequired(message='Expiry date is required')])

    CVV = StringField('Security Code (CVV)', [validators.Length(min=3, max=3, message='Security code must be 3 digits'),
                              validators.Regexp('^\d+$', message='Security code must only contain digits'),
                              validators.DataRequired(message='Security code is required')])


class CreateAdminForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = StringField('email', [validators.Length(min=1, max=150), validators.DataRequired()])
    password = PasswordField('Enter password',
                             [validators.DataRequired(), validators.Length(min=8, message='Too Short')])
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
    email = StringField('Recipient Email', [validators.Email(), validators.DataRequired()])

class CreateSearchForm(Form):
    search = SearchField('Search here by first name', [validators.Length(min=1, max=150), validators.DataRequired()])