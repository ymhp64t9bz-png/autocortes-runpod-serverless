# -*- coding: utf-8 -*-
"""
TESTE DE INTEGRAÇÃO - PREDIÇÃO TEMPORAL
Verifica se o TitleManager está gerando títulos baseados no roteiro/tempo
"""
import sys
import os
from pathlib import Path

# Adiciona diretório raiz
sys.path.append(str(Path(__file__).parent))

import config
from SISTEMA_DE_TITULOS.manager import TitleManager

def testar_predicao():
    print("="*60)
    print("TESTE DE PREDICAO TEMPORAL (GEMINI AI)")
    print("="*60)
    
    # Verifica chave
    if not config.GEMINI_API_KEY:
        print("[ERRO] Chave API nao encontrada no config.py")
        return

    print(f"[OK] Chave API detectada: {config.GEMINI_API_KEY[:5]}...")
    
    # Instancia Manager
    manager = TitleManager(api_key=config.GEMINI_API_KEY)
    
    # Casos de Teste
    filme = "Vingadores_Ultimato_1080p.mp4"
    
    print(f"\n[FILME]: {filme}")
    
    # Cena 1 (Início - Minutos 0-3)
    print("\n[Cena 1 - Inicio (0-3 min)]")
    t1 = manager.generate_smart_title(filme, 0)
    print(f"   Titulo: {t1}")
    
    # Cena 20 (Meio - Minutos 60-63)
    print("\n[Cena 20 - Meio (60-63 min)]")
    t2 = manager.generate_smart_title(filme, 20)
    print(f"   Titulo: {t2}")
    
    # Cena 60 (Final - Minutos 180-183)
    print("\n[Cena 60 - Climax (180-183 min)]")
    t3 = manager.generate_smart_title(filme, 60)
    print(f"   Titulo: {t3}")

    print("\n" + "="*60)
    print("TESTE CONCLUIDO")

if __name__ == "__main__":
    testar_predicao()
