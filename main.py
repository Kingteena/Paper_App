from flask import Flask, render_template
from wtforms import SubmitField, RadioField
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from wtforms.validators import DataRequired, InputRequired


class AnswerSheet(FlaskForm):
    answer = RadioField("answer",
                        choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')],)
    submit = SubmitField(label="Check Answer")


app = Flask(__name__)
Bootstrap(app)
app.secret_key = "ailsdhgkuasgiuasguasguoasgu"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Questions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(250), nullable=False)
    year = db.Column(db.String(250), nullable=False)
    chapter = db.Column(db.String(250), nullable=False)
    answer = db.Column(db.String(250), nullable=False)

@app.route("/")
def home():
    return render_template("index.html")


@app.route('/<int:question_id>', methods=['GET', 'POST'])
def question(question_id):
    answer_sheet = AnswerSheet()
    question = Question.query.filter_by(id=question_id).first()
    if answer_sheet.validate_on_submit():
        print(answer_sheet.answer.data)
        return render_template("answer_question.html", form=answer_sheet, question=question, user_answer=answer_sheet.answer.data, section="answer")
    return render_template("answer_question.html", form=answer_sheet, question=question)


if __name__ == "__main__":
    app.run(debug=True)
