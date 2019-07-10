# -*- coding: utf-8 -*-
import os, pymongo
from flask import Flask, jsonify, request, render_template
from flask_json_schema import JsonSchema, JsonValidationError

from mod.pessoa import pessoa_blue

app = Flask(__name__)
schema = JsonSchema(app)

app.config.from_object('settings')
app.register_blueprint(pessoa_blue, url_prefix="/pessoa")

##app.config['MONGO_DBNAME'] = 'TCC.Pessoas'
##app.config['MONGO_URI'] = 'mongodb+srv://admin_connect:<#_n2noficial_#>@cluster0-hygoa.gcp.mongodb.net/test?retryWrites=true&w=majority'


## ----------------------------------------------------------
## Rotas padrões
## ----------------------------------------------------------

## Setando tratamento de erros na validação
@app.errorhandler(JsonValidationError)
def validation_error(e):
    return jsonify({ 'Erro': e.message, 'Errors': [validation_error.message for validation_error in e.errors]})

## Endpoint de boas vindas
@app.route("/hi")
def boas_vindas():
    return render_template("bem_vindos.html")

## Endpoint index
@app.route("/")
def index():
    return render_template("index.html")


## ----------------------------------------------------------
## configuração de IP e porta
## ----------------------------------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)