# -*- coding: utf-8 -*-
import sys
import os
import streamlit as st

# Configuração de Caminhos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
MODULES_DIR = os.path.join(ROOT_DIR, 'modules')

sys.path.append(BASE_DIR)
sys.path.append(ROOT_DIR)
sys.path.append(MODULES_DIR)

# Configuração da Página
st.set_page_config(
    page_title="KortexClip AI Studio",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_css():
    # Carrega style.css se existir
    css_path = os.path.join(ROOT_DIR, "style.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def main():
    load_css()
    
    # MENU LATERAL
    with st.sidebar:
        st.markdown("## KORTEXCLIP AI")
        st.markdown("<div style='background-color:#d4edda; color:#155724; padding:5px; border-radius:5px; text-align:center;'>v4.2.0 ECOSSISTEMA</div>", unsafe_allow_html=True)
        st.markdown("---")
        
        # Sistema de Conexão com Google Colab
        st.markdown("### Ambiente de Execução")
        st.caption("Migre para Google Colab Pro para processamento em nuvem")
        
        # Campo de entrada de URL
        colab_url_input = st.text_input(
            "URL do Notebook Colab Pro (Para Setup)",
            placeholder="https://colab.research.google.com/drive/...",
            help="Cole aqui a URL do seu notebook KortexClip AI no Google Colab"
        )
        
        # Botão de conexão
        if st.button("Conectar e Iniciar Setup Remoto", use_container_width=True):
            if colab_url_input:
                # Validação da URL
                if colab_url_input.startswith("https://colab.research.google.com"):
                    st.success("Conexão estabelecida! Redirecionando para iniciar o ambiente KortexClip AI...")
                    
                    # Redirecionamento em nova aba
                    st.markdown(
                        f"""
                        <script>
                            window.open('{colab_url_input}', '_blank');
                        </script>
                        <p style='color: #28a745; font-weight: bold;'>
                            Abrindo Google Colab em nova aba...<br>
                            Se não abrir automaticamente, <a href='{colab_url_input}' target='_blank'>clique aqui</a>
                        </p>
                        """,
                        unsafe_allow_html=True
                    )
                    
                    st.info("Próximos passos no Colab:\n1. Execute a célula de instalação de dependências\n2. Carregue os modelos (DeepSeek + Whisper)\n3. Inicie o processamento de vídeos")
                else:
                    st.error("URL inválida. Certifique-se de usar uma URL do Google Colab.")
            else:
                st.error("Por favor, insira a URL do seu Notebook Colab Pro.")
        
        st.markdown("---")
        
        # Menu Restaurado com 5 Ferramentas
        menu = st.radio(
            "Ferramentas",
            ["Dashboard", "AnimeCut", "KwaiCut", "ViralPro", "Configurações"],
            index=1
        )
        
        st.markdown("---")
        st.progress(1.0, text="RTX 4060: Ativa")

    # ROTEAMENTO DE FERRAMENTAS
    
    if menu == "Dashboard":
        st.title("Painel de Controle")
        st.info("Estatísticas de produção em desenvolvimento.")
        
    elif menu == "AnimeCut":
        try:
            from modules.AnimeCut.app import main as anime_main
            anime_main()
        except ImportError as e:
            st.error(f"Erro ao carregar AnimeCut: {e}")
            
    elif menu == "KwaiCut":
        try:
            from modules.KwaiCut.app import main as kwai_main
            kwai_main()
        except ImportError as e:
            st.error(f"Erro ao carregar KwaiCut: {e}")
            st.info("Certifique-se de que opencv-python está instalado: `pip install opencv-python`")
        
    elif menu == "ViralPro":
        try:
            from modules.VIRAL_PRO.app import main as viral_main
            viral_main()
        except ImportError as e:
            st.error(f"Erro ao carregar ViralPro: {e}")
            st.info("Instale as dependências: `pip install mediapipe faster-whisper opencv-python`")
        
    elif menu == "Configurações":
        st.title("Configurações do Sistema")
        st.write("Hardware: NVIDIA RTX 4060 (8GB VRAM)")
        st.write("IA Local: DeepSeek R1 + Whisper (Serializado)")
        st.write("Renderizador: FFmpeg (NVENC)")

if __name__ == "__main__":
    main()