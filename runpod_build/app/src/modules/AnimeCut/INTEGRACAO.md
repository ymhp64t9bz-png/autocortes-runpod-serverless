# 🎌 AnimeCut - Integração com Ecossistema AutoCortes

Este documento descreve como o **AnimeCut** se integra ao ecossistema de ferramentas do AutoCortes.

---

## 📊 Visão Geral do Ecossistema

```
AutoCortes (Raiz)
├── AutoCortes Clássico    → Cortes automáticos gerais
├── Detector de Cenas      → Análise e exportação de cenas
├── Kwai Cut              → Cortes longos para filmes
├── AnimeCut              → Cortes otimizados para animes ⭐ NOVO
├── ViralPro              → Geração de títulos virais
└── SISTEMA_DE_TITULOS    → Títulos inteligentes com IA
```

---

## 🔗 Pontos de Integração

### 1. **Compartilhamento de Assets**

O AnimeCut pode usar os mesmos assets do AutoCortes:

```python
# Usar templates do AutoCortes
template_path = "c:/AutoCortes/assets/templates/anime_template.png"

# Usar fontes do AutoCortes
from config_fonts import FONT_PATHS
```

### 2. **Integração com SISTEMA_DE_TITULOS**

Os clips gerados pelo AnimeCut podem receber títulos automáticos:

```python
# Exemplo de integração
from SISTEMA_DE_TITULOS.title_generator import generate_smart_title

# Gerar título para clip de anime
titulo = generate_smart_title(
    filename="naruto_ep_100.mp4",
    scene_index=5,
    platform="tiktok"
)
```

### 3. **Integração com ViralPro**

Usar o ViralPro para gerar títulos virais para clips de anime:

```python
# Exemplo de integração
from VIRAL_PRO.viral_title_generator import generate_viral_title

# Gerar título viral
titulo_viral = generate_viral_title(
    video_path="AnimeClip_001.mp4",
    mode="viral",
    platform="shorts"
)
```

---

## 🚀 Fluxo de Trabalho Integrado

### **Workflow Completo: Anime → Clips → Títulos → Publicação**

```
1. AnimeCut
   ↓ Processa episódio de anime
   ↓ Gera clips verticais (AnimeClip_001.mp4, etc.)
   
2. SISTEMA_DE_TITULOS ou ViralPro
   ↓ Gera títulos para cada clip
   ↓ "NARUTO MODO SÁBIO ÉPICO! 🔥"
   
3. Publicação Manual
   ↓ Upload para TikTok/Shorts/Reels
   ↓ Com título otimizado
```

---

## 📁 Estrutura de Diretórios Compartilhados

```
AutoCortes/
├── assets/                    # Compartilhado
│   ├── templates/
│   │   ├── anime_template.png
│   │   └── kwai_template.png
│   └── fonts/
│       └── NotoSans-Bold.ttf
│
├── AnimeCut/                  # Módulo AnimeCut
│   ├── app.py
│   ├── config.py
│   ├── requirements.txt
│   ├── README.md
│   └── outputs/               # Clips gerados
│
├── SISTEMA_DE_TITULOS/        # Geração de títulos
│   └── title_generator.py
│
└── ViralPro/                  # Títulos virais
    └── viral_title_generator.py
```

---

## 🔧 Configuração da Integração

### **Opção 1: Importação Direta**

Se você quiser usar o AnimeCut como módulo dentro do AutoCortes:

```python
# Em webapp.py do AutoCortes
import sys
sys.path.append('AnimeCut')

from AnimeCut.app import detectar_mudancas_cena_anime, processar_corte_anime

# Usar funções do AnimeCut
info = detectar_mudancas_cena_anime(video_path, sensibilidade=25)
```

### **Opção 2: Standalone com Referências**

Manter AnimeCut independente mas referenciar assets:

```python
# Em AnimeCut/app.py
import os
from pathlib import Path

# Caminho para assets do AutoCortes
AUTOCORTES_ROOT = Path(__file__).parent.parent
ASSETS_DIR = AUTOCORTES_ROOT / "assets"
TEMPLATES_DIR = ASSETS_DIR / "templates"
```

---

## 🎯 Casos de Uso Integrados

