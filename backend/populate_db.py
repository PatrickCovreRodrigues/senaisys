
from database import SessionLocal
from models import Curso, Docente, UC, Calendario

def populate_database():
    db = SessionLocal()
    
    try:
        # Criar cursos de exemplo
        cursos = [
            Curso(nome="Análise e Desenvolvimento de Sistemas", carga_horaria=2400, fases="Fase 1,Fase 2,Fase 3,Fase 4"),
            Curso(nome="Ciência de Dados", carga_horaria=2000, fases="Fase 1,Fase 2,Fase 3"),
            Curso(nome="Desenvolvimento Web", carga_horaria=1800, fases="Fase 1,Fase 2"),
            Curso(nome="Redes de Computadores", carga_horaria=2200, fases="Fase 1,Fase 2,Fase 3")
        ]
        
        for curso in cursos:
            db.add(curso)
        db.commit()
        
        # Criar docentes de exemplo
        docentes = [
            Docente(
                nome="Prof. João Silva",
                disciplinas=["Lógica de Programação", "Python", "Algoritmos"],
                disponibilidade={
                    "segunda": True,
                    "terca": True,
                    "quarta": True,
                    "quinta": False,
                    "sexta": True,
                    "sabado": False
                },
                horarios={
                    "segunda": {"inicio": "08:00", "fim": "17:00"},
                    "terca": {"inicio": "08:00", "fim": "17:00"},
                    "quarta": {"inicio": "08:00", "fim": "17:00"},
                    "quinta": {"inicio": "", "fim": ""},
                    "sexta": {"inicio": "08:00", "fim": "12:00"},
                    "sabado": {"inicio": "", "fim": ""}
                }
            ),
            Docente(
                nome="Prof.ª Maria Santos",
                disciplinas=["Banco de Dados", "SQL", "Modelagem de Dados"],
                disponibilidade={
                    "segunda": True,
                    "terca": False,
                    "quarta": True,
                    "quinta": True,
                    "sexta": True,
                    "sabado": True
                },
                horarios={
                    "segunda": {"inicio": "13:00", "fim": "17:00"},
                    "terca": {"inicio": "", "fim": ""},
                    "quarta": {"inicio": "08:00", "fim": "17:00"},
                    "quinta": {"inicio": "08:00", "fim": "17:00"},
                    "sexta": {"inicio": "13:00", "fim": "17:00"},
                    "sabado": {"inicio": "08:00", "fim": "12:00"}
                }
            ),
            Docente(
                nome="Prof. Carlos Oliveira",
                disciplinas=["JavaScript", "HTML/CSS", "React"],
                disponibilidade={
                    "segunda": False,
                    "terca": True,
                    "quarta": True,
                    "quinta": True,
                    "sexta": False,
                    "sabado": False
                },
                horarios={
                    "segunda": {"inicio": "", "fim": ""},
                    "terca": {"inicio": "08:00", "fim": "17:00"},
                    "quarta": {"inicio": "13:00", "fim": "17:00"},
                    "quinta": {"inicio": "08:00", "fim": "17:00"},
                    "sexta": {"inicio": "", "fim": ""},
                    "sabado": {"inicio": "", "fim": ""}
                }
            )
        ]
        
        for docente in docentes:
            db.add(docente)
        db.commit()
        
        # Criar UCs de exemplo
        ucs = [
            UC(nome="Lógica de Programação", carga_horaria=80, docente_id=1, curso_id=1),
            UC(nome="Banco de Dados I", carga_horaria=60, docente_id=2, curso_id=1),
            UC(nome="Desenvolvimento Web Frontend", carga_horaria=120, docente_id=3, curso_id=1),
            UC(nome="Python para Ciência de Dados", carga_horaria=100, docente_id=1, curso_id=2),
            UC(nome="Análise de Dados", carga_horaria=80, docente_id=2, curso_id=2),
            UC(nome="HTML5 e CSS3", carga_horaria=60, docente_id=3, curso_id=3),
            UC(nome="JavaScript Avançado", carga_horaria=80, docente_id=3, curso_id=3)
        ]
        
        for uc in ucs:
            db.add(uc)
        db.commit()
        
        # Criar calendários de exemplo
        calendarios = [
            Calendario(
                curso_id=1,
                mes=4,
                ano=2025,
                fases_selecionadas=[1, 2],
                eventos=[
                    {
                        "id": "evento_1_1",
                        "title": "Início das Aulas - Fase 1",
                        "subtitle": "ADS",
                        "date": "2025-04-07",
                        "type": "inicio"
                    },
                    {
                        "id": "evento_1_2",
                        "title": "Avaliação Lógica de Programação",
                        "subtitle": "Fase 1",
                        "date": "2025-04-15",
                        "type": "avaliacao"
                    }
                ]
            ),
            Calendario(
                curso_id=2,
                mes=4,
                ano=2025,
                fases_selecionadas=[1],
                eventos=[
                    {
                        "id": "evento_2_1",
                        "title": "Workshop Python",
                        "subtitle": "Ciência de Dados",
                        "date": "2025-04-10",
                        "type": "workshop"
                    }
                ]
            )
        ]
        
        for calendario in calendarios:
            db.add(calendario)
        db.commit()
        
        print("✅ Banco de dados populado com sucesso!")
        print(f"📚 {len(cursos)} cursos criados")
        print(f"👨‍🏫 {len(docentes)} docentes criados")
        print(f"📖 {len(ucs)} UCs criadas")
        print(f"📅 {len(calendarios)} calendários criados")
        
    except Exception as e:
        print(f"❌ Erro ao popular banco de dados: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    populate_database() 