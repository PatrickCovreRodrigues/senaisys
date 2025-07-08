from __future__ import annotations
"""
Sistema de Gestão Docente (SGD) - Alocação Automática de Docentes
Implementa a lógica de alocação de professores em disciplinas (UCs) durante a semana.
"""

import csv
import random
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional, Sequence
import holidays
import pandas as pd
from sqlalchemy.orm import Session
from models import Docente, UC, Assoc_UDD
from database import SessionLocal

# Constantes
DIAS_SEMANA = ['segunda', 'terca', 'quarta', 'quinta', 'sexta']
HORARIOS_NOTURNOS = ['19:00', '20:00', '21:00', '22:00']
DURACAO_AULA = 3.33  # 3h20min em horas decimais

class DocenteAlocacao:
    """Classe para representar um docente no sistema de alocação"""
    
    def __init__(self, docente_db: Docente):
        self.id: int = docente_db.id
        self.mat: int = docente_db.matricula
        self.ch: float = docente_db.carga_horaria_total
        self.tipo: int = docente_db.tipo_docente
        self.saldo: float = docente_db.saldo_horas if docente_db.saldo_horas is not None and docente_db.saldo_horas > 0 else self.ch
        self.rest: List[int] = docente_db.restricoes_dias or []
        self.dias_fixos = []
        self.alocacoes = []

