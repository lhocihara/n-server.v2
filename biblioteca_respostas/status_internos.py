# -*- coding: utf-8 -*-
from flask import jsonify

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
      self.mensagem = "Login inválido."
    else: 
      self.mensagem = "Situação não catalogada."
    
    self.errors = self.retorno()
    
  def retorno(self):
    if (self.objeto):
      print("\n[Status interno] JSON de retorno: \n" + str({
        "codigo": self.codigo,
        "mensagem": self.mensagem,
        "objeto": self.objeto,
        "timestamp": "0000-00-00 00000000000"
      }) + "\n")

    
      return jsonify(
        codigo= self.codigo,
        mensagem= self.mensagem,
        objeto= self.objeto,
        timestamp= "0000-00-00 00000000000"
      )
    else:
      print("\n[Status retorno] JSON de retorno: \n" + str({
        "codigo": self.codigo,
        "mensagem": self.mensagem,
        "timestamp": "0000-00-00 00000000000"
      }) + "\n")

      return jsonify(
        codigo= self.codigo,
        mensagem= self.mensagem, 
        timestamp= "0000-00-00 00000000000"
      )