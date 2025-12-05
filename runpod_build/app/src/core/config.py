# -*- coding: utf-8 -*-
"""
CONFIGURAÇÕES DO SISTEMA AUTOCORTES
Sistema Profissional de Automação de Cortes para Redes Sociais
"""

import os
from pathlib import Path

# ==================== CONFIGURAÇÕES DE PASTAS ====================
BASE_DIR = Path(__file__).parent.absolute()
PASTA_INPUTS = BASE_DIR / "inputs"
PASTA_OUTPUTS = BASE_DIR / "outputs"
PASTA_TEMP = BASE_DIR / "temp"
PASTA_TEMPLATE = BASE_DIR / "template"
PASTA_LOGS = BASE_DIR / "logs"

# ==================== CONFIGURAÇÕES DE VÍDEO ====================
# Formatos de vídeo suportados
FORMATOS_VIDEO = ['.mp4', '.avi', '.mov', '.mkv', '.m4v', '.wmv', '.flv', '.webm']

# Configurações de resolução para diferentes plataformas
RESOLUCOES = {
    'tiktok': (1080, 1920),      # 9:16 - Vertical
    'instagram': (1080, 1920),   # 9:16 - Vertical
    'youtube_shorts': (1080, 1920),  # 9:16 - Vertical
    'youtube': (1920, 1080),     # 16:9 - Horizontal
    'facebook': (1080, 1080),    # 1:1 - Quadrado
}

# Configuração padrão
RESOLUCAO_PADRAO = RESOLUCOES['tiktok']
LARGURA_PADRAO, ALTURA_PADRAO = RESOLUCAO_PADRAO

# ==================== CONFIGURAÇÕES DE CORTE ====================
# Durações ideais para cada plataforma (em segundos)
DURACOES = {
    'tiktok': (15, 60),          # Mínimo 15s, Máximo 60s
    'instagram': (15, 90),       # Mínimo 15s, Máximo 90s
    'youtube_shorts': (15, 60),  # Mínimo 15s, Máximo 60s
    'youtube': (30, 300),        # Mínimo 30s, Máximo 5min
}

# Duração padrão dos cortes
DURACAO_MINIMA = 15  # segundos
DURACAO_MAXIMA = 60  # segundos
DURACAO_IDEAL = 30   # segundos

# ==================== CONFIGURAÇÕES DE ANÁLISE ====================
# Detecção de cenas
THRESHOLD_MUDANCA_CENA = 30.0  # Sensibilidade para detectar mudanças de cena
MIN_DURACAO_CENA = 3.0         # Duração mínima de uma cena em segundos
INTERVALO_ANALISE = 1.0        # Intervalo entre frames analisados (segundos)

# Detecção de áudio
THRESHOLD_VOLUME = -30         # dB - Threshold para detectar silêncio
# Efeitos visuais
APLICAR_ZOOM = True
INTENSIDADE_ZOOM = 1.1  # 1.0 = sem zoom, 1.2 = 20% zoom
DURACAO_ZOOM = 2.0  # segundos

# Filtros de cor
APLICAR_FILTROS = True
SATURACAO = 1.2  # 1.0 = normal, >1.0 = mais saturado
CONTRASTE = 1.1  # 1.0 = normal, >1.0 = mais contraste
BRILHO = 1.0     # 1.0 = normal, >1.0 = mais brilho

# ==================== CONFIGURAÇÕES DE TEXTO ====================
# Legendas automáticas
GERAR_LEGENDAS = False
FONTE_LEGENDA = 'Arial-Bold'
TAMANHO_FONTE = 60
COR_FONTE = 'white'
COR_CONTORNO = 'black'
ESPESSURA_CONTORNO = 3

# ==================== CONFIGURAÇÕES DE CATEGORIZAÇÃO ====================
# Tipos de cortes detectados
TIPOS_CORTE = {
    'acao': {
        'nome': 'Ação',
        'cor': '#FF4444',
        'prioridade': 5,
        'descricao': 'Cenas com muito movimento e ação'
    },
    'dialogo': {
        'nome': 'Diálogo',
        'cor': '#4444FF',
        'prioridade': 3,
        'descricao': 'Cenas com conversas importantes'
    },
    'emocional': {
        'nome': 'Emocional',
        'cor': '#FF44FF',
        'prioridade': 4,
        'descricao': 'Momentos emocionantes ou dramáticos'
    },
    'comedia': {
        'nome': 'Comédia',
        'cor': '#FFFF44',
        'prioridade': 4,
        'descricao': 'Momentos engraçados ou cômicos'
    },
    'epico': {
        'nome': 'Épico',
        'cor': '#FF8844',
        'prioridade': 5,
        'descricao': 'Cenas épicas e impactantes'
    },
    'viral': {
        'nome': 'Viral',
        'cor': '#44FF44',
        'prioridade': 5,
        'descricao': 'Potencial viral alto'
    }
}

