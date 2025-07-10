"""
Sistema de Gestão Docente (SGD) - Alocação Automática Otimizada
Implementação otimizada da lógica de alocação de professores seguindo as regras matemáticas especificadas.
"""

import csv
import random
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional, Any
import holidays
import pandas as pd
from sqlalchemy.orm import Session
from models import Docente, UC, Assoc_UDD
from database import SessionLocal


class MatrizAlocacao:
    """Classe para gerenciar a matriz de alocação 5x4 (dias x horários)"""
    
    def __init__(self):
        self.matriz_inicial = self._criar_matriz_inicial()
        self.matriz_ajustada = None
        self.matriz_agendada = None
        self.matriz_calendario = None
    
    def _criar_matriz_inicial(self) -> np.ndarray:
        """Cria matriz inicial 5x4 com todos elementos = 1"""
        return np.ones((5, 4), dtype=int)
    
    def ajustar_para_feriados(self, dias_nao_letivos: List[int]) -> np.ndarray:
        """
        Ajusta matriz para dias não-letivos (feriados)
        
        Args:
            dias_nao_letivos: Lista de índices de dias não-letivos (0=Segunda, 4=Sexta)
            
        Returns:
            Matriz ajustada com dias não-letivos zerados
        """
        self.matriz_ajustada = self.matriz_inicial.copy()
        
        # Operação elementar: 0 * Li para cada dia não-letivo
        for dia in dias_nao_letivos:
            if 0 <= dia < 5:
                self.matriz_ajustada[dia, :] = 0
        
        return self.matriz_ajustada
    
    def gerar_matriz_agendada(self, alocacao_docentes: List[int]) -> np.ndarray:
        """
        Gera matriz agendada aplicando operações elementares
        
        Args:
            alocacao_docentes: Lista com matrícula do docente para cada dia [mat1, mat2, mat3, mat4, mat5]
            
        Returns:
            Matriz agendada com matrículas dos docentes
        """
        if self.matriz_ajustada is None:
            raise ValueError("Matriz deve ser ajustada antes do agendamento")
        
        self.matriz_agendada = np.zeros((5, 4), dtype=int)
        
        # Operação elementar: mati * Li para cada linha
        for i in range(5):
            if any(self.matriz_ajustada[i]):  # Se o dia é letivo
                matricula = alocacao_docentes[i]
                self.matriz_agendada[i, :] = matricula
        
        return self.matriz_agendada
    
    def gerar_matriz_calendario(self) -> np.ndarray:
        """
        Gera matriz calendário (transposta da matriz agendada)
        
        Returns:
            Matriz calendário (4x5) - horários x dias
        """
        if self.matriz_agendada is None:
            raise ValueError("Matriz deve ser agendada antes de gerar calendário")
        
        self.matriz_calendario = self.matriz_agendada.T
        return self.matriz_calendario


class DocenteOtimizado:
    """Classe otimizada para representar docente no sistema de alocação"""
    
    def __init__(self, dados: Dict[str, Any]):
        self.id: str = dados.get('id', '')
        self.mat: int = dados.get('mat', 0)
        self.ch: float = dados.get('ch', 0.0)
        self.saldo: float = dados.get('saldo', self.ch)
        self.rest: List[int] = dados.get('rest', [])
        self.tipo: int = self._classificar_tipo()
        self.dias_alocados: List[int] = []
        self.horas_reduzidas: float = 0.0
    
    def _classificar_tipo(self) -> int:
        """Classifica docente por tipo baseado na carga horária"""
        if self.ch > 100:
            return 1
        elif 50 <= self.ch <= 99:
            return 2
        else:
            return 3
    
    def reduzir_saldo(self, horas: float = 3.33) -> None:
        """Reduz saldo de horas do docente (3h20min = 3.33h)"""
        self.saldo -= horas
        self.horas_reduzidas += horas
        if self.saldo < 0:
            self.saldo = 0
    
    def tem_saldo_disponivel(self) -> bool:
        """Verifica se docente tem saldo disponível"""
        return self.saldo > 0
    
    def pode_ser_alocado_no_dia(self, dia: int) -> bool:
        """Verifica se docente pode ser alocado no dia especificado"""
        return dia not in self.rest and self.tem_saldo_disponivel()


