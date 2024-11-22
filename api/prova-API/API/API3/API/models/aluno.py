from config import db

class Aluno(db.Model):
    __tablename__ = 'alunos'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer)
    data_nascimento = db.Column(db.Date)
    nota_primeiro_semestre = db.Column(db.Float)
    nota_segundo_semestre = db.Column(db.Float)
    media_final = db.Column(db.Float)
    turma_id = db.Column(db.Integer, db.ForeignKey('turmas.id'))
    
    turma = db.relationship('Turma', back_populates='alunos')

    def __init__(self, nome, idade=None, data_nascimento=None, nota_primeiro_semestre=None, nota_segundo_semestre=None, turma_id=None):
        self.nome = nome
        self.idade = idade
        self.data_nascimento = data_nascimento
        self.nota_primeiro_semestre = nota_primeiro_semestre
        self.nota_segundo_semestre = nota_segundo_semestre
        self.media_final = self.calcular_media_final(nota_primeiro_semestre, nota_segundo_semestre)
        self.turma_id = turma_id

    def calcular_media_final(self, nota1, nota2):
        if nota1 is not None and nota2 is not None:
            return (nota1 + nota2) / 2
        return None

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'idade': self.idade,
            'data_nascimento': self.data_nascimento,
            'nota_primeiro_semestre': self.nota_primeiro_semestre,
            'nota_segundo_semestre': self.nota_segundo_semestre,
            'media_final': self.media_final,
            'turma_id': self.turma_id
        }

class AlunoNaoEncontrado(Exception):
    pass

def aluno_por_id(id_aluno):
    aluno = Aluno.query.get(id_aluno)
    if not aluno:
        raise AlunoNaoEncontrado
    return aluno.to_dict()

def listar_alunos():
    alunos = Aluno.query.all()
    return [aluno.to_dict() for aluno in alunos]

def adicionar_aluno(dados_aluno):
    novo_aluno = Aluno(
        nome=dados_aluno['nome'],
        idade=dados_aluno.get('idade'),
        data_nascimento=dados_aluno.get('data_nascimento'),
        nota_primeiro_semestre=dados_aluno.get('nota_primeiro_semestre'),
        nota_segundo_semestre=dados_aluno.get('nota_segundo_semestre'),
        turma_id=dados_aluno.get('turma_id')
    )
    db.session.add(novo_aluno)
    db.session.commit()

def atualizar_aluno(id_aluno, dados_novos):
    aluno = Aluno.query.get(id_aluno)
    if not aluno:
        raise AlunoNaoEncontrado
    aluno.nome = dados_novos.get('nome', aluno.nome)
    aluno.idade = dados_novos.get('idade', aluno.idade)
    aluno.data_nascimento = dados_novos.get('data_nascimento', aluno.data_nascimento)
    aluno.nota_primeiro_semestre = dados_novos.get('nota_primeiro_semestre', aluno.nota_primeiro_semestre)
    aluno.nota_segundo_semestre = dados_novos.get('nota_segundo_semestre', aluno.nota_segundo_semestre)
    aluno.media_final = aluno.calcular_media_final(aluno.nota_primeiro_semestre, aluno.nota_segundo_semestre)
    aluno.turma_id = dados_novos.get('turma_id', aluno.turma_id)
    db.session.commit()

def excluir_aluno(id_aluno):
    aluno = Aluno.query.get(id_aluno)
    if not aluno:
        raise AlunoNaoEncontrado
    db.session.delete(aluno)
    db.session.commit()
