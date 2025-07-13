#!/usr/bin/env python3
"""
Script de teste para o Sistema de Alocação Otimizada
Demonstra como usar a função otimizada com diferentes cenários
"""

from sistema_alocacao_otimizado import alocar_docentes_otimizado
from datetime import datetime
import json

def teste_basico():
    """Teste básico com dados de exemplo"""
    print("=== TESTE BÁSICO ===")
    
    docentes = [
        {'id': 'P1', 'mat': 48273, 'ch': 108, 'saldo': 108, 'rest': []},
        {'id': 'P2', 'mat': 19385, 'ch': 108, 'saldo': 108, 'rest': []},
        {'id': 'P3', 'mat': 60714, 'ch': 108, 'saldo': 108, 'rest': [3]},  # Não quinta
        {'id': 'P4', 'mat': 84529, 'ch': 72, 'saldo': 72, 'rest': []},
        {'id': 'P5', 'mat': 21947, 'ch': 72, 'saldo': 72, 'rest': []},
        {'id': 'P6', 'mat': 73018, 'ch': 72, 'saldo': 72, 'rest': []},
        {'id': 'P7', 'mat': 59136, 'ch': 36, 'saldo': 36, 'rest': []},
        {'id': 'P8', 'mat': 36402, 'ch': 36, 'saldo': 36, 'rest': []},
        {'id': 'P9', 'mat': 10675, 'ch': 36, 'saldo': 36, 'rest': []},
        {'id': 'P10', 'mat': 95821, 'ch': 36, 'saldo': 36, 'rest': []},
    ]
    
    resultado = alocar_docentes_otimizado(
        dados_docentes=docentes,
        ano=2025,
        mes=4,
        exportar_csv=True
    )
    
    print(f"Ano: {resultado['ano']}, Mês: {resultado['mes']}")
    print(f"Feriados detectados: {resultado['feriados_detectados']}")
    print(f"Taxa de alocação: {resultado['estatisticas']['taxa_alocacao']:.1f}%")
    print(f"Arquivo CSV: {resultado.get('arquivo_csv', 'N/A')}")
    
    print("\nMatriz Agendada:")
    dias = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex']
    for i, linha in enumerate(resultado['matriz_agendada']):
        print(f"  {dias[i]}: {linha}")
    
    print("\nDocentes Alocados:")
    for docente in resultado['docentes_processados']:
        if docente['dias_alocados']:
            print(f"  {docente['id']} (Mat: {docente['matricula']}) - "
                  f"Tipo {docente['tipo']} - Dias: {docente['dias_alocados']}")
    
    return resultado

def teste_com_restricoes():
    """Teste com múltiplas restrições"""
    print("\n=== TESTE COM RESTRIÇÕES ===")
    
    docentes = [
        {'id': 'D1', 'mat': 1001, 'ch': 120, 'saldo': 120, 'rest': [0, 4]},  # Não seg/sex
        {'id': 'D2', 'mat': 1002, 'ch': 110, 'saldo': 110, 'rest': [1, 3]},  # Não ter/qui
        {'id': 'D3', 'mat': 1003, 'ch': 80, 'saldo': 80, 'rest': [2]},       # Não qua
        {'id': 'D4', 'mat': 1004, 'ch': 60, 'saldo': 60, 'rest': []},        # Sem restrição
        {'id': 'D5', 'mat': 1005, 'ch': 40, 'saldo': 40, 'rest': [0, 1, 2]}, # Só qui/sex
    ]
    
    resultado = alocar_docentes_otimizado(
        dados_docentes=docentes,
        ano=2025,
        mes=7,  # Julho
        exportar_csv=False
    )
    
    print(f"Mês: {resultado['mes']}/2025")
    print(f"Dias não-letivos: {resultado['dias_nao_letivos']}")
    print(f"Taxa de alocação: {resultado['estatisticas']['taxa_alocacao']:.1f}%")
    
    print("\nAlocação por Tipo:")
    tipos = {1: [], 2: [], 3: []}
    for docente in resultado['docentes_processados']:
        tipos[docente['tipo']].append(docente)
    
    for tipo, lista in tipos.items():
        print(f"  Tipo {tipo}: {len(lista)} docentes")
        for d in lista:
            if d['dias_alocados']:
                print(f"    {d['id']} - CH: {d['carga_horaria_original']}h - "
                      f"Dias: {d['dias_alocados']} - Restrições: {d['restricoes']}")
    
    return resultado

