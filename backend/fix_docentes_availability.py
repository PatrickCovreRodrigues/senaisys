"""
Script para corrigir a disponibilidade dos docentes existentes
"""
import sys
import os
import json

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal
from models import Docente

def corrigir_disponibilidade_docentes():
    """Corrige a disponibilidade dos docentes existentes para que possam ser alocados"""
    db = SessionLocal()
    
    try:
        # Buscar todos os docentes
        docentes = db.query(Docente).all()
        
        print(f"Encontrados {len(docentes)} docentes para atualizar...")
        
        for docente in docentes:
            print(f"Atualizando docente: {docente.nome} (ID: {docente.id})")
            
            # Atualizar disponibilidade para pelo menos alguns dias
            docente.disponibilidade = {
                "segunda": True,
                "terca": True, 
                "quarta": True,
                "quinta": True,
                "sexta": True,
                "sabado": False
            }
            
            # Garantir que os horários estejam preenchidos para os dias disponíveis
            docente.horarios = {
                "segunda": {"inicio": "19:00", "fim": "23:00"},
                "terca": {"inicio": "19:00", "fim": "23:00"},
                "quarta": {"inicio": "19:00", "fim": "23:00"}, 
                "quinta": {"inicio": "19:00", "fim": "23:00"},
                "sexta": {"inicio": "19:00", "fim": "23:00"},
                "sabado": {"inicio": "", "fim": ""}
            }
            
            # Definir tipo de docente e carga horária se não estiverem definidos
            if docente.tipo_docente is None:
                docente.tipo_docente = 1  # Tipo 1 (alta prioridade)
            
            if docente.carga_horaria_total == 0.0:
                docente.carga_horaria_total = 120.0  # 120 horas
                
            if docente.saldo_horas == 0.0:
                docente.saldo_horas = 120.0  # 120 horas disponíveis
            
            print(f"  - Disponibilidade atualizada para seg-sex")
            print(f"  - Horários definidos como 19:00-23:00")
            print(f"  - Tipo docente: {docente.tipo_docente}")
            print(f"  - Carga horária: {docente.carga_horaria_total}")
        
        db.commit()
        print("\nTodos os docentes foram atualizados com sucesso!")
        print("Agora o sistema deve conseguir gerar aulas.")
        
    except Exception as e:
        print(f"Erro ao atualizar docentes: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    corrigir_disponibilidade_docentes()
