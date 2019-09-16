# -*- coding: utf-8 -*-

# JsonSchemas para validações de requisições HTTP tratando de projetos


schemaCadastro = {
    "title": "Projeto",
    "type": "object",
    "required": ["nome_projeto", "empresa_id", "requerimentos", "encarregado_dados"],
    "properties": {
        "nome_projeto": {
            "type": "string"
        },
        "empresa_id": {
            "type": "string"
        },
        "requerimentos": {
            "type": "array",
            "items": {
                "type": "object"
            },
            "properties": {
                "campo": {
                    "type": "string"
                },
                "motivo": {
                    "type": "string"
                }
            },
            "encarregado_dados": {
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
                        "email": {
                            "type": "string", "format": "email"
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
                                },
                            },
                            "additionalProperties": False
                        }
                    },
                },
            },
            "additionalProperties": False
        },
        "additionalProperties": False
    }
}
