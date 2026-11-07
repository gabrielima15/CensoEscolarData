from marshmallow import Schema, fields,validate

class InstituicaoEnsino():
    
    def __init__(
        self,
        id,
        co_entidade,
        no_entidade,
        no_uf,
        sg_uf,
        co_uf,
        no_municipio,
        co_municipio,
        nu_ano_censo,
        qt_mat_bas,
        qt_mat_inf,
        qt_mat_fund,
        qt_mat_med,
        qt_mat_prof,
        qt_mat_eja,
        qt_mat_esp
    ):
        self.id = id
        self.co_entidade = co_entidade
        self.no_entidade = no_entidade
        self.no_uf = no_uf
        self.sg_uf = sg_uf
        self.co_uf = co_uf
        self.no_municipio = no_municipio
        self.co_municipio = co_municipio
        self.nu_ano_censo = nu_ano_censo
        self.qt_mat_bas = qt_mat_bas
        self.qt_mat_inf = qt_mat_inf 
        self.qt_mat_fund = qt_mat_fund 
        self.qt_mat_med = qt_mat_med 
        self.qt_mat_prof = qt_mat_prof
        self.qt_mat_eja = qt_mat_eja 
        self.qt_mat_esp = qt_mat_esp 
        
    def to_dict(self):
        
        return {
            "id": self.id,
            "co_entidade": self.co_entidade,
            "no_entidade": self.no_entidade,
            "no_uf": self.no_uf,
            "sg_uf": self.sg_uf,
            "co_uf": self.co_uf,
            "no_municipio": self.no_municipio,
            "co_municipio": self.co_municipio,
            "nu_ano_censo": self.nu_ano_censo,
            "qt_mat_bas": self.qt_mat_bas,
            "qt_mat_inf": self.qt_mat_inf,
            "qt_mat_fund": self.qt_mat_fund,
            "qt_mat_med": self.qt_mat_med,
            "qt_mat_prof": self.qt_mat_prof,
            "qt_mat_eja": self.qt_mat_eja,
            "qt_mat_esp": self.qt_mat_esp,
            
        }
        
class InstituicaoEnsinoSchema(Schema):
    
    id = fields.Int(dump_only=True)
    
    co_entidade = fields.Int(
        required=True,
        validate=validate.Range(min=1, max=9999999999)
    )
    no_entidade = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100)
    )
    no_uf = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=50)
    )
    sg_uf = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=2)
    )
    co_uf = fields.Int(
        required=True,
        validate=validate.Range(min=1, max=99)
    )
    no_municipio = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100)
    )
    co_municipio = fields.Int(
        required=True,
        validate=validate.Range(min=1, max=9999999999)
    )
    nu_ano_censo = fields.Int(
        required=True,
        validate=validate.Range(min=1000, max=9999)
    )
    
    qt_mat_bas = fields.Int(
        required=True,
        validate=validate.Range(min=0)
    )
    qt_mat_inf = fields.Int(
        required=True,
        validate=validate.Range(min=0)
    )
    qt_mat_fund = fields.Int(
        required=True,
        validate=validate.Range(min=0)
    )
    qt_mat_med = fields.Int(
        required=True,
        validate=validate.Range(min=0)
    )
    qt_mat_prof = fields.Int(
        required=True,
        validate=validate.Range(min=0)
    )
    qt_mat_eja = fields.Int(
        required=True,
        validate=validate.Range(min=0)
    )
    qt_mat_esp = fields.Int(
        required=True,
        validate=validate.Range(min=0)
    )