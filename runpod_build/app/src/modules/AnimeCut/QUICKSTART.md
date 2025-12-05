# 🚀 AnimeCut - Guia Rápido de 5 Minutos

## ⚡ Início Rápido

### 1️⃣ **Instalação (1 minuto)**

```bash
cd c:\AutoCortes\AnimeCut
pip install -r requirements.txt
```

### 2️⃣ **Executar (30 segundos)**

**Opção A - Windows:**
```bash
START.bat
```

**Opção B - Manual:**
```bash
streamlit run app.py
```

### 3️⃣ **Processar Anime (3 minutos)**

1. **Abra o navegador** em `http://localhost:8501`

2. **Configure** (sidebar esquerda):
   - ✅ Pular Opening/Ending
   - Sensibilidade: **25**
   - Duração: **45s**

3. **Upload** do episódio de anime

4. **Clique** em "🚀 DETECTAR CENAS E PROCESSAR ANIME"

5. **Aguarde** o processamento

6. **Baixe** os clips em ZIP

---

## 🎯 Configurações Recomendadas

### Para TikTok/Shorts (30-45s)
```
Sensibilidade: 25
Duração Máxima: 45s
Pular Opening/Ending: ✅
Posição Vertical: 0.5 (centro)
```

### Para Instagram Reels (45-60s)
```
Sensibilidade: 25
Duração Máxima: 60s
Pular Opening/Ending: ✅
Posição Vertical: 0.5 (centro)
```

### Para Clips Longos (60-90s)
```
Sensibilidade: 30
Duração Máxima: 90s
Pular Opening/Ending: ❌
Posição Vertical: 0.5 (centro)
```

---

## 🎨 Tipos de Anime

### Ação/Shounen (Naruto, One Piece, etc.)
```
Sensibilidade: 20-25 (muitas mudanças de cena)
Duração: 30-45s
```

### Slice of Life (K-On, Nichijou, etc.)
```
Sensibilidade: 30-35 (menos mudanças de cena)
Duração: 45-60s
```

### Drama/Romance (Your Name, etc.)
```
Sensibilidade: 25-30
Duração: 45-60s
```

---

## 📊 Resultados Esperados

| Episódio (24min) | Sensibilidade | Clips Gerados |
|------------------|---------------|---------------|
| Anime de Ação    | 25            | 15-25 clips   |
| Slice of Life    | 30            | 8-15 clips    |
| Drama            | 25            | 10-18 clips   |

---

## 🐛 Problemas Comuns

### "Muitos cortes detectados"
**Solução:** Aumente a sensibilidade para 30-35

### "Poucos cortes detectados"
**Solução:** Diminua a sensibilidade para 15-20

### "Processamento muito lento"
**Solução:** 
- Reduza a duração máxima
- Use vídeos de menor resolução
- Feche outros programas

### "Qualidade ruim"
**Solução:**
- Use vídeos de alta qualidade (1080p+)
- Verifique se o anime original tem boa qualidade

---

## 💡 Dicas Pro

1. **Opening/Ending**: Sempre ative "Pular Opening/Ending" para focar no conteúdo

2. **Duração Ideal**: 
   - TikTok: 30-45s
   - Instagram: 45-60s
   - YouTube Shorts: 30-60s

3. **Sensibilidade**:
   - Animes de ação: 20-25
   - Animes calmos: 30-35

4. **Templates**: Crie templates personalizados (1080x1920) para dar identidade

5. **Batch Processing**: Processe vários episódios de uma vez

---

## 📁 Estrutura de Saída

```
AnimeCut/
└── outputs/
    ├── AnimeClip_001.mp4  (45s, 8000k bitrate)
    ├── AnimeClip_002.mp4
    ├── AnimeClip_003.mp4
    └── ...
```

---

## 🎬 Workflow Completo

```
1. Baixar episódio de anime
   ↓
2. Abrir AnimeCut (START.bat)
   ↓
3. Configurar (sensibilidade, duração)
   ↓
4. Upload do episódio
   ↓
5. Processar (aguardar 2-5 min)
   ↓
6. Baixar clips em ZIP
   ↓
7. Publicar no TikTok/Shorts/Reels
```

---

## ⚙️ Requisitos Mínimos

- **Python**: 3.8+
- **RAM**: 4GB+
- **Espaço**: 2GB+ livre
- **Processador**: Dual-core+

---

## 📞 Suporte

Problemas? Verifique:
1. `README.md` - Documentação completa
2. `INTEGRACAO.md` - Integração com ecossistema
3. `config.py` - Configurações avançadas

---

**Pronto para criar clips incríveis de anime! 🎌**
