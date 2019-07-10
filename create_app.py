# coding: utf-8
## ----------------------------------------------------------
## Modulos padrões
## ----------------------------------------------------------
import os
from flask import Flask, jsonify, render_template
from flask_json_schema import JsonSchema, JsonValidationError

## ----------------------------------------------------------
## Blueprints de Endpoint
## ----------------------------------------------------------
from blueprints_list.pessoa import pessoa_blueprint


## ----------------------------------------------------------
## Instanciando projeto N
## ----------------------------------------------------------
app = Flask("n")
app.config.from_object('settings')


## ----------------------------------------------------------
## Registrando Blueprints
## ----------------------------------------------------------
app.register_blueprint(pessoa_blueprint)

## ----------------------------------------------------------
## Tratamento de erros
## ----------------------------------------------------------
@app.errorhandler(JsonValidationError)
def validation_error(e):
    return jsonify({ 'Erro': e.message, 'Errors': [validation_error.message for validation_error in e.errors]})




## ----------------------------------------------------------
## Rotas padrões
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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)