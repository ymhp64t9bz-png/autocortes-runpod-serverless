# -*- coding: utf-8 -*-
"""
Configurações do AnimeCut
"""

# ==================== CONFIGURAÇÕES DE DETECÇÃO ====================

# Sensibilidade padrão para detecção de cenas em animes
DEFAULT_SENSITIVITY = 25.0

# Intervalo de frames para análise (menor = mais preciso, mais lento)
DEFAULT_FRAME_INTERVAL = 15

# Detectar opening/ending por padrão
DEFAULT_DETECT_OPENING = True

# ==================== CONFIGURAÇÕES DE PROCESSAMENTO ====================

# Duração máxima padrão dos cortes (segundos)
DEFAULT_MAX_DURATION = 45

# Posição vertical padrão (0.0 = topo, 0.5 = centro, 1.0 = base)
DEFAULT_VERTICAL_POSITION = 0.5

# Adicionar borda por padrão
DEFAULT_ADD_BORDER = True

# ==================== CONFIGURAÇÕES DE VÍDEO ====================

# Dimensões do vídeo de saída (vertical 9:16)
OUTPUT_WIDTH = 1080
OUTPUT_HEIGHT = 1920

# Codec de vídeo
VIDEO_CODEC = 'libx264'

# Codec de áudio
AUDIO_CODEC = 'aac'

# FPS do vídeo de saída
OUTPUT_FPS = 30

# Preset de codificação (ultrafast, fast, medium, slow, veryslow)
# 'slow' oferece melhor qualidade para anime
ENCODING_PRESET = 'slow'

# ==================== CONFIGURAÇÕES DE GPU ====================

# Usar aceleração por GPU (NVIDIA CUDA)
USE_GPU = True

# Codec de vídeo com GPU (h264_nvenc para NVIDIA)
GPU_VIDEO_CODEC = 'h264_nvenc'

# Preset de GPU NVENC (slow, medium, fast)
# Nota: Usamos presets legados para maior compatibilidade
GPU_PRESET = 'slow'  # Equivalente a alta qualidade

# Qualidade NVENC (CQ - Constant Quality)
# 0-51, onde menor = melhor qualidade (recomendado: 18-23 para anime)
GPU_CQ = 19  # Alta qualidade para anime

# Rate control NVENC
GPU_RC = 'vbr'  # vbr, cbr, ou vbr_hq

# Usar GPU para detecção de cenas (OpenCV CUDA)
USE_GPU_DETECTION = True

# Threads para processamento (ajustado para GPU)
GPU_THREADS = 4  # Menos threads quando usando GPU

# Bitrate de vídeo (maior = melhor qualidade)
VIDEO_BITRATE = '8000k'

# Threads para processamento (CPU)
PROCESSING_THREADS = 8

# ==================== CONFIGURAÇÕES DE IA (GEMINI) ====================

# Chave de API do Google Gemini
# Você pode definir aqui ou criar um arquivo .env com GEMINI_API_KEY=sua_chave
GEMINI_API_KEY = "AIzaSyBYNwQ3l2YfxKycFaWdOVFS4iJwbBevZzM"

# ==================== CONFIGURAÇÃO DE MODELOS GEMINI ====================
# Sistema de Fallback: Tenta usar o modelo mais recente, se falhar usa o estável

# MODELO PRIMÁRIO: Gemini 2.5 Flash (Mais recente e poderoso)
# Requer: Faturamento ativado no Google AI Studio
# Benefícios: Mais rápido, melhor qualidade, mais contexto
GEMINI_MODEL_PRIMARY = "gemini-2.5-flash"

# MODELO SECUNDÁRIO: Gemini 1.5 Flash (Estável e gratuito)
# Funciona: No Free Tier sem faturamento
# Benefícios: Estável, testado, sempre disponível
GEMINI_MODEL_SECONDARY = "gemini-1.5-flash"

# MODELO PADRÃO (usado se não houver fallback implementado)
# IMPORTANTE: Sempre tente usar o primário primeiro
GEMINI_MODEL = GEMINI_MODEL_PRIMARY

# Prompt para análise de viralidade (SUPER PROMPT ANIME + TITLES)
GEMINI_PROMPT = """
ATUE COMO UM EDITOR DE ELITE (GOD MODE).
Sua missão é extrair TODOS os momentos virais deste episódio. NÃO SE LIMITE. Se houver 15 cenas boas, extraia as 15.

🔥 OBJETIVO: Criar clips prontos para postar que explodam de visualizações.

PARA CADA CENA IDENTIFICADA, VOCÊ DEVE GERAR:
1. TIMESTAMP PRECISO (Inicio e Fim).
2. TÍTULO DE ARQUIVO VIRAL (Obrigatório):
   - Deve ser curto, impactante e "Clickbait".
   - Use UPPERCASE.
   - Use underlines (_) em vez de espaços.
   - Exemplo: LUFFY_GEAR_5_APARECE, ZORO_SOLA_KING, SAKURA_CHORA_DE_NOVO.

🔍 O QUE EXTRAIR (Score > 70):
- ⚔️ AÇÃO: Qualquer troca de golpes bem animada (Sakuga).
- 😭 DRAMA: Qualquer momento que gere arrepio ou choro.
- 🤣 HUMOR: Qualquer piada que funcione fora de contexto.
- 🤯 PLOT: Qualquer revelação ou gancho.
- ❤️ SHIP: Qualquer momento romântico ou tenso entre casais.

📏 REGRA DE OURO (TEMPO):
- ALVO: 60 Segundos.
- MÍNIMO: 40s (Se for menos, inclua contexto antes/depois).
- MÁXIMO: 90s.

JSON DE SAÍDA (Obrigatório):
{
  "cortes": [
    {
      "inicio": "MM:SS",
      "fim": "MM:SS",
      "titulo_arquivo": "NOME_DO_ARQUIVO_VIRAL",
      "descricao": "Explicação breve",
      "viral_score": 95
    }
  ]
}
"""

