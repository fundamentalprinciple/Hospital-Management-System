
from flask_security.forms import RegisterForm
from wtforms import StringField, EmailField, PasswordField
from wtforms.validators import DataRequired, Length, Email, ValidationError, EqualTo

def min_email_length(form, field):
    if field.data and len(field.data) < 8:
        raise ValidationError('Email is too short to be valid.')

class ExtendedRegisterForm(RegisterForm):
    email = EmailField('Email', validators=[DataRequired(), Email(), min_email_length])
    name = StringField('Full name', validators=[DataRequired(), Length(min=2, max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password_confirm = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match.')
    ])

    def validate(self, **kwargs):
        print("DEBUG: ExtendedRegisterForm.validate called")
        rv = super().validate(**kwargs)
        # Ensure password mismatch is always caught
        if self.password.data and self.password_confirm.data:
            print(f"DEBUG: password={self.password.data}, password_confirm={self.password_confirm.data}")
            if self.password.data != self.password_confirm.data:
                self.password_confirm.errors.append('Passwords must match.')
                print("DEBUG: Passwords do not match error added")
                return False
        return rv
