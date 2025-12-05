# -*- coding: utf-8 -*-
"""
KWAI CUT - Detecção Automática de Cenas com Títulos IA
Versão 2.0.0 Final - Integração com Gemini 2.5 Flash
"""

import streamlit as st
import os
import sys
import tempfile
import time
import cv2
import numpy as np
from pathlib import Path
from moviepy.editor import VideoFileClip, ColorClip, CompositeVideoClip
import zipfile

# Imports de IA (opcional)
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

def detect_scenes(video_path, threshold=30):
    """Detecta mudanças de cena baseado em análise de histograma."""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return []
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    scenes = []
    prev_hist = None
    frame_idx = 0
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Calcula histograma
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
        hist = cv2.normalize(hist, hist).flatten()
        
        if prev_hist is not None:
            # Calcula diferença
            diff = cv2.compareHist(prev_hist, hist, cv2.HISTCMP_CORREL)
            
            # Se diferença for grande, marca como mudança de cena
            if diff < (1 - threshold / 100):
                timestamp = frame_idx / fps
                scenes.append(timestamp)
        
        prev_hist = hist
        frame_idx += 1
        
        # Atualiza progresso
        if frame_idx % 30 == 0:
            progress = frame_idx / total_frames
            progress_bar.progress(progress)
            status_text.text(f"Analisando frames: {frame_idx}/{total_frames}")
    
    cap.release()
    progress_bar.progress(1.0)
    status_text.text("Análise concluída!")
    
    return scenes

def filter_scenes_by_duration(scenes, duration_total, min_duration=5, max_duration=300):
    """Filtra cenas por duração mínima e máxima."""
    filtered = []
    
    for i in range(len(scenes) - 1):
        start = scenes[i]
        end = scenes[i + 1]
        duration = end - start
        
        if min_duration <= duration <= max_duration:
            filtered.append({'start': start, 'end': end})
    
    # Última cena
    if scenes:
        start = scenes[-1]
        end = duration_total
        duration = end - start
        if min_duration <= duration <= max_duration:
            filtered.append({'start': start, 'end': end})
    
    return filtered

def clean_filename(text):
    """Remove caracteres inválidos para nome de arquivo."""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        text = text.replace(char, '')
    return text.strip()

def generate_viral_title_gemini(api_key, movie_name, scene_index):
    """Gera título viral usando Gemini com predição temporal."""
    if not GEMINI_AVAILABLE or not api_key:
        return f"CENA_{scene_index:03d}"
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # Calcula tempo aproximado
        start_min = scene_index * 3
        end_min = start_min + 3
        
        prompt = f"""No filme/vídeo "{movie_name}", o que acontece aproximadamente entre os minutos {start_min} e {end_min}?

Crie um título viral curto (máximo 6 palavras) em Português, usando MAIÚSCULAS.
Responda APENAS com o título, sem aspas ou explicações."""
        
        response = model.generate_content(prompt)
        title = response.text.strip().upper()
        
        # Remove aspas e caracteres inválidos
        title = title.replace('"', '').replace("'", '')
        title = clean_filename(title)
        
        return title[:50]  # Limita tamanho
        
    except Exception as e:
        st.warning(f"Erro ao gerar título com IA: {e}")
        return f"CENA_{scene_index:03d}"

def process_kwai_clip(video_path, start, end, output_dir, clip_number, config):
    """Processa um clip vertical 9:16 para Kwai/TikTok."""
    status_text = st.empty()
    progress_bar = st.progress(0)
    
    try:
        status_text.text(f"Processando clip {clip_number}...")
        
        with VideoFileClip(video_path) as video:
            # Extrai segmento
            clip = video.subclip(start, end)
            
            # Dimensões verticais
            target_w, target_h = 1080, 1920
            
            # Fundo (se fornecido)
            if config.get('template_path') and os.path.exists(config['template_path']):
                from moviepy.editor import ImageClip
                fundo = ImageClip(config['template_path']).set_duration(clip.duration).resize((target_w, target_h))
            else:
                fundo = ColorClip(size=(target_w, target_h), color=(20, 10, 40)).set_duration(clip.duration)
            
            # Crop centralizado
            video_w, video_h = clip.size
            scale = max(target_w / video_w, target_h / video_h)
            clip_resized = clip.resize(scale)
            
            # Centraliza verticalmente
            pos_y = int((target_h - clip_resized.h) * config.get('pos_vertical', 0.5))
            clip_resized = clip_resized.set_position(('center', pos_y))
            
            # Compõe
            final_clip = CompositeVideoClip([fundo, clip_resized], size=(target_w, target_h))
            
            # Gera título (se IA ativada)
            if config.get('use_ai') and config.get('api_key'):
                title = generate_viral_title_gemini(
                    config['api_key'],
                    config.get('movie_name', 'Video'),
                    clip_number
                )
                st.info(f"📝 Título gerado: {title}")
            else:
                title = f"Clip_{clip_number:03d}"
            
            # Nome do arquivo
            filename = f"{title}.mp4"
            output_path = os.path.join(output_dir, filename)
            
            # Exporta
            status_text.text(f"Renderizando {filename}...")
            final_clip.write_videofile(
                output_path,
                codec='libx264',
                audio_codec='aac',
                preset='ultrafast',
                threads=4,
                logger=None
            )
            
            progress_bar.progress(1.0)
            status_text.success(f"✅ Salvo: {filename}")
            
            return output_path
            
    except Exception as e:
        st.error(f"Erro no clip {clip_number}: {e}")
        return None