# ==================== CONFIGURAÇÕES DE OPENING/ENDING ====================

# Tempo de início do opening (segundos)
OPENING_START = 60

# Tempo de fim do opening (segundos)
OPENING_END = 150

# Tempo antes do fim para início do ending (segundos)
ENDING_OFFSET_START = 150

# Tempo antes do fim para término do ending (segundos)
ENDING_OFFSET_END = 30

# ==================== CONFIGURAÇÕES DE INTERFACE ====================

# Título da página
PAGE_TITLE = "AnimeCut - Cortes Automáticos para Animes"

# Ícone da página
PAGE_ICON = "🎌"

# Layout da página
PAGE_LAYOUT = "wide"

# ==================== CORES DO TEMA ANIME ====================

# Gradiente principal (Rosa → Roxo)
GRADIENT_START_COLOR = (255, 107, 157)  # RGB
GRADIENT_END_COLOR = (108, 91, 123)     # RGB

# Cor de destaque
ACCENT_COLOR = "#FF6B9D"

# ==================== CONFIGURAÇÕES DE FUNDO ====================

def criar_gradiente_personalizado(largura: int, altura: int, 
                                  cor_inicio: tuple = None, 
                                  cor_fim: tuple = None):
    """
    Cria um gradiente personalizado
    
    Args:
        largura: Largura do gradiente
        altura: Altura do gradiente
        cor_inicio: Cor RGB inicial (padrão: rosa)
        cor_fim: Cor RGB final (padrão: roxo escuro)
    
    Returns:
        Array numpy com o gradiente
    """
    import numpy as np
    
    if cor_inicio is None:
        cor_inicio = (255, 108, 157)  # Rosa
    if cor_fim is None:
        cor_fim = (80, 48, 123)  # Roxo escuro
    
    img = np.zeros((altura, largura, 3), dtype=np.uint8)
    
    for y in range(altura):
        ratio = y / altura
        img[y, :] = [
            int(cor_inicio[2] + (cor_fim[2] - cor_inicio[2]) * ratio),  # B
            int(cor_inicio[1] + (cor_fim[1] - cor_inicio[1]) * ratio),  # G
            int(cor_inicio[0] + (cor_fim[0] - cor_inicio[0]) * ratio)   # R
        ]
    
    return img

# ==================== CONFIGURAÇÕES DE NOMENCLATURA ====================

# Prefixo dos arquivos de saída
OUTPUT_PREFIX = "AnimeClip"

# Formato de numeração (3 dígitos: 001, 002, etc.)
OUTPUT_NUMBER_FORMAT = "{:03d}"

# Extensão dos arquivos
OUTPUT_EXTENSION = ".mp4"

# ==================== LIMITES ====================

# Duração mínima de um corte (segundos)
MIN_CUT_DURATION = 50  # Ajustado para ~1 min

# Duração máxima de um corte (segundos)
MAX_CUT_DURATION = 90

# Sensibilidade mínima
MIN_SENSITIVITY = 10.0

# Sensibilidade máxima
MAX_SENSITIVITY = 40.0

# ==================== OUTROS ====================

# Limpar arquivos temporários após processamento
LIMPAR_TEMP = True

# ==================== MENSAGENS ====================

MESSAGES = {
    "welcome": "🎌 Bem-vindo ao AnimeCut - Sistema otimizado para cortes de anime!",
    "processing": "🎬 Processando episódio de anime...",
    "detecting": "🔍 Detectando mudanças de cena...",
    "opening_detected": "🎵 Opening detectado: {start:.1f}s - {end:.1f}s",
    "ending_detected": "🎵 Ending detectado: {start:.1f}s - {end:.1f}s",
    "scenes_found": "✅ {count} cenas detectadas!",
    "processing_clip": "🎌 Processando clip de anime {current}/{total}...",
    "complete": "✅ Processamento de anime concluído!",
    "success": "🎉 {count} clips de anime gerados com qualidade premium!",
    "error_fps": "❌ FPS inválido no vídeo",
    "error_no_scenes": "⚠️ Nenhuma mudança de cena detectada. Tente ajustar a sensibilidade.",
    "error_processing": "❌ Erro ao processar corte {number}: {error}",
}

# ==================== DICAS ====================

TIPS = [
    "💡 Sensibilidade 25 é ideal para animes",
    "💡 Ative 'Pular Opening/Ending' para focar no conteúdo",
    "💡 Cortes de 30-45s são perfeitos para redes sociais",
    "💡 Alta qualidade preserva detalhes da arte anime",
    "💡 Use templates personalizados para dar identidade aos seus clips",
    "💡 Animes com muita ação podem precisar de sensibilidade menor",
    "💡 Episódios de slice-of-life funcionam melhor com sensibilidade maior",
]
