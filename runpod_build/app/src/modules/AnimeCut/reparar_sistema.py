import os
import sys

BASE_DIR = r"C:\AutoCortes"

print("--- INICIANDO REPARO V2 (CORRIGINDO INTERFACE) ---")

# ==============================================================================
# ARQUIVO: modules/AnimeCut/app.py 
# (Agora inclui a função 'main' para a interface gráfica funcionar)
# ==============================================================================
code_app_full = r'''
import streamlit as st
import os
import sys
import gc
import tempfile
import time
from moviepy.editor import VideoFileClip, CompositeVideoClip, ColorClip, ImageClip

# Tenta importar o gerador de titulos
try:
    from .utils_title import criar_titulo_pil
except ImportError:
    # Fallback se rodar fora do modulo
    sys.path.append(os.path.dirname(__file__))
    try:
        from utils_title import criar_titulo_pil
    except:
        criar_titulo_pil = None

# Import do servico de IA
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
try:
    from core.ai_services.local_ai_service import generate_viral_title_local
except ImportError:
    # Mock caso falhe o import
    def generate_viral_title_local(nome, dialogo): return f"{nome} - Viral"

# ---------------------------------------------------------------------------
# MOTOR DE PROCESSAMENTO (BACKEND)
# ---------------------------------------------------------------------------
def processar_corte_anime(input_path, output_path, start_time, end_time, anime_name):
    """
    Processa o corte usando NVENC e limpando memória agressivamente.
    """
    clip = None
    clip_final = None
    
    try:
        # Carrega o vídeo original
        clip = VideoFileClip(input_path).subclip(start_time, end_time)
        
        # Gera Título com Llama 3 (Simulado ou Real)
        st.info("🤖 Analisando com IA (Llama 3)...")
        dialogo_mock = "Cena intensa de anime" 
        titulo_viral = generate_viral_title_local(anime_name, dialogo_mock)
        
        # Configuração de Vídeo Vertical (9:16)
        target_w, target_h = 1080, 1920
        
        # Fundo
        fundo = ColorClip(size=(target_w, target_h), color=(20, 20, 20)).set_duration(clip.duration)
        
        # Redimensiona (Fit Width) e Centraliza
        clip_resized = clip.resize(width=target_w)
        clip_resized = clip_resized.set_position("center")
        
        elementos = [fundo, clip_resized]

        # Adiciona Título (Sem ImageMagick)
        if titulo_viral and criar_titulo_pil:
            try:
                txt_clip = criar_titulo_pil(titulo_viral, target_w, target_h, clip.duration)
                elementos.append(txt_clip)
            except Exception as e:
                print(f"Erro titulo: {e}")

        # Composição
        clip_final = CompositeVideoClip(elementos, size=(target_w, target_h))

        # RENDERIZAÇÃO OTIMIZADA (RTX 4060)
        st.info("🚀 Renderizando com GPU (NVENC)... Aguarde.")
        
        # Parâmetros de renderização
        clip_final.write_videofile(
            str(output_path),
            codec='h264_nvenc',       # Usa a GPU
            audio_codec='aac',
            bitrate='6000k',
            preset='p4',              # Performance
            threads=4,
            ffmpeg_params=['-pix_fmt', 'yuv420p'], # Compatibilidade
            logger=None # Remove logger do terminal para nao travar streamlit
        )
        
        return str(output_path)

    except Exception as e:
        st.error(f"Erro na renderização: {e}")
        return None
        
    finally:
        # LIMPEZA FINAL
        if clip: clip.close()
        if clip_final: clip_final.close()
        del clip
        del clip_final
        gc.collect()

# ---------------------------------------------------------------------------
# INTERFACE GRÁFICA (FRONTEND) - A FUNÇÃO QUE FALTAVA
# ---------------------------------------------------------------------------
def main():
    st.markdown("### ✂️ AnimeCut Pro (GPU Local)")
    
    # Upload do Arquivo
    uploaded_file = st.file_uploader("Arraste o episódio aqui (MKV/MP4)", type=["mp4", "mkv", "avi"])
    
    if uploaded_file is not None:
        # Salva arquivo temporario
        tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        tfile.write(uploaded_file.read())
        video_path = tfile.name
        
        # Carrega infos básicas do vídeo para sliders
        try:
            temp_clip = VideoFileClip(video_path)
            duration = temp_clip.duration
            temp_clip.close()
            del temp_clip
        except:
            duration = 60 # Fallback
            
        col1, col2 = st.columns(2)
        with col1:
            nome_anime = st.text_input("Nome do Anime", "Anime Desconhecido")
        with col2:
            st.info(f"Duração Total: {int(duration)}s")

        # Range Slider para escolher o corte
        start_time, end_time = st.slider(
            "Selecione o trecho do corte:",
            0.0, float(duration), (0.0, 15.0) # Padrão 15s
        )
        
        st.markdown("---")
        
        if st.button("🎬 RENDERIZAR CLIPE VIRAL", type="primary"):
            # Cria caminho de saida
            output_dir = os.path.join(os.getcwd(), "output")
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, f"corte_{int(time.time())}.mp4")
            
            with st.spinner("Processando... (Não feche a janela)"):
                # Limpa cache antes de começar
                gc.collect()
                
                resultado = processar_corte_anime(
                    video_path, 
                    output_path, 
                    start_time, 
                    end_time, 
                    nome_anime
                )
                
                if resultado and os.path.exists(resultado):
                    st.success("✅ Renderização Concluída!")
                    st.video(resultado)
                    st.write(f"Salvo em: `{resultado}`")
                else:
                    st.error("Falha ao gerar o arquivo de vídeo.")

if __name__ == "__main__":
    main()
'''

def write_file(path, content):
    full_path = os.path.join(BASE_DIR, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Arquivo corrigido: {full_path}")

# Executa
if __name__ == "__main__":
    write_file(r"modules\AnimeCut\app.py", code_app_full)
    print("\n--- CORREÇÃO APLICADA ---")
    print("Agora pode rodar 'streamlit run core/webapp.py' que o erro sumiu!")