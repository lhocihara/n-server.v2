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

@blueprint_externos.route("/login_externo", methods=['POST'])
@cross_origin()
def Logar_Externo():
    try:
        metodo_entrada = request.json['metodo_entrada']
        senha = request.json['senha']
        tipo_entrada = request.json['tipo_entrada']
        id_projeto = request.json['segredo']
    
        id_pessoa_logada = orq.login_pessoa(metodo_entrada, senha, tipo_entrada)
        print(str(pessoa_logada))
        
        pessoa_info = orq.verificar_id_usuario(id_pessoa_logada['segredo'])
        print(str(pessoa_info))
        
        projeto_info = orq.verificar_id_projeto_externos(id_projeto)
        if projeto_info:                  
            projeto_required_chaves = projeto_info['requerimentos']
            print(str(projeto_required_chaves))
            
            pessoa_req = []        
            
            for key in pessoa_info.keys():
                pessoa_req.append(key)
            print (str(pessoa_req))

            projeto_req = []

            for key in projeto_required_chaves.keys():
                projeto_req.append(key)
            print (str(projeto_req))

            missed_keys = []

            for key in projeto_req.keys():
                if key not in pessoa_req():
                    missed_keys.append(key)

            if (len(missed_keys) == 0):
                # O vinculo pode ser feito

                # retornar login: ok e que o status de vinculo: ok
                json_retorno = RespostasAPI('Vinculo : Ok',
                                    { 
                                        "status" : True,
                                        "segredo": id_pessoa_logada["segredo"]
                                    }
                                    ).JSON
                return json_retorno
            else:
                json_retorno = RespostasAPI('Vinculo : NOK',
                                    { 
                                        "status" : False,
                                        "campos_incompletos" : str(missed_keys)
                                    }
                                    ).JSON

    except StatusInternos as e:
        return e.errors
