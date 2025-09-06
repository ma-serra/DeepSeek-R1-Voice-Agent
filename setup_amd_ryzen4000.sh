#!/bin/bash

# Script de Configuração para DeepSeek R1 Voice Agent
# Otimizado para AMD Ryzen 4000 Series
# 
# Este script automatiza a instalação e configuração do sistema

set -e  # Parar em caso de erro

echo "======================================================================"
echo "🚀 CONFIGURAÇÃO DEEPSEEK R1 VOICE AGENT - AMD RYZEN 4000 OPTIMIZED"
echo "======================================================================"

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para imprimir com cor
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️ $1${NC}"
}

# Verificar se é Ubuntu/Debian
if ! command -v apt &> /dev/null; then
    print_error "Este script é para Ubuntu/Debian. Para outros sistemas, instale manualmente."
    exit 1
fi

print_info "Verificando sistema..."

# Verificar recursos do sistema
RAM_GB=$(free -g | awk '/^Mem:/{print $2}')
CPU_CORES=$(nproc)
DISK_FREE_GB=$(df / | awk 'NR==2{print int($4/1024/1024)}')

echo ""
echo "📊 RECURSOS DO SISTEMA:"
echo "   RAM: ${RAM_GB}GB"
echo "   CPU Cores: ${CPU_CORES}"
echo "   Espaço Livre: ${DISK_FREE_GB}GB"

# Verificar requisitos mínimos
if [ "$RAM_GB" -lt 8 ]; then
    print_error "RAM insuficiente: ${RAM_GB}GB (mínimo: 8GB)"
    exit 1
fi

if [ "$DISK_FREE_GB" -lt 20 ]; then
    print_error "Espaço em disco insuficiente: ${DISK_FREE_GB}GB (mínimo: 20GB)"
    exit 1
fi

print_status "Recursos do sistema adequados"

# Verificar se é AMD Ryzen
CPU_INFO=$(cat /proc/cpuinfo | grep "model name" | head -1)
if [[ $CPU_INFO == *"AMD"* ]] && [[ $CPU_INFO == *"Ryzen"* ]]; then
    print_status "CPU AMD Ryzen detectada: $CPU_INFO"
else
    print_warning "CPU não identificada como AMD Ryzen, mas continuando..."
fi

echo ""
print_info "Iniciando instalação..."

# 1. Atualizar sistema
print_info "1/7 Atualizando sistema..."
sudo apt update
print_status "Sistema atualizado"

# 2. Instalar dependências do sistema
print_info "2/7 Instalando dependências do sistema..."
sudo apt install -y portaudio19-dev python3-pip curl build-essential git
print_status "Dependências do sistema instaladas"

# 3. Instalar Python dependencies
print_info "3/7 Instalando dependências Python..."
pip3 install --user "assemblyai[extras]" ollama elevenlabs psutil
print_status "Dependências Python instaladas"

# 4. Instalar Ollama
print_info "4/7 Instalando Ollama..."
if ! command -v ollama &> /dev/null; then
    curl -fsSL https://ollama.com/install.sh | sh
    print_status "Ollama instalado"
else
    print_status "Ollama já instalado"
fi

# 5. Iniciar serviço Ollama
print_info "5/7 Iniciando serviço Ollama..."
ollama serve &
OLLAMA_PID=$!
sleep 5  # Aguardar o serviço iniciar

# 6. Baixar modelo apropriado baseado na RAM
print_info "6/7 Baixando modelo de IA apropriado..."

if [ "$RAM_GB" -ge 32 ]; then
    MODEL="deepseek-r1:7b"
    print_info "RAM abundante (${RAM_GB}GB) - baixando modelo grande (7B)"
elif [ "$RAM_GB" -ge 16 ]; then
    MODEL="deepseek-r1:1.5b"
    print_info "RAM adequada (${RAM_GB}GB) - baixando modelo médio (1.5B)"
else
    MODEL="tinyllama:1.1b"
    print_info "RAM limitada (${RAM_GB}GB) - baixando modelo pequeno (1.1B)"
fi

echo "Baixando modelo: $MODEL"
echo "⏳ Isso pode demorar alguns minutos..."
ollama pull $MODEL
print_status "Modelo $MODEL baixado com sucesso"

# 7. Criar configuração otimizada
print_info "7/7 Criando arquivos de configuração..."

# Criar script de configuração de API
cat > configure_apis.sh << 'EOF'
#!/bin/bash
echo "🔑 CONFIGURAÇÃO DE APIS"
echo "======================"
echo ""
echo "Para usar o DeepSeek R1 Voice Agent, você precisa de:"
echo "1. Chave da API AssemblyAI (gratuita)"
echo "2. Chave da API ElevenLabs (gratuita)"
echo ""
echo "📋 PASSOS:"
echo "1. AssemblyAI:"
echo "   - Acesse: https://www.assemblyai.com/"
echo "   - Crie conta gratuita"
echo "   - Copie sua API key"
echo ""
echo "2. ElevenLabs:"
echo "   - Acesse: https://elevenlabs.io/"
echo "   - Crie conta gratuita"
echo "   - Copie sua API key"
echo ""
echo "3. Edite os arquivos:"
echo "   - AIVoiceAgent.py (linha 52 e 54)"
echo "   - AIVoiceAgent_AMD_Optimized.py (linha 34 e 37)"
echo ""
read -p "Pressione Enter para continuar..."
EOF

chmod +x configure_apis.sh

# Criar script de execução otimizado
cat > run_optimized.sh << EOF
#!/bin/bash
echo "🎙️ Iniciando DeepSeek R1 Voice Agent (Versão AMD Ryzen 4000)"
echo "============================================================="

# Verificar se Ollama está rodando
if ! pgrep -x "ollama" > /dev/null; then
    echo "🚀 Iniciando Ollama..."
    ollama serve &
    sleep 3
fi

# Verificar modelo disponível
if ! ollama list | grep -q "$MODEL"; then
    echo "⚠️ Modelo $MODEL não encontrado. Baixando..."
    ollama pull $MODEL
fi

# Configurar performance da CPU para AMD Ryzen
echo "⚡ Otimizando performance da CPU..."
echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor > /dev/null 2>&1 || true

# Executar versão otimizada
python3 AIVoiceAgent_AMD_Optimized.py
EOF

chmod +x run_optimized.sh

print_status "Arquivos de configuração criados"

# Matar processo Ollama temporário
kill $OLLAMA_PID 2>/dev/null || true

echo ""
echo "======================================================================"
print_status "INSTALAÇÃO CONCLUÍDA COM SUCESSO!"
echo "======================================================================"
echo ""
echo "📋 PRÓXIMOS PASSOS:"
echo ""
echo "1. 🔑 Configure suas API keys:"
echo "   ./configure_apis.sh"
echo ""
echo "2. 🎙️ Execute o agente de voz:"
echo "   ./run_optimized.sh"
echo ""
echo "📊 CONFIGURAÇÃO DO SEU SISTEMA:"
echo "   - Modelo recomendado: $MODEL"
echo "   - RAM disponível: ${RAM_GB}GB"
echo "   - CPU Cores: ${CPU_CORES}"
echo ""
echo "📖 DOCUMENTAÇÃO COMPLETA:"
echo "   - Análise detalhada: ANALISE_AMD_RYZEN_4000.md"
echo "   - Verificar sistema: python3 verificar_compatibilidade.py"
echo ""
print_warning "IMPORTANTE: Configure as API keys antes de usar!"
echo ""