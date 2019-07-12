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
app.register_blueprint(pessoa_blue)

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

##Definição do endpoint
@app.route("/panic", methods=['POST'])
def nao_entre_em_panico():
    return jsonify({"message": "Nao entre em panico, isso é soh um retorno padrao"})

## ----------------------------------------------------------
## Endpoint index
## ----------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")