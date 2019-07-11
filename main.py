# -*- coding: utf-8 -*-
## ----------------------------------------------------------
## Importação dos módulos padrões
## ----------------------------------------------------------
import os, pymongo
from flask import Flask, jsonify, request, render_template
from flask_json_schema import JsonSchema, JsonValidationError


## ----------------------------------------------------------
## Importação dos módulos dos Blueprints
## ----------------------------------------------------------
from endpoints.pessoa import pessoa_blue


## ----------------------------------------------------------
## Instanciando a API
## ----------------------------------------------------------
app = Flask(__name__)
app.config.from_object('settings')


## ----------------------------------------------------------
## Lista de Blueprints
## ----------------------------------------------------------
app.register_blueprint(pessoa_blue, url_prefix="/pessoa")

##app.config['MONGO_DBNAME'] = 'TCC.Pessoas'
##app.config['MONGO_URI'] = 'mongodb+srv://admin_connect:<#_n2noficial_#>@cluster0-hygoa.gcp.mongodb.net/test?retryWrites=true&w=majority'


## ----------------------------------------------------------
## Tratamento de erros na validação
## ----------------------------------------------------------
@app.errorhandler(JsonValidationError)
def validation_error(e):
    return jsonify({ 'Erro': e.message, 'Errors': [validation_error.message for validation_error in e.errors]})


## ----------------------------------------------------------
## Rotas padrões
## ----------------------------------------------------------
##
## @pessoa_blue.route: A rota do endpoint
## ----------------------------------------------------------

## ----------------------------------------------------------
## Endpoint de boas vindas
## ----------------------------------------------------------
@app.route("/hi")
def boas_vindas():
    return render_template("bem_vindos.html")

## ----------------------------------------------------------
## Endpoint index
## ----------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")


## ----------------------------------------------------------
## configuração de IP e porta
## ----------------------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)