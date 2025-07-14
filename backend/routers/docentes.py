from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Docente as DocenteModel
from schemas import Docente, DocenteCreate, DocenteUpdate

router = APIRouter()

@router.post("/", response_model=Docente)
def criar_docente(docente: DocenteCreate, db: Session = Depends(get_db)):
    """Criar um novo docente"""
    docente_data = docente.model_dump()
    ucs_ids = docente_data.pop('ucs_ids', [])
    
    db_docente = DocenteModel(**docente_data)
    db.add(db_docente)
    db.commit()
    db.refresh(db_docente)
    
    # Vincular UCs ao docente
    if ucs_ids:
        from models import UC as UCModel
        for uc_id in ucs_ids:
            uc = db.query(UCModel).filter(UCModel.id == uc_id).first()
            if uc:
                uc.docente_id = db_docente.id
        db.commit()
        db.refresh(db_docente)
    
    return db_docente

@router.get("/", response_model=List[Docente])
def listar_docentes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Listar todos os docentes"""
    docentes = db.query(DocenteModel).offset(skip).limit(limit).all()
    return docentes

@router.get("/{docente_id}", response_model=Docente)
def obter_docente(docente_id: int, db: Session = Depends(get_db)):
    """Obter um docente específico por ID"""
    docente = db.query(DocenteModel).filter(DocenteModel.id == docente_id).first()
    if docente is None:
        raise HTTPException(status_code=404, detail="Docente não encontrado")
    return docente

@router.put("/{docente_id}", response_model=Docente)
def atualizar_docente(docente_id: int, docente_update: DocenteUpdate, db: Session = Depends(get_db)):
    """Atualizar um docente existente"""
    docente = db.query(DocenteModel).filter(DocenteModel.id == docente_id).first()
    if docente is None:
        raise HTTPException(status_code=404, detail="Docente não encontrado")
    
    update_data = docente_update.model_dump(exclude_unset=True)
    
    # Se houver ucs_ids, atualizar as UCs vinculadas
    if 'ucs_ids' in update_data:
        ucs_ids = update_data.pop('ucs_ids')
        
        # Desvincular todas as UCs atuais do docente
        from models import UC as UCModel
        db.query(UCModel).filter(UCModel.docente_id == docente_id).update({"docente_id": None})
        
        # Vincular as novas UCs
        if ucs_ids:
            for uc_id in ucs_ids:
                uc = db.query(UCModel).filter(UCModel.id == uc_id).first()
                if uc:
                    uc.docente_id = docente_id
    
    for field, value in update_data.items():
        setattr(docente, field, value)
    
    db.commit()
    db.refresh(docente)
    return docente

@router.delete("/{docente_id}")
def deletar_docente(docente_id: int, db: Session = Depends(get_db)):
    """Deletar um docente"""
    docente = db.query(DocenteModel).filter(DocenteModel.id == docente_id).first()
    if docente is None:
        raise HTTPException(status_code=404, detail="Docente não encontrado")
    
    db.delete(docente)
    db.commit()
    return {"message": "Docente deletado com sucesso"}

@router.get("/{docente_id}/ucs")
def listar_ucs_do_docente(docente_id: int, db: Session = Depends(get_db)):
    """Listar todas as UCs de um docente específico"""
    docente = db.query(DocenteModel).filter(DocenteModel.id == docente_id).first()
    if docente is None:
        raise HTTPException(status_code=404, detail="Docente não encontrado")
    
    return docente.ucs

@router.get("/{docente_id}/disponibilidade")
def obter_disponibilidade_docente(docente_id: int, db: Session = Depends(get_db)):
    """Obter a disponibilidade de um docente"""
    docente = db.query(DocenteModel).filter(DocenteModel.id == docente_id).first()
    if docente is None:
        raise HTTPException(status_code=404, detail="Docente não encontrado")
    
    return {
        "disponibilidade": docente.disponibilidade,
        "horarios": docente.horarios
    } 