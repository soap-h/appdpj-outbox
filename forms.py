from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators, TelField, PasswordField
from wtforms.fields import EmailField, DateField



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
    # picture =
    drinks = StringField('Drinks', [validators.Length(min=1, max=150), validators.DataRequired()])


class CreateQuestionForm(Form):  # inherit from Form
    title = StringField('Title',[validators.Length(min=1, max=150), validators.DataRequired()])
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    date_posted = DateField('Date Posted', format='%Y-%m-%d')
    question = TextAreaField('Question(s)', [validators.DataRequired()])
