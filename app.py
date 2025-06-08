from flask import Flask, render_template
from models import db, Team, Player, Game, Wynik, Gol
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'SQLITE_URL',
    'sqlite:///liga.db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# 🔧 UTWÓRZ BAZĘ – to nowy sposób, zamiast @before_first_request
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    games = Game.query.order_by(Game.date_time.desc()).all()
    return render_template('index.html', games=games)

@app.route('/top_scorers')
def top_scorers():
    top = db.session.query(
        Player.nazwa, db.func.count(Gol.id).label('gole')
    ).join(Gol, Gol.strzelec_id == Player.id) \
     .group_by(Player.id) \
     .order_by(db.desc('gole')).all()
    return render_template('top_scorers.html', top=top)

if __name__ == '__main__':
    app.run(debug=True)
