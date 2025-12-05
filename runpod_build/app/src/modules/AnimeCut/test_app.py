# -*- coding: utf-8 -*-
"""
TESTE SIMPLES - AnimeCut
Versão de teste para verificar se tudo está funcionando
"""

import streamlit as st

st.set_page_config(
    page_title="AnimeCut - Teste",
    page_icon="🎌",
    layout="wide"
)

st.title("🎌 AnimeCut - Teste de Funcionamento")

st.success("✅ Sistema está funcionando!")

# Teste de GPU
st.subheader("🔍 Verificando GPU...")

try:
    import subprocess
    result = subprocess.run(['nvidia-smi'], 
                          capture_output=True, 
                          text=True, 
                          timeout=5)
    if result.returncode == 0:
        st.success("⚡ GPU NVIDIA detectada!")
        st.code(result.stdout[:500])  # Mostra primeiras linhas
    else:
        st.warning("💻 GPU não detectada, usando CPU")
except Exception as e:
    st.warning(f"💻 GPU não detectada: {e}")
    st.info("Sistema vai usar CPU para processamento")

# Teste de imports
st.subheader("📦 Verificando Dependências...")

try:
    import cv2
    st.success(f"✅ OpenCV: {cv2.__version__}")
except Exception as e:
    st.error(f"❌ OpenCV: {e}")

try:
    import moviepy
    st.success(f"✅ MoviePy instalado")
except Exception as e:
    st.error(f"❌ MoviePy: {e}")

try:
    import numpy as np
    st.success(f"✅ NumPy: {np.__version__}")
except Exception as e:
    st.error(f"❌ NumPy: {e}")

st.markdown("---")
st.info("Se você vê esta mensagem, o AnimeCut está pronto para usar!")
st.info("Execute: streamlit run app.py")
