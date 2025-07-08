from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Calendario as CalendarioModel, Curso as CursoModel
from schemas import Calendario, CalendarioCreate, CalendarioUpdate
from datetime import datetime, timedelta
import calendar

router = APIRouter()

@router.post("/", response_model=Calendario)
def criar_calendario(calendario: CalendarioCreate, db: Session = Depends(get_db)):
    """Criar um novo calendário"""
    # Validar se curso existe
    curso = db.query(CursoModel).filter(CursoModel.id == calendario.curso_id).first()
    if not curso:
        raise HTTPException(status_code=404, detail="Curso não encontrado")
    
    db_calendario = CalendarioModel(**calendario.model_dump())
    db.add(db_calendario)
    db.commit()
    db.refresh(db_calendario)
    return db_calendario

@router.get("/", response_model=List[Calendario])
def listar_calendarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Listar todos os calendários"""
    calendarios = db.query(CalendarioModel).offset(skip).limit(limit).all()
    return calendarios

@router.get("/{calendario_id}", response_model=Calendario)
def obter_calendario(calendario_id: int, db: Session = Depends(get_db)):
    """Obter um calendário específico por ID"""
    calendario = db.query(CalendarioModel).filter(CalendarioModel.id == calendario_id).first()
    if calendario is None:
        raise HTTPException(status_code=404, detail="Calendário não encontrado")
    return calendario

@router.put("/{calendario_id}", response_model=Calendario)
def atualizar_calendario(calendario_id: int, calendario_update: CalendarioUpdate, db: Session = Depends(get_db)):
    """Atualizar um calendário existente"""
    calendario = db.query(CalendarioModel).filter(CalendarioModel.id == calendario_id).first()
    if calendario is None:
        raise HTTPException(status_code=404, detail="Calendário não encontrado")
    
    update_data = calendario_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(calendario, field, value)
    
    db.commit()
    db.refresh(calendario)
    return calendario

@router.delete("/{calendario_id}")
def deletar_calendario(calendario_id: int, db: Session = Depends(get_db)):
    """Deletar um calendário"""
    calendario = db.query(CalendarioModel).filter(CalendarioModel.id == calendario_id).first()
    if calendario is None:
        raise HTTPException(status_code=404, detail="Calendário não encontrado")
    
    db.delete(calendario)
    db.commit()
    return {"message": "Calendário deletado com sucesso"}

@router.get("/por-curso/{curso_id}")
def listar_calendarios_por_curso(curso_id: int, db: Session = Depends(get_db)):
    """Listar calendários de um curso específico"""
    calendarios = db.query(CalendarioModel).filter(CalendarioModel.curso_id == curso_id).all()
    return calendarios

@router.post("/gerar")
def gerar_calendario(
    curso_id: int,
    mes: int,
    ano: int,
    fases_selecionadas: List[int] = [],
    db: Session = Depends(get_db)
):
    """Gerar calendário para um curso específico"""
    # Validar se curso existe
    curso = db.query(CursoModel).filter(CursoModel.id == curso_id).first()
    if not curso:
        raise HTTPException(status_code=404, detail="Curso não encontrado")
    
    # Gerar eventos do calendário baseado nas fases
    eventos = []
    
    # Obter número de dias no mês
    num_dias = calendar.monthrange(ano, mes)[1]
    
    # Gerar eventos de exemplo baseados nas fases selecionadas
    for fase_id in fases_selecionadas:
        fase_nome = f"Fase {fase_id}"
        
        # Adicionar eventos de exemplo para cada fase
        if fase_id == 1:  # Fase 1 - Fundamentos
            eventos.extend([
                {
                    "id": f"evento_{fase_id}_1",
                    "title": "Introdução aos Fundamentos",
                    "subtitle": fase_nome,
                    "date": f"{ano}-{mes:02d}-05",
                    "type": "aula"
                },
                {
                    "id": f"evento_{fase_id}_2",
                    "title": "Avaliação Teórica",
                    "subtitle": fase_nome,
                    "date": f"{ano}-{mes:02d}-15",
                    "type": "avaliacao"
                }
            ])
        elif fase_id == 2:  # Fase 2 - Desenvolvimento
            eventos.extend([
                {
                    "id": f"evento_{fase_id}_1",
                    "title": "Projeto Prático",
                    "subtitle": fase_nome,
                    "date": f"{ano}-{mes:02d}-10",
                    "type": "projeto"
                },
                {
                    "id": f"evento_{fase_id}_2",
                    "title": "Apresentação",
                    "subtitle": fase_nome,
                    "date": f"{ano}-{mes:02d}-25",
                    "type": "apresentacao"
                }
            ])
        # Adicionar mais fases conforme necessário
    
    # Criar ou atualizar calendário
    calendario_existente = db.query(CalendarioModel).filter(
        CalendarioModel.curso_id == curso_id,
        CalendarioModel.mes == mes,
        CalendarioModel.ano == ano
    ).first()
    
    if calendario_existente:
        # Atualizar calendário existente
        calendario_existente.fases_selecionadas = fases_selecionadas
        calendario_existente.eventos = eventos
        db.commit()
        db.refresh(calendario_existente)
        return calendario_existente
    else:
        # Criar novo calendário
        novo_calendario = CalendarioModel(
            curso_id=curso_id,
            mes=mes,
            ano=ano,
            fases_selecionadas=fases_selecionadas,
            eventos=eventos
        )
        db.add(novo_calendario)
        db.commit()
        db.refresh(novo_calendario)
        return novo_calendario

@router.get("/calendario-mes/{curso_id}/{ano}/{mes}")
def obter_calendario_mes(curso_id: int, ano: int, mes: int, db: Session = Depends(get_db)):
    """Obter calendário específico de um mês/ano para um curso"""
    calendario = db.query(CalendarioModel).filter(
        CalendarioModel.curso_id == curso_id,
        CalendarioModel.mes == mes,
        CalendarioModel.ano == ano
    ).first()
    
    if not calendario:
        raise HTTPException(status_code=404, detail="Calendário não encontrado para este período")
    
    return calendario

@router.get("/eventos/{curso_id}")
def listar_eventos_curso(curso_id: int, db: Session = Depends(get_db)):
    """Listar todos os eventos de um curso"""
    calendarios = db.query(CalendarioModel).filter(CalendarioModel.curso_id == curso_id).all()
    
    todos_eventos = []
    for calendario in calendarios:
        if calendario.eventos:
            todos_eventos.extend(calendario.eventos)
    
    return {"eventos": todos_eventos} 