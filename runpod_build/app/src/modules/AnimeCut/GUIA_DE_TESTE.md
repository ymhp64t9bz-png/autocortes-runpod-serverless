# 🧪 AnimeCut - Guia de Teste

## Como Testar o AnimeCut

Este guia vai te ajudar a testar todas as funcionalidades do AnimeCut.

---

## ⚡ TESTE RÁPIDO (5 minutos)

### **1. Verificar Instalação**

```bash
cd c:\AutoCortes\AnimeCut
python --version
# Deve mostrar Python 3.8+
```

### **2. Instalar Dependências**

```bash
pip install -r requirements.txt
```

**Esperado**: Instalação de:
- streamlit
- opencv-python
- numpy
- moviepy
- Pillow

### **3. Iniciar Aplicação**

```bash
START.bat
# ou
streamlit run app.py
```

**Esperado**: 
- Navegador abre automaticamente
- URL: `http://localhost:8501`
- Interface com gradiente rosa→roxo

---

## 🎨 TESTE DE INTERFACE

### **Elementos Visuais**

Verifique se aparecem:

- [x] Header com gradiente rosa→roxo
- [x] Título "🎌 AnimeCut - Cortes Automáticos para Animes"
- [x] Badges coloridos (Preservação, Detecção OP/ED, etc.)
- [x] Sidebar com configurações
- [x] Área principal para upload

### **Configurações Disponíveis**

Verifique na sidebar:

- [x] Upload de template (PNG/JPG)
- [x] Slider de sensibilidade (10-40)
- [x] Checkbox "Pular Opening/Ending"
- [x] Checkbox "Adicionar Borda"
- [x] Slider de duração (15-90s)
- [x] Slider de posição vertical (0-1)
- [x] Card de dicas

---

## 🎬 TESTE DE PROCESSAMENTO

### **Preparação**

1. **Obter vídeo de teste**
   - Baixe um episódio de anime curto (5-10 min)
   - Formatos: MP4, MKV, AVI
   - Resolução: 720p ou 1080p

### **Teste Básico**

1. **Upload do vídeo**
   - Arraste ou clique para upload
   - Verifique métricas (duração, resolução, FPS)

2. **Configurar**
   ```
   Sensibilidade: 25
   Duração: 45s
   Pular OP/ED: ✅
   Posição: 0.5
   ```

3. **Processar**
   - Clique em "🚀 DETECTAR CENAS E PROCESSAR ANIME"
   - Observe barra de progresso
   - Aguarde conclusão

### **Resultados Esperados**

- [x] Detecção de cenas (2-3 min)
- [x] Mensagem de Opening/Ending detectado
- [x] Processamento de clips (3-5 min)
- [x] Lista de clips gerados
- [x] Botão de download ZIP

---

## 🔍 TESTE DE DETECÇÃO

### **Teste 1: Detecção de Opening**

**Vídeo**: Episódio completo de anime (20+ min)

**Configuração**:
```
Pular Opening/Ending: ✅
Sensibilidade: 25
```

**Esperado**:
- Mensagem: "🎵 Opening detectado: 60s - 150s"
- Clips não gerados nesse intervalo

### **Teste 2: Detecção de Ending**

**Vídeo**: Episódio completo de anime (20+ min)

**Configuração**:
```
Pular Opening/Ending: ✅
Sensibilidade: 25
```

**Esperado**:
- Mensagem: "🎵 Ending detectado: XXs - XXs"
- Clips não gerados nesse intervalo

### **Teste 3: Sensibilidade**

**Teste A - Baixa (15)**:
- Muitos cortes detectados (20-30)
- Clips curtos

**Teste B - Média (25)**:
- Cortes moderados (10-20)
- Clips balanceados

**Teste C - Alta (35)**:
- Poucos cortes (5-10)
- Clips longos

---

## 📊 TESTE DE QUALIDADE

### **Verificar Clips Gerados**

1. **Localização**
   - Diretório temporário (mostrado na interface)
   - Nomenclatura: `AnimeClip_001.mp4`, `AnimeClip_002.mp4`, etc.

2. **Propriedades**
   ```
   Resolução: 1080x1920 (vertical)
   FPS: 30
   Codec: H.264
   Áudio: AAC
   Tamanho: ~100-150MB por clip
   ```

3. **Qualidade Visual**
   - Detalhes preservados
   - Cores vibrantes
   - Sem artefatos visíveis
   - Áudio sincronizado

---

## 🎨 TESTE DE TEMPLATES

### **Criar Template de Teste**

1. **Criar imagem 1080x1920**
   - Use qualquer editor de imagem
   - Gradiente ou cor sólida
   - Salvar como PNG

2. **Upload do Template**
   - Carregar na interface
   - Verificar preview

3. **Processar com Template**
   - Vídeo deve aparecer sobre o template
   - Fundo personalizado visível

---

