import Flask
from routes.requisicao import requisicao_bp

app = Flask(__name__)
app.secret_key = "chave_segura"


app.register_blueprint(requisicao_bp)

if __name__ == "__main__":
    app.run(debug=True)

