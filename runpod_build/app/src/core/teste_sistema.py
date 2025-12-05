# -*- coding: utf-8 -*-
"""
TESTE RÁPIDO DO SISTEMA AUTOCORTES
Verifica se tudo está funcionando corretamente
"""

import sys
import os
from pathlib import Path

# Configura encoding UTF-8 para Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def teste_importacoes():
    """Testa se todas as bibliotecas necessárias estão instaladas"""
    print("🔍 Testando importações...\n")
    
    erros = []
    
    # Testa cada biblioteca
    bibliotecas = {
        'moviepy': 'MoviePy',
        'cv2': 'OpenCV',
        'numpy': 'NumPy',
        'PIL': 'Pillow',
        'pandas': 'Pandas',
        'skimage': 'scikit-image',
        'pydub': 'Pydub'
    }
    
    for modulo, nome in bibliotecas.items():
        try:
            __import__(modulo)
            print(f"   ✅ {nome}")
        except ImportError as e:
            print(f"   ❌ {nome} - {e}")
            erros.append(nome)
    
    # Testa FFmpeg
    try:
        import imageio_ffmpeg
        ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
        print(f"   ✅ FFmpeg: {Path(ffmpeg_path).name}")
    except Exception as e:
        print(f"   ❌ FFmpeg - {e}")
        erros.append("FFmpeg")
    
    return erros


def teste_estrutura():
    """Testa se a estrutura de pastas está correta"""
    print("\n📁 Testando estrutura de pastas...\n")
    
    base = Path(__file__).parent
    pastas = ['inputs', 'outputs', 'temp', 'template', 'logs']
    
    erros = []
    for pasta in pastas:
        caminho = base / pasta
        if caminho.exists():
            print(f"   ✅ {pasta}/")
        else:
            print(f"   ❌ {pasta}/ - Não existe")
            erros.append(pasta)
    
    return erros


def teste_modulos():
    """Testa se os módulos do sistema podem ser importados"""
    print("\n🔧 Testando módulos do sistema...\n")
    
    erros = []
    modulos = ['config', 'detector_cenas', 'editor_profissional']
    
    for modulo in modulos:
        try:
            __import__(modulo)
            print(f"   ✅ {modulo}.py")
        except Exception as e:
            print(f"   ❌ {modulo}.py - {e}")
            erros.append(modulo)
    
    return erros


def teste_configuracao():
    """Testa se as configurações estão válidas"""
    print("\n⚙️  Testando configurações...\n")
    
    try:
        import config
        
        print(f"   ✅ Resolução: {config.LARGURA_PADRAO}x{config.ALTURA_PADRAO}")
        print(f"   ✅ Duração: {config.DURACAO_MINIMA}s - {config.DURACAO_MAXIMA}s")
        print(f"   ✅ Codec: {config.VIDEO_CODEC}")
        print(f"   ✅ FPS: {config.FPS_PADRAO}")
        
        return []
    except Exception as e:
        print(f"   ❌ Erro nas configurações: {e}")
        return ['config']


def main():
    """Executa todos os testes"""
    print("""
╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║              🧪 TESTE DO SISTEMA AUTOCORTES 🧪                    ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
""")
    
    erros_total = []
    
    # Executa testes
    erros_total.extend(teste_importacoes())
    erros_total.extend(teste_estrutura())
    erros_total.extend(teste_modulos())
    erros_total.extend(teste_configuracao())
    
    # Resultado final
    print("\n" + "=" * 70)
    if not erros_total:
        print("✅ TODOS OS TESTES PASSARAM!")
        print("\n🚀 O sistema está pronto para uso!")
        print("\n💡 Execute: python main_automacao.py")
    else:
        print("❌ ALGUNS TESTES FALHARAM!")
        print(f"\n⚠️  Problemas encontrados ({len(erros_total)}):")
        for erro in set(erros_total):
            print(f"   • {erro}")
        print("\n💡 Soluções:")
        print("   1. Execute: pip install -r requirements.txt")
        print("   2. Verifique se todas as pastas existem")
        print("   3. Verifique os arquivos .py do sistema")
    
    print("=" * 70)


if __name__ == "__main__":
    main()
