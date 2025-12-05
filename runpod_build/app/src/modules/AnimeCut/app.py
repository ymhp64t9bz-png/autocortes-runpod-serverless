# -*- coding: utf-8 -*-
import streamlit as st
import os
import sys
import time
import tempfile
import gc
import torch
import logging
import numpy as np
from pathlib import Path
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip, ColorClip
from moviepy.video.fx.all import speedx
from PIL import Image

# Configurar logger
logger = logging.getLogger(__name__)

# Oculta erros DOM do Streamlit no front-end
st.markdown("""
<style>
    /* Oculta mensagens de erro do Streamlit */
    .stException {
        display: none !important;
    }
    
    /* Oculta stack traces */
    .stException > div {
        display: none !important;
    }
    
    /* Oculta NotFoundError específico */
    div[data-testid="stException"] {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

# Imports Locais
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'core'))

AI_AVAILABLE = False
IMPORT_ERROR_MSG = ""

try:
    from ai_services.local_ai_service import (
        transcribe_audio_local, 
        transcribe_audio_batch,
        manually_unload_whisper,
        generate_viral_title_local,
        generate_viral_title_batch,
        manually_unload_llama,
        analyze_viral_segments_deepseek,
        is_running_in_colab
    )
    AI_AVAILABLE = True
except ImportError as e:
    AI_AVAILABLE = False
    IMPORT_ERROR_MSG = str(e)
except Exception as e:
    AI_AVAILABLE = False
    IMPORT_ERROR_MSG = str(e)

try:
    from modules.AnimeCut.utils_title import criar_titulo_pil
except ImportError:
    sys.path.append(os.path.dirname(__file__))
    from utils_title import criar_titulo_pil

# ==================== CAMINHOS DINÂMICOS ====================

def get_font_directory():
    """Retorna o diretório de fontes (Colab ou Local)."""
    colab_dir = '/content/Fontes'
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    local_dir = os.path.join(base_dir, 'Fontes')
    
    if os.path.exists(colab_dir):
        return colab_dir
    elif os.path.exists(local_dir):
        return local_dir
    else:
        os.makedirs(local_dir, exist_ok=True)
        return local_dir

FONT_DIR = get_font_directory()

# ==================== ENGINE DE RENDERIZAÇÃO ====================

def processar_corte_anime_engine(
    video_path, inicio, fim, 
    output_dir, numero_corte,
    config
):
    """
    Motor de renderização V5.0 (NVENC + Anti-Shadowban + DeepSeek).
    """
    status_text = st.empty()
    progress_bar = st.progress(0)
    
    try:
        status_text.text(f"Iniciando corte {numero_corte}...")
        
        with VideoFileClip(video_path) as video:
            duracao_corte = min(fim - inicio, 300)
            clip = video.subclip(inicio, min(inicio + duracao_corte, video.duration))
            
            # --- ANTI-SHADOWBAN (Lógica de Vídeo) ---
            if config.get("anti_shadowban"):
                status_text.text("Aplicando Anti-Shadowban (Speed Ramp)...")
                clip = clip.fx(speedx, 1.05)
            
            # --- IA (Título) ---
            titulo_viral = None
            if config.get("usar_ia") and AI_AVAILABLE:
                status_text.text("Gerando Título Viral (DeepSeek)...")
                try:
                    fd, temp_audio = tempfile.mkstemp(suffix=".wav")
                    os.close(fd)
                    
                    # Converte para caminho absoluto
                    temp_audio = os.path.abspath(temp_audio)
                    
                    clip.audio.write_audiofile(temp_audio, logger=None)
                    
                    dialogo_res = transcribe_audio_batch(temp_audio)
                    dialogo_text = dialogo_res['text'] if isinstance(dialogo_res, dict) else dialogo_res
                    
                    if dialogo_text:
                        titulo_viral = generate_viral_title_batch(config.get("nome_anime", "Anime"), dialogo_text)
                        
                        # Limpa memória após gerar título para evitar degradação
                        gc.collect()
                    
                    # Remove arquivo temporário se existir
                    if os.path.exists(temp_audio):
                        os.remove(temp_audio)
                except Exception as e:
                    print(f"Erro IA Título: {e}")
                    import traceback
                    print(f"Traceback: {traceback.format_exc()}")

            
            # --- COMPOSIÇÃO ---
            target_w, target_h = 1080, 1920
            
            # Fundo
            if config.get("template_path") and os.path.exists(config.get("template_path")):
                from PIL import Image as PILImage
                fundo_img = PILImage.open(config["template_path"]).convert('RGB')
                fundo_img = fundo_img.resize((target_w, target_h), PILImage.Resampling.LANCZOS)
                fundo_array = np.array(fundo_img)
                fundo = ImageClip(fundo_array).set_duration(duracao_corte)
            else:
                fundo = ColorClip(size=(target_w, target_h), color=(20, 10, 40)).set_duration(duracao_corte)
            
            # Vídeo (Fit)
            video_w, video_h = clip.size
            scale = min(target_w / video_w, target_h / video_h)
            if video_w * (target_h/video_h) < target_w: scale = target_w / video_w
            
            clip_resized = clip.resize(scale)
            pos_y = int((target_h - clip_resized.h) * 0.5)  # Vídeo sempre centralizado
            clip_resized = clip_resized.set_position(('center', pos_y))
            
            elementos = [fundo, clip_resized]
            
            # Título
            if titulo_viral:
                t_clip = criar_titulo_pil(
                    titulo_viral, target_w, target_h, duracao_corte, 
                    font_filename=config.get("font_filename", "arial.ttf"),
                    font_size=config.get("font_size", None),
                    text_color=config.get("text_color", "#FFFFFF"),
                    stroke_color=config.get("stroke_color", "#000000"),
                    stroke_width=config.get("stroke_width", 6),
                    pos_vertical=config.get("pos_vertical", 0.15)
                )
                elementos.append(t_clip)
            
            clip_final = CompositeVideoClip(elementos, size=(target_w, target_h))
            
            # --- EXPORTAÇÃO (MP4 COMPATÍVEL) ---
            filename = f"Corte_{numero_corte:03d}_{int(time.time())}.mp4"
            output_path = os.path.join(output_dir, filename)
            
            status_text.text("Renderizando com GPU (NVENC)...")
            
            # Parâmetros NVENC otimizados para RTX 4060
            ffmpeg_params = [
                '-preset', 'fast',         # Presets válidos: slow, medium, fast, hp, hq, bd, ll, llhq, llhp, lossless
                '-profile:v', 'high',      # Profile H.264 compatível
                '-level', '4.1',           # Level compatível
                '-pix_fmt', 'yuv420p',     # Pixel format universal
                '-movflags', '+faststart', # Permite streaming
                '-rc:v', 'vbr',            # Variable bitrate
                '-cq:v', '23',             # Qualidade constante (0-51, menor=melhor)
                '-b:v', '5M',              # Bitrate máximo
                '-maxrate:v', '8M',        # Bitrate pico
                '-bufsize:v', '10M',       # Buffer
                '-b:a', '192k'             # Bitrate de áudio
            ]
            
            if config.get("anti_shadowban"):
                # Anti-shadowban: noise + contrast
                ffmpeg_params.extend(['-vf', 'noise=alls=1:allf=t,eq=contrast=1.02'])
            
            # Verifica se GPU está disponível
            if torch.cuda.is_available():
                logger.info(f"[NVENC] GPU disponível. Tentando usar h264_nvenc...")
            else:
                logger.warning(f"[NVENC] GPU não disponível. Usando CPU...")
            
            try:
                clip_final.write_videofile(
                    output_path,
                    codec='h264_nvenc',
                    audio_codec='aac',
                    audio_bitrate='192k',
                    ffmpeg_params=ffmpeg_params,
                    threads=4,
                    logger=None
                )
                status_text.success(f"✓ Renderizado com GPU (NVENC): {filename}")
                logger.info(f"[NVENC] Sucesso! Vídeo renderizado com GPU.")
            except Exception as nvenc_error:
                # Fallback para CPU se NVENC falhar
                import traceback
                print(f"[NVENC] Erro: {nvenc_error}")
                print(f"[NVENC] Traceback: {traceback.format_exc()}")
                
                status_text.warning("⚠ NVENC falhou. Usando CPU (libx264)...")
                
                ffmpeg_params_cpu = [
                    '-preset', 'ultrafast',    # Mais rápido possível na CPU
                    '-profile:v', 'high',
                    '-level', '4.1',
                    '-pix_fmt', 'yuv420p',
                    '-movflags', '+faststart',
                    '-crf', '23',
                    '-b:a', '192k'
                ]
                if config.get("anti_shadowban"):
                    ffmpeg_params_cpu.extend(['-vf', 'noise=alls=1:allf=t,eq=contrast=1.02'])
                
                clip_final.write_videofile(
                    output_path,
                    codec='libx264',
                    audio_codec='aac',
                    audio_bitrate='192k',
                    ffmpeg_params=ffmpeg_params_cpu,
                    threads=4,
                    logger=None
                )
            
            progress_bar.progress(100)
            status_text.success(f"Salvo: {filename}")
            
            # Limpa VRAM e RAM após cada clip para evitar travamento
            gc.collect()  # Limpa RAM
            if torch.cuda.is_available():
                torch.cuda.empty_cache()  # Limpa VRAM
                torch.cuda.synchronize()
            
            return output_path

    except Exception as e:
        st.error(f"Erro no corte {numero_corte}: {e}")
        # Limpa VRAM e RAM mesmo em caso de erro
        gc.collect()  # Limpa RAM
        if torch.cuda.is_available():
            torch.cuda.empty_cache()  # Limpa VRAM
        return None

# ==================== INTERFACE (MAIN) ====================

def get_local_fonts():
    """Lista fontes no diretório dinâmico (Colab ou Local), incluindo subpastas."""
    if not os.path.exists(FONT_DIR):
        return ["arial.ttf"]
    
    fonts = []
    # Busca recursivamente em todas as subpastas
    for root, dirs, files in os.walk(FONT_DIR):
        for file in files:
            if file.lower().endswith(('.ttf', '.otf')):
                # Retorna apenas o nome do arquivo (não o caminho completo)
                # O get_font_path() em utils_title.py vai resolver o caminho
                fonts.append(file)
    
    return fonts if fonts else ["arial.ttf"]

def main():
    st.title("✂️ AnimeCut Pro V5.1 (DeepSeek Auto)")
    
    if 'cortes' not in st.session_state:
        st.session_state.cortes = []
    
    # --- SIDEBAR ---
    with st.sidebar:
        st.header("Configurações")
        nome_anime = st.text_input("Nome do Anime", "Anime Genérico")
        
        st.subheader("Modo de Operação")
        
        # Desabilita modo automático se IA não estiver disponível
        opcoes_corte = ["Manual (Em Massa)"]
        if AI_AVAILABLE:
            opcoes_corte.append("Automático (DeepSeek AI)")
            
        modo_corte = st.radio("Tipo de Corte", opcoes_corte)
        
        if modo_corte == "Manual (Em Massa)":
            qtd_cortes = st.number_input("Quantidade de Cortes", 1, 20, 5)
            duracao_corte_manual = st.number_input("Duração por Corte (s)", 15, 300, 60)
        elif modo_corte == "Automático (DeepSeek AI)":
            st.info("O DeepSeek analisará o roteiro para encontrar cortes virais (60s-180s).")
        
        st.markdown("---")
        st.subheader("Estilo do Título")
        
        local_fonts = get_local_fonts()
        selected_font_name = st.selectbox("Fonte", local_fonts)
        
        c1, c2 = st.columns(2)
        with c1:
            text_color = st.color_picker("Cor do Texto", "#FFD700")
        with c2:
            stroke_color = st.color_picker("Cor da Borda", "#000000")
            
        stroke_width = st.slider("Espessura Borda", 0, 10, 6)
        font_size = st.slider("Tamanho da Fonte", 30, 120, 70, 5)
        pos_vertical = st.slider("Posição Vertical", 0.0, 1.0, 0.15, 0.01)
        
        # Template de fundo (antes do preview para estar disponível)
        template_file = st.file_uploader("Template de Fundo", type=["png", "jpg"])
        template_path = None
        if template_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as f:
                f.write(template_file.getbuffer())
                template_path = f.name
        
        # Preview do texto
        st.markdown("---")
        st.subheader("🔍 Preview do Texto")
        preview_text = st.text_input("Texto de Preview", "EXEMPLO DE TÍTULO VIRAL")
        
        if st.button("👁️ Gerar Preview"):
            try:
                from PIL import Image as PILImage, ImageDraw
                import numpy as np
                from moviepy.editor import ColorClip, CompositeVideoClip
                
                # Dimensões 9:16 (vertical - TikTok/Shorts)
                preview_width = 1080
                preview_height = 1920
                
                # Quebra texto em no máximo 2 linhas
                words = preview_text.split()
                if len(words) > 6:
                    line1 = " ".join(words[:len(words)//2])
                    line2 = " ".join(words[len(words)//2:])
                    preview_text_formatted = f"{line1}\n{line2}"
                else:
                    preview_text_formatted = preview_text
                
                # Cria fundo (template ou cor sólida)
                if template_path and os.path.exists(template_path):
                    # Usa template do usuário
                    fundo_img = PILImage.open(template_path).convert('RGB')
                    fundo_img = fundo_img.resize((preview_width, preview_height), PILImage.Resampling.LANCZOS)
                    fundo = ColorClip(size=(preview_width, preview_height), color=(0,0,0), duration=1.0)
                    fundo_array = np.array(fundo_img)
                    from moviepy.editor import ImageClip
                    fundo = ImageClip(fundo_array).set_duration(1.0)
                else:
                    # Fundo preto padrão
                    fundo = ColorClip(size=(preview_width, preview_height), color=(0,0,0), duration=1.0)
                
                # Gera título
                titulo_clip = criar_titulo_pil(
                    preview_text_formatted,
                    preview_width,
                    preview_height,
                    1.0,  # duração de 1 segundo
                    selected_font_name,
                    font_size,
                    text_color,
                    stroke_color,
                    stroke_width,
                    pos_vertical
                )
                
                # Compõe fundo + título
                preview_composite = CompositeVideoClip([fundo, titulo_clip], size=(preview_width, preview_height))
                
                # Extrai frame
                frame = preview_composite.get_frame(0)
                
                # Detecta número de canais (RGB ou RGBA)
                if len(frame.shape) == 3:
                    if frame.shape[2] == 4:
                        mode = 'RGBA'
                    elif frame.shape[2] == 3:
                        mode = 'RGB'
                    else:
                        mode = 'L'
                else:
                    mode = 'L'
                
                preview_img = PILImage.fromarray(frame.astype('uint8'), mode)
                
                # Mostra preview
                st.image(preview_img, caption="Preview do Título (9:16 - Vertical)", use_container_width=True)
                st.success("✅ Preview gerado! Ajuste os controles acima para modificar.")
                
            except Exception as e:
                st.error(f"Erro ao gerar preview: {e}")
        
        st.markdown("---")
        anti_shadowban = st.checkbox("🛡️ Ativar Anti-Shadowban", value=True)
        
        # Checkbox de IA desabilitado se não disponível
        usar_ia = st.checkbox("Gerar Títulos com IA", value=AI_AVAILABLE, disabled=not AI_AVAILABLE)
        if not AI_AVAILABLE:
            st.caption("⚠️ IA indisponível (dependências não encontradas).")

    # --- ÁREA PRINCIPAL ---
    uploaded_video = st.file_uploader("Carregar Episódio", type=["mp4", "mkv", "avi"])
    
    if uploaded_video:
        tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") 
        tfile.write(uploaded_video.read())
        video_path = tfile.name
        
        try:
            clip_info = VideoFileClip(video_path)
            duration = clip_info.duration
            clip_info.close()
            st.info(f"Duração Total: {duration:.1f}s")
            
            # --- LÓGICA DE GERAÇÃO DE CORTES ---
            if st.button("🔍 GERAR LISTA DE CORTES"):
                st.session_state.cortes = []
                
                if modo_corte == "Manual (Em Massa)":
                    intervalo = duration / qtd_cortes
                    for i in range(qtd_cortes):
                        start = i * intervalo
                        end = min(start + duracao_corte_manual, duration)
                        if end - start > 10:
                            st.session_state.cortes.append({'start': start, 'end': end})
                    st.success(f"{len(st.session_state.cortes)} cortes manuais gerados.")
                    
                elif modo_corte == "Automático (DeepSeek AI)":
                    if not AI_AVAILABLE:
                        st.error(f"IA não disponível. Erro técnico: {globals().get('IMPORT_ERROR_MSG', 'Desconhecido')}")
                        st.warning("Se estiver no Colab, certifique-se de ter instalado as dependências. Se local, instale llama-cpp-python e whisper.")
                    else:
                        # Container para feedback visual
                        status_container = st.container()
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        try:
                            # ETAPA 1: Extração de Áudio (0-20%)
                            status_text.info("🎵 **Etapa 1/3:** Extraindo áudio do vídeo...")
                            progress_bar.progress(5)
                            
                            fd, temp_audio_full = tempfile.mkstemp(suffix=".wav")
                            os.close(fd)
                            temp_audio_full = os.path.abspath(temp_audio_full)
                            
                            with VideoFileClip(video_path) as v:
                                v.audio.write_audiofile(temp_audio_full, logger=None)
                            
                            progress_bar.progress(20)
                            status_text.success("✅ Áudio extraído com sucesso!")
                            time.sleep(0.5)
                            
                            # ETAPA 2: Transcrição (20-60%)
                            status_text.info("🎤 **Etapa 2/3:** Transcrevendo áudio (pode levar 1-2 minutos)...")
                            progress_bar.progress(25)
                            
                            res_whisper = transcribe_audio_local(temp_audio_full)
                            
                            if res_whisper:
                                progress_bar.progress(60)
                                status_text.success(f"✅ Transcrição concluída! {len(res_whisper.get('text', ''))} caracteres processados.")
                                time.sleep(0.5)
                                
                                # ETAPA 3: Análise IA (60-100%)
                                status_text.info("🤖 **Etapa 3/3:** Analisando conteúdo e identificando momentos virais...")
                                progress_bar.progress(65)
                                
                                # Simula progresso durante análise (DeepSeek pode demorar)
                                import threading
                                
                                # Flag para controlar progresso
                                analysis_done = threading.Event()
                                
                                def simulate_progress():
                                    """Simula progresso visual enquanto DeepSeek processa"""
                                    progress = 65
                                    while not analysis_done.is_set() and progress < 95:
                                        time.sleep(2)  # Atualiza a cada 2 segundos
                                        if not analysis_done.is_set():
                                            progress = min(progress + 2, 95)
                                            
                                            try:
                                                # Tenta atualizar UI (pode falhar se elementos foram removidos)
                                                progress_bar.progress(progress)
                                                
                                                # Mensagens de progresso
                                                elapsed = int((progress - 65) / 2) * 2
                                                if elapsed < 30:
                                                    status_text.info(f"🤖 **Etapa 3/3:** Analisando conteúdo... ({elapsed}s)")
                                                elif elapsed < 60:
                                                    status_text.info(f"🤖 **Etapa 3/3:** Identificando momentos virais... ({elapsed}s)")
                                                else:
                                                    status_text.info(f"🤖 **Etapa 3/3:** Finalizando análise... ({elapsed}s)")
                                            except:
                                                # Ignora erros de atualização de UI
                                                pass
                                
                                # Inicia thread de progresso
                                progress_thread = threading.Thread(target=simulate_progress, daemon=True)
                                progress_thread.start()
                                
                                try:
                                    # Chama DeepSeek (pode demorar)
                                    segments = analyze_viral_segments_deepseek(res_whisper['text'], duration)
                                finally:
                                    # Para thread de progresso
                                    analysis_done.set()
                                    progress_thread.join(timeout=1)
                                
                                progress_bar.progress(100)
                                
                                if segments:
                                    st.session_state.cortes = segments
                                    status_text.success(f"🎉 **Processo Concluído!** {len(segments)} momentos virais identificados!")
                                    st.success(f"✅ DeepSeek identificou {len(segments)} momentos virais!")
                                    st.info("📋 Role para baixo para ver a lista de cortes e iniciar a renderização.")
                                    
                                    # LIMPEZA COMPLETA antes de renderização
                                    status_text.info("🧹 Liberando recursos antes da renderização...")
                                    
                                    # 1. Descarrega modelos de IA
                                    if AI_AVAILABLE:
                                        manually_unload_whisper()  # Descarrega Whisper (GPU)
                                        manually_unload_llama()    # Descarrega DeepSeek (CPU)
                                    
                                    # 2. Limpa RAM
                                    gc.collect()
                                    
                                    # 3. Limpa VRAM
                                    if torch.cuda.is_available():
                                        torch.cuda.empty_cache()
                                        torch.cuda.synchronize()
                                    
                                    # 4. Pausa para SO liberar recursos
                                    time.sleep(2)
                                    
                                    status_text.success("✅ Recursos liberados! Pronto para renderização.")
                                    time.sleep(1)
                                    
                                    # Força atualização da interface para mostrar lista de cortes
                                    st.rerun()
                                else:
                                    status_text.warning("⚠️ Nenhum segmento identificado.")
                                    st.warning("DeepSeek não encontrou segmentos óbvios. Tente o modo Manual.")
                            else:
                                progress_bar.progress(0)
                                status_text.error("❌ Falha na transcrição do áudio.")
                                st.error("Falha na transcrição do áudio.")
                            
                        except Exception as e:
                            progress_bar.progress(0)
                            status_text.error(f"❌ Erro durante o processamento: {str(e)}")
                            st.error(f"Erro: {e}")
                        
                        finally:
                            # Remove arquivo temporário
                            if 'temp_audio_full' in locals() and os.path.exists(temp_audio_full):
                                os.remove(temp_audio_full)

            # --- LISTA E RENDERIZAÇÃO ---
            if st.session_state.cortes:
                st.write(f"### Fila de Processamento ({len(st.session_state.cortes)} clips)")
                
                df_data = [{"#": i+1, "Início": f"{c['start']:.1f}s", "Fim": f"{c['end']:.1f}s", "Duração": f"{c['end']-c['start']:.1f}s"} for i, c in enumerate(st.session_state.cortes)]
                st.table(df_data)
                
                if st.button("🚀 INICIAR RENDERIZAÇÃO EM MASSA (NVENC)", type="primary"):
                    # LIMPEZA COMPLETA antes de iniciar renderização
                    st.info("🧹 Liberando recursos antes de iniciar...")
                    
                    # 1. Descarrega modelos de IA
                    if AI_AVAILABLE:
                        manually_unload_whisper()  # Descarrega Whisper (GPU)
                        manually_unload_llama()    # Descarrega DeepSeek (CPU)
                    
                    # 2. Limpa RAM
                    gc.collect()
                    
                    # 3. Limpa VRAM
                    if torch.cuda.is_available():
                        torch.cuda.empty_cache()
                        torch.cuda.synchronize()
                    
                    # 4. Pausa para SO liberar recursos
                    time.sleep(2)
                    
                    st.success("✅ Recursos liberados! Iniciando renderização...")
                    time.sleep(1)
                    
                    output_dir = os.path.join(os.path.dirname(__file__), "..", "..", "models", "AnimCut", "Output")
                    os.makedirs(output_dir, exist_ok=True)
                    
                    config = {
                        "nome_anime": nome_anime,
                        "usar_ia": usar_ia,
                        "anti_shadowban": anti_shadowban,
                        "font_filename": selected_font_name,
                        "font_size": font_size,
                        "text_color": text_color,
                        "stroke_color": stroke_color,
                        "stroke_width": stroke_width,
                        "pos_vertical": pos_vertical,
                        "template_path": template_path
                    }
                    
                    results = []
                    
                    # Feedback visual para renderização
                    st.write("---")
                    st.write("### 🎬 Renderização em Andamento")
                    progress_bar_render = st.progress(0)
                    status_render = st.empty()
                    clip_status = st.empty()
                    
                    total_clips = len(st.session_state.cortes)
                    
                    for i, corte in enumerate(st.session_state.cortes):
                        clip_num = i + 1
                        
                        # MEMORY WALL: Limpa memória ANTES de cada clip
                        gc.collect()
                        if torch.cuda.is_available():
                            torch.cuda.empty_cache()
                        time.sleep(0.5)  # Pequena pausa para o SO liberar recursos
                        
                        # Atualiza status do clip atual
                        status_render.info(f"🎥 **Processando Clip {clip_num}/{total_clips}** ({corte['start']:.1f}s - {corte['end']:.1f}s)")
                        
                        # Mostra sub-etapas
                        with clip_status.container():
                            st.write(f"**Clip {clip_num}:**")
                            sub_col1, sub_col2, sub_col3 = st.columns(3)
                            with sub_col1:
                                st.caption("⏳ Extraindo...")
                            with sub_col2:
                                if usar_ia:
                                    st.caption("⏳ Gerando título...")
                            with sub_col3:
                                st.caption("⏳ Renderizando...")
                        
                        # Feedback: Iniciando renderização
                        st.toast(f"Iniciando renderização do Corte {clip_num}...", icon="🎬")
                        
                        # Processa o clip
                        res = processar_corte_anime_engine(
                            video_path, corte['start'], corte['end'],
                            output_dir, clip_num, config
                        )
                        
                        if res:
                            results.append(res)
                            # Atualiza para concluído
                            with clip_status.container():
                                st.write(f"**Clip {clip_num}:**")
                                sub_col1, sub_col2, sub_col3 = st.columns(3)
                                with sub_col1:
                                    st.caption("✅ Extraído")
                                with sub_col2:
                                    if usar_ia:
                                        st.caption("✅ Título gerado")
                                with sub_col3:
                                    st.caption("✅ Renderizado")
                        
                        # Atualiza barra de progresso
                        progress_bar_render.progress((clip_num) / total_clips)
                    
                    # Descarrega os modelos após processar todos os clips
                    if usar_ia and AI_AVAILABLE:
                        status_render.info("🧹 Liberando recursos...")
                        manually_unload_whisper()  # Descarrega Whisper
                        manually_unload_llama()    # Descarrega DeepSeek
                    
                    # Finalização
                    progress_bar_render.progress(100)
                    status_render.success(f"🎉 **Renderização Concluída!** {len(results)} vídeos gerados com sucesso!")
                    
                    if results:
                        st.success(f"✅ Processamento em Massa Concluído! {len(results)} vídeos gerados.")
                        st.info(f"📁 Vídeos salvos em: `{output_dir}`")
                        st.balloons()

        except Exception as e:
            st.error(f"Erro ao processar vídeo: {e}")

if __name__ == "__main__":
    main()
