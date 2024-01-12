from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators, EmailField, DateField


class CreateQuestionForm(Form):  # inherit from Form
    title = StringField('Title',[validators.Length(min=1, max=150), validators.DataRequired()])
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    date_posted = DateField('Date Posted', format='%Y-%m-%d')
    question = TextAreaField('Question(s)', [validators.DataRequired()])

