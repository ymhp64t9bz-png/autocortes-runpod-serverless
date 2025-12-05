import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageColor
from moviepy.editor import ImageClip

def get_font_path(font_filename):
    """Verifica se a fonte está no Colab ou localmente (busca recursiva)."""
    # Caminho Colab (fontes do sistema)
    colab_paths = [
        f'/usr/share/fonts/truetype/msttcorefonts/{font_filename}',
        f'/usr/share/fonts/truetype/dejavu/{font_filename}',
        f'/content/Fontes/{font_filename}'
    ]
    
    # Caminho Local (pasta Fontes do projeto - busca recursiva)
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    fontes_dir = os.path.join(base_dir, 'fontes')
    
    # Busca recursivamente na pasta local
    if os.path.exists(fontes_dir):
        for root, dirs, files in os.walk(fontes_dir):
            if font_filename in files:
                return os.path.join(root, font_filename)
    
    # Verifica Colab
    for colab_path in colab_paths:
        if os.path.exists(colab_path):
            return colab_path
    
    # Fallback: retorna o nome e deixa o PIL tentar encontrar
    return font_filename

def hex_to_rgb(hex_color):
    """Converte hex (#RRGGBB) para tupla RGB."""
    if hex_color.startswith('#'):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    else:
        # Se já for RGB ou outro formato, tenta usar ImageColor
        try:
            return ImageColor.getrgb(hex_color)
        except:
            return (255, 255, 255)  # Branco como fallback

def criar_titulo_pil(texto, largura_video, altura_video, duracao, 
                     font_filename="arial.ttf", 
                     font_size=None,
                     text_color="#FFFFFF", 
                     stroke_color="#000000", 
                     stroke_width=6,
                     pos_vertical=0.5):
    """
    Renderiza título com configurações dinâmicas de fonte e cor.
    Compatível com Windows e Google Colab.
    
    Args:
        texto: Texto do título
        largura_video: Largura do vídeo em pixels
        altura_video: Altura do vídeo em pixels
        duracao: Duração do clip em segundos
        font_filename: Nome do arquivo de fonte (ex: "Impact.ttf")
        font_size: Tamanho da fonte (None = automático)
        text_color: Cor do texto em HEX (ex: "#FFD700") ou RGB tuple
        stroke_color: Cor do contorno em HEX (ex: "#000000") ou RGB tuple
        stroke_width: Largura do contorno em pixels
        pos_vertical: Posição vertical (0.0 = topo, 1.0 = base)
    """
    
    # Converte cores para RGB se necessário
    if isinstance(text_color, str):
        text_color_rgb = hex_to_rgb(text_color)
    else:
        text_color_rgb = text_color
        
    if isinstance(stroke_color, str):
        stroke_color_rgb = hex_to_rgb(stroke_color)
    else:
        stroke_color_rgb = stroke_color
    
    # Configuração de Fonte
    if font_size is None:
        font_size = int(largura_video * 0.08)
    font_path = get_font_path(font_filename)
    
    try:
        font = ImageFont.truetype(font_path, font_size)
    except Exception as e:
        print(f"[AVISO] Fonte {font_path} não carregada ({e}). Tentando Arial...")
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            print("[AVISO] Usando fonte padrão do sistema.")
            font = ImageFont.load_default()
    
    # Cria Canvas Transparente
    canvas_h = int(altura_video * 0.3)
    img = Image.new('RGBA', (largura_video, canvas_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Quebra de Linha Automática (MÁXIMO 2 LINHAS)
    palavras = texto.split()
    linhas = []
    linha_atual = []
    
    for palavra in palavras:
        linha_atual.append(palavra)
        try:
            bbox = draw.textbbox((0, 0), " ".join(linha_atual), font=font)
            w = bbox[2] - bbox[0]
        except:
            w, h = draw.textsize(" ".join(linha_atual), font=font)
            
        if w > largura_video * 0.9:
            linha_atual.pop()
            if linha_atual:
                linhas.append(" ".join(linha_atual))
            linha_atual = [palavra]
            
            # LIMITA A 2 LINHAS
            if len(linhas) >= 2:
                break
            
    if linha_atual and len(linhas) < 2:
        linhas.append(" ".join(linha_atual))
    
    # GARANTE MÁXIMO DE 2 LINHAS
    linhas = linhas[:2]
        
    # Desenha Texto com Contorno
    y = 20
    
    for linha in linhas:
        # Desenha Contorno (Stroke)
        for off_x in range(-stroke_width, stroke_width + 1):
            for off_y in range(-stroke_width, stroke_width + 1):
                if off_x != 0 or off_y != 0:  # Não desenha no centro
                    draw.text(
                        (largura_video / 2 + off_x, y + off_y), 
                        linha, 
                        font=font, 
                        fill=stroke_color_rgb, 
                        anchor="mt"
                    )
        
        # Desenha Texto Principal
        draw.text(
            (largura_video / 2, y), 
            linha, 
            font=font, 
            fill=text_color_rgb, 
            anchor="mt"
        )
        
        # Avança Y para próxima linha
        try:
            bbox = draw.textbbox((0, 0), linha, font=font)
            h = bbox[3] - bbox[1]
        except:
            w, h = draw.textsize(linha, font=font)
        y += h + 15
        
    # Converte para MoviePy ImageClip
    numpy_img = np.array(img)
    clip = ImageClip(numpy_img).set_duration(duracao)
    
    # Posiciona usando pos_vertical (0.0 = topo, 1.0 = base)
    pos_y = int(altura_video * pos_vertical)
    clip = clip.set_position(('center', pos_y))
    
    return clip
