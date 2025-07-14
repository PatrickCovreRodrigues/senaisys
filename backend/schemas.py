from pydantic import BaseModel, ConfigDict
from typing import List, Dict, Optional, Any
from datetime import datetime

# Schemas para Curso
class CursoBase(BaseModel):
    nome: str
    carga_horaria: int
    fases: Optional[str] = None

class CursoCreate(CursoBase):
    pass

class CursoUpdate(BaseModel):
    nome: Optional[str] = None
    carga_horaria: Optional[int] = None
    fases: Optional[str] = None

class Curso(CursoBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Schemas para Docente
class DocenteBase(BaseModel):
    nome: str
    email: Optional[str] = None
    especialidade: Optional[str] = None
    matricula: Optional[int] = None
    carga_horaria_total: Optional[float] = 0.0
    tipo_docente: Optional[int] = None
    saldo_horas: Optional[float] = 0.0
    restricoes_dias: Optional[List[int]] = []
    disciplinas: Optional[List[str]] = []
    disponibilidade: Optional[Dict[str, bool]] = {}
    horarios: Optional[Dict[str, Dict[str, str]]] = {}

class DocenteCreate(DocenteBase):
    ucs_ids: Optional[List[int]] = []

class DocenteUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    especialidade: Optional[str] = None
    matricula: Optional[int] = None
    carga_horaria_total: Optional[float] = None
    tipo_docente: Optional[int] = None
    saldo_horas: Optional[float] = None
    restricoes_dias: Optional[List[int]] = None
    disciplinas: Optional[List[str]] = None
    disponibilidade: Optional[Dict[str, bool]] = None
    horarios: Optional[Dict[str, Dict[str, str]]] = None
    ucs_ids: Optional[List[int]] = None

class Docente(DocenteBase):
    id: int
    created_at: datetime
    updated_at: datetime
    ucs: Optional[List['UC']] = []
    
    model_config = ConfigDict(from_attributes=True)

# Schemas para UC
class UCBase(BaseModel):
    nome: str
    carga_horaria: int
    docente_id: Optional[int] = None
    curso_id: Optional[int] = None

class UCCreate(UCBase):
    pass

class UCUpdate(BaseModel):
    nome: Optional[str] = None
    carga_horaria: Optional[int] = None
    docente_id: Optional[int] = None
    curso_id: Optional[int] = None

class UC(UCBase):
    id: int
    created_at: datetime
    updated_at: datetime
    curso: Optional['Curso'] = None
    
    model_config = ConfigDict(from_attributes=True)

# Schemas para Calendario
class CalendarioBase(BaseModel):
    curso_id: int
    fases_selecionadas: Optional[List[int]] = []
    mes: int
    ano: int
    eventos: Optional[List[Dict[str, Any]]] = []

class CalendarioCreate(CalendarioBase):
    pass

class CalendarioUpdate(BaseModel):
    curso_id: Optional[int] = None
    fases_selecionadas: Optional[List[int]] = None
    mes: Optional[int] = None
    ano: Optional[int] = None
    eventos: Optional[List[Dict[str, Any]]] = None

class Calendario(CalendarioBase):
    id: int
    created_at: datetime
    updated_at: datetime
    curso: Optional[Curso] = None
    
    model_config = ConfigDict(from_attributes=True)

# Schemas para Assoc_UDD
class AssocUDDBase(BaseModel):
    uc_id: int
    docente_id: int
    dia_semana: int
    horario_inicio: str
    horario_fim: str
    data_alocacao: datetime
    mes: int
    ano: int
    ativa: bool = True

class AssocUDDCreate(AssocUDDBase):
    pass

class AssocUDDUpdate(BaseModel):
    uc_id: Optional[int] = None
    docente_id: Optional[int] = None
    dia_semana: Optional[int] = None
    horario_inicio: Optional[str] = None
    horario_fim: Optional[str] = None
    data_alocacao: Optional[datetime] = None
    mes: Optional[int] = None
    ano: Optional[int] = None
    ativa: Optional[bool] = None

class AssocUDD(AssocUDDBase):
    id: int
    created_at: datetime
    updated_at: datetime
    uc: Optional[UC] = None
    docente: Optional[Docente] = None
    
    model_config = ConfigDict(from_attributes=True) 