"""
AIVoiceAgent Otimizado para AMD Ryzen 4000 Series

Esta versão foi otimizada para funcionar melhor em sistemas com recursos limitados,
especificamente AMD Ryzen 4000 series com 8-16GB RAM.

Principais otimizações:
- Modelo AI configurável (padrão: modelo menor)
- Gerenciamento de memória aprimorado
- Monitoramento de recursos
- Configurações otimizadas para CPU
"""
import assemblyai as aai
from elevenlabs.client import ElevenLabs
from elevenlabs import stream
import ollama
import psutil
import time
import threading
import sys

class AIVoiceAgentOptimized:
    def __init__(self, model_size="small"):
        """
        Inicializa o agente de voz otimizado
        
        Args:
            model_size: "small" (1.5B), "medium" (3B), "large" (7B)
        """
        # Configuração de APIs - SUBSTITUA PELAS SUAS CHAVES
        aai.settings.api_key = "ASSEMBLYAI_API_KEY"
        self.client = ElevenLabs(
            api_key = "ELEVENLABS_API_KEY"
        )
        
        # Configuração do modelo baseada no tamanho escolhido
        self.model_configs = {
            "small": {
                "model": "tinyllama:1.1b",
                "max_tokens": 150,
                "context_length": 1024,
                "description": "Modelo pequeno - rápido mas menos inteligente"
            },
            "medium": {
                "model": "deepseek-r1:1.5b", 
                "max_tokens": 200,
                "context_length": 2048,
                "description": "Modelo médio - balanceado"
            },
            "large": {
                "model": "deepseek-r1:7b",
                "max_tokens": 300,
                "context_length": 4096,
                "description": "Modelo grande - mais inteligente mas lento"
            }
        }
        
        self.current_config = self.model_configs.get(model_size, self.model_configs["small"])
        self.transcriber = None
        self.monitoring_active = False
        
        # Histórico de conversa otimizado
        self.full_transcript = [
            {
                "role": "system", 
                "content": f"Você é um assistente de IA chamado R1 criado pela DeepSeek. "
                          f"Responda às perguntas em no máximo {self.current_config['max_tokens']} caracteres. "
                          f"Seja conciso e útil."
            },
        ]
        
        # Verificar sistema
        self._check_system_resources()
        
    def _check_system_resources(self):
        """Verifica recursos do sistema e emite avisos se necessário"""
        ram_gb = psutil.virtual_memory().total / (1024**3)
        cpu_count = psutil.cpu_count()
        
        print(f"\n🔍 VERIFICAÇÃO DO SISTEMA:")
        print(f"   RAM Total: {ram_gb:.1f}GB")
        print(f"   CPU Cores: {cpu_count}")
        print(f"   Modelo Selecionado: {self.current_config['model']}")
        print(f"   Descrição: {self.current_config['description']}")
        
        if ram_gb < 8:
            print("   ⚠️ AVISO: RAM baixa. Performance pode ser limitada.")
        elif ram_gb < 16 and "7b" in self.current_config['model']:
            print("   ⚠️ AVISO: RAM limitada para modelo 7B. Considere modelo menor.")
        
        # Verificar se modelo está disponível
        try:
            ollama.show(self.current_config['model'])
            print(f"   ✅ Modelo {self.current_config['model']} disponível")
        except:
            print(f"   ❌ ERRO: Modelo {self.current_config['model']} não encontrado!")
            print(f"   💡 Execute: ollama pull {self.current_config['model']}")
            
    def start_monitoring(self):
        """Inicia monitoramento de recursos em thread separada"""
        self.monitoring_active = True
        monitor_thread = threading.Thread(target=self._monitor_resources, daemon=True)
        monitor_thread.start()
        
    def _monitor_resources(self):
        """Monitora uso de CPU e RAM"""
        while self.monitoring_active:
            cpu_percent = psutil.cpu_percent(interval=1)
            ram_percent = psutil.virtual_memory().percent
            
            if cpu_percent > 90 or ram_percent > 90:
                print(f"\n⚠️ RECURSOS ALTOS - CPU: {cpu_percent:.1f}% | RAM: {ram_percent:.1f}%")
            
            time.sleep(5)
    
    def start_transcription(self):
        """Inicia transcrição em tempo real"""
        print(f"\n🎤 Transcrição em tempo real ativa...")
        print(f"💡 Dica: Fale claramente e aguarde a resposta completa")
        
        # Configurações otimizadas para recursos limitados
        self.transcriber = aai.RealtimeTranscriber(
            sample_rate=16_000,
            on_data=self.on_data,
            on_error=self.on_error,
            on_open=self.on_open,
            on_close=self.on_close,
        )
        
        self.transcriber.connect()
        microphone_stream = aai.extras.MicrophoneStream(sample_rate=16_000)
        self.transcriber.stream(microphone_stream)
        
    def stop_transcription(self):
        """Para transcrição"""
        if self.transcriber:
            self.transcriber.close()
            self.transcriber = None

    def on_open(self, session_opened: aai.RealtimeSessionOpened):
        print(f"🔗 Sessão iniciada: {session_opened.session_id}")
        return
    
    def on_data(self, transcript: aai.RealtimeTranscript):
        """Processa dados de transcrição"""
        if not transcript.text:
            return

        if isinstance(transcript, aai.RealtimeFinalTranscript):
            print(f"\n👤 Você: {transcript.text}")
            self.generate_ai_response(transcript)
        else:
            print(f"🎤 {transcript.text}", end="\r")

    def on_error(self, error: aai.RealtimeError):
        print(f"\n❌ Erro de transcrição: {error}")
        return

    def on_close(self):
        print(f"\n🔌 Sessão de transcrição fechada")
        return    
    
    def generate_ai_response(self, transcript):
        """Gera resposta da IA com otimizações"""
        self.stop_transcription()
        
        # Adicionar ao histórico
        self.full_transcript.append({"role": "user", "content": transcript.text})
        
        # Limitar histórico para economizar memória (manter apenas últimas 10 mensagens)
        if len(self.full_transcript) > 21:  # system + 10 pares user/assistant
            # Manter mensagem do sistema + últimas 10 interações
            self.full_transcript = [self.full_transcript[0]] + self.full_transcript[-20:]
        
        print(f"🤖 DeepSeek R1 está pensando...")
        start_time = time.time()
        
        try:
            # Configurações otimizadas para ollama
            ollama_stream = ollama.chat(
                model=self.current_config['model'],
                messages=self.full_transcript,
                stream=True,
                options={
                    "num_ctx": self.current_config['context_length'],
                    "num_predict": self.current_config['max_tokens'],
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "num_thread": min(psutil.cpu_count(), 8),  # Limitar threads
                }
            )
            
            print("🤖 DeepSeek R1:", end=" ")
            text_buffer = ""
            full_text = ""
            
            for chunk in ollama_stream:
                content = chunk['message']['content']
                text_buffer += content
                full_text += content
                
                # Transmitir áudio em frases menores para AMD Ryzen 4000
                if text_buffer.endswith(('.', '!', '?')) and len(text_buffer.strip()) > 10:
                    try:
                        audio_stream = self.client.generate(
                            text=text_buffer.strip(),
                            model="eleven_turbo_v2",
                            stream=True
                        )
                        print(text_buffer.strip(), end=" ", flush=True)
                        stream(audio_stream)
                        text_buffer = ""
                    except Exception as e:
                        print(f"\n⚠️ Erro no áudio: {e}")
                        break
            
            # Processar texto restante
            if text_buffer.strip():
                try:
                    audio_stream = self.client.generate(
                        text=text_buffer.strip(),
                        model="eleven_turbo_v2",
                        stream=True
                    )
                    print(text_buffer.strip(), flush=True)
                    stream(audio_stream)
                except Exception as e:
                    print(f"\n⚠️ Erro no áudio final: {e}")
            
            # Adicionar resposta ao histórico
            self.full_transcript.append({"role": "assistant", "content": full_text})
            
            # Mostrar tempo de resposta
            response_time = time.time() - start_time
            print(f"\n⏱️ Tempo de resposta: {response_time:.1f}s")
            
        except Exception as e:
            print(f"\n❌ Erro na geração de resposta: {e}")
            print("💡 Dica: Verifique se o modelo está instalado e o Ollama está rodando")
        
        # Reiniciar transcrição
        print(f"\n🎤 Pronto para próxima pergunta...")
        self.start_transcription()

