import sys
import os
from sqlalchemy.orm import Session

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal, engine
from models import Base, Curso, Docente, UC, Assoc_UDD

def setup_database():
    """Drops and recreates all tables."""
    print("Recriando tabelas...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("Tabelas recriadas.")

def clear_data(db: Session):
    """Clears all data from the relevant tables."""
    print("Limpando dados antigos...")
    # Deleting from child to parent
    db.query(Assoc_UDD).delete(synchronize_session=False)
    db.query(UC).delete(synchronize_session=False)
    db.query(Docente).delete(synchronize_session=False)
    db.query(Curso).delete(synchronize_session=False)
    db.commit()
    print("Dados antigos removidos.")

def populate_data():
    """Populates the database with test data designed to cause conflicts."""
    db = SessionLocal()
    
    try:
        # Clear existing data for a fresh start
        clear_data(db)

        print("Iniciando a criação de dados de teste...")

        # 1. Criar Cursos
        curso_ads = Curso(nome="Análise e Desenvolvimento de Sistemas", carga_horaria=2000, fases="1,2,3,4")
        curso_redes = Curso(nome="Redes de Computadores", carga_horaria=1800, fases="1,2,3")
        db.add_all([curso_ads, curso_redes])
        db.commit()
        print("Cursos criados.")

        # 2. Criar Unidades Curriculares (UCs)
        ucs_ads = [
            UC(nome="Algoritmos e Lógica de Programação", carga_horaria=80, curso_id=curso_ads.id),
            UC(nome="Banco de Dados", carga_horaria=80, curso_id=curso_ads.id),
            UC(nome="Desenvolvimento Web Front-End", carga_horaria=120, curso_id=curso_ads.id),
            UC(nome="Desenvolvimento Web Back-End", carga_horaria=120, curso_id=curso_ads.id),
        ]
        ucs_redes = [
            UC(nome="Fundamentos de Redes", carga_horaria=80, curso_id=curso_redes.id),
            UC(nome="Segurança da Informação", carga_horaria=100, curso_id=curso_redes.id),
        ]
        db.add_all(ucs_ads + ucs_redes)
        db.commit()
        print("UCs criadas.")

        # 3. Criar Docentes com cenários de conflito
        print("Criando docentes com cenários de conflito...")
        docentes_para_criar = [
            # TIPO 1 (> 100h) - Alta prioridade
            Docente(
                nome="Ana Professora Full-Time", matricula=1001, email="ana.full@email.com", especialidade="Full-Stack",
                carga_horaria_total=120, tipo_docente=1, saldo_horas=120,
                disponibilidade={'segunda': True, 'terca': True, 'quarta': True, 'quinta': True, 'sexta': True},
                horarios={
                    'segunda': {'inicio': '19:00', 'fim': '23:00'}, 'terca': {'inicio': '19:00', 'fim': '23:00'},
                    'quarta': {'inicio': '19:00', 'fim': '23:00'}, 'quinta': {'inicio': '19:00', 'fim': '23:00'},
                    'sexta': {'inicio': '19:00', 'fim': '23:00'}
                }
            ),
            # TIPO 2 (50-99h) - Média prioridade
            Docente(
                nome="Bruno Meio-Período", matricula=1002, email="bruno.meio@email.com", especialidade="Back-End",
                carga_horaria_total=80, tipo_docente=2, saldo_horas=80,
                disponibilidade={'terca': True, 'quinta': True},
                horarios={'terca': {'inicio': '19:00', 'fim': '23:00'}, 'quinta': {'inicio': '19:00', 'fim': '23:00'}},
                restricoes_dias=[0, 2, 4]  # Restrição para Seg, Qua, Sex
            ),
            # TIPO 3 (< 50h) - Baixa prioridade, CONFLITO na SEXTA
            Docente(
                nome="Carlos Conflito Sexta 1", matricula=1003, email="carlos.sexta@email.com", especialidade="Front-End",
                carga_horaria_total=40, tipo_docente=3, saldo_horas=40,
                disponibilidade={'sexta': True},
                horarios={'sexta': {'inicio': '19:00', 'fim': '23:00'}}
            ),
            Docente(
                nome="Daniela Conflito Sexta 2", matricula=1004, email="daniela.sexta@email.com", especialidade="Banco de Dados",
                carga_horaria_total=40, tipo_docente=3, saldo_horas=40,
                disponibilidade={'sexta': True},
                horarios={'sexta': {'inicio': '19:00', 'fim': '23:00'}}
            ),
             # Docente sem disponibilidade para testar se ele não é alocado
            Docente(
                nome="Fernanda Férias", matricula=1005, email="fernanda.ferias@email.com", especialidade="Redes",
                carga_horaria_total=60, tipo_docente=2, saldo_horas=60,
                disponibilidade={'segunda': False, 'terca': False, 'quarta': False, 'quinta': False, 'sexta': False},
            ),
             # Docente com alta carga horária mas pouca disponibilidade, para forçar o saldo a não zerar
            Docente(
                nome="Gustavo Super-Focado", matricula=1006, email="gustavo.foco@email.com", especialidade="Segurança",
                carga_horaria_total=150, tipo_docente=1, saldo_horas=150,
                disponibilidade={'quarta': True},
                horarios={'quarta': {'inicio': '19:00', 'fim': '23:00'}},
                restricoes_dias=[0, 1, 3, 4]
            )
        ]
        db.add_all(docentes_para_criar)
        db.commit()
        print(f"{len(docentes_para_criar)} docentes criados.")
        print("\nBanco de dados populado com sucesso!")
        print("Execute o endpoint de alocação para ver o resultado dos conflitos e priorização.")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    setup_database()
    populate_data() 