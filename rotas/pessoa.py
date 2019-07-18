# ----------------------------------------------------------
# Importação dos módulos padrões
# ----------------------------------------------------------
from flask_json_schema import JsonSchema, JsonValidationError
from flask import Flask, Blueprint, request, jsonify
import pymongo
import dns

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
# Importação dos schemas referentes a Pessoa
# ----------------------------------------------------------
from schemas.pessoa import schemaCadastro, schemaLoginPessoa


orq = Orquestrador()

# ----------------------------------------------------------
# Definição do Blueprint
# ----------------------------------------------------------
blueprint_pessoa = Blueprint("Pessoa", __name__)

# ----------------------------------------------------------
# Definição do Subapp e Schema
# ----------------------------------------------------------
app = Flask("Pessoa")
schema = JsonSchema(app)

# ----------------------------------------------------------
# Rotas dos serviços para o APP
# ----------------------------------------------------------
##
# @pessoa_blue.route: A rota do endpoint
# @schema.validate: O schema a ser validado durante a requisição
# ----------------------------------------------------------

# ----------------------------------------------------------
# Endpoint de cadastro inicial de pessoas
# ----------------------------------------------------------
@blueprint_pessoa.route("/cadastro", methods=['POST'])
@schema.validate(schemaCadastro)
def Cadastrar_Pessoa():
    """ Endpoint responsável por cadastrar pessoas dentro da base de dados.

        `Requisição:` Deve ser feita com base no `SchemaCadastro`.

        `Resposta:` Será com base na `Classe StatusInternos` caso houver `erros internos`, ou na `Classe RespostasAPI` para formatar as referidas respostas.
    """
    pessoa_request = request.json

    print("\n[Requisição-POST] /pessoa/cadastro:\n" +
          str(pessoa_request) + "\n")

    try:
        retorno_id = orq.cadastrar_pessoa(pessoa_request)

        json_retorno = RespostasAPI('Cadastro realizado com sucesso',
                {
                    'segredo': str(retorno_id),
                    'nome_usuario': str(pessoa_request['nome_completo'])
                }
            ).JSON

        return json_retorno
    except StatusInternos as e:
        return e.errors


# ----------------------------------------------------------
# Endpoint de cadastro inicial de pessoas
# ----------------------------------------------------------
@blueprint_pessoa.route("/login", methods=['POST'])
@schema.validate(schemaLoginPessoa)
def Logar_Pessoa():

    login_request = request.json

    print("\n[Requisição-POST] /pessoa/login:\n" + str(login_request) + "\n")

    try:
        metodo_entrada = login_request['metodo_entrada']
        senha = login_request['senha']
        tipo_entrada = login_request['tipo_entrada']

        retorno = orq.login_pessoa(metodo_entrada, senha, tipo_entrada)
        print(retorno)
        json_retorno = RespostasAPI('Login realizado com sucesso',
        {
                'segredo': retorno["segredo"],
                'nome_usuario': retorno["nome_usuario"],
        }
        ).JSON

        return json_retorno
    except StatusInternos as e:
        return e.errors