class SGDAlocacao:
    """Sistema de Gestão Docente - Alocação Automática"""
    
    def __init__(self, db: Session, ano: Optional[int] = None, mes: Optional[int] = None):
        self.db = db
        self.ano = ano or datetime.now().year
        self.mes = mes or datetime.now().month
        self.matriz_agendamento = [[[] for _ in range(4)] for _ in range(5)]  # 5 dias x 4 horários
        self.feriados = self._obter_feriados()
        self.dias_letivos = self._calcular_dias_letivos()
        
    def _obter_feriados(self) -> List[datetime]:
        """Obtém os feriados nacionais para o ano/mês especificado"""
        try:
            br_holidays = holidays.country_holidays('BR', years=self.ano)
            feriados_mes = []
            
            for data, nome in br_holidays.items():
                if data.year == self.ano and data.month == self.mes:
                    feriados_mes.append(data)
                    
            return feriados_mes
        except Exception:
            return []
    
    def _calcular_dias_letivos(self) -> List[int]:
        """Calcula quais dias da semana são letivos (exclui feriados)"""
        dias_letivos = list(range(5))  # Segunda a sexta (0-4)
        
        # Remove dias que são feriados
        for feriado in self.feriados:
            dia_semana = feriado.weekday()  # 0=Segunda, 6=Domingo
            if dia_semana < 5 and dia_semana in dias_letivos:
                dias_letivos.remove(dia_semana)
                
        return dias_letivos
    
    def _validar_disponibilidade(self, docente: DocenteAlocacao, dia: int, horario: int) -> bool:
        """Verifica se o docente está disponível no dia e horário especificados"""
        # Verifica restrições de dia
        if dia in docente.rest:
            return False
            
        # Verifica se já tem alocação neste horário
        for alocacao in docente.alocacoes:
            if alocacao['dia'] == dia and alocacao['horario'] == horario:
                return False
                
        # Verifica se o dia é letivo
        if dia not in self.dias_letivos:
            return False
            
        return True
    
    def _verificar_conflito_horario(self, dia: int, horario: int, docente_id: int) -> bool:
        """Verifica se há conflito de horário na matriz"""
        if not self.matriz_agendamento[dia][horario]:
            return False
            
        for alocacao in self.matriz_agendamento[dia][horario]:
            if alocacao['docente_id'] == docente_id:
                return True
                
        return False
    
    def _alocar_docente(self, docente: DocenteAlocacao, uc_id: int, dia: int, horario: int) -> bool:
        """Aloca um docente em uma UC em um dia e horário específicos"""
        if not self._validar_disponibilidade(docente, dia, horario):
            return False
            
        if self._verificar_conflito_horario(dia, horario, docente.id):
            return False
            
        # Cria a alocação
        alocacao = {
            'docente_id': docente.id,
            'uc_id': uc_id,
            'dia': dia,
            'horario': horario,
            'horario_inicio': HORARIOS_NOTURNOS[horario],
            'horario_fim': self._calcular_horario_fim(HORARIOS_NOTURNOS[horario])
        }
        
        # Adiciona na matriz
        self.matriz_agendamento[dia][horario].append(alocacao)
        
        # Adiciona na lista de alocações do docente
        docente.alocacoes.append(alocacao)
        
        # Reduz o saldo do docente
        docente.saldo -= DURACAO_AULA
        
        return True
    
    def _calcular_horario_fim(self, horario_inicio: str) -> str:
        """Calcula o horário de fim baseado no início (adiciona 3h20min)"""
        hora, minuto = map(int, horario_inicio.split(':'))
        inicio = datetime(2000, 1, 1, hora, minuto)
        fim = inicio + timedelta(hours=3, minutes=20)
        return fim.strftime('%H:%M')
    
    def _classificar_docentes(self, docentes: List[DocenteAlocacao]) -> Dict[int, List[DocenteAlocacao]]:
        """Classifica docentes por tipo (1, 2, 3) baseado na carga horária"""
        classificacao: Dict[int, List[DocenteAlocacao]] = {1: [], 2: [], 3: []}
        
        for docente in docentes:
            if docente.ch > 100:
                docente.tipo = 1
            elif 50 <= docente.ch <= 99:
                docente.tipo = 2
            else:
                docente.tipo = 3
            
            if docente.tipo in classificacao:
                classificacao[docente.tipo].append(docente)
            
        return classificacao
    
    def _alocar_tipo_1(self, docentes: List[DocenteAlocacao], ucs: List[int]) -> None:
        """Aloca docentes Tipo 1 (>100h) em 2 dias fixos por semana"""
        for docente in docentes:
            if docente.saldo <= 0:
                continue
                
            # Seleciona 2 dias fixos aleatórios (excluindo restrições)
            dias_disponiveis = [d for d in self.dias_letivos if d not in docente.rest]
            
            if len(dias_disponiveis) >= 2:
                docente.dias_fixos = random.sample(dias_disponiveis, 2)
                
                # Aloca em horários nos dias fixos
                for uc_id in ucs:
                    if docente.saldo <= 0:
                        break
                        
                    for dia in docente.dias_fixos:
                        if docente.saldo <= 0:
                            break
                            
                        for horario in range(4):
                            if docente.saldo <= 0:
                                break
                                
                            if self._alocar_docente(docente, uc_id, dia, horario):
                                break
    
    def _alocar_tipo_2(self, docentes: List[DocenteAlocacao], ucs: List[int]) -> None:
        """Aloca docentes Tipo 2 (50-99h) em 1 dia fixo por semana"""
        for docente in docentes:
            if docente.saldo <= 0:
                continue
                
            # Seleciona 1 dia fixo aleatório (excluindo restrições)
            dias_disponiveis = [d for d in self.dias_letivos if d not in docente.rest]
            
            if dias_disponiveis:
                docente.dias_fixos = [random.choice(dias_disponiveis)]
                
                # Aloca em horários no dia fixo
                for uc_id in ucs:
                    if docente.saldo <= 0:
                        break
                        
                    dia = docente.dias_fixos[0]
                    for horario in range(4):
                        if docente.saldo <= 0:
                            break
                            
                        if self._alocar_docente(docente, uc_id, dia, horario):
                            break
    
    def _alocar_tipo_3(self, docentes: List[DocenteAlocacao], ucs: List[int]) -> None:
        """Aloca docentes Tipo 3 (<50h) de forma aleatória nos dias restantes"""
        for docente in docentes:
            if docente.saldo <= 0:
                continue
                
            # Aloca aleatoriamente nos dias disponíveis
            dias_disponiveis = [d for d in self.dias_letivos if d not in docente.rest]
            
            for uc_id in ucs:
                if docente.saldo <= 0:
                    break
                    
                random.shuffle(dias_disponiveis)
                for dia in dias_disponiveis:
                    if docente.saldo <= 0:
                        break
                        
                    horarios_disponiveis = list(range(4))
                    random.shuffle(horarios_disponiveis)
                    
                    for horario in horarios_disponiveis:
                        if docente.saldo <= 0:
                            break
                            
                        if self._alocar_docente(docente, uc_id, dia, horario):
                            break
    
    def processar_alocacao(self) -> Dict:
        """Processa a alocação completa dos docentes"""
        
        # 1. Carregar docentes e UCs do banco
        docentes_db = self.db.query(Docente).all()
        ucs_db = self.db.query(UC).all()
        
        if not docentes_db or not ucs_db:
            return {"status": "erro", "mensagem": "Não há docentes ou UCs cadastrados."}

        # 2. Converter para objetos DocenteAlocacao
        docentes = [DocenteAlocacao(d) for d in docentes_db]
        ucs_ids = [uc.id for uc in ucs_db]
        
        # 3. Classificar docentes
        classificacao = self._classificar_docentes(docentes)
        
        # 4. Executar alocação por tipo
        # A ordem de alocação é importante para a priorização
        self._alocar_tipo_1(classificacao.get(1, []), ucs_ids)
        self._alocar_tipo_2(classificacao.get(2, []), ucs_ids)
        self._alocar_tipo_3(classificacao.get(3, []), ucs_ids)
        
        # 5. Gerar resultado
        resultado = self._gerar_resultado(docentes)
        
        # 6. Persistir no banco
        self.persistir_banco(resultado)
        
        return resultado

    def _gerar_resultado(self, docentes: List[DocenteAlocacao]) -> Dict:
        """Gera o dicionário de resultados com as matrizes e saldos"""
        
        # Matriz Agendada (M_agen)
        m_agen = [[0 for _ in range(4)] for _ in range(5)]
        for dia in range(5):
            for horario in range(4):
                if self.matriz_agendamento[dia][horario]:
                    # Pega a matrícula do primeiro docente alocado no slot
                    alocacao_info = self.matriz_agendamento[dia][horario][0]
                    docente_id = alocacao_info['docente_id']
                    docente_obj = next((d for d in docentes if d.id == docente_id), None)
                    m_agen[dia][horario] = docente_obj.mat if docente_obj else 'N/A'
                else:
                    m_agen[dia][horario] = 0 # Slot vazio

        # Matriz Calendário (transposta)
        m_cal = list(map(list, zip(*m_agen)))

        # Saldos finais
        saldos = {d.mat: round(d.saldo, 2) for d in docentes}
        
        return {
            "status": "sucesso",
            "matriz_agendada": m_agen,
            "matriz_calendario": m_cal,
            "saldos_finais": saldos,
            "alocacoes_detalhadas": self.matriz_agendamento
        }

    def exportar_csv(self, resultado: Dict, nome_arquivo: Optional[str] = None) -> str:
        """Exporta o resultado para CSV"""
        if not nome_arquivo:
            nome_arquivo = f"alocacao_docentes_{self.ano}_{self.mes:02d}.csv"
            
        dados = []
        for dia in range(5):
            for horario in range(4):
                for alocacao in self.matriz_agendamento[dia][horario]:
                    dados.append({
                        'Dia': DIAS_SEMANA[dia],
                        'Horario': HORARIOS_NOTURNOS[horario],
                        'Docente_ID': alocacao['docente_id'],
                        'UC_ID': alocacao['uc_id'],
                        'Horario_Inicio': alocacao['horario_inicio'],
                        'Horario_Fim': alocacao['horario_fim'],
                        'Ano': self.ano,
                        'Mes': self.mes
                    })
        
        df = pd.DataFrame(dados)
        df.to_csv(nome_arquivo, index=False, encoding='utf-8')
        return nome_arquivo

    def persistir_banco(self, resultado: Dict) -> bool:
        """Salva o resultado da alocação no banco de dados"""
        if resultado['status'] != 'sucesso':
            return False
            
        try:
            # Limpa alocações antigas para o mesmo período
            self.db.query(Assoc_UDD).filter(
                Assoc_UDD.ano == self.ano,
                Assoc_UDD.mes == self.mes
            ).delete(synchronize_session=False)

            # Insere novas alocações
            for dia_semana, horarios in enumerate(resultado['alocacoes_detalhadas']):
                for slot in horarios:
                    for alocacao in slot:
                        nova_alocacao = Assoc_UDD(
                            uc_id=alocacao['uc_id'],
                            docente_id=alocacao['docente_id'],
                            dia_semana=dia_semana,
                            horario_inicio=alocacao['horario_inicio'],
                            horario_fim=alocacao['horario_fim'],
                            data_alocacao=datetime.now(),
                            mes=self.mes,
                            ano=self.ano
                        )
                        self.db.add(nova_alocacao)
            
            # Atualiza saldo dos docentes
            docentes_db = {d.mat: d for d in self.db.query(Docente).all()}
            for mat, saldo in resultado['saldos_finais'].items():
                if mat in docentes_db:
                    docentes_db[mat].saldo_horas = saldo
            
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            print(f"Erro ao persistir no banco: {e}")
            return False


