import os
import json
from functools import wraps
from flask import Flask, render_template, redirect, flash, url_for, request, abort
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from forms import RegisterForm, LoginForm, AnswerSheet, NewPaperForm, NewQPForm
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import PDFEditor as pdf_editor

app = Flask(__name__)
Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)

app.secret_key = "ailsdhgkuasgiuasguasguoasgu"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100), unique=True)
    permission_level = db.Column(db.Integer)


class Question(db.Model):
    __tablename__ = "questions"
    question_id = db.Column(db.String(250), primary_key=True)
    session = db.Column(db.String(250), nullable=False)
    chapter = db.Column(db.String(250), nullable=False)
    answer = db.Column(db.String(250), nullable=False)
    is_mcq = db.Column(db.Boolean, nullable=False)


db.create_all()


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_anonymous:
            return abort(403)
        elif current_user.permission_level < 2:
            return abort(403)
        return f(*args, **kwargs)

    return decorated_function


def owner_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_anonymous:
            return abort(403)
        elif current_user.permission_level < 3:
            return abort(403)
        return f(*args, **kwargs)

    return decorated_function


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/questions")
def question_index():
    questions = [question.split('.')[0] for question in os.listdir(f'{app.static_folder}/questions')]
    questions.sort()
    print(questions)
    return render_template("question_index.html", questions=questions)


@app.route('/mcq', methods=['GET', 'POST'])
def mcq():
    question_id = request.args.get('question_id')
    answer_sheet = AnswerSheet()
    question = Question.query.filter_by(question_id=question_id).first()
    if answer_sheet.validate_on_submit():
        return render_template("answer_question.html", form=answer_sheet, question=question,
                               user_answer=answer_sheet.answer.data, current_user=current_user)
    print(question_id, question.question_id, question.session)
    return render_template("answer_question.html", form=answer_sheet, question=question, current_user=current_user)


@app.route("/add-question", methods=["GET", "POST"])
@admin_only
def add_question():
    form = NewPaperForm()
    if form.validate_on_submit():
        paper_type = form.paper_type.data
        qp = form.qp.data
        qp.filename = f"{form.subject_code.data}_{form.session_code.data}_qp_{form.paper_code.data}.pdf"
        qp_filename = secure_filename(qp.filename)
        qp.save(os.path.join(app.static_folder, 'questions_predit', qp_filename))
        ms = form.ms.data

        if paper_type == "mcq":
            answer_dict = pdf_editor.readMarkingScheme(ms)
            with open(
                    f"{app.static_folder}/questions_predit/{form.subject_code.data}_{form.session_code.data}_ms_{form.paper_code.data}.json",
                    "w") as f:
                json.dump(answer_dict, f)
            return redirect(url_for("add_mcq",
                                    subject=form.subject_code.data,
                                    session=form.session_code.data,
                                    paper=form.paper_code.data))
        elif paper_type == "nmcq":
            ms.filename = f"{form.subject_code.data}_{form.session_code.data}_ms_{form.paper_code.data}.pdf"
            ms_filename = secure_filename(ms.filename)
            ms.save(os.path.join(app.static_folder, 'questions_predit', ms_filename))
            return redirect(url_for("add_nmcq",
                                    subject=form.subject_code.data,
                                    session=form.session_code.data,
                                    paper=form.paper_code.data))

    return render_template("add_question.html", form=form)


@app.route("/add-mcq", methods=["GET", "POST"])
@admin_only
def add_mcq():
    form = NewQPForm()
    qp = f"{request.args.get('subject')}_{request.args.get('session')}_qp_{request.args.get('paper')}"
    ms = f"{app.static_folder}/questions_predit/{request.args.get('subject')}_{request.args.get('session')}_ms_{request.args.get('paper')}.json"
    if form.validate_on_submit():
        with open(ms) as f:
            answers = json.load(f)
        questions = [form.q1, form.q2, form.q3, form.q4, form.q5, form.q6, form.q7, form.q8, form.q9, form.q10,
                     form.q11, form.q12, form.q13, form.q14, form.q15, form.q16, form.q17, form.q18, form.q19, form.q20,
                     form.q21, form.q22, form.q23, form.q24, form.q25, form.q26, form.q27, form.q28, form.q29, form.q30,
                     form.q31, form.q32, form.q33, form.q34, form.q35, form.q36, form.q37, form.q38, form.q39, form.q40]
        for i in range(40):
            pdf_editor.cropPage(start=questions[i].start.data,
                                end=questions[i].end.data,
                                page_number=questions[i].page.data,
                                question_number=i + 1,
                                paper_code=qp,
                                static_folder=app.static_folder)
            new_question = Question(
                question_id=f"{qp}_{i}",
                session=qp,
                chapter=questions[i].chapter.data,
                answer=answers[str(i + 1)],
                is_mcq=True
            )
            db.session.add(new_question)

        for f_name in os.listdir(f"{app.static_folder}/questions_predit"):
            if f_name.startswith(qp) and f_name.endswith('.pdf'):
                os.remove(f"{app.static_folder}/questions_predit/{f_name}")
        if os.path.exists(qp):
            os.remove(qp)

        db.session.commit()
        flash("Sucessfully commited new questions")
        return redirect(url_for("question_index"))

    num_pages = pdf_editor.getPages(paper_code=qp, static_folder=app.static_folder)
    return render_template("add_mcq.html", paper_code=qp, static_folder=app.static_folder, num=num_pages, form=form)


# @app.route("/add-mcq", methods=["GET", "POST"])
# @admin_only
# def add_nmcq():
#     form = NewMCQPaperForm()
#     qp = f"{request.args.get('subject')}_{request.args.get('session')}_qp_{request.args.get('paper')}"
#     if form.validate_on_submit():
#         questions = [form.q1, form.q2, form.q3, form.q4, form.q5, form.q6, form.q7, form.q8, form.q9, form.q10, form.q11, form.q12, form.q13, form.q14, form.q15, form.q16, form.q17, form.q18, form.q19, form.q20, form.q21, form.q22, form.q23, form.q24, form.q25, form.q26, form.q27, form.q28, form.q29, form.q30, form.q31, form.q32, form.q33, form.q34, form.q35, form.q36, form.q37, form.q38, form.q39, form.q40]
#         for i in range(40):
#             pdf_editor.cropPage(start=questions[i].start.data,
#                                 end=questions[i].end.data,
#                                 page_number=questions[i].page.data,
#                                 question_number=i+1,
#                                 paper_code=qp,
#                                 static_folder=app.static_folder)
#         ms = f"{request.args.get('subject')}_{request.args.get('session')}_ms_{request.args.get('paper')}"
#         return redirect(url_for("add_nmcq_2", subject=request.args.get('subject'), session=request.args.get('session'), paper=request.args.get('paper')))
#     num_pages = pdf_editor.getPages(paper_code=qp, static_folder=app.static_folder)
#
#     return render_template("add_mcq.html", paper_code=qp, static_folder=app.static_folder, num=num_pages, form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        # Email doesn't exist or password incorrect.
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('question_index'))
    return render_template("login.html", form=form, current_user=current_user)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('question_index'))


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        if User.query.filter_by(email=form.email.data).first():
            print(User.query.filter_by(email=form.email.data).first())
            # User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=form.email.data,
            name=form.name.data,
            password=hash_and_salted_password,
            permission_level=1
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("question_index"))

    return render_template("register.html", form=form, current_user=current_user)


if __name__ == "__main__":
    app.run(debug=True)
