# -*- coding: utf-8 -*-
"""
SCRIPT DE INICIALIZAÇÃO - AUTOCORTES
Configura o ambiente e desabilita dependências desnecessárias
"""

import os
import sys
import warnings

# Desabilita TensorFlow (não é necessário para o sistema)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Silencia warnings do TF
os.environ['CUDA_VISIBLE_DEVICES'] = ''   # Desabilita GPU para TF

# Desabilita warnings desnecessários
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=DeprecationWarning)

# Bloqueia import do TensorFlow
class TensorFlowBlocker:
    def find_module(self, fullname, path=None):
        if 'tensorflow' in fullname.lower():
            return self
        return None
    
    def load_module(self, fullname):
        raise ImportError(f"TensorFlow está desabilitado. Use PyTorch. (tentou importar: {fullname})")

# Adiciona bloqueador ao sys.meta_path
sys.meta_path.insert(0, TensorFlowBlocker())

print("=" * 70)
print("AUTOCORTES - AMBIENTE CONFIGURADO")
print("=" * 70)
print("✓ TensorFlow desabilitado (usando PyTorch)")
print("✓ Warnings silenciados")
print("✓ Sistema pronto para uso")
print("=" * 70)
