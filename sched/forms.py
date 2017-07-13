import sys
sys.path.append('/Users/johntran/Documents/virtualenv/scheduler/lib/python2.7/site-packages')

from wtforms import (Form, BooleanField, DateTimeField, TextAreaField, 
    TextField, PasswordField)
from wtforms.validators import Length, required

class AppointmentForm(Form):
    title = TextField('Title', [Length(max=26), required()])
    start = DateTimeField('Start', [required()])
    end = DateTimeField('End')
    allday = BooleanField('All Day')
    location = TextField('Location', [Length(max=26)])
    description = TextAreaField('Description', [Length(max=26)])

class LoginForm(Form):
    '''Render HTML input for user login form. Authentication (i.e. password 
    verification) happens in the view function.'''
    username = TextField('Username', [required()])
    password = PasswordField('Password', [required()])

if __name__ == '__main__':
    # Demonstration of a WTForms form by itself
    form = AppointmentForm()
    print('Here is how a form field displays:')
    print(form.title.label)
    print(form.title)

    from werkzeug.datastructures import ImmutableMultiDict as multidict
    data = multidict([('title', 'Hello, form!'), ('start', '2017-04-23 23:45:03.9')])
    form = AppointmentForm(data)
    print('Here is our validation...')
    print('Does it validate: {}'.format(form.validate()))
    print('There is an error attached to the field...')
    print('form.start.errors: {}'.format(form.start.errors))