class SGDAlocacaoOtimizada:
    """Sistema de Gestão Docente - Alocação Automática Otimizada"""
    
    def __init__(self, ano: int = None, mes: int = None):
        self.ano = ano or datetime.now().year
        self.mes = mes or datetime.now().month
        self.matriz = MatrizAlocacao()
        self.docentes: List[DocenteOtimizado] = []
        self.feriados_nacionais = self._obter_feriados_nacionais()
        self.dias_nao_letivos = self._calcular_dias_nao_letivos()
        
        # Configurações
        self.DURACAO_AULA = 3.33  # 3h20min
        self.DIAS_SEMANA = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta']
        self.HORARIOS = ['19:00', '19:50', '20:50', '21:40']
    
    def _obter_feriados_nacionais(self) -> List[datetime]:
        """Obtém feriados nacionais do Brasil para o ano especificado"""
        try:
            br_holidays = holidays.country_holidays('BR', years=self.ano)
            return [data for data in br_holidays.keys() if data.year == self.ano]
        except Exception:
            return []
    
    def _calcular_dias_nao_letivos(self) -> List[int]:
        """Calcula dias não-letivos baseado em feriados que caem em dias úteis"""
        dias_nao_letivos = []
        
        for feriado in self.feriados_nacionais:
            if feriado.month == self.mes:
                dia_semana = feriado.weekday()  # 0=Segunda, 6=Domingo
                if 0 <= dia_semana < 5:  # Dias úteis
                    dias_nao_letivos.append(dia_semana)
        
        return list(set(dias_nao_letivos))  # Remove duplicatas
    
    def carregar_docentes(self, dados_docentes: List[Dict[str, Any]]) -> None:
        """
        Carrega lista de docentes para alocação
        
        Args:
            dados_docentes: Lista de dicionários com dados dos docentes
                          Formato: [{'id': 'P1', 'mat': 12345, 'ch': 108, 'saldo': 108, 'rest': [3,4]}]
        """
        self.docentes = [DocenteOtimizado(dados) for dados in dados_docentes]
    
    def _classificar_docentes_por_tipo(self) -> Dict[int, List[DocenteOtimizado]]:
        """Classifica docentes por tipo (1, 2, 3)"""
        classificacao = {1: [], 2: [], 3: []}
        
        for docente in self.docentes:
            if docente.tem_saldo_disponivel():
                classificacao[docente.tipo].append(docente)
        
        return classificacao
    
    def _selecionar_docentes_para_dias(self) -> List[int]:
        """
        Seleciona docentes para cada dia da semana seguindo as regras de prioridade
        
        Returns:
            Lista com matrícula do docente para cada dia [mat1, mat2, mat3, mat4, mat5]
        """
        classificacao = self._classificar_docentes_por_tipo()
        dias_disponiveis = [i for i in range(5) if i not in self.dias_nao_letivos]
        alocacao = [0] * 5  # Inicializa com 0 (sem alocação)
        docentes_usados = set()
        
        # Embaralha listas para randomização
        random.shuffle(classificacao[1])
        random.shuffle(classificacao[2])
        random.shuffle(classificacao[3])
        random.shuffle(dias_disponiveis)
        
        # Tipo 1: 2 dias fixos (prioridade máxima)
        tipo1_alocados = 0
        for docente in classificacao[1]:
            if tipo1_alocados >= len(dias_disponiveis):
                break
            
            dias_possiveis = [d for d in dias_disponiveis 
                            if d not in docente.rest and docente.mat not in docentes_usados]
            
            if len(dias_possiveis) >= 2:
                dias_escolhidos = random.sample(dias_possiveis, min(2, len(dias_possiveis)))
                for dia in dias_escolhidos:
                    alocacao[dia] = docente.mat
                    docentes_usados.add(docente.mat)
                    docente.dias_alocados.extend(dias_escolhidos)
                    docente.reduzir_saldo(self.DURACAO_AULA)
                    tipo1_alocados += 1
                    
                    if tipo1_alocados >= len(dias_disponiveis):
                        break
        
        # Tipo 2: 1 dia fixo (prioridade secundária)
        for docente in classificacao[2]:
            dias_possiveis = [d for d in dias_disponiveis 
                            if d not in docente.rest and docente.mat not in docentes_usados 
                            and alocacao[d] == 0]
            
            if dias_possiveis:
                dia_escolhido = random.choice(dias_possiveis)
                alocacao[dia_escolhido] = docente.mat
                docentes_usados.add(docente.mat)
                docente.dias_alocados.append(dia_escolhido)
                docente.reduzir_saldo(self.DURACAO_AULA)
        
        # Tipo 3: Alocação aleatória nos dias restantes
        for docente in classificacao[3]:
            dias_possiveis = [d for d in dias_disponiveis 
                            if d not in docente.rest and docente.mat not in docentes_usados 
                            and alocacao[d] == 0]
            
            if dias_possiveis:
                dia_escolhido = random.choice(dias_possiveis)
                alocacao[dia_escolhido] = docente.mat
                docentes_usados.add(docente.mat)
                docente.dias_alocados.append(dia_escolhido)
                docente.reduzir_saldo(self.DURACAO_AULA)
        
        return alocacao
    
    def processar_alocacao(self) -> Dict[str, Any]:
        """
        Processa a alocação completa de docentes
        
        Returns:
            Dicionário com resultado da alocação
        """
        if not self.docentes:
            raise ValueError("Nenhum docente carregado para alocação")
        
        # Etapa 1: Ajustar matriz para feriados
        self.matriz.ajustar_para_feriados(self.dias_nao_letivos)
        
        # Etapa 2: Selecionar docentes para cada dia
        alocacao_docentes = self._selecionar_docentes_para_dias()
        
        # Etapa 3: Gerar matriz agendada
        matriz_agendada = self.matriz.gerar_matriz_agendada(alocacao_docentes)
        
        # Etapa 4: Gerar matriz calendário (transposta)
        matriz_calendario = self.matriz.gerar_matriz_calendario()
        
        # Etapa 5: Compilar resultado
        resultado = {
            'ano': self.ano,
            'mes': self.mes,
            'feriados_detectados': len(self.feriados_nacionais),
            'dias_nao_letivos': self.dias_nao_letivos,
            'matriz_inicial': self.matriz.matriz_inicial.tolist(),
            'matriz_ajustada': self.matriz.matriz_ajustada.tolist(),
            'matriz_agendada': matriz_agendada.tolist(),
            'matriz_calendario': matriz_calendario.tolist(),
            'alocacao_docentes': alocacao_docentes,
            'docentes_processados': self._gerar_relatorio_docentes(),
            'estatisticas': self._gerar_estatisticas()
        }
        
        return resultado
    
    def _gerar_relatorio_docentes(self) -> List[Dict[str, Any]]:
        """Gera relatório detalhado dos docentes processados"""
        relatorio = []
        
        for docente in self.docentes:
            relatorio.append({
                'id': docente.id,
                'matricula': docente.mat,
                'carga_horaria_original': docente.ch,
                'tipo': docente.tipo,
                'saldo_inicial': docente.ch,
                'saldo_final': docente.saldo,
                'horas_reduzidas': docente.horas_reduzidas,
                'dias_alocados': docente.dias_alocados,
                'restricoes': docente.rest
            })
        
        return relatorio
    
    def _gerar_estatisticas(self) -> Dict[str, Any]:
        """Gera estatísticas da alocação"""
        total_docentes = len(self.docentes)
        docentes_alocados = len([d for d in self.docentes if d.dias_alocados])
        total_horas_reduzidas = sum(d.horas_reduzidas for d in self.docentes)
        
        return {
            'total_docentes': total_docentes,
            'docentes_alocados': docentes_alocados,
            'taxa_alocacao': (docentes_alocados / total_docentes * 100) if total_docentes > 0 else 0,
            'total_horas_reduzidas': total_horas_reduzidas,
            'dias_letivos': len([i for i in range(5) if i not in self.dias_nao_letivos]),
            'feriados_no_mes': len(self.dias_nao_letivos)
        }
    
    def exportar_csv(self, resultado: Dict[str, Any], nome_arquivo: str = None) -> str:
        """
        Exporta resultado para arquivo CSV
        
        Args:
            resultado: Resultado da alocação
            nome_arquivo: Nome do arquivo (opcional)
            
        Returns:
            Caminho do arquivo gerado
        """
        if nome_arquivo is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"alocacao_docentes_{timestamp}.csv"
        
        # Preparar dados para CSV
        dados_csv = []
        
        # Cabeçalho
        dados_csv.append(['Sistema de Gestão Docente - Alocação Automática'])
        dados_csv.append([f'Ano: {resultado["ano"]}, Mês: {resultado["mes"]}'])
        dados_csv.append([f'Feriados detectados: {resultado["feriados_detectados"]}'])
        dados_csv.append([])
        
        # Matriz Agendada
        dados_csv.append(['MATRIZ AGENDADA (Dias x Horários)'])
        dados_csv.append(['Dia/Horário'] + self.HORARIOS)
        
        matriz_agendada = resultado['matriz_agendada']
        for i, dia in enumerate(self.DIAS_SEMANA):
            linha = [dia] + [str(matriz_agendada[i][j]) if matriz_agendada[i][j] != 0 else '-' 
                           for j in range(4)]
            dados_csv.append(linha)
        
        dados_csv.append([])
        
        # Matriz Calendário (Transposta)
        dados_csv.append(['MATRIZ CALENDÁRIO (Horários x Dias)'])
        dados_csv.append(['Horário/Dia'] + self.DIAS_SEMANA)
        
        matriz_calendario = resultado['matriz_calendario']
        for i, horario in enumerate(self.HORARIOS):
            linha = [horario] + [str(matriz_calendario[i][j]) if matriz_calendario[i][j] != 0 else '-' 
                               for j in range(5)]
            dados_csv.append(linha)
        
        dados_csv.append([])
        
        # Relatório de Docentes
        dados_csv.append(['RELATÓRIO DE DOCENTES'])
        dados_csv.append(['ID', 'Matrícula', 'CH Original', 'Tipo', 'Saldo Final', 
                         'Horas Reduzidas', 'Dias Alocados', 'Restrições'])
        
        for docente in resultado['docentes_processados']:
            linha = [
                docente['id'],
                docente['matricula'],
                docente['carga_horaria_original'],
                docente['tipo'],
                f"{docente['saldo_final']:.2f}",
                f"{docente['horas_reduzidas']:.2f}",
                ', '.join(map(str, docente['dias_alocados'])) if docente['dias_alocados'] else '-',
                ', '.join(map(str, docente['restricoes'])) if docente['restricoes'] else '-'
            ]
            dados_csv.append(linha)
        
        dados_csv.append([])
        
        # Estatísticas
        stats = resultado['estatisticas']
        dados_csv.append(['ESTATÍSTICAS'])
        dados_csv.append(['Total de Docentes', stats['total_docentes']])
        dados_csv.append(['Docentes Alocados', stats['docentes_alocados']])
        dados_csv.append(['Taxa de Alocação (%)', f"{stats['taxa_alocacao']:.1f}"])
        dados_csv.append(['Total Horas Reduzidas', f"{stats['total_horas_reduzidas']:.2f}"])
        dados_csv.append(['Dias Letivos', stats['dias_letivos']])
        dados_csv.append(['Feriados no Mês', stats['feriados_no_mes']])
        
        # Salvar arquivo
        with open(nome_arquivo, 'w', newline='', encoding='utf-8') as arquivo:
            writer = csv.writer(arquivo)
            writer.writerows(dados_csv)
        
        return nome_arquivo
    
    def persistir_banco_dados(self, resultado: Dict[str, Any], db: Session) -> bool:
        """
        Persiste resultado no banco de dados
        
        Args:
            resultado: Resultado da alocação
            db: Sessão do banco de dados
            
        Returns:
            True se persistido com sucesso
        """
        try:
            # Limpar alocações existentes do mês/ano
            db.query(Assoc_UDD).filter(
                Assoc_UDD.ano == self.ano,
                Assoc_UDD.mes == self.mes
            ).delete()
            
            # Inserir novas alocações
            matriz_agendada = resultado['matriz_agendada']
            
            for dia in range(5):
                for horario in range(4):
                    matricula = matriz_agendada[dia][horario]
                    if matricula != 0:
                        # Buscar docente e UC
                        docente = db.query(Docente).filter(Docente.matricula == matricula).first()
                        if docente and docente.ucs:
                            uc = docente.ucs[0]  # Primeira UC do docente
                            
                            # Criar alocação
                            alocacao = Assoc_UDD(
                                uc_id=uc.id,
                                docente_id=docente.id,
                                dia_semana=dia,
                                horario_inicio=self.HORARIOS[horario],
                                horario_fim=self._calcular_horario_fim(self.HORARIOS[horario]),
                                data_alocacao=datetime.now(),
                                mes=self.mes,
                                ano=self.ano,
                                ativa=True
                            )
                            
                            db.add(alocacao)
            
            # Atualizar saldo dos docentes
            for docente_info in resultado['docentes_processados']:
                docente = db.query(Docente).filter(
                    Docente.matricula == docente_info['matricula']
                ).first()
                if docente:
                    docente.saldo_horas = docente_info['saldo_final']
            
            db.commit()
            return True
            
        except Exception as e:
            db.rollback()
            print(f"Erro ao persistir no banco: {e}")
            return False
    
    def _calcular_horario_fim(self, horario_inicio: str) -> str:
        """Calcula horário de fim (início + 3h20min)"""
        hora, minuto = map(int, horario_inicio.split(':'))
        inicio = datetime(2000, 1, 1, hora, minuto)
        fim = inicio + timedelta(hours=3, minutes=20)
        return fim.strftime('%H:%M')


