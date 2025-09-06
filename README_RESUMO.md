# 🎙️ DeepSeek R1 Voice Agent - Guia Completo para AMD Ryzen 4000

## 📱 Resumo Rápido

O **DeepSeek R1 Voice Agent** é um assistente de voz com IA que:
- 🎤 **Escuta** sua voz em tempo real
- 🧠 **Processa** com IA (DeepSeek R1) rodando localmente
- 🔊 **Responde** com voz sintetizada natural
- 💬 **Mantém** contexto da conversa

## 🖥️ Seu Sistema AMD Ryzen 4000

### ✅ O que VAI FUNCIONAR:
- Captura e reprodução de áudio
- Reconhecimento de voz (AssemblyAI)
- Síntese de voz (ElevenLabs)
- Interface do sistema

### ⚠️ LIMITAÇÕES:
- **Velocidade**: Respostas em 30-60 segundos (não tempo real)
- **Modelo IA**: Precisa usar versão menor (1.5B em vez de 7B)
- **Recursos**: Alto uso de CPU e RAM durante uso

### 🎯 CONFIGURAÇÃO RECOMENDADA:
- **Modelo**: DeepSeek R1 1.5B (em vez de 7B)
- **RAM**: Mínimo 8GB, ideal 16GB+
- **Conexão**: Internet estável para APIs

## 🚀 Instalação Rápida

### Opção 1: Script Automático (RECOMENDADO)
```bash
chmod +x setup_amd_ryzen4000.sh
./setup_amd_ryzen4000.sh
```

### Opção 2: Instalação Manual
```bash
# 1. Dependências do sistema
sudo apt update
sudo apt install portaudio19-dev python3-pip curl

# 2. Dependências Python
pip3 install "assemblyai[extras]" ollama elevenlabs

# 3. Instalar Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 4. Baixar modelo apropriado
ollama pull deepseek-r1:1.5b  # Para 8-16GB RAM
# OU
ollama pull tinyllama:1.1b    # Para sistemas limitados
```

## 🔑 Configurar APIs (OBRIGATÓRIO)

### 1. AssemblyAI (Speech-to-Text)
- Acesse: https://www.assemblyai.com/
- Crie conta gratuita (5 horas/mês grátis)
- Copie sua API key

### 2. ElevenLabs (Text-to-Speech)
- Acesse: https://elevenlabs.io/
- Crie conta gratuita (10.000 caracteres/mês)
- Copie sua API key

### 3. Configurar no código:
Edite `AIVoiceAgent_AMD_Optimized.py`:
```python
# Linha 34-37:
aai.settings.api_key = "SUA_CHAVE_ASSEMBLYAI"
self.client = ElevenLabs(api_key="SUA_CHAVE_ELEVENLABS")
```

## 🎮 Como Usar

### Execução Simples:
```bash
python3 AIVoiceAgent_AMD_Optimized.py
```

### Execução com Script:
```bash
./run_optimized.sh
```

### Fluxo de Uso:
1. 🎤 **Fale** - O sistema escuta continuamente
2. ⏳ **Aguarde** - Processamento pode levar 30-60s
3. 🔊 **Escute** - Resposta em áudio
4. 🔄 **Continue** - Conversa mantém contexto

## 🔧 Ferramentas Incluídas

### 1. Verificar Compatibilidade:
```bash
python3 verificar_compatibilidade.py
```

### 2. Configurar APIs:
```bash
./configure_apis.sh
```

### 3. Executar Otimizado:
```bash
./run_optimized.sh
```

## 📊 Escolha do Modelo

| Modelo | RAM Necessária | Velocidade | Qualidade |
|--------|---------------|------------|-----------|
| TinyLlama 1.1B | 4-8GB | Rápido | Básica |
| DeepSeek R1 1.5B | 8-16GB | Médio | Boa |
| DeepSeek R1 7B | 16-32GB | Lento | Excelente |

**Para AMD Ryzen 4000**: Recomendamos **DeepSeek R1 1.5B**

## ⚡ Otimizações para AMD Ryzen 4000

### Performance da CPU:
```bash
# Modo performance
echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
```

### Monitoramento:
```bash
# Ver uso de recursos
htop
# ou
watch -n 1 "free -h"
```

### Swap adicional (se necessário):
```bash
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

## 🔍 Solução de Problemas

### "Modelo não encontrado":
```bash
ollama list  # Ver modelos instalados
ollama pull deepseek-r1:1.5b  # Baixar modelo
```

### "Ollama connection error":
```bash
ollama serve  # Iniciar Ollama
```

### "Audio device not found":
```bash
sudo apt install portaudio19-dev
# Verificar microfone com outros aplicativos
```

### Performance muito lenta:
- Use modelo menor: `tinyllama:1.1b`
- Feche outros aplicativos
- Verifique temperatura da CPU

## 💰 Custos das APIs

### AssemblyAI:
- **Grátis**: 5 horas/mês
- **Pago**: $0.37 por hora de áudio

### ElevenLabs:
- **Grátis**: 10.000 caracteres/mês
- **Pago**: $5/mês para 30.000 caracteres

### Estimativa de uso:
- **1 hora de conversa**: ~5.000-10.000 caracteres
- **Plano gratuito**: Suficiente para testes
- **Uso regular**: Considere planos pagos

## 📁 Arquivos Importantes

- `ANALISE_AMD_RYZEN_4000.md` - Análise técnica completa
- `AIVoiceAgent_AMD_Optimized.py` - Versão otimizada
- `verificar_compatibilidade.py` - Verificação do sistema
- `setup_amd_ryzen4000.sh` - Instalação automática
- `README_RESUMO.md` - Este arquivo

## 🎯 Expectativas Realistas

### ✅ Funcionará Bem:
- Reconhecimento de voz preciso
- Qualidade de áudio excelente
- Interface estável

### ⚠️ Limitações:
- Resposta não é instantânea (30-60s)
- Uso alto de recursos durante processamento
- Necessita internet para APIs

### 🚀 Para Melhor Experiência:
- RAM: 16GB+ 
- Modelo: DeepSeek R1 1.5B
- Internet: Conexão estável
- Microfone: Boa qualidade

---

## 📞 Suporte

**Problemas?** Consulte:
1. `verificar_compatibilidade.py` - Diagnóstico
2. `ANALISE_AMD_RYZEN_4000.md` - Documentação técnica
3. GitHub Issues - Reportar bugs

**Dica**: Sempre teste com modelo pequeno primeiro!