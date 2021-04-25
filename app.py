from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)

app.config['SECRET_KEY'] = 'derek'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

survey = satisfaction_survey

RESPONSES_KEY = 'responses'


@app.route('/')
def home_page():

    return render_template('survey.html', survey=survey)


@app.route('/start', methods=['POST'])
def start():
    # Starts the survey
    session[RESPONSES_KEY] = []
    return redirect('/questions/0')


@app.route('/questions/<int:qnum>')
def ask_question(qnum):

    responses = session.get(RESPONSES_KEY)

    if (responses is None):
        # Redirects to start if they havent started yet
        return redirect('/')

    if (len(responses) != qnum):
        # Redirects to right question
        flash('Wrong Question!')
        return redirect(f'questions/{len(responses)}')

    question = survey.questions[qnum]
    return render_template('question.html',
                           question_num=qnum, question=question)


@app.route('/answer', methods=['POST'])
def add_answer():

    answer = request.form['answer']
    responses = session[RESPONSES_KEY]
    responses.append(answer)
    session[RESPONSES_KEY] = responses

    if(len(responses)) == len(survey.questions):
        # All questions have been answered
        return redirect('/finished')

    else:
        return redirect(f'questions/{len(responses)}')


@app.route('/finished')
def finished():
    # Completed Survery Page
    return render_template('finished.html')
