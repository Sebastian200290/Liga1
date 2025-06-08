import os
from dotenv import load_dotenv
from flask import Flask, render_template
import certifi
from models import db, Team, Player, Game, Wynik, Gol

# Load .env
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Database config
db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASS')
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+pymysql://{db_user}:{db_pass}@{db_host}/{db_name}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'connect_args': {'ssl': {'ca': certifi.where()}}
}

# Register app with SQLAlchemy
db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()

# Routes
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
