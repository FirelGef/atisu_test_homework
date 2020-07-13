from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///users.db'
db = SQLAlchemy(app)


class UsersDB(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    # После беглого исследования в гугле, на самые длинные имена и фамилии...
    # Понял, что занимаюсь ерундой и поставил ограничение 50 символов :)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)


def generate_json_responce(endpoint, fields=None, error_text=None):
    body = {}
    if not error_text:
        for field in fields.items():
            body[field[0]] = field[1]
        return {"status": 200, "method": endpoint, "body": body}
    else:
        # В ответе можно было бы добавить причину ошибки, но посчитал это избыточным для тестового задания.
        return {"status": 400, "body": error_text, "method": endpoint}


@app.route('/add', methods=['POST', 'GET'])
def add_user():
    """
    Формат тела POST запроса:
     {'param': value...}

    Формат GET запроса:
     http://localhost:5000/add?param=value...

    :return: JSON
    """

    try:
        if request.method == "POST":
            name = request.form['name'].title().strip()
            surname = request.form['surname'].title().strip()
        else:
            name = request.args.get('name').title().strip()
            surname = request.args.get('surname').title().strip()
    except:
        return generate_json_responce('/add', error_text='missing parameter')

    try:
        users_db = UsersDB(name=name, surname=surname)
        # проверяет, что name и surname состоят из букв.(сделал упрощенный вариант)
        if not name.isalpha() or not surname.isalpha():
            raise ValueError()
        if not len(name) <= 50 or not len(surname) <= 50:
            raise ValueError()
        db.session.add(users_db)
        db.session.commit()
        return generate_json_responce('/add', fields={'name': name, 'surname': surname,
                                                      "user_id": users_db.user_id})
    except:
        return generate_json_responce('/add', error_text='invalid parameter')


@app.route('/get', methods=['POST', 'GET'])
def get_user_by_id():
    """
    Формат тела POST запроса:
     {'param': value...}

    Формат GET запроса:
     http://localhost:5000/get?param=value...

    :return: JSON
    """
    try:
        if request.method == "POST":
            user_id = request.form['user_id'].strip()
        else:
            user_id = request.args.get('user_id').strip()
    except:
        return generate_json_responce('/get', error_text='missing parameter: user_id')

    try:
        if not user_id.isnumeric():
            raise ValueError()
        user = UsersDB.query.get(user_id)
        return generate_json_responce('/get', fields={'name': user.name, 'surname': user.surname})
    except:
        return generate_json_responce('/get', error_text='invalid user id')


@app.route('/remove', methods=['POST', 'GET'])
def remove_user_by_id():
    """
    Формат тела POST запроса:
     {'param': value...}

    Формат GET запроса:
     http://localhost:5000/remove?param=value...

    :return: JSON
    """
    try:
        if request.method == "POST":
            user_id = request.form['user_id'].strip()
        else:
            user_id = request.args.get('user_id').strip()
    except:
        return generate_json_responce('/get', error_text='missing parameter: user_id')

    try:
        if not user_id.isnumeric():
            raise ValueError()
        user = UsersDB.query.get(user_id)
        db.session.delete(user)
        db.session.commit()
        return generate_json_responce('/remove', fields={'name': user.name,
                                                         'surname': user.surname,
                                                         "user_id": user.user_id})
    except:
        return generate_json_responce('/remove', error_text='invalid user id')


@app.route('/remove/all', methods=['POST', 'GET'])
def remove_all_users():
    try:
        users = UsersDB.query.all()
        for user in users:
            db.session.delete(user)
            db.session.commit()
        return generate_json_responce('/remove/all', fields={'remove_user_count': len(users)})
    except:
        return generate_json_responce('/remove/all', 'invalid')


if __name__ == '__main__':
    app.run(debug=True)
