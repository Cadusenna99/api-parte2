from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from models.professor import ProfessorNaoEncontrado, listar_professores, professor_por_id, adicionar_professor, atualizar_professor, excluir_professor

# Definindo o blueprint para professores
professor_blueprint = Blueprint('professores', __name__)

# ROTA PRINCIPAL PARA A PÁGINA DOS PROFESSORES
@professor_blueprint.route('/professores', methods=["GET"])
def visualizar_professores():
    todos_professores = listar_professores()  # Obtem a lista de todos os professores
    return render_template("professor/professores.html", professores=todos_professores)  # Passa a lista para o template

# ROTA PARA OBTER DADOS DE UM PROFESSOR ESPECÍFICO
@professor_blueprint.route('/professores/<int:professor_id>', methods=['GET'])
def visualizar_detalhes_professor(professor_id):
    try:
        professor = professor_por_id(professor_id)  # Busca o professor pelo ID
        return render_template('professor/professor_id.html', professor=professor)    # Passa os dados do professor para o template
    except ProfessorNaoEncontrado:
        return jsonify({'erro': 'Professor não encontrado'}), 404

# ROTA PARA CARREGAR O FORMULÁRIO DE ADIÇÃO DE UM NOVO PROFESSOR
@professor_blueprint.route('/professores/adicionar', methods=['GET'])
def carregar_formulario_adicionar():
    return render_template('professor/criarProfessor.html')  # Carrega o formulário para adicionar um professor

# ROTA PARA ADICIONAR UM NOVO PROFESSOR
@professor_blueprint.route('/professores', methods=['POST'])
def adicionar_novo_professor():
    dados_professor = {
        'nome': request.form.get('nome'),
        'idade': request.form.get('idade'),
        'materia': request.form.get('materia'),
        'observacoes': request.form.get('observacoes')
    }
    adicionar_professor(dados_professor)  # Adiciona o novo professor
    return redirect(url_for('professores.visualizar_professores'))  # Redireciona para a lista de professores

# ROTA PARA CARREGAR O FORMULÁRIO DE EDIÇÃO DE UM PROFESSOR EXISTENTE
@professor_blueprint.route('/professores/<int:professor_id>/editar', methods=['GET'])
def carregar_formulario_editar_professor(professor_id):
    try:
        professor = professor_por_id(professor_id)  # Busca o professor pelo ID
        return render_template('professor/professor_update.html', professor=professor, professor_id=professor_id)  # Carrega o formulário de edição
    except ProfessorNaoEncontrado:
        return jsonify({'erro': 'Professor não encontrado'}), 404

# ROTA PARA ATUALIZAR OS DADOS DE UM PROFESSOR
@professor_blueprint.route('/professores/<int:professor_id>', methods=['POST'])
def atualizar_professor_dados(professor_id):
    try:
        novos_dados_professor = {
            'nome': request.form.get('nome'),
            'idade': request.form.get('idade'),
            'materia': request.form.get('materia'),
            'observacoes': request.form.get('observacoes')
        }
        atualizar_professor(professor_id, novos_dados_professor)  # Atualiza os dados do professor
        return redirect(url_for('professores.visualizar_detalhes_professor', professor_id=professor_id))  # Redireciona para os detalhes do professor
    except ProfessorNaoEncontrado:
        return jsonify({'erro': 'Professor não encontrado'}), 404

# ROTA PARA REMOVER UM PROFESSOR
@professor_blueprint.route('/professor/delete/<int:professor_id>', methods=['POST'])
def deletar_professor(professor_id):
    try:
        excluir_professor(professor_id)  # Remove o professor
        return redirect(url_for('professores.visualizar_professores'))  # Redireciona para a lista de professores
    except ProfessorNaoEncontrado:
        return jsonify({'erro': 'Professor não encontrado'}), 404