# Função principal para uso externo
def alocar_docentes_otimizado(dados_docentes: List[Dict[str, Any]], 
                            ano: int = None, 
                            mes: int = None,
                            exportar_csv: bool = True,
                            nome_arquivo_csv: str = None,
                            persistir_db: bool = False,
                            db: Session = None) -> Dict[str, Any]:
    """
    Função principal para alocação otimizada de docentes
    
    Args:
        dados_docentes: Lista de dicionários com dados dos docentes
        ano: Ano para alocação (padrão: ano atual)
        mes: Mês para alocação (padrão: mês atual)
        exportar_csv: Se deve exportar resultado para CSV
        nome_arquivo_csv: Nome do arquivo CSV (opcional)
        persistir_db: Se deve persistir no banco de dados
        db: Sessão do banco de dados (necessária se persistir_db=True)
        
    Returns:
        Dicionário com resultado completo da alocação
        
    Example:
        >>> docentes = [
        ...     {'id': 'P1', 'mat': 12345, 'ch': 108, 'saldo': 108, 'rest': []},
        ...     {'id': 'P2', 'mat': 67890, 'ch': 72, 'saldo': 72, 'rest': [3, 4]}
        ... ]
        >>> resultado = alocar_docentes_otimizado(docentes, ano=2025, mes=4)
        >>> print(f"Taxa de alocação: {resultado['estatisticas']['taxa_alocacao']:.1f}%")
    """
    # Validação de entrada
    if not dados_docentes:
        raise ValueError("Lista de docentes não pode estar vazia")
    
    if persistir_db and db is None:
        raise ValueError("Sessão do banco de dados é necessária para persistir")
    
    # Criar sistema de alocação
    sistema = SGDAlocacaoOtimizada(ano=ano, mes=mes)
    
    # Carregar docentes
    sistema.carregar_docentes(dados_docentes)
    
    # Processar alocação
    resultado = sistema.processar_alocacao()
    
    # Exportar CSV se solicitado
    if exportar_csv:
        arquivo_csv = sistema.exportar_csv(resultado, nome_arquivo_csv)
        resultado['arquivo_csv'] = arquivo_csv
    
    # Persistir no banco se solicitado
    if persistir_db:
        sucesso_db = sistema.persistir_banco_dados(resultado, db)
        resultado['persistido_db'] = sucesso_db
    
    return resultado


