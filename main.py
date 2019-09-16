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
from rotas.pessoa import blueprint_pessoa
from rotas.empresa import blueprint_empresa
from rotas.projeto import blueprint_projeto
from rotas.externos import blueprint_externos


## ----------------------------------------------------------
## Instanciando a API
## ----------------------------------------------------------
app = Flask("n-server")
app.config.from_object('settings')


## ----------------------------------------------------------
## Lista de Blueprints
## ----------------------------------------------------------
app.register_blueprint(blueprint_pessoa,url_prefix="/pessoa")
app.register_blueprint(blueprint_empresa,url_prefix="/empresa")
app.register_blueprint(blueprint_projeto,url_prefix="/projeto")
app.register_blueprint(blueprint_externos,url_prefix="/externos")



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
@app.route("/panic", methods=['GET'])
def nao_entre_em_panico():
    return jsonify({"message": "Nao entre em panico, isso é soh um retorno padrao"})

## ----------------------------------------------------------
## Endpoint index
## ----------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")
