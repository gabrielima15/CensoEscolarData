from helpers.application import app
from controllers.instituicaoEnsinoController import instituicoes_bp

app.register_blueprint(instituicoes_bp)


if __name__ == "__main__":
    app.run(debug=True, port=5000)