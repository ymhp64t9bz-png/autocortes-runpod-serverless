# AutoCortes RunPod Serverless
FROM runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel-ubuntu22.04

# Metadados
LABEL maintainer="AutoCortes Team"
LABEL description="AutoCortes - AI Video Processing Serverless"

# Variáveis de ambiente
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive
ENV CUDA_HOME=/usr/local/cuda
ENV PATH=$CUDA_HOME/bin:$PATH
ENV LD_LIBRARY_PATH=$CUDA_HOME/lib64:$LD_LIBRARY_PATH

# Atualizar sistema
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    git \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Criar diretório de trabalho
WORKDIR /app

# Copiar requirements
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar aplicação
COPY app/ /app/

# Criar diretórios necessários
RUN mkdir -p /app/models /app/temp /app/output

# Download de modelos (opcional - pode ser feito em runtime)
# RUN python -c "import whisper; whisper.load_model('medium')"

# Expor porta (se necessário para testes)
EXPOSE 8000

# Comando de inicialização
CMD ["python", "handler.py"]