# ==================== CONFIGURAÇÕES DE PERFORMANCE ====================
# Threads e processamento paralelo
NUM_THREADS = 8
USAR_GPU = True  # Tentar usar aceleração por GPU se disponível

# Memória
MAX_MEMORIA_MB = 4096  # Máximo de memória RAM a usar
LIMPAR_CACHE = True    # Limpar cache após cada processamento

# ==================== CONFIGURAÇÕES DE LOG ====================
# Níveis de log: DEBUG, INFO, WARNING, ERROR, CRITICAL
NIVEL_LOG = 'INFO'
FORMATO_LOG = '[%(asctime)s] %(levelname)s: %(message)s'
DATA_LOG = '%Y-%m-%d %H:%M:%S'

# ==================== CONFIGURAÇÕES AVANÇADAS ====================
# Detecção de faces (opcional)
DETECTAR_FACES = False
MIN_CONFIANCA_FACE = 0.7

# Análise de sentimento (opcional)
ANALISAR_SENTIMENTO = False

# Detecção de objetos (opcional)
DETECTAR_OBJETOS = False

# ==================== CONFIGURAÇÕES DE QUALIDADE ====================
# Configurações de codec e qualidade
VIDEO_CODEC = 'libx264'
AUDIO_CODEC = 'aac'
VIDEO_BITRATE = '5000k'
AUDIO_BITRATE = '192k'
FPS_PADRAO = 30
PRESET = 'ultrafast'  # ultrafast (recomendado para testes), superfast, veryfast, faster, fast, medium, slow, slower, veryslow
CRF = 23  # 0-51, maior = menor tamanho e menor qualidade (18-28 recomendado para web)

# ==================== CONFIGURAÇÕES DE PERFORMANCE ====================
# Threads e processamento paralelo
NUM_THREADS = os.cpu_count()
USAR_GPU = True  # Tentar usar aceleração por GPU se disponível

# Memória
MAX_MEMORIA_MB = 4096  # Máximo de memória RAM a usar
LIMPAR_CACHE = True    # Limpar cache após cada processamento

# ==================== CONFIGURAÇÕES DE LOG ====================
# Níveis de log: DEBUG, INFO, WARNING, ERROR, CRITICAL
NIVEL_LOG = 'INFO'
FORMATO_LOG = '[%(asctime)s] %(levelname)s: %(message)s'
DATA_LOG = '%Y-%m-%d %H:%M:%S'

# ==================== CONFIGURAÇÕES DE IA ====================
# Chave da API do Google Gemini (Necessária para títulos inteligentes)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyB1xrzEStrgNAEdzyYzHtE0odJJlvDLAmM")

# ==================== FUNÇÕES AUXILIARES ====================
def criar_estrutura_pastas():
    """Cria todas as pastas necessárias para o sistema"""
    pastas = [PASTA_INPUTS, PASTA_OUTPUTS, PASTA_TEMP, PASTA_TEMPLATE, PASTA_LOGS]
    for pasta in pastas:
        pasta.mkdir(parents=True, exist_ok=True)
    return True

def validar_configuracao():
    """Valida se todas as configurações estão corretas"""
    erros = []
    
    # Valida durações
    if DURACAO_MINIMA >= DURACAO_MAXIMA:
        erros.append("DURACAO_MINIMA deve ser menor que DURACAO_MAXIMA")
    
    # Valida resolução
    if LARGURA_PADRAO <= 0 or ALTURA_PADRAO <= 0:
        erros.append("Resolução inválida")
    
    # Valida qualidade
    if not (0 <= CRF <= 51):
        erros.append("CRF deve estar entre 0 e 51")
    
    if erros:
        raise ValueError(f"Erros na configuração: {', '.join(erros)}")
    
    return True

# Valida configuração ao importar
validar_configuracao()
