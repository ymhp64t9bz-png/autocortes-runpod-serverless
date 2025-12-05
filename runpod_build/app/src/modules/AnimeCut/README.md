# 🎌 AnimeCut - Cortes Automáticos para Animes

Sistema profissional de cortes automáticos **otimizado especificamente para animes**, com detecção inteligente de cenas, preservação de qualidade visual e recursos exclusivos para conteúdo anime.

---

## 🌟 Características Principais

### 🎨 **Otimizado para Anime**
- **Análise HSV de Cores**: Detecta cores saturadas típicas de anime
- **Detecção de Opening/Ending**: Identifica automaticamente OP (1-2.5 min) e ED (últimos 2.5 min)
- **Preservação de Qualidade**: Bitrate alto (8000k) para manter detalhes da arte
- **Transições Abruptas**: Algoritmo ajustado para cortes rápidos de anime

### ⚡ **Aceleração por GPU**
- **NVIDIA CUDA/NVENC**: Usa GPU para processamento ultra-rápido
- **3-4x mais rápido**: Clip de 45s em ~10s (vs ~40s na CPU)
- **Detecção Automática**: Detecta GPU e usa automaticamente
- **RTX 4060 Otimizado**: Configurações específicas para sua GPU
- **[📖 Documentação GPU](GPU_ACELERACAO.md)**

### ✂️ **Cortes Personalizados**
- **Duração ajustável**: 15-90 segundos (ideal: 30-45s)
- **Sensibilidade otimizada**: Valor padrão 25 (vs 30 do Kwai Cut)
- **Intervalo de frames menor**: 15 frames (vs 30) para maior precisão

### 🎨 **Visual Premium**
- Gradiente rosa→roxo estilo anime
- Interface moderna com animações suaves
- Badges e cards com design vibrante
- Métricas visuais destacadas

---

## 🚀 Como Usar

### 1. **Instalação**

```bash
cd c:\AutoCortes\AnimeCut
pip install -r requirements.txt
```

### 2. **Executar**

```bash
streamlit run app.py
```

### 3. **Processar Anime**

1. **Configure as opções**:
   - Sensibilidade: 25 (padrão para anime)
   - Pular Opening/Ending: ✅ Ativado
   - Duração máxima: 45s (ideal para clips)
   - Posição vertical: 0.5 (centralizado)

2. **Upload**:
   - Envie seu episódio de anime (MP4, MKV, AVI)
   - Opcionalmente, envie um template de fundo personalizado

3. **Processar**:
   - Clique em "🚀 DETECTAR CENAS E PROCESSAR ANIME"
   - Aguarde a detecção e processamento
   - Baixe os clips individuais ou todos em ZIP

---

## 📊 Comparação: AnimeCut vs Kwai Cut

| Característica | AnimeCut | Kwai Cut |
|----------------|----------|----------|
| **Público-alvo** | Animes | Filmes/Séries |
| **Sensibilidade padrão** | 25 | 30 |
| **Intervalo de frames** | 15 | 30 |
| **Detecção OP/ED** | ✅ Sim | ❌ Não |
| **Análise de cor** | HSV (cores saturadas) | Histograma grayscale |
| **Duração padrão** | 45s | 240s (4min) |
| **Bitrate** | 8000k (alta qualidade) | Padrão |
| **Preset** | slow (melhor qualidade) | ultrafast |
| **Gradiente** | Rosa→Roxo | Azul escuro |
| **Nomenclatura** | AnimeClip_001.mp4 | Corte_001.mp4 |

---

## 🎯 Casos de Uso

### ✅ **Ideal para:**
- Criar clips de momentos épicos de animes
- Extrair cenas de luta/ação
- Compilar momentos engraçados
- Gerar conteúdo para TikTok/Shorts/Reels
- Preservar qualidade visual da animação

### ❌ **Não recomendado para:**
- Filmes live-action (use Kwai Cut)
- Vídeos longos sem mudanças de cena
- Conteúdo com transições suaves

---

## 🛠️ Tecnologias

