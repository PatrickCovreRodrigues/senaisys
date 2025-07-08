from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import UC as UCModel, Docente as DocenteModel, Curso as CursoModel
from schemas import UC, UCCreate, UCUpdate

router = APIRouter()

@router.post("/", response_model=UC)
def criar_uc(uc: UCCreate, db: Session = Depends(get_db)):
    """Criar uma nova UC"""
    # Validar se docente existe (se fornecido)
    if uc.docente_id:
        docente = db.query(DocenteModel).filter(DocenteModel.id == uc.docente_id).first()
        if not docente:
            raise HTTPException(status_code=404, detail="Docente não encontrado")
    
    # Validar se curso existe (se fornecido)
    if uc.curso_id:
        curso = db.query(CursoModel).filter(CursoModel.id == uc.curso_id).first()
        if not curso:
            raise HTTPException(status_code=404, detail="Curso não encontrado")
    
    db_uc = UCModel(**uc.model_dump())
    db.add(db_uc)
    db.commit()
    db.refresh(db_uc)
    return db_uc

@router.get("/", response_model=List[UC])
def listar_ucs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Listar todas as UCs"""
    ucs = db.query(UCModel).offset(skip).limit(limit).all()
    return ucs

@router.get("/{uc_id}", response_model=UC)
def obter_uc(uc_id: int, db: Session = Depends(get_db)):
    """Obter uma UC específica por ID"""
    uc = db.query(UCModel).filter(UCModel.id == uc_id).first()
    if uc is None:
        raise HTTPException(status_code=404, detail="UC não encontrada")
    return uc

@router.put("/{uc_id}", response_model=UC)
def atualizar_uc(uc_id: int, uc_update: UCUpdate, db: Session = Depends(get_db)):
    """Atualizar uma UC existente"""
    uc = db.query(UCModel).filter(UCModel.id == uc_id).first()
    if uc is None:
        raise HTTPException(status_code=404, detail="UC não encontrada")
    
    # Validar docente se fornecido na atualização
    if uc_update.docente_id is not None:
        docente = db.query(DocenteModel).filter(DocenteModel.id == uc_update.docente_id).first()
        if not docente:
            raise HTTPException(status_code=404, detail="Docente não encontrado")
    
    # Validar curso se fornecido na atualização
    if uc_update.curso_id is not None:
        curso = db.query(CursoModel).filter(CursoModel.id == uc_update.curso_id).first()
        if not curso:
            raise HTTPException(status_code=404, detail="Curso não encontrado")
    
    update_data = uc_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(uc, field, value)
    
    db.commit()
    db.refresh(uc)
    return uc

@router.delete("/{uc_id}")
def deletar_uc(uc_id: int, db: Session = Depends(get_db)):
    """Deletar uma UC"""
    uc = db.query(UCModel).filter(UCModel.id == uc_id).first()
    if uc is None:
        raise HTTPException(status_code=404, detail="UC não encontrada")
    
    db.delete(uc)
    db.commit()
    return {"message": "UC deletada com sucesso"}

@router.get("/por-curso/{curso_id}")
def listar_ucs_por_curso(curso_id: int, db: Session = Depends(get_db)):
    """Listar UCs de um curso específico"""
    ucs = db.query(UCModel).filter(UCModel.curso_id == curso_id).all()
    return ucs

@router.get("/por-docente/{docente_id}")
def listar_ucs_por_docente(docente_id: int, db: Session = Depends(get_db)):
    """Listar UCs de um docente específico"""
    ucs = db.query(UCModel).filter(UCModel.docente_id == docente_id).all()
    return ucs

@router.put("/{uc_id}/vincular-docente/{docente_id}")
def vincular_docente_uc(uc_id: int, docente_id: int, db: Session = Depends(get_db)):
    """Vincular um docente a uma UC"""
    uc = db.query(UCModel).filter(UCModel.id == uc_id).first()
    if not uc:
        raise HTTPException(status_code=404, detail="UC não encontrada")
    
    docente = db.query(DocenteModel).filter(DocenteModel.id == docente_id).first()
    if not docente:
        raise HTTPException(status_code=404, detail="Docente não encontrado")
    
    uc.docente_id = docente_id
    db.commit()
    db.refresh(uc)
    return {"message": "Docente vinculado à UC com sucesso"}

@router.put("/{uc_id}/desvincular-docente")
def desvincular_docente_uc(uc_id: int, db: Session = Depends(get_db)):
    """Desvincular docente de uma UC"""
    uc = db.query(UCModel).filter(UCModel.id == uc_id).first()
    if not uc:
        raise HTTPException(status_code=404, detail="UC não encontrada")
    
    uc.docente_id = None
    db.commit()
    db.refresh(uc)
    return {"message": "Docente desvinculado da UC com sucesso"} 