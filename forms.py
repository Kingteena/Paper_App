from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, RadioField, IntegerField, FormField
from wtforms.validators import DataRequired, InputRequired
from flask_wtf.file import FileField, FileRequired


class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Sign Me Up!")


class AnswerSheet(FlaskForm):
    answer = RadioField("answer",
                        choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')],
                        validators=[DataRequired(), InputRequired()])
    submit = SubmitField(label="Check Answer")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Let Me In!")


class NewPaperForm(FlaskForm):
    subject_code = StringField("Subject code", validators=[DataRequired()])
    session_code = StringField("Session eg:s19 for May/June 2019", validators=[DataRequired()])
    paper_code = StringField("Paper code", validators=[DataRequired()])
    qp = FileField('Question Paper PDF', validators=[FileRequired()])
    ms = FileField('Marking Scheme PDF', validators=[FileRequired()])
    paper_type = RadioField('Which type of paper is this? ', choices=[('mcq', 'MCQ'), ('nmcq', 'Non-MCQ')])
    submit = SubmitField("Lets make their lives miserable!")


class NewQuestionForm(FlaskForm):
    start = IntegerField('Start Y Coordinate' )
    end = IntegerField('End Y Coordinate')
    page = IntegerField('Page')
    chapter = IntegerField('Chapter Number')


class NewQPForm(FlaskForm):
    q1 = FormField(NewQuestionForm)
    q2 = FormField(NewQuestionForm)
    q3 = FormField(NewQuestionForm)
    q4 = FormField(NewQuestionForm)
    q5 = FormField(NewQuestionForm)
    q6 = FormField(NewQuestionForm)
    q7 = FormField(NewQuestionForm)
    q8 = FormField(NewQuestionForm)
    q9 = FormField(NewQuestionForm)
    q10 = FormField(NewQuestionForm)
    q11 = FormField(NewQuestionForm)
    q12 = FormField(NewQuestionForm)
    q13 = FormField(NewQuestionForm)
    q14 = FormField(NewQuestionForm)
    q15 = FormField(NewQuestionForm)
    q16 = FormField(NewQuestionForm)
    q17 = FormField(NewQuestionForm)
    q18 = FormField(NewQuestionForm)
    q19 = FormField(NewQuestionForm)
    q20 = FormField(NewQuestionForm)
    q21 = FormField(NewQuestionForm)
    q22 = FormField(NewQuestionForm)
    q23 = FormField(NewQuestionForm)
    q24 = FormField(NewQuestionForm)
    q25 = FormField(NewQuestionForm)
    q26 = FormField(NewQuestionForm)
    q27 = FormField(NewQuestionForm)
    q28 = FormField(NewQuestionForm)
    q29 = FormField(NewQuestionForm)
    q30 = FormField(NewQuestionForm)
    q31 = FormField(NewQuestionForm)
    q32 = FormField(NewQuestionForm)
    q33 = FormField(NewQuestionForm)
    q34 = FormField(NewQuestionForm)
    q35 = FormField(NewQuestionForm)
    q36 = FormField(NewQuestionForm)
    q37 = FormField(NewQuestionForm)
    q38 = FormField(NewQuestionForm)
    q39 = FormField(NewQuestionForm)
    q40 = FormField(NewQuestionForm)
    submit = SubmitField("Blood for the Blood God!")




