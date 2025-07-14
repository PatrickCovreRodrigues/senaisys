"""
Script de Demonstração da Funcionalidade de Recorrência
Mostra como usar a nova alocação automática de docentes para semestre
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from alocacao_recorrencia import AlocacaoRecorrencia
from database import get_db
from models import Docente as DocenteModel
from sqlalchemy.orm import Session
import json

def demonstrar_alocacao_recorrencia():
    """
    Demonstra o funcionamento da alocação com recorrência
    """
    print("🎯 DEMONSTRAÇÃO - Alocação de Docentes com Recorrência Semanal")
    print("=" * 70)
    
    # Obter sessão do banco
    db = next(get_db())
    
    try:
        # Criar instância do alocador
        alocador = AlocacaoRecorrencia(db)
        
        print("\n📋 1. Buscando docentes com disponibilidade...")
        docentes = alocador._buscar_docentes_disponiveis()
        print(f"   ✅ Encontrados {len(docentes)} docentes disponíveis")
        
        for docente in docentes[:3]:  # Mostrar apenas os primeiros 3
            print(f"   👨‍🏫 {docente['nome']} - {len(docente['ucs'])} UC(s) vinculada(s)")
        
        if len(docentes) > 3:
            print(f"   ... e mais {len(docentes) - 3} docente(s)")
        
        print("\n🔍 2. Detectando conflitos de horários...")
        conflitos = alocador._detectar_conflitos_horarios(docentes)
        print(f"   ⚠️  Encontrados {len(conflitos)} conflitos de horários")
        
        for chave, conflito in list(conflitos.items())[:3]:  # Mostrar apenas os primeiros 3
            dia = conflito['dia'].capitalize()
            horario = conflito['horario']
            num_docentes = len(conflito['docentes'])
            print(f"   📅 {dia} às {horario}: {num_docentes} docentes disponíveis")
        
        if len(conflitos) > 3:
            print(f"   ... e mais {len(conflitos) - 3} conflito(s)")
        
        print("\n📅 3. Processando alocação para semestre...")
        resultado = alocador.processar_alocacao_semestre(
            mes_inicio=3,  # Março
            ano_inicio=2025,
            duracao_meses=5
        )
        
        if resultado['status'] == 'sucesso':
            print("   ✅ Alocação processada com sucesso!")
            
            periodo = resultado['periodo']
            stats = resultado['estatisticas']
            
            print(f"\n📊 RESULTADOS:")
            print(f"   📈 Período: {periodo['inicio']} ({periodo['duracao_meses']} meses)")
            print(f"   📈 Total de semanas: {periodo['total_semanas']}")
            print(f"   📈 Total de eventos: {periodo['total_eventos']}")
            print(f"   📈 Docentes envolvidos: {stats['docentes_envolvidos']}")
            print(f"   📈 Conflitos detectados: {stats['conflitos_detectados']}")
            print(f"   📈 Alocações com recorrência: {stats['alocacoes_com_recorrencia']}")
            print(f"   📈 Alocações simples: {stats['alocacoes_simples']}")
            
            print(f"\n📋 EVENTOS GERADOS (primeiros 5):")
            for i, evento in enumerate(resultado['eventos'][:5]):
                data = evento['date'][:10]  # YYYY-MM-DD
                titulo = evento['title']
                docente = evento['docenteNome']
                horario = f"{evento['horarioInicio']}-{evento['horarioFim']}"
                tipo = evento.get('tipoAlocacao', 'indefinido')
                
                print(f"   {i+1}. 📅 {data} • {titulo} • Prof. {docente} • {horario} • ({tipo})")
            
            if len(resultado['eventos']) > 5:
                print(f"   ... e mais {len(resultado['eventos']) - 5} evento(s)")
            
            # Mostrar exemplo de recorrência
            if resultado.get('cronograma_detalhado'):
                print(f"\n🔄 EXEMPLO DE RECORRÊNCIA (primeiro conflito):")
                primeiro_conflito = list(resultado['cronograma_detalhado'].values())[0]
                
                for i, item in enumerate(primeiro_conflito[:4]):  # Primeiras 4 semanas
                    data = item['data'].strftime('%d/%m')
                    docente = item['docente']['nome']
                    semana = item['semana']
                    dia = item['dia'].capitalize()
                    horario = item['horario_inicio']
                    
                    print(f"   Semana {semana} ({data}): {dia} {horario} - Prof. {docente}")
                
                if len(primeiro_conflito) > 4:
                    print(f"   ... padrão continua por {len(primeiro_conflito)} semanas")
        
        else:
            print(f"   ❌ Erro: {resultado['mensagem']}")
        
        print("\n" + "=" * 70)
        print("✅ Demonstração concluída!")
        print("\n💡 Para usar na interface:")
        print("   1. Cadastre professores com disponibilidade")
        print("   2. Vincule UCs aos professores")
        print("   3. Acesse 'Gerar Calendário'")
        print("   4. Clique em 'Alocar Docentes para Semestre'")
        print("   5. Configure período e duração")
        print("   6. Visualize resultado no calendário!")
        
    except Exception as e:
        print(f"❌ Erro na demonstração: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        db.close()

if __name__ == "__main__":
    demonstrar_alocacao_recorrencia()
