#!/usr/bin/env python3
"""
Script de teste para o Sistema de Gestão Docente (SGD) - Alocação de Docentes
"""

import sys
import json
from datetime import datetime
from alocacao_docentes import alocar_docentes, verificar_disponibilidade_docente, obter_alocacoes_existentes

def teste_alocacao_basica():
    """Teste básico do sistema de alocação"""
    print("=== TESTE BÁSICO DO SISTEMA DE ALOCAÇÃO ===")
    
    # Dados de exemplo de docentes
    docentes_exemplo = [
        {
            'id': '1',
            'mat': 1001,
            'ch': 120.0,  # Tipo 1 (>100h)
            'tipo': 1,
            'saldo': 120.0,
            'rest': [3, 4]  # Não disponível quinta e sexta
        },
        {
            'id': '2',
            'mat': 1002,
            'ch': 80.0,   # Tipo 2 (50-99h)
            'tipo': 2,
            'saldo': 80.0,
            'rest': [0, 1]  # Não disponível segunda e terça
        },
        {
            'id': '3',
            'mat': 1003,
            'ch': 40.0,   # Tipo 3 (<50h)
            'tipo': 3,
            'saldo': 40.0,
            'rest': [2]   # Não disponível quarta
        },
        {
            'id': '4',
            'mat': 1004,
            'ch': 60.0,   # Tipo 2 (50-99h)
            'tipo': 2,
            'saldo': 60.0,
            'rest': []    # Disponível todos os dias
        }
    ]
    
    try:
        # Processa a alocação
        print("Processando alocação...")
        resultado = alocar_docentes(docentes_exemplo)
        
        # Exibe resultados
        print(f"\n✅ Alocação processada com sucesso!")
        print(f"📊 Estatísticas:")
        print(f"   - Total de alocações: {resultado['estatisticas']['total_alocacoes']}")
        print(f"   - Dias letivos: {resultado['estatisticas']['dias_letivos']}")
        print(f"   - Feriados detectados: {resultado['estatisticas']['feriados']}")
        print(f"   - Arquivo CSV gerado: {resultado['arquivo_csv']}")
        print(f"   - Persistido no banco: {resultado['persistido']}")
        
        # Exibe matriz de alocação
        print(f"\n📅 MATRIZ DE ALOCAÇÃO:")
        dias_semana = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta']
        horarios = ['19:00', '20:00', '21:00', '22:00']
        
        for dia_idx, dia_nome in enumerate(dias_semana):
            print(f"\n{dia_nome}:")
            for horario_idx, horario in enumerate(horarios):
                alocacoes = resultado['matriz_agendamento'][dia_idx][horario_idx]
                if alocacoes:
                    print(f"  {horario}: {len(alocacoes)} alocação(ões)")
                    for alocacao in alocacoes:
                        print(f"    - Docente {alocacao['docente_id']} em {alocacao['uc_id']}")
                else:
                    print(f"  {horario}: Livre")
        
        # Teste de verificação de disponibilidade
        print(f"\n🔍 TESTE DE VERIFICAÇÃO DE DISPONIBILIDADE:")
        docente_id = 1
        dia = 0  # Segunda-feira
        horario = 0  # 19:00
        
        disponivel = verificar_disponibilidade_docente(docente_id, dia, horario)
        print(f"Docente {docente_id} disponível na Segunda às 19:00? {disponivel}")
        
        # Teste de alocações existentes
        print(f"\n📋 ALOCAÇÕES EXISTENTES:")
        alocacoes_existentes = obter_alocacoes_existentes(dia, horario)
        print(f"Alocações na Segunda às 19:00: {len(alocacoes_existentes)}")
        
        for alocacao in alocacoes_existentes:
            print(f"  - Docente {alocacao['docente_id']} em UC {alocacao['uc_id']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()
        return False

def teste_conflitos():
    """Teste específico para detecção de conflitos"""
    print("\n=== TESTE DE DETECÇÃO DE CONFLITOS ===")
    
    # Simula docentes com possíveis conflitos
    docentes_conflito = [
        {
            'id': '10',
            'mat': 2001,
            'ch': 100.0,
            'tipo': 1,
            'saldo': 100.0,
            'rest': []
        },
        {
            'id': '11',
            'mat': 2002,
            'ch': 90.0,
            'tipo': 2,
            'saldo': 90.0,
            'rest': []
        }
    ]
    
    try:
        # Primeira alocação
        print("Primeira alocação...")
        resultado1 = alocar_docentes(docentes_conflito)
        print(f"✅ Primeira alocação: {resultado1['estatisticas']['total_alocacoes']} alocações")
        
        # Segunda alocação (deve detectar conflitos)
        print("Segunda alocação (teste de conflitos)...")
        resultado2 = alocar_docentes(docentes_conflito)
        print(f"✅ Segunda alocação: {resultado2['estatisticas']['total_alocacoes']} alocações")
        
        # Verifica conflitos
        conflitos_detectados = 0
        for dia in range(5):
            for horario in range(4):
                alocacoes = obter_alocacoes_existentes(dia, horario)
                if len(alocacoes) > 1:
                    conflitos_detectados += 1
                    print(f"⚠️  Conflito detectado: {len(alocacoes)} alocações no mesmo horário")
        
        if conflitos_detectados > 0:
            print(f"⚠️  Total de conflitos detectados: {conflitos_detectados}")
        else:
            print("✅ Nenhum conflito detectado!")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste de conflitos: {e}")
        return False

def teste_feriados():
    """Teste específico para verificação de feriados"""
    print("\n=== TESTE DE FERIADOS ===")
    
    from alocacao_docentes import SGDAlocacao
    
    try:
        # Teste com diferentes meses
        meses_teste = [1, 4, 9, 12]  # Janeiro, Abril, Setembro, Dezembro
        
        for mes in meses_teste:
            sgd = SGDAlocacao(2025, mes)
            feriados = sgd.feriados
            dias_letivos = sgd.dias_letivos
            
            print(f"\nMês {mes}/2025:")
            print(f"  Feriados encontrados: {len(feriados)}")
            for feriado in feriados:
                print(f"    - {feriado.strftime('%d/%m/%Y')}")
            print(f"  Dias letivos: {dias_letivos}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste de feriados: {e}")
        return False

def exibir_ajuda():
    """Exibe informações de ajuda"""
    print("""
🎯 SISTEMA DE GESTÃO DOCENTE (SGD) - TESTE DE ALOCAÇÃO

Este script testa o sistema de alocação automática de docentes.

📋 FUNCIONALIDADES TESTADAS:
  - Alocação automática baseada em tipos de docentes
  - Verificação de disponibilidade
  - Detecção de conflitos de horários
  - Verificação de feriados nacionais
  - Geração de matriz de agendamento
  - Exportação para CSV
  - Persistência no banco de dados

🔧 REGRAS DE ALOCAÇÃO:
  - Tipo 1 (>100h): 2 dias fixos por semana
  - Tipo 2 (50-99h): 1 dia fixo por semana  
  - Tipo 3 (<50h): alocação aleatória
  - Cada alocação = 3h20min
  - Horários noturnos: 19:00, 20:00, 21:00, 22:00
  - Dias úteis: Segunda a Sexta

💡 USO:
  python test_alocacao.py [opcao]
  
  Opções:
    basico     - Teste básico de alocação
    conflitos  - Teste de detecção de conflitos
    feriados   - Teste de verificação de feriados
    todos      - Executa todos os testes
    ajuda      - Exibe esta ajuda
""")

def main():
    """Função principal"""
    if len(sys.argv) < 2:
        opcao = 'basico'
    else:
        opcao = sys.argv[1].lower()
    
    print("🎯 SISTEMA DE GESTÃO DOCENTE (SGD) - TESTE DE ALOCAÇÃO")
    print("=" * 60)
    
    if opcao == 'ajuda' or opcao == 'help':
        exibir_ajuda()
        return
    
    sucessos = 0
    total = 0
    
    if opcao in ['basico', 'todos']:
        total += 1
        if teste_alocacao_basica():
            sucessos += 1
    
    if opcao in ['conflitos', 'todos']:
        total += 1
        if teste_conflitos():
            sucessos += 1
    
    if opcao in ['feriados', 'todos']:
        total += 1
        if teste_feriados():
            sucessos += 1
    
    if opcao not in ['basico', 'conflitos', 'feriados', 'todos']:
        print(f"❌ Opção '{opcao}' não reconhecida. Use 'ajuda' para ver as opções disponíveis.")
        return
    
    print(f"\n{'='*60}")
    print(f"📊 RESUMO DOS TESTES: {sucessos}/{total} sucessos")
    
    if sucessos == total:
        print("✅ Todos os testes passaram!")
    else:
        print("❌ Alguns testes falharam. Verifique os logs acima.")

if __name__ == "__main__":
    main() 