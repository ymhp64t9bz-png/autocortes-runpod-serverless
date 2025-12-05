#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AUTOCORTES RUNPOD SERVERLESS HANDLER
====================================
Handler principal para processar requisições no RunPod Serverless.
"""

import runpod
import os
import sys
import gc
import torch
import tempfile
import json
from pathlib import Path

# Adiciona src ao path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Imports do sistema
from core.ai_services.local_ai_service import (
    transcribe_audio_batch,
    generate_viral_title_batch,
    manually_unload_whisper,
    manually_unload_llama
)

# Variáveis globais para cache de modelos
MODELS_LOADED = False

def initialize_models():
    """Inicializa modelos uma única vez"""
    global MODELS_LOADED
    
    if not MODELS_LOADED:
        print("[INIT] Carregando modelos...")
        
        # Pre-load Whisper
        try:
            from core.ai_services.local_ai_service import load_whisper_model
            load_whisper_model()
            print("[INIT] ✅ Whisper carregado")
        except Exception as e:
            print(f"[INIT] ⚠️  Whisper: {e}")
        
        # Pre-load Llama
        try:
            from core.ai_services.local_ai_service import load_llama_model
            load_llama_model()
            print("[INIT] ✅ Llama carregado")
        except Exception as e:
            print(f"[INIT] ⚠️  Llama: {e}")
        
        MODELS_LOADED = True
        print("[INIT] ✅ Modelos inicializados")

def process_video(job):
    """
    Processa vídeo completo
    
    Input esperado:
    {
        "input": {
            "video_url": "https://...",
            "anime_name": "Nome do Anime",
            "mode": "auto|manual",
            "config": {
                "font_size": 70,
                "text_color": "#FFD700",
                "stroke_color": "#000000",
                "stroke_width": 6,
                "pos_vertical": 0.15,
                "anti_shadowban": true,
                "usar_ia": true
            }
        }
    }
    """
    try:
        input_data = job['input']
        video_url = input_data.get('video_url')
        anime_name = input_data.get('anime_name', 'Anime')
        mode = input_data.get('mode', 'auto')
        config = input_data.get('config', {})
        
        print(f"[PROCESS] Iniciando processamento: {anime_name}")
        print(f"[PROCESS] Modo: {mode}")
        
        # Download do vídeo
        import requests
        with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as tmp_video:
            response = requests.get(video_url, stream=True)
            for chunk in response.iter_content(chunk_size=8192):
                tmp_video.write(chunk)
            video_path = tmp_video.name
        
        print(f"[PROCESS] ✅ Vídeo baixado: {video_path}")
        
        # Processar baseado no modo
        if mode == 'auto':
            result = process_auto_mode(video_path, anime_name, config)
        else:
            result = process_manual_mode(video_path, anime_name, config)
        
        # Limpar
        os.remove(video_path)
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        return result
        
    except Exception as e:
        import traceback
        return {
            "error": str(e),
            "traceback": traceback.format_exc()
        }

def process_auto_mode(video_path, anime_name, config):
    """Modo automático com DeepSeek"""
    print("[AUTO] Iniciando modo automático...")
    
    # Extrair áudio
    from moviepy.editor import VideoFileClip
    clip = VideoFileClip(video_path)
    
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_audio:
        clip.audio.write_audiofile(tmp_audio.name, codec='pcm_s16le')
        audio_path = tmp_audio.name
    
    clip.close()
    
    # Transcrever
    print("[AUTO] Transcrevendo áudio...")
    transcript = transcribe_audio_batch(audio_path)
    transcript_text = transcript['text'] if isinstance(transcript, dict) else transcript
    
    # Analisar com DeepSeek (se disponível)
    # TODO: Implementar análise de segmentos
    
    # Gerar título
    print("[AUTO] Gerando título...")
    titulo = generate_viral_title_batch(anime_name, transcript_text)
    
    # Limpar
    os.remove(audio_path)
    
    return {
        "mode": "auto",
        "transcript": transcript_text,
        "title": titulo,
        "segments": []  # TODO
    }

def process_manual_mode(video_path, anime_name, config):
    """Modo manual com cortes definidos"""
    print("[MANUAL] Iniciando modo manual...")
    
    # TODO: Implementar lógica de cortes manuais
    
    return {
        "mode": "manual",
        "message": "Modo manual em desenvolvimento"
    }

def handler(job):
    """
    Handler principal do RunPod
    
    Suporta múltiplas operações:
    - process_video: Processa vídeo completo
    - transcribe_audio: Apenas transcrição
    - generate_title: Apenas geração de título
    """
    
    # Inicializa modelos (apenas uma vez)
    initialize_models()
    
    # Determina operação
    operation = job['input'].get('operation', 'process_video')
    
    print(f"[HANDLER] Operação: {operation}")
    
    if operation == 'process_video':
        return process_video(job)
    
    elif operation == 'transcribe_audio':
        audio_url = job['input'].get('audio_url')
        # Download e transcrição
        # TODO: Implementar
        return {"operation": "transcribe_audio", "status": "not_implemented"}
    
    elif operation == 'generate_title':
        anime_name = job['input'].get('anime_name')
        dialogue = job['input'].get('dialogue')
        titulo = generate_viral_title_batch(anime_name, dialogue)
        return {"title": titulo}
    
    else:
        return {"error": f"Operação desconhecida: {operation}"}

# Inicializa RunPod
if __name__ == "__main__":
    print("[RUNPOD] Iniciando serverless handler...")
    runpod.serverless.start({"handler": handler})