## 🔧 TESTE DE CONFIGURAÇÕES

### **Teste de Duração**

**15s**:
- Clips muito curtos
- Ideal para TikTok

**45s** (padrão):
- Clips balanceados
- Ideal para Reels

**90s**:
- Clips longos
- Ideal para Shorts

### **Teste de Posição**

**0.0 (Topo)**:
- Vídeo no topo
- Espaço embaixo

**0.5 (Centro)**:
- Vídeo centralizado
- Balanceado

**1.0 (Base)**:
- Vídeo na base
- Espaço em cima

---

## 📥 TESTE DE DOWNLOAD

### **Download Individual**

- [x] Clips listados na interface
- [x] Tamanho mostrado (MB)
- [x] Nome correto (AnimeClip_XXX.mp4)

### **Download ZIP**

1. **Clicar em "📥 BAIXAR TODOS OS CLIPS (ZIP)"**
2. **Verificar**:
   - Arquivo ZIP criado
   - Todos os clips incluídos
   - Nomenclatura correta
   - Tamanho total correto

---

## 🐛 TESTE DE ERROS

### **Teste 1: Vídeo Inválido**

**Ação**: Upload de arquivo não-vídeo (TXT, PNG)

**Esperado**: Mensagem de erro

### **Teste 2: Vídeo Corrompido**

**Ação**: Upload de vídeo corrompido

**Esperado**: Erro ao ler vídeo

### **Teste 3: Sem Mudanças de Cena**

**Ação**: Vídeo estático (sensibilidade alta)

**Esperado**: "⚠️ Nenhuma mudança de cena detectada"

---

## 📊 CHECKLIST DE TESTE COMPLETO

### **Interface**
- [ ] Header aparece corretamente
- [ ] Badges visíveis
- [ ] Sidebar funcional
- [ ] Animações suaves
- [ ] Cores corretas (rosa→roxo)

### **Upload**
- [ ] Upload de vídeo funciona
- [ ] Métricas mostradas
- [ ] Preview (se aplicável)
- [ ] Upload de template funciona

### **Detecção**
- [ ] Barra de progresso funciona
- [ ] Opening detectado
- [ ] Ending detectado
- [ ] Cenas detectadas corretamente

### **Processamento**
- [ ] Clips gerados
- [ ] Qualidade preservada
- [ ] Áudio sincronizado
- [ ] Nomenclatura correta

### **Download**
- [ ] Lista de clips aparece
- [ ] Tamanhos corretos
- [ ] ZIP criado corretamente
- [ ] Todos os clips incluídos

### **Configurações**
- [ ] Sensibilidade funciona
- [ ] Duração funciona
- [ ] Posição funciona
- [ ] Pular OP/ED funciona
- [ ] Template funciona

---

## 🎯 CASOS DE TESTE ESPECÍFICOS

### **Caso 1: Anime de Ação (Naruto, One Piece)**

```
Configuração:
- Sensibilidade: 20-25
- Duração: 30-45s
- Pular OP/ED: ✅

Esperado:
- 15-25 clips
- Muitas mudanças de cena
- Clips dinâmicos
```

### **Caso 2: Slice of Life (K-On, Nichijou)**

```
Configuração:
- Sensibilidade: 30-35
- Duração: 45-60s
- Pular OP/ED: ✅

Esperado:
- 8-15 clips
- Menos mudanças de cena
- Clips mais longos
```

### **Caso 3: Drama/Romance (Your Name)**

```
Configuração:
- Sensibilidade: 25-30
- Duração: 45-60s
- Pular OP/ED: ❌ (pode não ter)

Esperado:
- 10-18 clips
- Mudanças moderadas
- Clips balanceados
```

---

## 📝 RELATÓRIO DE TESTE

### **Template de Relatório**

```
Data: ___/___/___
Versão: 1.0.0
Testador: ___________

TESTES REALIZADOS:
[ ] Interface
[ ] Upload
[ ] Detecção
[ ] Processamento
[ ] Download
[ ] Configurações

RESULTADOS:
✅ Passou: ___
❌ Falhou: ___
⚠️  Avisos: ___

PROBLEMAS ENCONTRADOS:
1. _______________
2. _______________
3. _______________

SUGESTÕES:
1. _______________
2. _______________
3. _______________

CONCLUSÃO:
[ ] Aprovado para produção
[ ] Necessita correções
[ ] Necessita melhorias
```

---

## 🚀 PRÓXIMOS PASSOS APÓS TESTE

### **Se Tudo Funcionar**
1. ✅ Marcar como aprovado
2. ✅ Documentar resultados
3. ✅ Usar em produção

### **Se Houver Problemas**
1. 📝 Documentar problemas
2. 🔧 Corrigir bugs
3. 🧪 Testar novamente

---

**Boa sorte com os testes!** 🎌

*AnimeCut v1.0.0 - Sistema de Testes*
