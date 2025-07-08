from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Curso(Base):
    __tablename__ = "cursos"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    carga_horaria = Column(Integer, nullable=False)
    fases = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    ucs = relationship("UC", back_populates="curso")
    calendarios = relationship("Calendario", back_populates="curso")

class Docente(Base):
    __tablename__ = "docentes"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True)
    especialidade = Column(String(255), nullable=True)
    matricula = Column(Integer, nullable=True)
    carga_horaria_total = Column(Float, default=0.0)
    tipo_docente = Column(Integer, nullable=True)  # 1, 2 ou 3
    saldo_horas = Column(Float, default=0.0)
    restricoes_dias = Column(JSON, default=list)  # Lista de dias restritos (0=Seg, ..., 4=Sex)
    disciplinas = Column(JSON, default=list)  # Lista de disciplinas
    disponibilidade = Column(JSON, default=dict)  # Disponibilidade por dia da semana
    horarios = Column(JSON, default=dict)  # Horários de início e fim por dia
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    ucs = relationship("UC", back_populates="docente")
    alocacoes = relationship("Assoc_UDD", back_populates="docente")

class UC(Base):
    __tablename__ = "ucs"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    carga_horaria = Column(Integer, nullable=False)
    docente_id = Column(Integer, ForeignKey("docentes.id"), nullable=True)
    curso_id = Column(Integer, ForeignKey("cursos.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    docente = relationship("Docente", back_populates="ucs")
    curso = relationship("Curso", back_populates="ucs")
    alocacoes = relationship("Assoc_UDD", back_populates="uc")

class Assoc_UDD(Base):
    __tablename__ = "assoc_udd"
    
    id = Column(Integer, primary_key=True, index=True)
    uc_id = Column(Integer, ForeignKey("ucs.id"), nullable=False)
    docente_id = Column(Integer, ForeignKey("docentes.id"), nullable=False)
    dia_semana = Column(Integer, nullable=False)  # 0=Segunda, 1=Terça, ..., 4=Sexta
    horario_inicio = Column(String(10), nullable=False)  # Ex: "19:00"
    horario_fim = Column(String(10), nullable=False)  # Ex: "22:20"
    data_alocacao = Column(DateTime, nullable=False)
    mes = Column(Integer, nullable=False)
    ano = Column(Integer, nullable=False)
    ativa = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    uc = relationship("UC", back_populates="alocacoes")
    docente = relationship("Docente", back_populates="alocacoes")

class Calendario(Base):
    __tablename__ = "calendarios"
    
    id = Column(Integer, primary_key=True, index=True)
    curso_id = Column(Integer, ForeignKey("cursos.id"), nullable=False)
    fases_selecionadas = Column(JSON, default=list)  # IDs das fases selecionadas
    mes = Column(Integer, nullable=False)
    ano = Column(Integer, nullable=False)
    eventos = Column(JSON, default=list)  # Lista de eventos do calendário
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    curso = relationship("Curso", back_populates="calendarios") 