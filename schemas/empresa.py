# -*- coding: utf-8 -*-

# JsonSchemas para validações de requisições HTTP tratando de empresas

schemaCadastro = {
    "title": "Empresa",
    "type": "object",
    "required": ["razao_social", "cnpj", "nome_fantasia", "ie", "endereco", "contatos_internos", "responsavel"],
    "properties":
    {
        "razao_social": {
            "type": "string"
        },
        "cnpj": {
            "type": "string", "minLength": 14, "maxLength": 14
        },
        "nome_fantasia": {
            "type": "string"
        },
        "ie": {
            "type": "string"
        },
        "nire": {
            "type": "string"
        },
        "endereco": {
            "type": "array",
            "items": {
                "type": "object",
                "requeired": ["cep", "logradouro", "numero", "cidade", "UF", "tipo"],
                "properties": {
                    "cep": {
                        "type": "string"
                    },
                    "logradouro": {
                        "type": "string"
                    },
                    "bairro": {
                        "type": "string"
                    },
                    "numero": {
                        "type": "string"
                    },
                    "cidade": {
                        "type": "string", "pattern": "^[A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ ]+$"
                    },
                    "UF": {
                        "type": "string", "maxLength": 2
                    },
                    "complemento": {
                        "type": "string"
                    },
                    "tipo": {
                        "type": "string", "pattern": "^[M|F]$"
                    }
                }
            }
        },
        "contatos_internos": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["departamento", "ddi", "ddd", "numero", "email"],
                "properties": {
                    "departamento": {
                        "type": "string"
                    },
                    "ddi": {
                        "type": "string", "maxLength": 3
                    },
                    "ddd": {
                        "type": "string", "maxLength": 2
                    },
                    "numero": {
                        "type": "string", "minLength": 8, "maxLength": 9
                    },
                    "email": {
                        "type": "string", "format": "email"
                    }
                }
            }
        },
        "responsavel": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["nome_completo", "cargo", "email", "telefone"],
                "properties": {
                    "nome_completo": {
                        "type": "string", "pattern": "^[A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ ]+$"
                    },
                    "cargo": {
                        "type": "string", "pattern": "^[A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ ]+$"
                    },
                    "nacionalidade": {
                        "type": "string", "pattern": "^[A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ ]+$"
                    },
                    "cpf": {
                        "type": "string", "minLength": 11, "maxLength": 11
                    },
                    "rg:":
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
                    "email": {
                        "type": "string", "format": "email"
                    },
                    "estado_civil":
                    {
                        "type": "string", "pattern": "^[CA|SO|SE|DI|VI]+$"
                    },
                    "telefone": {
                        "type": "object",
                        "required": ["ddi", "ddd", "numero"],
                        "properties": {
                            "ddi": {
                                "type": "string", "minLength": 2, "maxLength": 2
                            },
                            "ddd": {
                                "type": "string", "minLength": 2, "maxLength": 2
                            },
                            "numero": {
                                "type": "string", "minLength": 8, "maxLength": 9
                            }
                        }
                    }
                }
            }
        }
    },
    "additionalProperties": False
}