def main():
    """Função principal com menu de seleção"""
    print("="*60)
    print("🎙️ DeepSeek R1 Voice Agent - Versão Otimizada AMD Ryzen 4000")
    print("="*60)
    
    print("\nSelecione o tamanho do modelo:")
    print("1. Pequeno (TinyLlama 1.1B) - Rápido, RAM mínima")
    print("2. Médio (DeepSeek R1 1.5B) - Balanceado")
    print("3. Grande (DeepSeek R1 7B) - Mais inteligente, mais recursos")
    
    while True:
        try:
            choice = input("\nEscolha (1-3): ").strip()
            if choice == "1":
                model_size = "small"
                break
            elif choice == "2":
                model_size = "medium"
                break
            elif choice == "3":
                model_size = "large"
                break
            else:
                print("❌ Escolha inválida. Digite 1, 2 ou 3.")
        except KeyboardInterrupt:
            print("\n👋 Saindo...")
            sys.exit(0)
    
    try:
        # Inicializar agente
        agent = AIVoiceAgentOptimized(model_size=model_size)
        
        # Iniciar monitoramento
        agent.start_monitoring()
        
        print(f"\n🚀 Iniciando agente de voz...")
        print(f"💡 Pressione Ctrl+C para sair")
        
        # Iniciar transcrição
        agent.start_transcription()
        
        # Manter programa rodando
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print(f"\n👋 Encerrando agente de voz...")
            agent.monitoring_active = False
            agent.stop_transcription()
            
    except Exception as e:
        print(f"\n❌ Erro fatal: {e}")
        print(f"💡 Verifique:")
        print(f"   - APIs configuradas corretamente")
        print(f"   - Ollama instalado e rodando")
        print(f"   - Modelo baixado: ollama pull {agent.current_config['model'] if 'agent' in locals() else 'deepseek-r1:1.5b'}")

if __name__ == "__main__":
    main()