from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField
from wtforms.validators import DataRequired, Regexp, NumberRange


class CasesForm(FlaskForm):

    datestamp = StringField(u'datestamp',
                            validators=[
                                DataRequired(
                                    message="enter date/time in 24hr format MM/DD/YYYY HH:MM")
                            ])

    # NB IntegerField() would not accept 0 as input!!
    # NumberRange is not working the way I expect

    new_cases = StringField(u'new_cases', default="0", validators=[
        DataRequired(message="enter new cases"),
        #        NumberRange(min=0, max=1000, message="'cases' is out of range")
    ])

    total_cases = StringField(u'total_cases', default="0", validators=[
        DataRequired(message="enter total cases"),
        #        NumberRange(min=0, max=10000, message="'cases' is out of range")
    ])

    negative = StringField(u'negative', default="0",  validators=[
        DataRequired(message="enter negative tests"),
        #        NumberRange(min=0, max=100000, message="'negative' is out of range")
    ])

    new_deaths = StringField(u'new_deaths', default="0", validators=[
        DataRequired(message="enter new deaths"),
        #        NumberRange(min=0, max=100, message="'new deaths' is out of range")
    ])

    total_deaths = StringField(u'total_deaths', default="0", validators=[
        DataRequired(message="enter total deaths"),
        #        NumberRange(min=0, max=10000, message="'total deaths' is out of range")
    ])

    submit = SubmitField(u"Submit")


class PPEForm(FlaskForm):

    datestamp = StringField(u'datestamp',
                            validators=[
                                DataRequired(
                                    message="enter date/time in 24hr format MM/DD/YYYY HH:MM")
                            ])

    facility = StringField(u'facility', default="Clatsop", validators=[
        DataRequired(message="enter facility name")
    ])

    # NB IntegerField() would not accept 0 as input!!
    # NumberRange is not working the way I expect

    updated = StringField(u'updated') # Date from HOSCAP

    n95 = StringField(u'n95')
    n95_burn = StringField(u'n95_burn')
    n95_goal = StringField(u'n95_goal')
    n95_complete = StringField(u'n95_complete')

    mask = StringField(u'mask')
    mask_burn = StringField(u'mask_burn')
    mask_goal = StringField(u'mask_goal')
    mask_complete = StringField(u'mask_complete')

    shield = StringField(u'shield')
    shield_burn = StringField(u'shield_burn')
    shield_goal = StringField(u'shield_goal')
    shield_complete = StringField(u'shield_complete')

    glove = StringField(u'glove')
    glove_burn = StringField(u'glove_burn')
    glove_goal = StringField(u'glove_goal')
    glove_complete = StringField(u'glove_complete')

    gown = StringField(u'gown')
    gown_burn = StringField(u'gown_burn')
    gown_goal = StringField(u'gown_goal')
    gown_complete = StringField(u'gown_complete')

    sanitizer = StringField(u'sanitizer')
    sanitizer_burn = StringField(u'sanitizer_burn')
    sanitizer_goal = StringField(u'sanitizer_goal')
    sanitizer_complete = StringField(u'sanitizer_complete')

    goggle = StringField(u'goggle')
    goggle_burn = StringField(u'goggle_burn')
    goggle_goal = StringField(u'goggle_goal')
    goggle_complete = StringField(u'goggle_complete')

    coverall = StringField(u'coverall')
    coverall_burn = StringField(u'coverall_burn')
    coverall_goal = StringField(u'coverall_goal')
    coverall_complete = StringField(u'coverall_complete')

    submit = SubmitField(u"Submit")


# That's all!