def alocar_docentes(db: Session, ano: Optional[int] = None, mes: Optional[int] = None) -> Dict:
    """
    Ponto de entrada para o processo de alocação de docentes.
    Esta função é chamada pela API para iniciar a alocação.
    """
    try:
        # Cria a instância do sistema de alocação
        sgd = SGDAlocacao(db=db, ano=ano, mes=mes)
        
        # Processa a alocação
        resultado = sgd.processar_alocacao()
        
        # Opcional: exporta para CSV
        if resultado['status'] == 'sucesso':
            sgd.exportar_csv(resultado)
            
        return resultado

    except Exception as e:
        print(f"Erro inesperado no processo de alocação: {e}")
        return {"status": "erro", "mensagem": str(e)}


# Funções auxiliares (podem ser movidas para outro módulo se necessário)

def obter_alocacoes_existentes(db: Session, dia: int, horario: int, ano: Optional[int] = None, mes: Optional[int] = None) -> List[Dict]:
    """
    Obtém as alocações existentes para um dia e horário específicos
    
    Args:
        dia: Dia da semana (0=Segunda, ..., 4=Sexta)
        horario: Horário (0-3)
        ano: Ano (padrão: ano atual)
        mes: Mês (padrão: mês atual)
    
    Returns:
        Lista de alocações existentes
    """
    ano_atual = ano or datetime.now().year
    mes_atual = mes or datetime.now().month

    alocacoes = db.query(Assoc_UDD).filter(
        Assoc_UDD.dia_semana == dia,
        Assoc_UDD.ano == ano_atual,
        Assoc_UDD.mes == mes_atual,
        Assoc_UDD.ativa == True
    ).all()

    # Simplificação: verificar se o horário do slot bate com o horário de início da alocação
    horario_str = HORARIOS_NOTURNOS[horario]
    resultado = []
    for aloc in alocacoes:
        if aloc.horario_inicio == horario_str:
            resultado.append({
                "docente_id": aloc.docente_id,
                "uc_id": aloc.uc_id
            })
            
    return resultado

