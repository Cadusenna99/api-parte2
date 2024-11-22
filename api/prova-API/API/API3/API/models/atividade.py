from config import db

class Atividade(db.Model):
    __tablename__ = 'atividades'

    id_atividade = db.Column(db.Integer, primary_key=True)
    id_disciplina = db.Column(db.Integer, nullable=False)
    enunciado = db.Column(db.String(500), nullable=False)
    respostas = db.Column(db.JSON, nullable=True)

    def __init__(self, id_disciplina, enunciado, respostas=None):
        self.id_disciplina = id_disciplina
        self.enunciado = enunciado
        self.respostas = respostas if respostas is not None else []

    def to_dict(self):
        return {
            'id_atividade': self.id_atividade,
            'id_disciplina': self.id_disciplina,
            'enunciado': self.enunciado,
            'respostas': self.respostas
        }

class AtividadeNaoEncontrada(Exception):
    pass

def listar_atividades():
    return [atividade.to_dict() for atividade in Atividade.query.all()]

def atividade_por_id(id_atividade):
    atividade = Atividade.query.get(id_atividade)
    if not atividade:
        raise AtividadeNaoEncontrada()
    return atividade.to_dict()

def adicionar_atividade(dados_atividade):
    nova_atividade = Atividade(
        id_disciplina=dados_atividade['id_disciplina'],
        enunciado=dados_atividade['enunciado'],
        respostas=dados_atividade.get('respostas', [])
    )
    db.session.add(nova_atividade)
    db.session.commit()
    print(f"Atividade criada: {nova_atividade.to_dict()}")

def atualizar_atividade(id_atividade, dados_novos):
    atividade = Atividade.query.get(id_atividade)
    if not atividade:
        raise AtividadeNaoEncontrada()
    atividade.id_disciplina = dados_novos.get('id_disciplina', atividade.id_disciplina)
    atividade.enunciado = dados_novos.get('enunciado', atividade.enunciado)
    atividade.respostas = dados_novos.get('respostas', atividade.respostas)
    db.session.commit()

def excluir_atividade(id_atividade):
    atividade = Atividade.query.get(id_atividade)
    if not atividade:
        raise AtividadeNaoEncontrada()
    db.session.delete(atividade)
    db.session.commit()
