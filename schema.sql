CREATE TABLE IF NOT EXISTS instituicoes_ensino (
	id_instituicao INTEGER PRIMARY KEY AUTOINCREMENT,
    co_entidade INTEGER  default 0,
    no_entidade TEXT default '',
    no_uf TEXT  default '',
    sg_uf TEXT  default '',
    co_uf INTEGER  default 0,
    no_municipio TEXT  default '',
    co_municipio INTEGER  default '',
    nu_ano_censo INTEGER  default 0,
    qt_mat_bas INTEGER DEFAULT 0,
    qt_mat_inf INTEGER DEFAULT 0,
    qt_mat_fund INTEGER DEFAULT 0,
    qt_mat_med INTEGER DEFAULT 0,
    qt_mat_prof INTEGER DEFAULT 0,
    qt_mat_eja INTEGER DEFAULT 0,
    qt_mat_esp INTEGER DEFAULT 0,
    ativo INTEGER DEFAULT 1
);
