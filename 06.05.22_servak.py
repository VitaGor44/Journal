import flask
from flask import Flask
from flask import jsonify
from flask import request, abort
from flask import render_template
from flask import Response
from random import randint, uniform
import psycopg2

app = Flask(__name__)

def connect():
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='test',
            user='postgres',
            password='masterkey'
        )
    except Exception as error:
        print(error)
    return conn


def close(conn):
    conn.close()

def get_journal():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM journal')
    rows = cursor.fetchall()

    students = []

    for i in rows:
        student = {
            'bio': i[1],
            'faculty': i[2],
            'specialise': i[3],
            'course': i[4],
            'format_stady': i[5],
            'prof_education': i[6],
            'grade': i[7]
        }
        students.append(student)
    return students

def create_table(journal):
    table = ''
    for i in range(len(journal)): # получение одной строки в таблице, которая будет выложена на страницу
        tr = """
            <tr>
                <th scope="row">{0}</th>
                <td>{1}</td>
                <td>{2}</td>
                <td>{3}</td>
                <td>{4}</td>
                <td>{5}</td>
                <td>{6}</td>
                <td>{7}</td>
            </tr>
        """.format(i+1, journal[i]['bio'], journal[i]['faculty'], journal[i]['specialise'], journal[i]['course'], journal[i]['format_stady'], journal[i]['prof_education'], journal[i]['grade'])

        table += tr # собирание строк, формирование table
    return table


@app.route('/')
def index(main=None):
    return render_template('index_06_05_22.html', name=main)

@app.route('/home')
def home(main=None):
    #
    # journal = get_journal()
    # table = create_table(journal)
    return render_template('home.html', name=main) #, table=table)


@app.route('/journal')
def journal(main=None):
    journal = get_journal()
    table = create_table(journal)
    return render_template('journal.html', name=main, table=table)

@app.route('/check_user')
def autorization():
    if request.method == 'GET':
        email = request.args.get('email')
        password = request.args.get('password')

        conn = connect()
        cursor = conn.cursor()
        cursor.execute('SELECT email, password FROM users')
        users = cursor.fetchall()
        print(users)

        for user in users:
            if user[0] == email and user[1] == password:
                resp = flask.Response('Done', status=200)
                resp.headers['Access-Control-Allow-Origin'] = '*'
                return resp

        resp = flask.Response('Fail', status=400)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp

@app.route('/search_student')
def search_student():
    if request.method == 'GET':
        number = request.args.get('number')
        bio = request.args.get('bio')

        try:
            conn = connect()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM journal WHERE student_id = " + number)
            student = cursor.fetchone()

            resp = {
                'facult': student[2],
                'special': student[3],
                'curse': student[4],
                'prof_aduc': student[5],
            }
            return jsonify(resp)

        except Exception as error:
            print(error)





if __name__ == '__main__':
    app.run(debug=True)
