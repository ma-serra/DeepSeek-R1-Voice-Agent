#!/usr/bin/env python3
"""
Sistema de Verificação de Compatibilidade
DeepSeek R1 Voice Agent - AMD Ryzen 4000 Series

Este script verifica se seu sistema AMD Ryzen 4000 pode executar 
o DeepSeek R1 Voice Agent e sugere otimizações.
"""

import psutil
import platform
import subprocess
import sys
import os
from pathlib import Path

def get_system_info():
    """Coleta informações do sistema"""
    info = {
        'os': platform.system(),
        'os_version': platform.release(),
        'architecture': platform.machine(),
        'processor': platform.processor(),
        'ram_total': round(psutil.virtual_memory().total / (1024**3), 2),
        'ram_available': round(psutil.virtual_memory().available / (1024**3), 2),
        'cpu_count': psutil.cpu_count(),
        'disk_free': round(psutil.disk_usage('/').free / (1024**3), 2)
    }
    return info

def check_cpu_info():
    """Verifica informações específicas da CPU"""
    try:
        if platform.system() == "Linux":
            with open('/proc/cpuinfo', 'r') as f:
                cpuinfo = f.read()
                if 'AMD' in cpuinfo and ('Ryzen' in cpuinfo or 'ryzen' in cpuinfo):
                    return True, "CPU AMD Ryzen detectada"
                else:
                    return False, "CPU AMD Ryzen não detectada"
        else:
            # Para Windows ou outros sistemas
            cpu_name = platform.processor()
            if 'AMD' in cpu_name and 'Ryzen' in cpu_name:
                return True, f"CPU detectada: {cpu_name}"
            else:
                return False, f"CPU detectada: {cpu_name} (não é AMD Ryzen)"
    except:
        return None, "Não foi possível detectar informações da CPU"

