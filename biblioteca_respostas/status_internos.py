# -*- coding: utf-8 -*-
from flask import jsonify
from datetime import datetime 
class StatusInternos(Exception):
  def __init__(self, codigo_status, objeto=None):
    # self.dados = ""
    
    self.codigo = codigo_status
    self.objeto = objeto

    if codigo_status == 'SI-1':
      self.mensagem = "CPF existente na coleção Pessoas."
    elif codigo_status == 'SI-2':
      self.mensagem = "E-mail existente na coleção Pessoas."
    elif codigo_status == 'SI-3':
      self.mensagem = "Erro ao cadastrar pessoa."
    elif codigo_status == 'SI-4':
      self.mensagem = "Erro acessar coleção."
    elif codigo_status == 'SI-5':
      self.mensagem = "Dado existente no banco de dados."
    elif codigo_status == 'SI-6':
      self.mensagem = "Erro ao logar pessoa."
    elif codigo_status == 'SI-7':
      self.mensagem = "Método de login não foi identificado."
    elif codigo_status == 'SI-8':
      self.mensagem = "Pessoa não encontrada."
    elif codigo_status == 'SI-9':
      self.mensagem = "CNPJ existente na coleção de Empresas."
    elif codigo_status == 'SI-10':
      self.mensagem = "Erro ao cadastrar empresa."
    elif codigo_status == 'SI-11':
      self.mensagem = "Projeto existente na coleção de Projetos."
    elif codigo_status == 'SI-12':
      self.mensagem = "Erro ao cadastrar projeto."
    elif codigo_status == 'SI-13': 
      self.mensagem = "Empresa não encontrada."
    elif codigo_status == 'SI-21': 
      self.mensagem = "Projeto não existente na coleção de dados" 
    elif codigo_status == 'SI-22': 
      self.mensagem = "Token expirado." 
    else: 
      self.mensagem = "Situação não catalogada."
    
    self.errors = self.retorno()
    
  def retorno(self):
    print("\n[Status retorno] JSON de retorno:\n" + str({
      "codigo": self.codigo,
      "mensagem": self.mensagem,
      "objeto": self.objeto,
      "timestamp": str(datetime.now())
    }) + "\n")
    
    return jsonify(
      codigo= self.codigo,
      mensagem= self.mensagem,
      objeto= self.objeto,
      timestamp= str(datetime.now())
    ), 400
