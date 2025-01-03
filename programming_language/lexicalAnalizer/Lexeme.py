import re

TOKEN_PATTERNS = [
    ("KEYWORD", re.compile(r"\b(recipe|input|output|tool_required|quantity|func|if|else|while|for|craft|log|int|float|char|return)\b")),
    ("NUMBER", re.compile(r"\b\d+(\.\d+)?\b")),  # Números enteros o decimales
    ("STRING", re.compile(r'\"[^\"]*\"')),       # Cadenas entre comillas
    ("IDENTIFIER", re.compile(r"\b[a-zA-Z_][a-zA-Z0-9_]*\b")),  # Identificadores válidos
    ("SYMBOL", re.compile(r"[{}\[\]:,;()]")),     # Símbolos delimitadores
    ("OPERATOR", re.compile(r"[=+*/<>!%\-]{1,2}")),  # Operadores (incluye +=, ==, etc.)
    ("COMMENT", re.compile(r"//.*")),            # Comentarios en línea
    ("WHITESPACE", re.compile(r"\s+")),          # Espacios en blanco
]