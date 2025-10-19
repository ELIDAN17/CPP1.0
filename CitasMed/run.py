# en run.py

from app import create_app, db
from app.models import Usuario, Medico, Cita
from flask_migrate import Migrate

app = create_app()

migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Usuario': Usuario, 'Medico': Medico, 'Cita': Cita}

if __name__ == '__main__':
    app.run(debug=True)