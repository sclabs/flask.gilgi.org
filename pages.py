index = {
    "header": "welcome to flask.gilgi.org",
    "prompts": [
        "you have reached the gilgi.org network utility server",
        "what can we help you with?"
        ],
    "options": [
        {"link": "/tsstatus", "text": "check status of scoot's canoe teamspeak server"},
        {"link": "/ventstatus", "text": "check status of scoot's canoe ventrilo server"},
        {"link": "/cssstatus", "text": "check status of scoot's canoe cs:s server"},
        {"link": "http://icanhas.cheezburger.com", "text": "show me funny cat pictures"},
        ]
    }

cssstatus = {
    "header": "cssstatus",
    "prompts": [
        "you have requested the status of the scoot's canoe cs:s server",
        "how would you like your response to be formatted?"
        ],
    "options": [
        {"link": "/cssstatus/json", "text": "json"},
        {"link": "/cssstatus/html", "text": "html"},
        {"link": "/", "text": "i just want to go home"},
        ]
    }

tsstatus = {
    "header": "tsstatus",
    "prompts": [
        "you have requested the status of the scoot's canoe teamspeak server",
        "how would you like your response to be formatted?"
        ],
    "options": [
        {"link": "/tsstatus/json", "text": "json"},
        {"link": "/tsstatus/html", "text": "html"},
        {"link": "/", "text": "i just want to go home"},
        ]
    }

ventstatus = {
    "header": "ventstatus",
    "prompts": [
        "you have requested the status of the scoot's canoe ventrilo server",
        "how would you like your response to be formatted?"
        ],
    "options": [
        {"link": "/ventstatus/json", "text": "json"},
        {"link": "/ventstatus/html", "text": "html"},
        {"link": "/", "text": "i just want to go home"},
        ]
    }
