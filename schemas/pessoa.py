# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# Definição do schema de validação do Json a ser recebido pela requisição HTTP
# ----------------------------------------------------------
schemaCadastro = {
    "title": "Pessoa",
    "type": "object",
    "required": ["nome_completo", "cpf", "data_nasc", "genero", "email", "senha"],
    "properties": {
        "nome_completo": {
            "type": "string", "pattern": "^[A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ ]+$"
        },
        "cpf": {
            "type": "string", "minLength": 11, "maxLength": 11
        },
        "rg": {
            "type": "object",
            "properties": {
                "emissor": {
                    "type": "string", "minLength": 3, "maxLength": 3
                },
                "numero": {
                    "type": "string", "maxLength": 14
                }
            }
        },
        "data_nasc": {
            "type": "string", "format": "date-time"
        },
        "genero": {
            "type": "string", "pattern": "^[M|F|D]$"
        },
        "email": {
            "type": "string", "format": "email"
        },
        "senha": {
            "type": "string", "minLength": 8 
        },
    },
         "additionalProperties": False
}


schemaLoginPessoa = {
  "title": "Login de Pessoa",
  "type": "object",
  "required": ["metodo_entrada", "senha", "tipo_entrada"],
  "properties": {
    "metodo_entrada": {
      "type": "string"
    },
    "senha": {
      "type": "string"
    },
    "tipo_entrada": {
      "type": "string", "pattern": "^[0|1]$"
    }
  },
    "additionalProperties": False
}

schemaEdicao = {
  "type": "object",
    "properties": {
      "_id":
      {
            "type": "string"
      },
      "dados_editados":  {
        "type": "object",
        "properties": {
          "nome_completo":
          {
            "type": "string", "pattern": "^[A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ ]+$"
          },
          "apelido":
          {
            "type": "string", "pattern": "^[A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ ]+$"
          },
          "cpf":
          {
            "type": "string", "minLength": 11, "maxLength": 11
          },
          "rg":
          {
            "type": "object",
            "properties": {
                "emissor": {
                    "type": "string", "minLength": 3, "maxLength": 3
                },
                "numero": {
                    "type": "string", "maxLength": 14
                }
            }
          },
          "data_nasc":
          {
            "type": "string", "format": "date-time"
          },
          "genero":
          {
            "type": "string", "pattern": "^[M|F|D]$"
          },
          "email":
          {
            "type": "string", "format": "email"
          },
          "senha":
          {
            "type": "string", "minLength": 8
          },
          "nacionalidade":
          {
            "type": "string"
          },
          "naturalidade":
          {
            "type": "object",
            "properties": {
              "pais": {
                "type": "string", "pattern": ""
              },
              "UF": {
                "type": "string", "maxLenght": 2
              },
              "cidade": {
                "type": "string"
              },
            }
          },
          "endereco": {
            "type": "object",
            "properties": {
              "CEP": {
                "type": "string"
              },
              "logradouro": {
                "type": "string"
              },
              "numero": {
                "type": "string"
              },
              "cidade": {
                "type": "string"
              },
              "UF": {
                "type": "string", "maxLenght": 2
              },
              "complemento": {
                "type": "string"
              },
            }
          },
        },
        "additionalProperties": False
      },              
      "dados_excluidos": {
          "type": "object",
      },
      "additionalProperties": False
    },
}

schemaAdicao = {
        "type": "object",
    "properties": {
        "nome_completo":
          {
            "type": "string", "pattern": "^[A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ ]+$"
          },
          "apelido":
          {
            "type": "string", "pattern": "^[A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ ]+$"
          },
        "cpf":
          {
            "type": "string", "minLength": 11, "maxLength": 11
          },
        "rg":
            {
            "type": "object",
            "properties": {
                "emissor":{
                    "type": "string", "minLength": 3, "maxLength": 3
                },
                "numero": {
                    "type": "string", "maxLength": 14
                }
              }
            },
        "data_nasc":
          {
            "type": "string", "format": "date-time"
          },
        "genero":
          {
            "type": "string", "pattern": "^[M|F|D]$"
          },
        "email":
          {
            "type": "string", "format": "email"
          },
        "senha":
          {
            "type": "string", "minLength": 8
          },
        "nacionalidade":
          {
            "type": "string", "pattern" : " "
          },
        "naturalidade" :
          {
          "type" : "object",
          "properties" : {
            "pais" : {
              "type" : "string", "pattern" : ""
            },
            "UF" : {
              "type" : "string", "maxLenght" : 2
            },
            "cidade" : {
              "type" : "string"
            },
          },
          "endereco" : {
            "type" : "object",
            "properties" : {
              "CEP" : {
                "type" : "string"
              },
              "logradouro" : {
                "type" : "string"
              },
              "numero" : {
                "type" : "number"
              },
              "cidade" : {
                "type" : "string"
              },
              "UF" : {
              "type" : "string", "maxLenght" : 2
            },
            "complemento" : {
              "type" : "string"
            }
          }
        }
      }
    }
  }
