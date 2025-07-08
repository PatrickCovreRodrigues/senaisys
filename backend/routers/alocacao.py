from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import List, Dict, Optional
from datetime import datetime
from database import get_db
from models import Docente as DocenteModel, UC as UCModel, Assoc_UDD as AssocUDDModel
from schemas import Docente, UC, AssocUDD, AssocUDDCreate, AssocUDDUpdate
from alocacao_docentes import (
    alocar_docentes, 
    obter_alocacoes_existentes, 
    verificar_disponibilidade_docente,
    DIAS_SEMANA,
    HORARIOS_NOTURNOS
)

router = APIRouter(prefix="/alocacao", tags=["alocacao"])

@router.post("/processar")
def processar_alocacao_docentes(
    ano: Optional[int] = Body(None, embed=True),
    mes: Optional[int] = Body(None, embed=True),
    db: Session = Depends(get_db)
):
    """
    Processa a alocação automática de docentes com base nos dados do banco.
    """
    try:
        # A função `alocar_docentes` agora usa o `db` para buscar os dados
        resultado = alocar_docentes(db, ano, mes)
        
        if resultado.get("status") == "erro":
            raise HTTPException(status_code=400, detail=resultado.get("mensagem"))
            
        return {
            "success": True,
            "resultado": resultado,
            "mensagem": "Alocação processada com sucesso"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar alocação: {str(e)}")

@router.get("/matriz-horarios")
def obter_matriz_horarios(
    ano: Optional[int] = None,
    mes: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Obtém a matriz de horários atual com todas as alocações"""
    try:
        ano_atual = ano or datetime.now().year
        mes_atual = mes or datetime.now().month
        
        # Cria matriz vazia 5x4 (dias x horários)
        matriz = [[[] for _ in range(4)] for _ in range(5)]
        
        # Busca todas as alocações do período
        alocacoes = db.query(AssocUDDModel).filter(
            AssocUDDModel.ano == ano_atual,
            AssocUDDModel.mes == mes_atual,
            AssocUDDModel.ativa == True
        ).all()
        
        # Preenche a matriz
        for alocacao in alocacoes:
            dia = int(alocacao.dia_semana)
            horario = HORARIOS_NOTURNOS.index(str(alocacao.horario_inicio))
            
            # Busca dados do docente e UC
            docente = db.query(DocenteModel).filter(DocenteModel.id == alocacao.docente_id).first()
            uc = db.query(UCModel).filter(UCModel.id == alocacao.uc_id).first()
            
            alocacao_info = {
                "id": alocacao.id,
                "docente_id": alocacao.docente_id,
                "docente_nome": docente.nome if docente else "Docente não encontrado",
                "uc_id": alocacao.uc_id,
                "uc_nome": uc.nome if uc else "UC não encontrada",
                "horario_inicio": alocacao.horario_inicio,
                "horario_fim": alocacao.horario_fim,
                "data_alocacao": alocacao.data_alocacao
            }
            
            matriz[dia][horario].append(alocacao_info)
        
        return {
            "success": True,
            "matriz": matriz,
            "dias_semana": DIAS_SEMANA,
            "horarios": HORARIOS_NOTURNOS,
            "ano": ano_atual,
            "mes": mes_atual
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter matriz de horários: {str(e)}")

@router.get("/disponibilidade/{docente_id}")
def verificar_disponibilidade_docente_endpoint(
    docente_id: int,
    dia: int,
    horario: int,
    ano: Optional[int] = None,
    mes: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Verifica se um docente está disponível em um dia e horário específicos"""
    try:
        # A função `verificar_disponibilidade_docente` espera o `db`
        disponivel = verificar_disponibilidade_docente(db, docente_id, dia, horario)
        return {
            "success": True,
            "disponivel": disponivel,
            "docente_id": docente_id,
            "dia": dia,
            "horario": horario,
            "dia_nome": DIAS_SEMANA[dia] if 0 <= dia < 5 else "Dia inválido",
            "horario_nome": HORARIOS_NOTURNOS[horario] if 0 <= horario < 4 else "Horário inválido"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao verificar disponibilidade: {str(e)}")

@router.get("/alocacoes-existentes")
def obter_alocacoes_existentes_endpoint(
    dia: int,
    horario: int,
    ano: Optional[int] = None,
    mes: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Obtém as alocações existentes para um dia e horário específicos"""
    try:
        # A função `obter_alocacoes_existentes` espera o `db`
        alocacoes = obter_alocacoes_existentes(db, dia, horario, ano, mes)
        return {
            "success": True,
            "alocacoes": alocacoes,
            "dia": dia,
            "horario": horario,
            "dia_nome": DIAS_SEMANA[dia] if 0 <= dia < 5 else "Dia inválido",
            "horario_nome": HORARIOS_NOTURNOS[horario] if 0 <= horario < 4 else "Horário inválido"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter alocações existentes: {str(e)}")

@router.post("/alocacao-manual", response_model=AssocUDD)
def criar_alocacao_manual(
    alocacao: AssocUDDCreate,
    db: Session = Depends(get_db)
):
    """Cria uma alocação manual de docente"""
    try:
        # Verifica se o docente existe
        docente = db.query(DocenteModel).filter(DocenteModel.id == alocacao.docente_id).first()
        if not docente:
            raise HTTPException(status_code=404, detail="Docente não encontrado")
        
        # Verifica se a UC existe
        uc = db.query(UCModel).filter(UCModel.id == alocacao.uc_id).first()
        if not uc:
            raise HTTPException(status_code=404, detail="UC não encontrada")
        
        # Verifica se já existe alocação para este docente no mesmo horário
        alocacao_existente = db.query(AssocUDDModel).filter(
            AssocUDDModel.docente_id == alocacao.docente_id,
            AssocUDDModel.dia_semana == alocacao.dia_semana,
            AssocUDDModel.horario_inicio == alocacao.horario_inicio,
            AssocUDDModel.ano == alocacao.ano,
            AssocUDDModel.mes == alocacao.mes,
            AssocUDDModel.ativa == True
        ).first()
        
        if alocacao_existente:
            raise HTTPException(status_code=400, detail="Docente já possui alocação neste horário")
        
        # Cria a alocação
        db_alocacao = AssocUDDModel(**alocacao.model_dump())
        db.add(db_alocacao)
        db.commit()
        db.refresh(db_alocacao)
        
        return db_alocacao
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao criar alocação manual: {str(e)}")

@router.put("/alocacao/{alocacao_id}", response_model=AssocUDD)
def atualizar_alocacao(
    alocacao_id: int,
    alocacao_update: AssocUDDUpdate,
    db: Session = Depends(get_db)
):
    """Atualiza uma alocação existente"""
    try:
        alocacao = db.query(AssocUDDModel).filter(AssocUDDModel.id == alocacao_id).first()
        if not alocacao:
            raise HTTPException(status_code=404, detail="Alocação não encontrada")
        
        # Atualiza os campos
        update_data = alocacao_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(alocacao, field, value)
        
        db.commit()
        db.refresh(alocacao)
        
        return alocacao
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar alocação: {str(e)}")

@router.delete("/alocacao/{alocacao_id}")
def deletar_alocacao(
    alocacao_id: int,
    db: Session = Depends(get_db)
):
    """Deleta uma alocação (marca como inativa)"""
    try:
        alocacao = db.query(AssocUDDModel).filter(AssocUDDModel.id == alocacao_id).first()
        if not alocacao:
            raise HTTPException(status_code=404, detail="Alocação não encontrada")
        
        # Marca como inativa ao invés de deletar
        setattr(alocacao, 'ativa', False)
        db.commit()
        
        return {"success": True, "mensagem": "Alocação removida com sucesso"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao deletar alocação: {str(e)}")

@router.get("/relatorio-docente/{docente_id}")
def obter_relatorio_docente(
    docente_id: int,
    ano: Optional[int] = None,
    mes: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Obtém relatório de alocações de um docente específico"""
    try:
        ano_atual = ano or datetime.now().year
        mes_atual = mes or datetime.now().month
        
        # Busca o docente
        docente = db.query(DocenteModel).filter(DocenteModel.id == docente_id).first()
        if not docente:
            raise HTTPException(status_code=404, detail="Docente não encontrado")
        
        # Busca as alocações do docente
        alocacoes = db.query(AssocUDDModel).filter(
            AssocUDDModel.docente_id == docente_id,
            AssocUDDModel.ano == ano_atual,
            AssocUDDModel.mes == mes_atual,
            AssocUDDModel.ativa == True
        ).all()
        
        # Formata o relatório
        relatorio = {
            "docente": {
                "id": docente.id,
                "nome": docente.nome,
                "email": docente.email,
                "especialidade": docente.especialidade,
                "carga_horaria_total": docente.carga_horaria_total,
                "saldo_horas": docente.saldo_horas
            },
            "alocacoes": [],
            "total_alocacoes": len(alocacoes),
            "carga_horaria_alocada": len(alocacoes) * 3.33,  # 3h20min por alocação
            "ano": ano_atual,
            "mes": mes_atual
        }
        
        for alocacao in alocacoes:
            uc = db.query(UCModel).filter(UCModel.id == alocacao.uc_id).first()
            relatorio["alocacoes"].append({
                "id": alocacao.id,
                "uc_id": alocacao.uc_id,
                "uc_nome": uc.nome if uc else "UC não encontrada",
                "dia_semana": alocacao.dia_semana,
                                 "dia_nome": DIAS_SEMANA[int(alocacao.dia_semana)],
                "horario_inicio": alocacao.horario_inicio,
                "horario_fim": alocacao.horario_fim,
                "data_alocacao": alocacao.data_alocacao
            })
        
        return {
            "success": True,
            "relatorio": relatorio
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar relatório: {str(e)}")

@router.get("/estatisticas")
def obter_estatisticas_alocacao(
    ano: Optional[int] = None,
    mes: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Obtém estatísticas gerais das alocações"""
    try:
        ano_atual = ano or datetime.now().year
        mes_atual = mes or datetime.now().month
        
        # Total de alocações
        total_alocacoes = db.query(AssocUDDModel).filter(
            AssocUDDModel.ano == ano_atual,
            AssocUDDModel.mes == mes_atual,
            AssocUDDModel.ativa == True
        ).count()
        
        # Docentes com alocações
        docentes_com_alocacoes = db.query(AssocUDDModel.docente_id).filter(
            AssocUDDModel.ano == ano_atual,
            AssocUDDModel.mes == mes_atual,
            AssocUDDModel.ativa == True
        ).distinct().count()
        
        # UCs com alocações
        ucs_com_alocacoes = db.query(AssocUDDModel.uc_id).filter(
            AssocUDDModel.ano == ano_atual,
            AssocUDDModel.mes == mes_atual,
            AssocUDDModel.ativa == True
        ).distinct().count()
        
        # Total de docentes cadastrados
        total_docentes = db.query(DocenteModel).count()
        
        # Total de UCs cadastradas
        total_ucs = db.query(UCModel).count()
        
        # Carga horária total alocada (3h20min por alocação)
        carga_horaria_total = total_alocacoes * 3.33
        
        return {
            "success": True,
            "estatisticas": {
                "total_alocacoes": total_alocacoes,
                "docentes_com_alocacoes": docentes_com_alocacoes,
                "ucs_com_alocacoes": ucs_com_alocacoes,
                "total_docentes": total_docentes,
                "total_ucs": total_ucs,
                "carga_horaria_total": carga_horaria_total,
                "taxa_utilizacao_docentes": round((docentes_com_alocacoes / total_docentes * 100), 2) if total_docentes > 0 else 0,
                "taxa_utilizacao_ucs": round((ucs_com_alocacoes / total_ucs * 100), 2) if total_ucs > 0 else 0,
                "ano": ano_atual,
                "mes": mes_atual
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter estatísticas: {str(e)}") 