# 🎬 AutoCortes - RunPod Serverless

Sistema completo de processamento de vídeo com IA para criação automática de cortes virais.

## 🚀 Features

- ✅ Transcrição automática com Whisper
- ✅ Geração de títulos virais com Llama 3
- ✅ Análise de segmentos com DeepSeek R1
- ✅ Renderização com NVENC (GPU)
- ✅ Anti-shadowban automático
- ✅ Suporte a templates personalizados
- ✅ Processamento em lote
- ✅ Serverless ready

## 📋 Requisitos

### GPU
- NVIDIA GPU com CUDA 11.8+
- Mínimo 8GB VRAM (recomendado 12GB+)

### Modelos
- Whisper Medium (~1.5GB)
- Llama 3 8B Q4 (~4.5GB)
- DeepSeek R1 8B Q4 (~4.5GB)

## 🛠️ Instalação Local

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/autocortes-runpod.git
cd autocortes-runpod

# Crie ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instale dependências
pip install -r requirements.txt

# Teste localmente
python handler.py
```

## ☁️ Deploy no RunPod Serverless

### 1. Preparar Imagem Docker

```bash
# Build
docker build -t autocortes-serverless .

# Tag para DockerHub
docker tag autocortes-serverless seu-usuario/autocortes-serverless:latest

# Push
docker push seu-usuario/autocortes-serverless:latest
```

### 2. Configurar no RunPod

1. Acesse [RunPod Serverless](https://www.runpod.io/serverless)
2. Crie novo endpoint
3. Configure:
   - **Docker Image**: `seu-usuario/autocortes-serverless:latest`
   - **GPU**: A6000 ou superior
   - **Container Disk**: 20GB
   - **Volume**: 50GB (para modelos)

### 3. Testar Endpoint

```python
import requests

endpoint_url = "https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/run"
headers = {
    "Authorization": "Bearer YOUR_API_KEY"
}

# Processar vídeo
payload = {
    "input": {
        "operation": "process_video",
        "video_url": "https://example.com/video.mp4",
        "anime_name": "Naruto",
        "mode": "auto",
        "config": {
            "font_size": 70,
            "text_color": "#FFD700",
            "stroke_color": "#000000",
            "stroke_width": 6,
            "pos_vertical": 0.15,
            "anti_shadowban": True,
            "usar_ia": True
        }
    }
}

response = requests.post(endpoint_url, json=payload, headers=headers)
print(response.json())
```

## 📊 Operações Suportadas

### 1. Processar Vídeo Completo

```json
{
  "input": {
    "operation": "process_video",
    "video_url": "https://...",
    "anime_name": "Nome do Anime",
    "mode": "auto",
    "config": {...}
  }
}
```

### 2. Transcrever Áudio

```json
{
  "input": {
    "operation": "transcribe_audio",
    "audio_url": "https://..."
  }
}
```

### 3. Gerar Título

```json
{
  "input": {
    "operation": "generate_title",
    "anime_name": "Naruto",
    "dialogue": "Texto do diálogo..."
  }
}
```

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────┐
│         RunPod Serverless               │
├─────────────────────────────────────────┤
│  handler.py                             │
│    ├─ initialize_models()               │
│    ├─ process_video()                   │
│    ├─ process_auto_mode()               │
│    └─ process_manual_mode()             │
├─────────────────────────────────────────┤
│  /app/src/                              │
│    ├─ core/                             │
│    │   ├─ ai_services/                  │
│    │   │   └─ local_ai_service.py       │
│    │   └─ webapp.py                     │
│    ├─ modules/                          │
│    │   ├─ AnimeCut/                     │
│    │   ├─ KwaiCut/                      │
│    │   └─ VIRAL_PRO/                    │
│    └─ fontes/                           │
├─────────────────────────────────────────┤
│  Models (cached)                        │
│    ├─ Whisper Medium                    │
│    ├─ Llama 3 8B                        │
│    └─ DeepSeek R1 8B                    │
└─────────────────────────────────────────┘
```

## ⚙️ Configuração

### Variáveis de Ambiente

```bash
# .env
RUNPOD_API_KEY=your_key_here
GEMINI_API_KEY=your_gemini_key  # Fallback opcional
```

## 📈 Performance

- **Transcrição**: ~2-3min para 10min de vídeo
- **Geração de Título**: ~5-10s por título
- **Renderização**: ~30s por corte de 60s

## 🐛 Troubleshooting

### Erro de VRAM

```bash
# Reduzir tamanho do modelo Whisper
# Em handler.py, mudar de 'medium' para 'small'
```

### Timeout

```bash
# Aumentar timeout no RunPod
# Settings > Timeout > 600s
```

## 📝 Licença

Proprietário - AutoCortes Team

## 🤝 Suporte

- Email: suporte@autocortes.com
- Discord: [Link]
- Docs: [Link]

---

**Desenvolvido com ❤️ por AutoCortes Team**
