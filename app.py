from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Konfiguracja połączenia z MySQL przez zmienne środowiskowe
db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASS')
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{db_user}:{db_pass}@{db_host}/{db_name}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicjalizacja bazy danych
db = SQLAlchemy(app)

# Import modeli (upewnij się, że masz modele.py z tymi klasami)
from models import Team, Player, Game, Wynik, Gol

# Tworzenie tabel — działa z Flask 3.x
with app.app_context():
    db.create_all()

# Trasa główna
@app.route('/')
def index():
    games = Game.query.order_by(Game.date_time.desc()).all()
    return render_template('index.html', games=games)

# Trasa z najlepszymi strzelcami
@app.route('/top_scorers')
def top_scorers():
    top = db.session.query(
        Player.nazwa, db.func.count(Gol.id).label('gole')
    ).join(Gol, Gol.strzelec_id == Player.id) \
     .group_by(Player.id) \
     .order_by(db.desc('gole')).all()
    return render_template('top_scorers.html', top=top)

# Lokalny serwer tylko do debugowania (nie działa na Azure)
if __name__ == '__main__':
    app.run(debug=True)
