from sqlite3 import OperationalError
from flask import request, jsonify
from marshmallow import ValidationError
from model.instituicaoEnsino import InstituicaoEnsinoSchema, InstituicaoEnsino
from helpers.database import get_connection
from helpers.application import app

instituicaoEnsino_schema = InstituicaoEnsinoSchema()

def row__to_instituicaoEnsino(row):
    return InstituicaoEnsino(
        id=row[0],
        co_entidade=row[1],
        no_entidade=row[2],
        no_uf=row[3],
        sg_uf=row[4],
        co_uf=row[5],
        no_municipio=row[6],
        co_municipio=row[7],
        nu_ano_censo=row[8],
        qt_mat_bas=row[9],
        qt_mat_inf=row[10],
        qt_mat_fund=row[11],
        qt_mat_med=row[12],
        qt_mat_prof=row[13],
        qt_mat_eja=row[14],
        qt_mat_esp=row[15]
    )

@app.before_request
def antes_da_requisicao():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS instituicoes_ensino (
            id_instituicao INTEGER PRIMARY KEY AUTOINCREMENT,
            co_entidade INTEGER NOT NULL DEFAULT 0,
            no_entidade TEXT NOT NULL DEFAULT '',
            no_uf TEXT NOT NULL DEFAULT '',
            sg_uf TEXT NOT NULL DEFAULT '',
            co_uf INTEGER NOT NULL DEFAULT 0,
            no_municipio TEXT NOT NULL DEFAULT '',
            co_municipio INTEGER NOT NULL DEFAULT 0,
            nu_ano_censo INTEGER NOT NULL DEFAULT 0,
            qt_mat_bas INTEGER DEFAULT 0,
            qt_mat_inf INTEGER DEFAULT 0,
            qt_mat_fund INTEGER DEFAULT 0,
            qt_mat_med INTEGER DEFAULT 0,
            qt_mat_prof INTEGER DEFAULT 0,
            qt_mat_eja INTEGER DEFAULT 0,
            qt_mat_esp INTEGER DEFAULT 0,
            ativo INTEGER DEFAULT 1
        );
    """)
    conn.commit()


@app.get("/instituicoes")
def get_instituicoesEnsinoAll():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
    
    offset = (page - 1) * per_page

    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT * FROM instituicoes_ensino WHERE ativo = 1 LIMIT ? OFFSET ?",
        (per_page, offset)
    )
    rows = cursor.fetchall()
    
    cursor.execute("SELECT COUNT(*) FROM instituicoes_ensino WHERE ativo = 1")
    total_registros = cursor.fetchone()[0]
    total_paginas = (total_registros + per_page - 1) // per_page
    
    instituicoes = [row__to_instituicaoEnsino(row) for row in rows]
    
    resposta = {
        "dados": InstituicaoEnsinoSchema(many=True).dump(instituicoes),
        "paginacao": {
            "pagina_atual": page,
            "itens_por_pagina": per_page,
            "total_registros": total_registros,
            "total_paginas": total_paginas
        }
    }
    return jsonify(resposta), 200


@app.get("/instituicoes/<int:id>")
def get_instituicaoEnsinoById(id):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM instituicoes_ensino WHERE id_instituicao = ? AND ativo = 1", (id,))
    row = cursor.fetchone()
    
    if row is None:
        return jsonify({"error": "Instituição de ensino não encontrada"}), 404
    
    instituicao = row__to_instituicaoEnsino(row)
    return jsonify(instituicaoEnsino_schema.dump(instituicao)), 200


@app.post("/instituicoes")
def post_instituicaoEnsino():
    data = request.get_json(silent=True) or {}
    try:
        validar_dados = instituicaoEnsino_schema.load(data)
        
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO instituicoes_ensino (
                co_entidade, no_entidade, no_uf, sg_uf, co_uf,
                no_municipio, co_municipio, nu_ano_censo, qt_mat_bas, qt_mat_inf,
                qt_mat_fund, qt_mat_med, qt_mat_prof, qt_mat_eja, qt_mat_esp
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            validar_dados['co_entidade'],
            validar_dados['no_entidade'],
            validar_dados['no_uf'],
            validar_dados['sg_uf'],
            validar_dados['co_uf'],
            validar_dados['no_municipio'],
            validar_dados['co_municipio'],
            validar_dados['nu_ano_censo'],
            validar_dados.get('qt_mat_bas', 0),
            validar_dados.get('qt_mat_inf', 0),
            validar_dados.get('qt_mat_fund', 0),
            validar_dados.get('qt_mat_med', 0),
            validar_dados.get('qt_mat_prof', 0),
            validar_dados.get('qt_mat_eja', 0),
            validar_dados.get('qt_mat_esp', 0)
        ))
        
        novo_id = cursor.lastrowid
        conn.commit()
        
        instituicao = InstituicaoEnsino(**validar_dados, id=novo_id)
        return jsonify(instituicaoEnsino_schema.dump(instituicao)), 201
    
    except ValidationError as e:
        return jsonify({"error": e.messages}), 400
    except OperationalError:
        conn.rollback()
        raise


@app.put("/instituicoes/<int:id>")
def put_instituicaoEnsino(id):
    data = request.get_json(silent=True) or {}
    try:
        validar_dados = instituicaoEnsino_schema.load(data)
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE instituicoes_ensino SET
                co_entidade = ?, no_entidade = ?, no_uf = ?, sg_uf = ?, co_uf = ?,
                no_municipio = ?, co_municipio = ?, nu_ano_censo = ?, qt_mat_bas = ?,
                qt_mat_inf = ?, qt_mat_fund = ?, qt_mat_med = ?, qt_mat_prof = ?,
                qt_mat_eja = ?, qt_mat_esp = ?
            WHERE id_instituicao = ? AND ativo = 1
        """, (
            validar_dados['co_entidade'], validar_dados['no_entidade'], validar_dados['no_uf'],
            validar_dados['sg_uf'], validar_dados['co_uf'], validar_dados['no_municipio'],
            validar_dados['co_municipio'], validar_dados['nu_ano_censo'],
            validar_dados.get('qt_mat_bas', 0), validar_dados.get('qt_mat_inf', 0),
            validar_dados.get('qt_mat_fund', 0), validar_dados.get('qt_mat_med', 0),
            validar_dados.get('qt_mat_prof', 0), validar_dados.get('qt_mat_eja', 0),
            validar_dados.get('qt_mat_esp', 0),
            id
        ))
        
        if cursor.rowcount == 0:
            return jsonify({"error": "Instituição de ensino não encontrada ou inativa"}), 404
        
        conn.commit()
        
        instituicao_atualizada = InstituicaoEnsino(**validar_dados, id=id)
        return jsonify(instituicaoEnsino_schema.dump(instituicao_atualizada)), 200
    
    except ValidationError as e:
        return jsonify({"error": e.messages}), 400
    except OperationalError:
        conn.rollback()
        raise
    

@app.delete("/instituicoes/<int:id>")
def delete_instituicaoEnsino(id):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("UPDATE instituicoes_ensino SET ativo = 0 WHERE id_instituicao = ? AND ativo = 1", (id,))
    
    if cursor.rowcount == 0:
        return jsonify({"error": "Instituição de ensino não encontrada ou já deletada"}), 404
    
    conn.commit()
    return jsonify({"message": "Instituição de ensino deletada com sucesso"}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)