def main():
    st.title("✂️ Kwai Cut - Detecção Automática de Cenas")
    st.caption("Cortes verticais 9:16 com títulos virais gerados por IA")
    
    # Sidebar - Configurações
    with st.sidebar:
        st.header("⚙️ Configurações")
        
        st.subheader("📐 Posicionamento")
        pos_vertical = st.slider("Posição Vertical", 0.0, 1.0, 0.5, 0.1)
        
        st.subheader("🎯 Detecção de Cenas")
        threshold = st.slider("Sensibilidade", 10, 50, 30, 
                             help="Menor = mais cenas detectadas")
        
        st.subheader("⏱️ Controle de Cortes")
        max_clips = st.number_input("Quantidade Máxima", 1, 50, 10)
        min_duration = st.number_input("Duração Mínima (s)", 5, 300, 30)
        max_duration = st.number_input("Duração Máxima (s)", 10, 600, 180)
        
        st.subheader("🤖 Títulos Virais (IA)")
        use_ai = st.checkbox("Gerar Títulos com Gemini", value=False, 
                            disabled=not GEMINI_AVAILABLE)
        
        if not GEMINI_AVAILABLE:
            st.caption("⚠️ google-generativeai não instalado")
        
        api_key = None
        movie_name = "Video"
        
        if use_ai and GEMINI_AVAILABLE:
            api_key = st.text_input("API Key do Gemini", type="password",
                                   help="Obtenha em: https://makersuite.google.com/app/apikey")
            movie_name = st.text_input("Nome/Nicho do Filme", "Meu Filme",
                                      help="Ex: Matrix, Breaking Bad, Flow Podcast")
        
        template_file = st.file_uploader("Template de Fundo (opcional)", type=['png', 'jpg'])
        template_path = None
        if template_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as f:
                f.write(template_file.getbuffer())
                template_path = f.name
    
    # Área Principal
    uploaded_video = st.file_uploader("📤 Carregar Vídeo Longo", type=['mp4', 'mkv', 'avi'])
    
    if uploaded_video:
        # Salva temporariamente
        tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
        tfile.write(uploaded_video.read())
        video_path = tfile.name
        
        try:
            # Info do vídeo
            with VideoFileClip(video_path) as clip:
                duration = clip.duration
                st.info(f"⏱️ Duração Total: {duration:.1f}s ({duration/60:.1f} min)")
            
            # Botão de detecção
            if st.button("🔍 DETECTAR CENAS", type="primary"):
                with st.spinner("Analisando vídeo..."):
                    # Detecta cenas
                    scenes = detect_scenes(video_path, threshold)
                    
                    if not scenes:
                        st.warning("Nenhuma mudança de cena detectada. Tente reduzir a sensibilidade.")
                    else:
                        st.success(f"✅ {len(scenes)} mudanças de cena detectadas!")
                        
                        # Filtra por duração
                        filtered_scenes = filter_scenes_by_duration(
                            scenes, duration, min_duration, max_duration
                        )
                        
                        # Limita quantidade
                        filtered_scenes = filtered_scenes[:max_clips]
                        
                        st.session_state['scenes'] = filtered_scenes
                        st.info(f"📊 {len(filtered_scenes)} cenas após filtros (duração e quantidade)")
            
            # Mostra lista de cenas
            if 'scenes' in st.session_state and st.session_state['scenes']:
                scenes_list = st.session_state['scenes']
                
                st.write(f"### 📋 Fila de Processamento ({len(scenes_list)} clips)")
                
                # Tabela
                df_data = []
                for i, scene in enumerate(scenes_list):
                    df_data.append({
                        "#": i + 1,
                        "Início": f"{scene['start']:.1f}s",
                        "Fim": f"{scene['end']:.1f}s",
                        "Duração": f"{scene['end'] - scene['start']:.1f}s"
                    })
                st.table(df_data)
                
                # Botão de processamento
                if st.button("🚀 PROCESSAR TODOS OS CLIPS", type="primary"):
                    output_dir = os.path.join(tempfile.gettempdir(), f"kwai_cut_{int(time.time())}")
                    os.makedirs(output_dir, exist_ok=True)
                    
                    config = {
                        'pos_vertical': pos_vertical,
                        'template_path': template_path,
                        'use_ai': use_ai,
                        'api_key': api_key,
                        'movie_name': movie_name
                    }
                    
                    results = []
                    total_progress = st.progress(0)
                    
                    for i, scene in enumerate(scenes_list):
                        st.write(f"### Processando Clip {i+1}/{len(scenes_list)}")
                        
                        result = process_kwai_clip(
                            video_path,
                            scene['start'],
                            scene['end'],
                            output_dir,
                            i + 1,
                            config
                        )
                        
                        if result:
                            results.append(result)
                        
                        total_progress.progress((i + 1) / len(scenes_list))
                    
                    # Sucesso
                    if results:
                        st.success(f"✅ {len(results)} clips processados com sucesso!")
                        st.balloons()
                        
                        # Cria ZIP
                        zip_path = os.path.join(output_dir, "kwai_cut_clips.zip")
                        with zipfile.ZipFile(zip_path, 'w') as zipf:
                            for file_path in results:
                                zipf.write(file_path, os.path.basename(file_path))
                        
                        # Download
                        with open(zip_path, 'rb') as f:
                            st.download_button(
                                label="📦 BAIXAR TODOS (ZIP)",
                                data=f,
                                file_name="kwai_cut_clips.zip",
                                mime="application/zip"
                            )
                        
                        # Downloads individuais
                        st.write("### 📥 Downloads Individuais")
                        for file_path in results:
                            filename = os.path.basename(file_path)
                            with open(file_path, 'rb') as f:
                                st.download_button(
                                    label=f"⬇️ {filename}",
                                    data=f,
                                    file_name=filename,
                                    mime="video/mp4",
                                    key=filename
                                )
        
        except Exception as e:
            st.error(f"Erro ao processar vídeo: {e}")

if __name__ == "__main__":
    main()
