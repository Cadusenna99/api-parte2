from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from models.aluno import AlunoNaoEncontrado, listar_alunos, aluno_por_id, adicionar_aluno, atualizar_aluno, excluir_aluno

alunos_blueprint = Blueprint('alunos', __name__)

@alunos_blueprint.route('/', methods=['GET'])
def home():
    return "Página Inicial"

# ROTA PARA LISTAR TODOS OS ALUNOS
@alunos_blueprint.route('/alunos', methods=['GET'])
def obter_lista_alunos():
    alunos = listar_alunos()
    return render_template("alunos/alunos.html", alunos=alunos)

# ROTA PARA OBTER UM ALUNO ESPECÍFICO POR ID
@alunos_blueprint.route('/alunos/<int:aluno_id>', methods=['GET'])
def mostrar_aluno(aluno_id):
    try:
        aluno = aluno_por_id(aluno_id)
        return render_template('alunos/aluno_id.html', aluno=aluno)
    except AlunoNaoEncontrado:
        return jsonify({'error': 'Aluno não encontrado'}), 404

# ROTA PARA EXIBIR FORMULÁRIO DE CRIAÇÃO DE UM NOVO ALUNO
@alunos_blueprint.route('/alunos/adicionar', methods=['GET'])
def formulario_novo_aluno():
    return render_template('alunos/criarAlunos.html')

# ROTA PARA CRIAR UM NOVO ALUNO
@alunos_blueprint.route('/alunos', methods=['POST'])
def adicionar_novo_aluno():
    nome = request.form.get('nome')  # Usando get para evitar KeyError
    aluno_data = {'nome': nome}
    adicionar_aluno(aluno_data)
    return redirect(url_for('alunos.obter_lista_alunos'))

# ROTA PARA EXIBIR FORMULÁRIO PARA EDITAR UM ALUNO
@alunos_blueprint.route('/alunos/<int:aluno_id>/editar', methods=['GET'])
def formulario_editar_aluno(aluno_id):
    try:
        aluno = aluno_por_id(aluno_id)
        return render_template('alunos/aluno_update.html', aluno=aluno)
    except AlunoNaoEncontrado:
        return jsonify({'error': 'Aluno não encontrado'}), 404

# ROTA PARA EDITAR UM ALUNO
@alunos_blueprint.route('/alunos/<int:aluno_id>', methods=['POST'])
def salvar_atualizacao_aluno(aluno_id):
    try:
        nome = request.form.get('nome')  # Usando get para evitar KeyError
        atualizacao = {'nome': nome}
        atualizar_aluno(aluno_id, atualizacao)
        return redirect(url_for('alunos.mostrar_aluno', aluno_id=aluno_id))
    except AlunoNaoEncontrado:
        return jsonify({'error': 'Aluno não encontrado'}), 404

# ROTA PARA DELETAR UM ALUNO
@alunos_blueprint.route('/alunos/delete/<int:aluno_id>', methods=['POST'])
def excluir_aluno_por_id(aluno_id):
    try:
        excluir_aluno(aluno_id)
        return redirect(url_for('alunos.obter_lista_alunos'))
    except AlunoNaoEncontrado:
        return jsonify({'error': 'Aluno não encontrado'}), 404  