def verificar_disponibilidade_docente(db: Session, docente_id: int, dia: int, horario: int) -> bool:
    """
    Verifica a disponibilidade de um docente específico em um dia/horário.
    Usado para verificações pontuais, não no loop principal de alocação.
    """
    docente = db.query(Docente).filter(Docente.id == docente_id).first()
    if not docente:
        return False

    # Verifica se o dia está nas restrições
    if docente.restricoes_dias and dia in docente.restricoes_dias:
        return False

    # Verifica a disponibilidade detalhada (se existir)
    dia_str = DIAS_SEMANA[dia]
    disponibilidade = docente.disponibilidade or {}
    if not disponibilidade.get(dia_str, False):
        return False
        
    # Verifica se o horário está dentro do range de disponibilidade do docente
    horario_inicio_slot = datetime.strptime(HORARIOS_NOTURNOS[horario], '%H:%M').time()
    
    horarios_docente = docente.horarios or {}
    inicio_docente_str = horarios_docente.get(dia_str, {}).get('inicio')
    fim_docente_str = horarios_docente.get(dia_str, {}).get('fim')

    if not inicio_docente_str or not fim_docente_str:
        return True # Se não há horário específico, considera disponível

    inicio_docente = datetime.strptime(inicio_docente_str, '%H:%M').time()
    fim_docente = datetime.strptime(fim_docente_str, '%H:%M').time()

    return inicio_docente <= horario_inicio_slot <= fim_docente 