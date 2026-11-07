

from models.instituicaoEnsino import InstituicaoEnsinoSchema, InstituicaoEnsino
from helpers.database import get_connection

instituicaoEnsino_schema = InstituicaoEnsinoSchema()

def row_to_instituicaoEnsino(row):
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



def estrutura_tabela():
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


def buscar_todas_instituicao(per_page, offset):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM instituicoes_ensino WHERE ativo = 1 LIMIT ? OFFSET ?",
        (per_page, offset)
    )
    rows = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM instituicoes_ensino WHERE ativo = 1")
    total_registros = cursor.fetchone()[0]

    conn.close()
    return rows, total_registros

def buscar_por_id(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM instituicoes_ensino WHERE id_instituicao = ? AND ativo = 1", (id,))
    row = cursor.fetchone()
    conn.close()
    return row

def inserir_instituicao(dados):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO instituicoes_ensino (
            co_entidade, no_entidade, no_uf, sg_uf, co_uf,
            no_municipio, co_municipio, nu_ano_censo, qt_mat_bas, qt_mat_inf,
            qt_mat_fund, qt_mat_med, qt_mat_prof, qt_mat_eja, qt_mat_esp
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        dados['co_entidade'], dados['no_entidade'], dados['no_uf'],
        dados['sg_uf'], dados['co_uf'], dados['no_municipio'],
        dados['co_municipio'], dados['nu_ano_censo'],
        dados.get('qt_mat_bas', 0), dados.get('qt_mat_inf', 0),
        dados.get('qt_mat_fund', 0), dados.get('qt_mat_med', 0),
        dados.get('qt_mat_prof', 0), dados.get('qt_mat_eja', 0),
        dados.get('qt_mat_esp', 0)
    ))
    novo_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return novo_id

def atualizar_instituicao(id, dados):
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
        dados['co_entidade'], dados['no_entidade'], dados['no_uf'],
        dados['sg_uf'], dados['co_uf'], dados['no_municipio'],
        dados['co_municipio'], dados['nu_ano_censo'],
        dados.get('qt_mat_bas', 0), dados.get('qt_mat_inf', 0),
        dados.get('qt_mat_fund', 0), dados.get('qt_mat_med', 0),
        dados.get('qt_mat_prof', 0), dados.get('qt_mat_eja', 0),
        dados.get('qt_mat_esp', 0),
        id
    ))
    linhas_afetadas = cursor.rowcount
    conn.commit()
    conn.close()
    return linhas_afetadas

def desativar_instituicao(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE instituicoes_ensino SET ativo = 0 WHERE id_instituicao = ? AND ativo = 1", (id,))
    linhas_afetadas = cursor.rowcount
    conn.commit()
    conn.close()
    return linhas_afetadas