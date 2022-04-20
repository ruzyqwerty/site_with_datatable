from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    name = db.Column(db.String(64))
    count = db.Column(db.Integer, index=True)
    distance = db.Column(db.Float)

    def to_dict(self):
        return {
            'date': self.date,
            'name': self.name,
            'count': self.count,
            'distance': self.distance
        }


db.create_all()

ROWS_PER_PAGE = 10


@app.route('/')
def index():
    return render_template('index.html', title='Таблица поездок')


@app.route("/api/data")
def data():
    query = User.query

    # search filter
    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            User.name.like(f'%{search}%'),
            User.count.like(f'%{search}%'),
            User.distance.like(f'%{search}%')
        ))
    total_filtered = query.count()

    # sorting
    order = []
    i = 0
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_name = request.args.get(f'columns[{col_index}][data]')
        if col_name not in ['name', 'count', 'distance']:
            col_name = 'name'
        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        col = getattr(User, col_name)
        if descending:
            col = col.desc()
        order.append(col)
        i += 1
    if order:
        query = query.order_by(*order)

    # pagination
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    query = query.offset(start).limit(length)

    return {
        'data': [user.to_dict() for user in query],
        'recordsFiltered': User.query.count(),
        'recordsTotal': User.query.count(),
        'draw': request.args.get('draw', type=int),
    }


if __name__ == "__main__":
    app.run()
