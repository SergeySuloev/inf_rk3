from os import path
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
basedir = path.dirname(path.abspath(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + path.join(basedir, 'countries.db')
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = "unique_key"


class Countries(db.Model):
    """Students database table class"""
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    country = db.Column(db.String, nullable=False)
    capital = db.Column(db.String, nullable=False)
    population = db.Column(db.Integer, nullable=False)
    language = db.Column(db.String, nullable=False)

    def __init__(self, country, capital, population, language):
        """Initializing database table"""
        self.country = country
        self.capital = capital
        self.population = population
        self.language = language

    @staticmethod
    def push(country, capital, population, language):
        c = Countries(country=country, capital=capital, population=int(population), language=language)
        db.session.add(c)
        db.session.commit()


with app.app_context():
    db.create_all()
    db.session.commit()
    Countries.push('Россия', 'Москва', 137000000, 'Русский')
    Countries.push('Франция', 'Париж', 9000000, 'Французский')
    Countries.push('Германия', 'Берлин', 7000000, 'Немецкий')


@app.route('/edit', methods=['GET', 'POST'])
def edit_population():
    if request.method == 'POST':
        if not request.form['identifier'] or not request.form['population']:
            print('Not everything is filled up')
        else:
            identifier = request.form['identifier']
            population = request.form['population']
            a = db.session.execute(f"UPDATE countries SET population={population} WHERE id={identifier}")
            db.session.commit()
            return redirect(url_for('show_all'))
    return render_template('edit_population.html')

@app.route('/delete', methods=['GET', 'POST'])
def delete_line():
    if request.method == 'POST':
        if not request.form['identifier']:
            print('Not everything is filled up')
        else:
            identifier = request.form['identifier']
            a = db.session.execute(f"DELETE FROM countries WHERE id={identifier}")
            db.session.commit()
            return redirect(url_for('show_all'))
    return render_template('delete.html')


@app.route('/')
def show_all():
    """Webpage table renderer"""
    return render_template('show_all.html', Countries=Countries.query.all())


if __name__ == '__main__':
    app.run(debug=True)