### **Caso 1: Pipeline Completo de Anime**

```python
# 1. Processar anime com AnimeCut
clips = processar_anime("naruto_ep_100.mp4")

# 2. Gerar títulos com SISTEMA_DE_TITULOS
for i, clip in enumerate(clips):
    titulo = generate_smart_title(
        filename=clip,
        scene_index=i,
        platform="tiktok"
    )
    # Salvar título em metadata ou arquivo separado
```

### **Caso 2: Batch Processing com Múltiplas Ferramentas**

```python
# Processar múltiplos episódios
episodios = ["ep_01.mp4", "ep_02.mp4", "ep_03.mp4"]

for ep in episodios:
    # AnimeCut: Gerar clips
    clips = processar_anime(ep)
    
    # ViralPro: Gerar títulos virais
    for clip in clips:
        titulo = generate_viral_title(clip, mode="viral")
        
    # AutoCortes: Aplicar efeitos adicionais (opcional)
    # ...
```

---

## 📊 Comparação de Ferramentas

| Ferramenta | Uso Principal | Integração com AnimeCut |
|------------|---------------|-------------------------|
| **AutoCortes Clássico** | Cortes gerais | Compartilha assets e templates |
| **Kwai Cut** | Filmes longos | Mesma base de código, diferentes parâmetros |
| **AnimeCut** | Animes | - |
| **ViralPro** | Títulos virais | Gera títulos para clips de anime |
| **SISTEMA_DE_TITULOS** | Títulos IA | Gera títulos inteligentes para clips |

---

## 🔄 API de Integração (Futuro)

### **Proposta de API Unificada**

```python
# api_integrada.py (futuro)

class AutoCortesAPI:
    def __init__(self):
        self.anime_cut = AnimeCut()
        self.kwai_cut = KwaiCut()
        self.title_gen = TitleGenerator()
        self.viral_pro = ViralPro()
    
    def processar_anime_completo(self, video_path, gerar_titulos=True):
        """
        Pipeline completo: Anime → Clips → Títulos
        """
        # 1. Gerar clips
        clips = self.anime_cut.processar(video_path)
        
        # 2. Gerar títulos (opcional)
        if gerar_titulos:
            for clip in clips:
                titulo = self.title_gen.gerar(clip)
                clip.titulo = titulo
        
        return clips
```

---

## 🛠️ Manutenção e Atualizações

### **Sincronização de Dependências**

Manter `requirements.txt` sincronizado entre módulos:

```bash
# Atualizar todas as dependências
cd c:\AutoCortes
pip install -r requirements.txt

cd AnimeCut
pip install -r requirements.txt
```

### **Versionamento**

Usar tags de versão para controle:

```
AnimeCut v1.0.0 - Lançamento inicial
AnimeCut v1.1.0 - Integração com SISTEMA_DE_TITULOS
AnimeCut v1.2.0 - API unificada
```

---

## 📝 Checklist de Integração

- [x] AnimeCut criado como módulo separado
- [x] Documentação completa (README.md)
- [x] Script de inicialização (START.bat)
- [x] Arquivo de configuração (config.py)
- [ ] Integração com SISTEMA_DE_TITULOS
- [ ] Integração com ViralPro
- [ ] Compartilhamento de assets
- [ ] API unificada
- [ ] Testes de integração
- [ ] Documentação de API

---

## 🎓 Próximos Passos

1. **Testar AnimeCut standalone**
   ```bash
   cd c:\AutoCortes\AnimeCut
   START.bat
   ```

2. **Criar templates de anime**
   - Adicionar templates em `c:\AutoCortes\assets\templates\`
   - Usar no AnimeCut

3. **Integrar com títulos**
   - Conectar AnimeCut com SISTEMA_DE_TITULOS
   - Gerar títulos automáticos para clips

4. **Criar workflow automatizado**
   - Script que processa anime + gera títulos
   - Exporta tudo pronto para publicação

---

## 🤝 Contribuindo

Para adicionar novas integrações:

1. Criar branch de feature
2. Implementar integração
3. Atualizar documentação
4. Testar com casos de uso reais
5. Merge para main

---

**AnimeCut** - Parte do ecossistema AutoCortes 🎌
