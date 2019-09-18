# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# Importação dos módulos padrões
# ----------------------------------------------------------
from flask_json_schema import JsonSchema, JsonValidationError
from flask import Flask, Blueprint, request, jsonify
from flask_cors import CORS, cross_origin
from bson.objectid import ObjectId
from datetime import datetime, timedelta


import pymongo
import dns
import hashlib

# ----------------------------------------------------------
# Importação do orquestrador da conexão com BD
# ----------------------------------------------------------
from orquestrador.orquestrador import Orquestrador
# ----------------------------------------------------------
# Importação dos Objetos de tratamento de erros
# ----------------------------------------------------------
from biblioteca_respostas.status_internos import StatusInternos
from biblioteca_respostas.respostas_api import RespostasAPI
# ----------------------------------------------------------
# Importação dos schemas referentes a Externos
# ----------------------------------------------------------

orq = Orquestrador()

# ----------------------------------------------------------
# Definição do Blueprint
# ----------------------------------------------------------
blueprint_externos = Blueprint("Externos", __name__)

# ----------------------------------------------------------
# Definição do Subapp e Schema
# ----------------------------------------------------------
app = Flask("Externos")
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
schema = JsonSchema(app)

# ----------------------------------------------------------
# Rotas dos serviços para o APP
# ----------------------------------------------------------
##
# @pessoa_blue.route: A rota do endpoint
# @schema.validate: O schema a ser validado durante a requisição
# ----------------------------------------------------------


@blueprint_externos.route("/gera_token", methods=['POST'])
@cross_origin()
def Gerar_Token():
    try:       
        segredo = request.json['segredo']
        projeto_existente = orq.verificar_id_projeto_externos(segredo)
        if projeto_existente:
            token = hashlib.sha256((str(segredo) + str(datetime.now())).encode()).hexdigest()
            vencimento = datetime.now() + timedelta(minutes=5)
            orq.armazenar_tokens(segredo, token, vencimento)
            return RespostasAPI('Token gerado com sucesso',
                                {
                                    'token': str(token),
                                }
                                ).JSON
        else:
            raise StatusInternos('SI-21', {'projeto': segredo})
    except StatusInternos as e:
        return e.errors


@blueprint_externos.route("/valida_token", methods=['POST'])
@cross_origin()
def Validar_Token():
    try:        
        token = request.json['token']
        info_token = orq.consulta_info_token(token)
        vencimento_token = info_token['vencimento']
        projeto_token = info_token['id_projeto']       
        if datetime.now() < vencimento_token:
            projeto = orq.verificar_id_projeto(projeto_token)
            json_retorno = RespostasAPI('Token válido',
                                    { "token" : token,
                                      "id_projeto" : projeto_token,
                                      "objeto_projeto" : projeto  
                                    }
                                    ).JSON
            return json_retorno      
        else:
            raise StatusInternos('SI-22', {'projeto': projeto_token})
    except StatusInternos as e:
        return e.errors