def teste_mes_com_feriados():
    """Teste com mês que tem feriados"""
    print("\n=== TESTE MÊS COM FERIADOS ===")
    
    docentes = [
        {'id': 'F1', 'mat': 2001, 'ch': 150, 'saldo': 150, 'rest': []},
        {'id': 'F2', 'mat': 2002, 'ch': 90, 'saldo': 90, 'rest': []},
        {'id': 'F3', 'mat': 2003, 'ch': 45, 'saldo': 45, 'rest': []},
    ]
    
    # Setembro (Independence Day - 7 de setembro)
    resultado = alocar_docentes_otimizado(
        dados_docentes=docentes,
        ano=2025,
        mes=9,
        exportar_csv=False
    )
    
    print(f"Setembro/2025 - Feriados: {resultado['feriados_detectados']}")
    print(f"Dias não-letivos: {resultado['dias_nao_letivos']}")
    print(f"Dias letivos disponíveis: {resultado['estatisticas']['dias_letivos']}")
    
    print("\nMatriz Ajustada (após feriados):")
    for i, linha in enumerate(resultado['matriz_ajustada']):
        print(f"  {['Seg', 'Ter', 'Qua', 'Qui', 'Sex'][i]}: {linha}")
    
    return resultado

def teste_performance():
    """Teste de performance com muitos docentes"""
    print("\n=== TESTE DE PERFORMANCE ===")
    
    import time
    
    # Gera 100 docentes aleatórios
    docentes = []
    for i in range(100):
        docentes.append({
            'id': f'PERF{i+1}',
            'mat': 3000 + i,
            'ch': 30 + (i % 100),  # CH entre 30-129
            'saldo': 30 + (i % 100),
            'rest': [i % 5] if i % 10 == 0 else []  # 10% com restrições
        })
    
    inicio = time.time()
    resultado = alocar_docentes_otimizado(
        dados_docentes=docentes,
        ano=2025,
        mes=3,
        exportar_csv=False
    )
    fim = time.time()
    
    print(f"Processamento de {len(docentes)} docentes:")
    print(f"Tempo: {fim - inicio:.3f} segundos")
    print(f"Taxa de alocação: {resultado['estatisticas']['taxa_alocacao']:.1f}%")
    print(f"Docentes alocados: {resultado['estatisticas']['docentes_alocados']}")
    
    # Análise por tipo
    tipos_count = {1: 0, 2: 0, 3: 0}
    for docente in resultado['docentes_processados']:
        tipos_count[docente['tipo']] += 1
    
    print(f"Distribuição por tipo: Tipo1={tipos_count[1]}, Tipo2={tipos_count[2]}, Tipo3={tipos_count[3]}")
    
    return resultado

def teste_formato_json():
    """Demonstra como usar com dados JSON (ex: vindo de API)"""
    print("\n=== TESTE FORMATO JSON ===")
    
    # Simula dados vindos de uma API JSON
    json_data = '''
    [
        {
            "id": "JSON1",
            "mat": 4001,
            "ch": 108.0,
            "saldo": 108.0,
            "rest": []
        },
        {
            "id": "JSON2",
            "mat": 4002,
            "ch": 72.0,
            "saldo": 72.0,
            "rest": [0, 4]
        },
        {
            "id": "JSON3",
            "mat": 4003,
            "ch": 36.0,
            "saldo": 36.0,
            "rest": [2]
        }
    ]
    '''
    
    docentes = json.loads(json_data)
    
    resultado = alocar_docentes_otimizado(
        dados_docentes=docentes,
        ano=2025,
        mes=6,
        exportar_csv=False
    )
    
    print("Dados JSON processados com sucesso!")
    print(f"Docentes processados: {len(docentes)}")
    print(f"Taxa de alocação: {resultado['estatisticas']['taxa_alocacao']:.1f}%")
    
    # Exporta resultado como JSON
    resultado_json = json.dumps(resultado, indent=2, default=str)
    print(f"Tamanho do JSON resultado: {len(resultado_json)} caracteres")
    
    return resultado

def main():
    """Executa todos os testes"""
    print("🎓 SISTEMA DE GESTÃO DOCENTE - TESTES DE ALOCAÇÃO OTIMIZADA")
    print("=" * 70)
    
    try:
        # Executa todos os testes
        teste_basico()
        teste_com_restricoes()
        teste_mes_com_feriados()
        teste_performance()
        teste_formato_json()
        
        print("\n" + "=" * 70)
        print("✅ TODOS OS TESTES EXECUTADOS COM SUCESSO!")
        print("\nO sistema está pronto para integração com FastAPI.")
        print("Use os endpoints:")
        print("  POST /api/alocacao/processar-otimizado")
        print("  POST /api/alocacao/processar-banco")
        
    except Exception as e:
        print(f"\n❌ ERRO DURANTE OS TESTES: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 