- **Streamlit**: Interface web moderna
- **OpenCV**: Processamento de vídeo e detecção de cenas
- **MoviePy**: Edição e composição de vídeo
- **NumPy**: Processamento numérico
- **Pillow**: Manipulação de imagens

---

## 📁 Estrutura de Arquivos

```
AnimeCut/
├── app.py                 # Aplicação principal
├── requirements.txt       # Dependências
├── README.md             # Esta documentação
├── START.bat             # Inicializador Windows
└── outputs/              # Clips gerados (criado automaticamente)
```

---

## 🎨 Templates Personalizados

Você pode criar seus próprios templates de fundo:

### Especificações:
- **Resolução**: 1080x1920 (vertical 9:16)
- **Formato**: PNG, JPG ou JPEG
- **Estilo**: Fundos com tema anime funcionam melhor

### Exemplos de templates:
- Gradientes vibrantes (rosa, roxo, azul)
- Padrões geométricos
- Texturas de papel japonês
- Fundos com elementos anime (sakura, nuvens, etc.)

---

## 🔧 Configurações Avançadas

### Sensibilidade
- **10-15**: Muitos cortes (cenas muito curtas)
- **20-25**: Ideal para animes (padrão)
- **30-40**: Poucos cortes (apenas mudanças grandes)

### Duração dos Cortes
- **15-30s**: Clips rápidos para TikTok
- **30-45s**: Ideal para Instagram Reels
- **45-90s**: Cenas completas para YouTube Shorts

### Posição Vertical
- **0.0-0.3**: Topo (bom para legendas na parte inferior)
- **0.4-0.6**: Centro (padrão, mais equilibrado)
- **0.7-1.0**: Base (bom para legendas no topo)

---

## 📝 Notas Técnicas

### Por que HSV para Animes?
Animes têm **cores altamente saturadas** e **paletas vibrantes**. A análise HSV (Hue, Saturation, Value) detecta melhor essas mudanças de cor do que análise em escala de cinza.

### Por que Intervalo Menor?
Animes têm **cortes mais rápidos** e **transições abruptas**. Analisar a cada 15 frames (vs 30) garante que não percamos mudanças de cena importantes.

### Por que Bitrate Alto?
A **arte anime** tem **linhas finas** e **detalhes precisos**. Compressão excessiva causa artefatos visíveis. Bitrate de 8000k preserva a qualidade visual.

---

## 🐛 Solução de Problemas

### Muitos cortes detectados
- Aumente a sensibilidade (30-35)
- Aumente o intervalo de frames no código (linha 191)

### Poucos cortes detectados
- Diminua a sensibilidade (15-20)
- Desative "Pular Opening/Ending"

### Qualidade baixa
- Verifique se o vídeo original tem boa qualidade
- Considere aumentar o bitrate no código (linha 407)

### Processamento lento
- Reduza o bitrate para 5000k
- Mude preset de 'slow' para 'medium'
- Reduza a duração máxima dos cortes

---

## 🎯 Roadmap Futuro

- [ ] Detecção automática de legendas
- [ ] Remoção/preservação de legendas
- [ ] Detecção de personagens (face detection)
- [ ] Filtros estilo anime (cel shading, etc.)
- [ ] Suporte para batch processing
- [ ] Integração com APIs de anime (MAL, AniList)
- [ ] Detecção de cenas de ação vs diálogo
- [ ] Templates pré-configurados por gênero

---

## 📄 Licença

Parte do ecossistema **AutoCortes** - Desenvolvido para processamento profissional de vídeos.

---

## 🤝 Integração com Ecossistema

O **AnimeCut** faz parte do ecossistema de ferramentas:

- **AutoCortes**: Cortes automáticos gerais
- **Kwai Cut**: Cortes para filmes longos
- **AnimeCut**: Cortes otimizados para animes ⭐
- **ViralPro**: Geração de títulos virais
- **SISTEMA_DE_TITULOS**: Títulos inteligentes com IA

---

**Desenvolvido com ❤️ para a comunidade anime**
