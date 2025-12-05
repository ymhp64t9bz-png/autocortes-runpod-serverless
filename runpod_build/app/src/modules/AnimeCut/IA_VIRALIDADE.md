# 🤖 Detecção de Viralidade com IA (Gemini)

O AnimeCut agora suporta análise inteligente de episódios usando o **Google Gemini 2.0 Flash**.

## 🚀 Como Funciona

1. **Upload**: O vídeo é enviado para a API do Google (File API).
2. **Análise Multimodal**: O Gemini assiste ao vídeo e analisa:
   - Ação visual (lutas, explosões)
   - Diálogos e contexto (roteiro)
   - Emoções dos personagens
3. **Seleção**: A IA retorna os timestamps exatos dos momentos mais "virais" com um score de 0 a 100.
4. **Corte**: O sistema corta exatamente nos momentos indicados pela IA.

## 🔑 Configuração

Você precisa de uma **API Key do Google Gemini**.

1. Obtenha em: [aistudio.google.com](https://aistudio.google.com/)
2. Configure de uma das formas:
   - No arquivo `.env`: `GEMINI_API_KEY=sua_chave`
   - No arquivo `config.py`: `GEMINI_API_KEY = "sua_chave"`
   - Diretamente na interface do AnimeCut (campo de senha)

## 🆚 Comparativo

| Método | Velocidade | Precisão Viral | Contexto | Custo |
|--------|------------|----------------|----------|-------|
| **Visual (Padrão)** | Rápido (Local) | Baixa (apenas mudanças de cena) | Nenhum | Grátis |
| **IA Viral (Gemini)** | Lento (Upload + Análise) | Altíssima (entende o conteúdo) | Total | Grátis (Tier Free) |

## 📝 Notas

- O modelo usado é o `gemini-2.0-flash`, otimizado para velocidade e janelas de contexto longas (vídeos inteiros).
- O upload pode demorar dependendo da sua internet.
- A análise da IA leva cerca de 30-60 segundos após o upload.
