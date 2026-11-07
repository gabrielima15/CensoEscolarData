from repositorys.instituicaoRepository import buscar_todas_instituicao, row_to_instituicaoEnsino, buscar_por_id, \
    instituicaoEnsino_schema, inserir_instituicao, atualizar_instituicao, desativar_instituicao
from models.instituicaoEnsino import InstituicaoEnsinoSchema, InstituicaoEnsino


def listar_instituicoes_paginadas(page, per_page):
    offset = (page - 1) * per_page

    rows, total_registros = buscar_todas_instituicao(per_page, offset)

    total_paginas = (total_registros + per_page - 1) // per_page

    instituicoes = [row_to_instituicaoEnsino(row) for row in rows]

    return {
        "dados": InstituicaoEnsinoSchema(many=True).dump(instituicoes),
        "paginacao": {
            "pagina_atual": page,
            "itens_por_pagina": per_page,
            "total_registros": total_registros,
            "total_paginas": total_paginas
        }
    }


def obter_por_id(id):
    row = buscar_por_id(id)
    if not row:
        return None
    instituicao = row_to_instituicaoEnsino(row)
    return instituicaoEnsino_schema.dump(instituicao)


def criar_instituicao(data):
    validar_dados = instituicaoEnsino_schema.load(data)
    novo_id = inserir_instituicao(validar_dados)

    instituicao = InstituicaoEnsino(**validar_dados, id=novo_id)
    return instituicaoEnsino_schema.dump(instituicao)


def atualizar_dados_instituicao(id, data):
    validar_dados = instituicaoEnsino_schema.load(data)
    linhas_afetadas = atualizar_instituicao(id, validar_dados)

    if linhas_afetadas == 0:
        return None

    instituicao_atualizada = InstituicaoEnsino(**validar_dados, id=id)
    return instituicaoEnsino_schema.dump(instituicao_atualizada)


def deletar_instituicao(id):
    linhas_afetadas = desativar_instituicao(id)
    return linhas_afetadas > 0