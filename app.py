import glob
import warnings
from flask import (Flask, session, flash, redirect, render_template, request,
                   url_for, send_from_directory)

import screen

warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

app = Flask(__name__)

app.config.from_object(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    USERNAME='admin ',
    PASSWORD='root',
    SECRET_KEY='root',
))

app.config['UPLOAD_FOLDER'] = 'data/Uploaded_Resumes/'
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


class jd:
    def __init__(self, name):
        self.name = name


def getfilepath(loc):
    temp = str(loc).split('\\')
    return temp[-1]


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        session['logged_in'] = True
        flash('You were logged in')
        return redirect(url_for('home'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('home'))


@app.route('/')
def home():
    x = []
    for file in glob.glob("./data/job_descriptions/*.txt"):
        res = jd(file)
        x.append(jd(getfilepath(file)))
    print(x)
    return render_template('index.html', results=x)


@app.route('/results', methods=['GET', 'POST'])
def res():
    if request.method == 'POST':
        jobfile = request.form['des']
        print(jobfile)
        flask_return = screen.res(jobfile)

        print(flask_return)
        return render_template('result.html', results=flask_return)


@app.route('/Uploaded_Resumes/<path:filename>')
def custom_static(filename):
    return send_from_directory('./data/Uploaded_Resumes', filename)


if __name__ == '__main__':
    # app.run(debug = True)
    app.run('localhost', 8000, debug=True, threaded=True)