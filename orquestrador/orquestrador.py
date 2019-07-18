# -*- coding: utf-8 -*-
import json
from flask import jsonify
from pymongo import MongoClient # Para acessar o MongoDB
from bson.objectid import ObjectId
import urllib.parse # (OPCIONAL) Para criar texto de URI 

from biblioteca_respostas.status_internos import StatusInternos

class Orquestrador(object):
    def __init__(self):
        print("\n[Orquestrador] instanciado com sucesso!\n")
        
        # Carregando com paramêtros de acesso para desenvolvedor
        usuario_banco = urllib.parse.quote_plus('dev_connect')
        senha_banco = urllib.parse.quote_plus('rgPuzhTgc8HAHFlV')

        # Criando conexão com o MongoDB
        conexao_servidor = MongoClient('mongodb+srv://%s:%s@cluster0-hygoa.gcp.mongodb.net/?retryWrites=true' % (usuario_banco, senha_banco))

        # Instanciando um gerenciador do banco de dados TCC
        self.conexao_bd = conexao_servidor.TCC

    def cadastrar_pessoa(self, pessoa):
        if self.verificar_cpf(pessoa["cpf"]):
            raise StatusInternos('SI-1', {'cpf': str(pessoa["cpf"])})
        if self.verificar_email(pessoa["email"]):
            raise StatusInternos('SI-2', {'email': str(pessoa["email"])})

        try:
            colecao_pessoas = self.conexao_bd.Pessoas
        except:
            raise StatusInternos('SI-4')
        
        try:
            #Chamada de função para inserir documento de cadastro
            pessoa_id = colecao_pessoas.insert_one(pessoa)
            
            # Chama função de cadastro do Blockchain
            print("\n[Orquestrador] pessoa cadastrada com sucesso!\n")
            print("id:" + str(pessoa_id.inserted_id))

            return(str(pessoa_id.inserted_id))
        except:
            raise StatusInternos('SI-3', {'pessoa': pessoa})

    def adcionar_dados_pessoa(self, pessoa):
        # simulando retorno OK
        return True
        
    def editar_dados_pessoa(self, pessoa):
        # simulando retorno OK
        return True

    def excluir_pessoa(self, pessoa_id_usuario):
        # simulando retorno OK
        return True

    def login_pessoa(self,valor_login, senha, tipo):  
        # Login por cpf
        if(tipo == '0'):
            metodo_login = "cpf"
        # Login por e-mail  
        elif(tipo == '1'):  
            metodo_login = "email"
        # Login com identificador errado
        else:
            print("[Orquestrador.ERRO] Método de login não foi identificado.")
            raise StatusInternos('SI-7', {"metodo_login": tipo, metodo_login: valor_login, 'senha': senha})

        try:
            if(self.conexao_bd.Pessoas.find({"$and": [{metodo_login: valor_login}, {"senha": senha}]}).limit(1).count() > 0):
                print("[Orquestrador] "+ metodo_login + ": '"+ valor_login +"' encontrado na coleção de Pessoas, exibindo documento retornado:")                
                

                dados_pessoa = self.conexao_bd.Pessoas.find({"$and": [{metodo_login: valor_login}, {"senha": senha}]})
                
                print(str({
                    "Segredo": str(dados_pessoa[0]['_id']),
                    "Usuario_nome": str(dados_pessoa[0]['nome_completo'])
                  }))

                return jsonify(
                    segredo= str(dados_pessoa[0]['_id']),
                    usuario_nome= str(dados_pessoa[0]['nome_completo'])
                  )
                
            else:
                print("[Orquestrador] "+ metodo_login + ": '"+ valor_login +"' não encontrado na coleção de Pessoas.")
                raise StatusInternos
        except Exception as e:
            print(e)
            raise StatusInternos('SI-6')

    def verificar_id_usuario(self,pessoa_id_usuario):
        try:
            if(self.conexao_bd.Pessoas.find({ "_id": ObjectId(pessoa_id_usuario)}).limit(1).count() > 0):
                print("[Orquestrador] id pessoa '" + str(pessoa_id_usuario) + "' encontrado na coleção de Pessoas, exibindo documento retornado:\n")

                dados_pessoa = self.conexao_bd.Pessoas.find({ "_id": ObjectId(pessoa_id_usuario)})
                
                print(str(dados_pessoa[0]))
                
                return dados_pessoa[0]
            else:
                print("[Orquestrador] id pessoa '" + str(pessoa_id_usuario) + "' não encontrado na coleção de Pessoas\n")
                
                return None 
        except Exception as e:
            print("[Orquestrador.ERRO] erro durante a execução do comando de seleção")
            raise(e)
        
      # raise Exception(CodigoStatusHttp(500).retorno())
    
    def verificar_cpf(self, pessoa_cpf):
        if(self.conexao_bd.Pessoas.find({"cpf": pessoa_cpf}).limit(1).count() > 0):
            return True
        else:
            return False
    
    def verificar_email(self, pessoa_email):
        if(self.conexao_bd.Pessoas.find({"email": pessoa_email}).limit(1).count() > 0):
            return True
        else:
            return False

    def verificar_metodo_login_existente(self, pessoa_cpf, pessoa_email):
        if(self.conexao_bd.Pessoas.find({"$or": [{"cpf": pessoa_cpf}, {"email": pessoa_email}]}).limit(1).count() > 0):
            return True
        else:
            return False