def check_dependencies():
    """Verifica dependências instaladas"""
    deps = {
        'python': sys.version,
        'pip': None,
        'ollama': None,
        'portaudio': None
    }
    
    # Verificar pip
    try:
        import pip
        deps['pip'] = pip.__version__
    except:
        deps['pip'] = "Não instalado"
    
    # Verificar ollama
    try:
        result = subprocess.run(['ollama', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            deps['ollama'] = result.stdout.strip()
        else:
            deps['ollama'] = "Não instalado"
    except:
        deps['ollama'] = "Não instalado"
    
    # Verificar PortAudio (aproximado)
    if platform.system() == "Linux":
        try:
            result = subprocess.run(['dpkg', '-l', 'portaudio19-dev'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                deps['portaudio'] = "Instalado"
            else:
                deps['portaudio'] = "Não instalado"
        except:
            deps['portaudio'] = "Status desconhecido"
    else:
        deps['portaudio'] = "Verificação não disponível"
    
    return deps

def analyze_compatibility(info):
    """Analisa compatibilidade do sistema"""
    recommendations = []
    warnings = []
    errors = []
    
    # Verificar RAM
    if info['ram_total'] < 8:
        errors.append(f"❌ RAM insuficiente: {info['ram_total']}GB (mínimo: 8GB)")
    elif info['ram_total'] < 16:
        warnings.append(f"⚠️ RAM limitada: {info['ram_total']}GB (recomendado: 16GB+)")
        recommendations.append("💡 Considere usar modelo menor (1.5B em vez de 7B)")
    else:
        recommendations.append(f"✅ RAM adequada: {info['ram_total']}GB")
    
    # Verificar espaço em disco
    if info['disk_free'] < 20:
        errors.append(f"❌ Espaço em disco insuficiente: {info['disk_free']}GB (mínimo: 20GB)")
    else:
        recommendations.append(f"✅ Espaço em disco adequado: {info['disk_free']}GB")
    
    # Verificar CPU
    if info['cpu_count'] < 4:
        warnings.append(f"⚠️ Poucos cores de CPU: {info['cpu_count']} (recomendado: 4+)")
    else:
        recommendations.append(f"✅ CPU adequada: {info['cpu_count']} cores")
    
    return recommendations, warnings, errors

def suggest_model_size(ram_gb):
    """Sugere tamanho de modelo baseado na RAM"""
    if ram_gb >= 32:
        return "deepseek-r1:7b", "Modelo completo recomendado"
    elif ram_gb >= 16:
        return "deepseek-r1:1.5b", "Modelo médio recomendado"
    elif ram_gb >= 8:
        return "tinyllama:1.1b", "Modelo pequeno recomendado"
    else:
        return "API online", "Use APIs online (OpenAI, etc.)"

def print_report(info, deps, cpu_info, recommendations, warnings, errors):
    """Imprime relatório completo"""
    print("="*60)
    print("🔍 RELATÓRIO DE COMPATIBILIDADE - DeepSeek R1 Voice Agent")
    print("="*60)
    
    print(f"\n📊 INFORMAÇÕES DO SISTEMA:")
    print(f"   SO: {info['os']} {info['os_version']}")
    print(f"   Arquitetura: {info['architecture']}")
    print(f"   RAM Total: {info['ram_total']}GB")
    print(f"   RAM Disponível: {info['ram_available']}GB")
    print(f"   CPU Cores: {info['cpu_count']}")
    print(f"   Espaço Livre: {info['disk_free']}GB")
    
    print(f"\n🔧 DETECÇÃO DE CPU:")
    if cpu_info[0] is True:
        print(f"   ✅ {cpu_info[1]}")
    elif cpu_info[0] is False:
        print(f"   ⚠️ {cpu_info[1]}")
    else:
        print(f"   ❓ {cpu_info[1]}")
    
    print(f"\n📦 DEPENDÊNCIAS:")
    for dep, status in deps.items():
        if status and "Não instalado" not in status:
            print(f"   ✅ {dep}: {status}")
        else:
            print(f"   ❌ {dep}: {status}")
    
    print(f"\n🎯 ANÁLISE DE COMPATIBILIDADE:")
    
    if errors:
        print(f"\n❌ PROBLEMAS CRÍTICOS:")
        for error in errors:
            print(f"   {error}")
    
    if warnings:
        print(f"\n⚠️ AVISOS:")
        for warning in warnings:
            print(f"   {warning}")
    
    if recommendations:
        print(f"\n✅ RECOMENDAÇÕES:")
        for rec in recommendations:
            print(f"   {rec}")
    
    # Sugestão de modelo
    model, reason = suggest_model_size(info['ram_total'])
    print(f"\n🤖 MODELO RECOMENDADO:")
    print(f"   Modelo: {model}")
    print(f"   Motivo: {reason}")
    
    # Comandos de instalação
    print(f"\n📋 PRÓXIMOS PASSOS:")
    if errors:
        print("   1. ❌ Resolva os problemas críticos primeiro")
        print("   2. ❌ Sistema não compatível no momento")
    else:
        print("   1. ✅ Instale dependências faltantes")
        print("   2. ✅ Configure APIs (AssemblyAI + ElevenLabs)")
        print(f"   3. ✅ Baixe modelo: ollama pull {model}")
        print("   4. ✅ Execute: python AIVoiceAgent.py")

def main():
    print("Verificando compatibilidade do sistema...")
    
    # Coletar informações
    info = get_system_info()
    cpu_info = check_cpu_info()
    deps = check_dependencies()
    
    # Analisar compatibilidade
    recommendations, warnings, errors = analyze_compatibility(info)
    
    # Gerar relatório
    print_report(info, deps, cpu_info, recommendations, warnings, errors)
    
    print("\n" + "="*60)
    print("📖 Para informações detalhadas, consulte: ANALISE_AMD_RYZEN_4000.md")
    print("="*60)

if __name__ == "__main__":
    main()