# Exemplo de uso
if __name__ == "__main__":
    # Dados de exemplo
    docentes_exemplo = [
        {'id': 'P1', 'mat': 48273, 'ch': 108, 'saldo': 108, 'rest': []},
        {'id': 'P2', 'mat': 19385, 'ch': 108, 'saldo': 108, 'rest': []},
        {'id': 'P3', 'mat': 60714, 'ch': 108, 'saldo': 108, 'rest': [3]},  # Não quinta
        {'id': 'P4', 'mat': 84529, 'ch': 72, 'saldo': 72, 'rest': []},
        {'id': 'P5', 'mat': 21947, 'ch': 72, 'saldo': 72, 'rest': []},
        {'id': 'P6', 'mat': 73018, 'ch': 72, 'saldo': 72, 'rest': []},
        {'id': 'P7', 'mat': 59136, 'ch': 36, 'saldo': 36, 'rest': []},
        {'id': 'P8', 'mat': 36402, 'ch': 36, 'saldo': 36, 'rest': []},
        {'id': 'P9', 'mat': 10675, 'ch': 36, 'saldo': 36, 'rest': []},
        {'id': 'P10', 'mat': 95821, 'ch': 36, 'saldo': 36, 'rest': []},
    ]
    
    # Executar alocação
    resultado = alocar_docentes_otimizado(
        dados_docentes=docentes_exemplo,
        ano=2025,
        mes=4,
        exportar_csv=True
    )
    
    # Exibir resultado
    print("=== SISTEMA DE GESTÃO DOCENTE - ALOCAÇÃO OTIMIZADA ===")
    print(f"Ano: {resultado['ano']}, Mês: {resultado['mes']}")
    print(f"Feriados detectados: {resultado['feriados_detectados']}")
    print(f"Taxa de alocação: {resultado['estatisticas']['taxa_alocacao']:.1f}%")
    print(f"Arquivo CSV gerado: {resultado.get('arquivo_csv', 'N/A')}")
    
    print("\nMatriz Agendada:")
    for i, linha in enumerate(resultado['matriz_agendada']):
        print(f"  {['Seg', 'Ter', 'Qua', 'Qui', 'Sex'][i]}: {linha}")
    
    print("\nMatriz Calendário (Transposta):")
    for i, linha in enumerate(resultado['matriz_calendario']):
        print(f"  {['19:00', '19:50', '20:50', '21:40'][i]}: {linha}") 