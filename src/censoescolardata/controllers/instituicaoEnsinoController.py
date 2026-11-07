from flask import jsonify, Blueprint
from marshmallow import ValidationError

from helpers.application import request
from services.instituicaoService import listar_instituicoes_paginadas, obter_por_id, criar_instituicao, \
    atualizar_dados_instituicao, deletar_instituicao

instituicoes_bp = Blueprint('instituicoes', __name__, url_prefix='/instituicoes')

# passou
@instituicoes_bp.get("")
def get_instituicoesEnsinoAll():
    print("entrou no controller para rodar o codigo.")
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)

    # Delega a lógica para o service
    resposta = listar_instituicoes_paginadas(page, per_page)

    return resposta, 200

# passou
@instituicoes_bp.get("/<int:id>")
def get_instituicaoEnsinoById(id):
    instituicao = obter_por_id(id)
    if not instituicao:
        return jsonify({"error": "Instituição de ensino não encontrada"}), 404
    return jsonify(instituicao), 200

# passou
@instituicoes_bp.post("")
def post_instituicaoEnsino():
    data = request.get_json(silent=True) or {}
    try:
        resultado = criar_instituicao(data)
        return jsonify(resultado), 201
    except ValidationError as e:
        return jsonify({"error": e.messages}), 400

# passou
@instituicoes_bp.put("/<int:id>")
def put_instituicaoEnsino(id):
    data = request.get_json(silent=True) or {}
    try:
        resultado = atualizar_dados_instituicao(id, data)
        if not resultado:
            return jsonify({"error": "Instituição de ensino não encontrada ou inativa"}), 404
        return jsonify(resultado), 200
    except ValidationError as e:
        return jsonify({"error": e.messages}), 400


# passou
@instituicoes_bp.delete("/<int:id>")
def delete_instituicaoEnsino(id):
    sucesso = deletar_instituicao(id)
    if not sucesso:
        return jsonify({"error": "Instituição de ensino não encontrada ou já deletada"}), 404
    return jsonify({"message": "Instituição de ensino deletada com sucesso"}), 200