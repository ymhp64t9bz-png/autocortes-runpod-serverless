# -*- coding: utf-8 -*-
"""
HYPERCLIP AI - LICENSE GUARD
Sistema de proteção baseado em Hardware ID (HWID).
"""

import uuid
import hashlib
import os

LICENSE_FILE = "license.key"

def get_hwid():
    """Gera um ID único baseado no hardware da máquina (MAC Address)."""
    mac = uuid.getnode()
    hwid_raw = f"HYPERCLIP_AI_SALT_{mac}"
    return hashlib.sha256(hwid_raw.encode()).hexdigest().upper()

def generate_license_key():
    """Gera a chave de licença válida para esta máquina (Uso interno/Admin)."""
    hwid = get_hwid()
    # A licença é um hash duplo do HWID para segurança
    license_key = hashlib.sha256(f"OFFICIAL_KEY_{hwid}".encode()).hexdigest().upper()
    return license_key

def validate_license():
    """
    Verifica se a licença atual é válida.
    Retorna: (bool, str) -> (Status, Mensagem)
    """
    if not os.path.exists(LICENSE_FILE):
        return False, "Arquivo de licença não encontrado."

    try:
        with open(LICENSE_FILE, "r") as f:
            stored_key = f.read().strip()
        
        expected_key = generate_license_key()
        
        if stored_key == expected_key:
            return True, "Licença Ativa."
        else:
            return False, "Licença Inválida para este Hardware."
            
    except Exception as e:
        return False, f"Erro ao ler licença: {e}"

def create_trial_license():
    """Cria uma licença válida automaticamente (Apenas para demonstração/dev)."""
    key = generate_license_key()
    with open(LICENSE_FILE, "w") as f:
        f.write(key)
    return key

if __name__ == "__main__":
    print(f"HWID: {get_hwid()}")
    print(f"Expected License: {generate_license_key()}")
    valid, msg = validate_license()
    print(f"Status: {msg}")
