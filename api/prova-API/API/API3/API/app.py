import os
from config import app, db
from controller.aluno import alunos_blueprint
from controller.professor import professor_blueprint
from controller.turma import turma_blueprint  # Importando o blueprint 
from controller.atividades import atividades_blueprint


# Registrando os blueprints
app.register_blueprint(alunos_blueprint)
app.register_blueprint(professor_blueprint)
app.register_blueprint(turma_blueprint)  # Registrando o blueprint
app.register_blueprint(atividades_blueprint)

# Criar todas as tabelas no banco de dados se elas não existirem
with app.app_context():
    db.create_all()

# Executar a aplicação
if __name__ == '__main__':
    app.run(host=app.config["HOST"], port=app.config['PORT'], debug=app.config['DEBUG'])
