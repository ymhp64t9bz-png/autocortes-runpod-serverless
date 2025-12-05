# 🚀 GUIA RÁPIDO - ANIMECUT v2.0

## ⚡ NOVIDADES DA VERSÃO 2.0

### 1. **4x MAIS RÁPIDO** com GPU RTX 4060
### 2. **TÍTULOS VIRAIS** com IA Gemini
### 3. **ANTI-SHADOWBAN** para Kwai/TikTok

---

## 📋 INÍCIO RÁPIDO

### Passo 1: Abrir AnimeCut
```bash
cd C:\AutoCortes\modules\AnimeCut
streamlit run app.py
```

### Passo 2: Configurar
1. **Upload**: Arraste seu episódio de anime
2. **Sensibilidade**: 25 (padrão para animes)
3. **Duração**: 30-60s por clip

### Passo 3: (Opcional) Ativar Títulos Virais
1. ✅ Marque "Gerar Títulos com Gemini"
2. ✅ Digite nome do anime: "Naruto"
3. ✅ Cole API Key do Gemini

### Passo 4: (Opcional) Ativar Anti-Shadowban
1. ✅ Marque "Aplicar Filtros Anti-Detecção"
2. ✅ Veja aviso de confirmação

### Passo 5: Processar
1. ✅ Clique em "DETECTAR CENAS E PROCESSAR ANIME"
2. ✅ Aguarde (agora 4x mais rápido!)
3. ✅ Baixe os clips gerados

---

## 🎯 CONFIGURAÇÕES RECOMENDADAS

### Para Máxima Velocidade:
- ✅ GPU detectada automaticamente
- ✅ Preset `p4` (Performance)
- ✅ Sem filtros anti-shadowban

### Para Kwai/TikTok:
- ✅ Ativar "Anti-Shadowban"
- ✅ Ativar "Títulos Virais"
- ✅ Duração: 30-45s

### Para YouTube Shorts:
- ✅ Ativar "Títulos Virais"
- ✅ Duração: 45-60s
- ✅ Anti-Shadowban opcional

---

## 📊 COMPARAÇÃO DE VELOCIDADE

| Configuração | Tempo (60s clip) | Uso GPU |
|--------------|------------------|---------|
| **v1.0 (CPU)** | 5-6 min | 0% |
| **v1.0 (GPU Básica)** | 2-3 min | 40% |
| **v2.0 (GPU Otimizada)** | 30-45s | 95% ⚡ |

---

## 🎬 EXEMPLOS DE TÍTULOS

### Sem IA:
- `AnimeClip_001.mp4`
- `AnimeClip_002.mp4`

### Com IA (Naruto):
- `NARUTO_MOMENTO_EPICO_RASENGAN.mp4`
- `SASUKE_VS_ITACHI_LUTA_FINAL.mp4`
- `SAKURA_PODER_OCULTO_REVELADO.mp4`

---

## 🛡️ FILTROS ANTI-SHADOWBAN

### O que fazem:
1. **Speed +5%**: Acelera imperceptivelmente
2. **Zoom 9%**: Remove bordas, altera fingerprint
3. **Color +7%**: Ajusta contraste/saturação
4. **Noise**: Adiciona ruído digital sutil

### Quando usar:
- ✅ Kwai
- ✅ TikTok
- ✅ Instagram Reels
- ❌ YouTube (não necessário)

---

## ⚠️ TROUBLESHOOTING

### GPU não detectada?
```bash
# Verifique drivers
nvidia-smi
```

### Títulos não gerando?
- Verifique API Key do Gemini
- Certifique-se que digitou o nome do anime

### Muito lento ainda?
- Verifique se GPU está sendo usada
- Veja mensagem: "⚡ GPU: NVIDIA RTX 4060 - ACELERAÇÃO MÁXIMA"

---

## 📞 SUPORTE

Veja documentação completa:
- `IMPLEMENTACAO_COMPLETA.md` - Detalhes técnicos
- `MELHORIAS_IMPLEMENTADAS.md` - Código modificado

---

**Versão**: 2.0  
**Data**: 02/12/2024  
**Status**: ✅ Pronto para uso
