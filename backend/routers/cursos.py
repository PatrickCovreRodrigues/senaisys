from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Curso as CursoModel
from schemas import Curso, CursoCreate, CursoUpdate

router = APIRouter()

@router.post("/", response_model=Curso)
def criar_curso(curso: CursoCreate, db: Session = Depends(get_db)):
    """Criar um novo curso"""
    db_curso = CursoModel(**curso.model_dump())
    db.add(db_curso)
    db.commit()
    db.refresh(db_curso)
    return db_curso

@router.get("/", response_model=List[Curso])
def listar_cursos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Listar todos os cursos"""
    cursos = db.query(CursoModel).offset(skip).limit(limit).all()
    return cursos

@router.get("/{curso_id}", response_model=Curso)
def obter_curso(curso_id: int, db: Session = Depends(get_db)):
    """Obter um curso específico por ID"""
    curso = db.query(CursoModel).filter(CursoModel.id == curso_id).first()
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso não encontrado")
    return curso

@router.put("/{curso_id}", response_model=Curso)
def atualizar_curso(curso_id: int, curso_update: CursoUpdate, db: Session = Depends(get_db)):
    """Atualizar um curso existente"""
    curso = db.query(CursoModel).filter(CursoModel.id == curso_id).first()
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso não encontrado")
    
    update_data = curso_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(curso, field, value)
    
    db.commit()
    db.refresh(curso)
    return curso

@router.delete("/{curso_id}")
def deletar_curso(curso_id: int, db: Session = Depends(get_db)):
    """Deletar um curso"""
    curso = db.query(CursoModel).filter(CursoModel.id == curso_id).first()
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso não encontrado")
    
    db.delete(curso)
    db.commit()
    return {"message": "Curso deletado com sucesso"}

@router.get("/{curso_id}/ucs")
def listar_ucs_do_curso(curso_id: int, db: Session = Depends(get_db)):
    """Listar todas as UCs de um curso específico"""
    curso = db.query(CursoModel).filter(CursoModel.id == curso_id).first()
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso não encontrado")
    
    return curso.ucs 