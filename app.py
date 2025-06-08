import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# ——— Konfiguracja połączenia z MySQL ———
db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASS')
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')

app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+pymysql://{db_user}:{db_pass}@{db_host}/{db_name}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ——— Ścieżka do certyfikatu SSL (Windows vs Linux) ———
if os.name == 'nt':
    # lokalnie na Windowsie
    ca_path = r"C:\Users\krzys\Desktop\Liga\BaltimoreCyberTrustRoot.crt.pem"
else:
    # w Azure App Service (Linux)
    ca_path = '/home/site/wwwroot/BaltimoreCyberTrustRoot.crt.pem'

app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'connect_args': {
        'ssl': {'ca': ca_path}
    }
}

# Inicjalizacja bazy
db = SQLAlchemy(app)

# Import modeli
from models import Team, Player, Game, Gol

# Tworzenie tabel (uruchomi się raz przy starcie, jeśli nie ma tabel)
with app.app_context():
    db.create_all()

# ——— Trasy ———
@app.route('/')
def index():
    games = Game.query.order_by(Game.date_time.desc()).all()
    return render_template('index.html', games=games)

@app.route('/top_scorers')
def top_scorers():
    top = (
        db.session.query(
            Player.nazwa,
            db.func.count(Gol.id).label('gole')
        )
        .join(Gol, Gol.strzelec_id == Player.id)
        .group_by(Player.id)
        .order_by(db.desc('gole'))
        .all()
    )
    return render_template('top_scorers.html', top=top)

# ——— Local debug ———
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
