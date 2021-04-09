'''
Title: api.py
Description: simple api to
            talk to todo db
Author: Jordan Phillips
Email: ejordanphillips@gmail.com
Date: 03-09-2021
'''

import os

from dotenv import load_dotenv
from flask import Flask, render_template, request, abort, redirect
from flask_mysqldb import MySQL

app = Flask(__name__, template_folder='templates')

app.config['DEBUG'] = True

# this allows for better JSON response from our API
app.config['JSON_SORT_KEYS'] = False

project_folder = os.path.expanduser('~/my_site/UNOAgileCourse2')
load_dotenv(os.path.join(project_folder, '.env'))

app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')

mysql = MySQL(app)


@app.route('/v1/all', methods=['GET', 'POST'])
def all():
    '''
    Title: all
    Description: returns all records in json
    Arguments: none
    Returns: contents - json - <str>
    Raises: none
    '''
    if request.method == 'POST':
        return 'POST not implemented'
    try:
        cursor = mysql.connection.cursor()
        query = '''
                SELECT id, label, name, description, date, importance
                FROM todo;
                '''
        cursor.execute(query)
        contents = (cursor.fetchall())
        mysql.connection.commit()
        cursor.close()

        data = {}
        for item in contents:
            data[item[0]] = {}
            data[item[0]]['label'] = item[1]
            data[item[0]]['name'] = item[2]
            data[item[0]]['description'] = item[3]
            data[item[0]]['date'] = item[4]
            data[item[0]]['importance'] = item[5]
        return data
    except Exception as err:
        app.logger.error(err)
        abort(404)


@app.route('/v1/add', methods=['GET', 'POST'])
def add():
    '''
    Title: add
    Arguments:
        request - <str>
            .name - required
            .description - required
            .date - required
            .importance - required
    Returns: MySQL query status - <str>
    Raises: none
    '''
    if request.method == 'POST':
        try:
            data = request.form
            args = ['name', 'description', 'date', 'importance']
            for arg in args:
                if not data[arg]:
                    return f'{arg} is a required argument'
            name = data['name']
            description = data['description']
            date = data['date']
            importance = data['importance']
            cursor = mysql.connection.cursor()
            query = '''
                    INSERT INTO todo
                    (name, description, date, importance)
                    VALUES (%s, %s, %s, %s);
                    '''
            params = [name, description, date, importance]
            cursor.execute(query, params)
            status = cursor.fetchall()
            mysql.connection.commit()
            cursor.close()
            return redirect('/')
        except Exception as err:
            app.logger.error(err)
            abort(404)
    else:
        try:
            args = ['name', 'description', 'date', 'importance']
            for arg in args:
                if not request.args.get(arg):
                    return f'{arg} is a required argument'

            app.logger.debug('ARGS are %s', request.args)
            name = request.args.get('name')
            description = request.args.get('description')
            date = request.args.get('date')
            importance = request.args.get('importance')
            cursor = mysql.connection.cursor()
            query = '''
                    INSERT INTO todo
                    (name, description, date, importance)
                    VALUES (%s, %s, %s, %s);
                    '''
            params = [name, description, date, importance]
            cursor.execute(query, params)
            status = cursor.fetchall()
            mysql.connection.commit()
            cursor.close()
            return f'{status}'
        except Exception as err:
            app.logger.error(err)
            abort(404)


@app.route('/v1/update', methods=['GET', 'POST'])
def update():
    '''
    Title: update
    Description: updates an existing entry
    Arguments:
            .id - required
            .name - required
            .description - required
            .date - required
            .importance - required
    '''
    if request.method == 'POST':
        try:
            data = request.form
            args = ['id', 'name', 'description', 'date', 'importance']
            for arg in args:
                if not data[arg]:
                    return f'{arg} is a required argument'
            id = data['id']
            name = data['name']
            description = data['description']
            date = data['date']
            importance = data['importance']
            cursor = mysql.connection.cursor()
            query = '''
                    UPDATE todo SET
                    name = %s, description = %s,
                    date = %s, importance = %s
                    WHERE id = %s;
                    '''
            app.logger.debug(f'QUERY IS :: {query}')
            params = [name, description, date, importance, id]
            cursor.execute(query, params)
            status = cursor.fetchall()
            mysql.connection.commit()
            cursor.close()
            return redirect('/')
        except Exception as err:
            app.logger.error(err)
            abort(404)
    else:
        try:
            args = ['id', 'name', 'description', 'date', 'importance']
            for arg in args:
                if not request.args.get(arg):
                    return f'{arg} is a required argument'
            id = request.args.get('id')
            name = request.args.get('name')
            description = request.args.get('description')
            date = request.args.get('date')
            importance = request.args.get('importance')
            cursor = mysql.connection.cursor()
            query = '''
                    UPDATE todo SET name = %s, description = %s,
                    date = %s, importance = %s
                    WHERE id = %s;
                    '''
            app.logger.debug(f'QUERY IS :: {query}')
            params = [id, name, description, date, importance]
            cursor.execute(query, params)
            status = cursor.fetchall()
            mysql.connection.commit()
            cursor.close()
            return f'{status}'
        except Exception as err:
            app.logger.error(err)
            abort(404)


@app.route('/v1/delete', methods=['GET', 'POST'])
def delete():
    '''
    Title: delete
    Description: deletes an existing entry
    Arguments:
            .id
    '''
    if request.method == 'POST':
        try:
            data = request.form
            args = ['id']
            for arg in args:
                if not data[arg]:
                    return f'{arg} is a required argument'
            id = data['id']
            app.logger.error(id)
            cursor = mysql.connection.cursor()
            query = '''
                    DELETE FROM todo
                    WHERE id = %s;
                    '''
            params = [id]
            cursor.execute(query, params)
            status = cursor.fetchall()
            mysql.connection.commit()
            cursor.close()
            app.logger.debug('CALLING HOME()')
            return redirect('/')
        except Exception as err:
            app.logger.error(err)
            abort(404)
    else:
        try:
            args = ['id']
            for arg in args:
                if not request.args.get(arg):
                    return f'{arg} is a required argument'
            id = request.args.get('id')
            cursor = mysql.connection.cursor()
            query = '''
                    DELETE FROM todo
                    WHERE id = %s;
                    '''
            params = [id]
            cursor.execute(query, params)
            status = cursor.fetchall()
            mysql.connection.commit()
            cursor.close()
            return f'{status}'
        except Exception as err:
            app.logger.error(err)
            abort(404)


@app.route('/', methods=['GET', 'POST'])
def home():
    '''
    Title: home
    Description: home page for website
    Arguments: none
    Returns: home template with data
    '''
    data = all()
    return render_template("index.html", data=data)


if __name__ == '__main__':
    app.run()
