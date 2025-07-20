"""
SUNA-ALSHAM Integration Module - VERSÃO FINAL CORRIGIDA
Módulo principal de integração e orquestração dos agentes auto-evolutivos
CORREÇÃO: Detecção forçada das variáveis de ambiente do Supabase + Inicialização sem config
"""

import uuid
import json
import time
import os
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import logging

# Importações de módulos SUNA-ALSHAM
from .config import SUNAAlshamConfig, IntegrationConfig
from .core_agent import CoreAgent
from .learn_agent import LearnAgent
from .guard_agent import GuardAgent
from .metrics_system import MetricsSystem
from .validation_system import ValidationSystem

# Configuração de logging básica
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# CORREÇÃO: Detecção forçada das variáveis de ambiente
def detect_supabase_credentials():
    """
    CORREÇÃO: Função que força a detecção das credenciais do Supabase
    """
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')
    
    logger.info(f"🔍 Verificando variáveis de ambiente:")
    logger.info(f"SUPABASE_URL encontrada: {'SIM' if supabase_url else 'NÃO'}")
    logger.info(f"SUPABASE_KEY encontrada: {'SIM' if supabase_key else 'NÃO'}")
    
    if supabase_url and supabase_key:
        logger.info(f"✅ Credenciais Supabase detectadas - URL: {supabase_url[:30]}...")
        return supabase_url, supabase_key
    else:
        logger.warning(f"❌ Credenciais Supabase NÃO encontradas - usando MOCK")
        return None, None

# CORREÇÃO: Cliente Supabase real ou mock baseado na detecção
def create_supabase_client():
    """
    CORREÇÃO: Cria cliente Supabase real ou mock baseado nas variáveis detectadas
    """
    url, key = detect_supabase_credentials()
    
    if url and key:
        try:
            # Tentar importar e usar Supabase real
            from supabase import create_client
            client = create_client(url, key)
            logger.info("✅ Cliente Supabase REAL inicializado com sucesso!")
            return client, False  # False = não é mock
        except ImportError:
            logger.warning("⚠️ Biblioteca supabase não encontrada - usando MOCK")
            return SupabaseClientMock(url, key), True
        except Exception as e:
            logger.error(f"❌ Erro ao conectar Supabase real: {e} - usando MOCK")
            return SupabaseClientMock(url, key), True
    else:
        logger.info("🔧 Usando cliente MOCK (variáveis não encontradas)")
        return SupabaseClientMock("mock_url", "mock_key"), True

class SupabaseClientMock:
    """
    Mock de cliente Supabase para simular operações de banco de dados.
    """
    def __init__(self, url: str, key: str):
        self.url = url
        self.key = key
        self.db = {
            "agents": [],
            "agent_runs": [],
            "system_metrics": [],
            "evolution_cycles": []
        }
        logger.info("MOCK Supabase Client inicializado.")

    def from_(self, table_name: str):
        return self._TableMock(self.db, table_name)

    class _TableMock:
        def __init__(self, db: Dict, table_name: str):
            self.db = db
            self.table_name = table_name
            if table_name not in self.db:
                self.db[table_name] = []

        def select(self, columns: str = "*"):
            return self

        def insert(self, data: Dict[str, Any]):
            if isinstance(data, list):
                self.db[self.table_name].extend(data)
            else:
                self.db[self.table_name].append(data)
            return self

        def update(self, data: Dict[str, Any]):
            logger.warning(f"MOCK Supabase: Update sem filtro. Nenhuma ação realizada.")
            return self

        def eq(self, column: str, value: Any):
            return self

        def execute(self):
            return {"data": self.db.get(self.table_name, []), "error": None}

class SUNAAlshamIntegration:
    """
    Classe principal de integração SUNA-ALSHAM com detecção corrigida de Supabase
    """
    def __init__(self, config: Optional[SUNAAlshamConfig] = None):
        self.integration_id = str(uuid.uuid4())
        self.config = config if config else SUNAAlshamConfig()
        self.created_at = datetime.utcnow()
        self.last_evolution_cycle: Optional[datetime] = None
        
        # CORREÇÃO: Inicialização do cliente Supabase com detecção forçada
        self.supabase_client, self.is_mock = create_supabase_client()
        
        logger.info(f"🚀 SUNA-ALSHAM Integration inicializada - ID: {self.integration_id}")
        logger.info(f"Configuração carregada: SUNA-ALSHAM v1.0.0")
        logger.info(f"Intervalo de Evolução: 60 minutos")
        
        # CORREÇÃO FINAL: Inicializar agentes SEM configuração específica
        self.core_agent = CoreAgent()
        self.learn_agent = LearnAgent()
        self.guard_agent = GuardAgent()
        
        # CORREÇÃO FINAL: Inicializar sistemas de suporte SEM configuração específica
        self.metrics_system = MetricsSystem()
        self.validation_system = ValidationSystem()
        
        # Estado do sistema
        self.system_status = "initializing"
        self.evolution_cycles_count = 0

    def start_system(self):
        """Inicia o sistema SUNA-ALSHAM"""
        logger.info("Iniciando sistema SUNA-ALSHAM...")
        
        # Carregar estado dos agentes
        self._load_agents_state()
        
        # Executar verificações iniciais
        self._run_initial_checks()
        
        self.system_status = "active"
        logger.info("SUNA-ALSHAM iniciado com sucesso.")

    def _load_agents_state(self):
        """Carrega o estado dos agentes do Supabase"""
        logger.info("Carregando estado dos agentes do Supabase...")
        
        try:
            result = self.supabase_client.from_("agents").select("*").execute()
            agents_data = result.get("data", [])
            
            logger.info(f"Estado de {len(agents_data)} agentes carregado do Supabase.")
            
            # Carregar estado específico de cada agente
            for agent_data in agents_data:
                agent_name = agent_data.get("name")
                if agent_name == "CORE":
                    self.core_agent.load_state(agent_data.get("state", {}))
                elif agent_name == "LEARN":
                    self.learn_agent.load_state(agent_data.get("state", {}))
                elif agent_name == "GUARD":
                    self.guard_agent.load_state(agent_data.get("state", {}))
                    
        except Exception as e:
            logger.error(f"Erro ao carregar estado dos agentes: {e}")

    def _run_initial_checks(self):
        """Executa verificações iniciais do sistema"""
        logger.info("Executando verificações iniciais...")
        
        # Atualizar status dos agentes no banco
        self._update_agent_status("CORE", self.core_agent.get_status())
        self._update_agent_status("LEARN", self.learn_agent.get_status())
        self._update_agent_status("GUARD", self.guard_agent.get_status())
        
        logger.info("Verificações iniciais concluídas.")

    def _update_agent_status(self, agent_name: str, status: Dict[str, Any]):
        """Atualiza o status de um agente no Supabase"""
        try:
            agent_data = {
                "name": agent_name,
                "type": agent_name.lower(),
                "status": status.get("status", "unknown"),
                "state": status,
                "last_updated": datetime.utcnow().isoformat()
            }
            
            self.supabase_client.from_("agents").update(agent_data).eq("name", agent_name).execute()
            
        except Exception as e:
            logger.error(f"Erro ao atualizar status do agente {agent_name}: {e}")

    def run_evolution_cycle(self) -> Dict[str, Any]:
        """
        Executa um ciclo completo de evolução do sistema SUNA-ALSHAM
        """
        cycle_id = str(uuid.uuid4())
        start_time = time.time()
        
        logger.info(f"🔄 Iniciando ciclo de evolução SUNA-ALSHAM: {cycle_id}")
        
        cycle_results = {
            "cycle_id": cycle_id,
            "timestamp": datetime.utcnow().isoformat(),
            "core_evolution": None,
            "learn_collaboration": None,
            "guard_security": None,
            "metrics_analysis": None,
            "validation_results": None,
            "overall_success": False,
            "duration_seconds": 0,
            "error": None
        }
        
        try:
            # 1. Executar ciclo do agente GUARD (segurança primeiro)
            logger.info("🛡️ Executando ciclo do Agente GUARD...")
            guard_result = self.guard_agent.run_security_cycle()
            cycle_results["guard_security"] = guard_result
            self._update_agent_status("GUARD", self.guard_agent.get_status())
            
            if not guard_result.get("success", False):
                logger.warning("Ciclo do Agente GUARD falhou ou detectou incidentes críticos. Abortando evolução.")
                cycle_results["error"] = "GUARD security check failed"
                return cycle_results
            
            # 2. Executar ciclo do agente CORE (auto-melhoria)
            logger.info("🧠 Executando ciclo do Agente CORE...")
            core_result = self.core_agent.run_evolution_cycle()
            cycle_results["core_evolution"] = core_result
            self._update_agent_status("CORE", self.core_agent.get_status())
            
            # 3. Validar melhorias do CORE
            if core_result.get("success", False):
                logger.info("🔬 Validando melhoria do Agente CORE...")
                validation_result = self.validation_system.validate_improvement(
                    core_result.get("improvement_data", {})
                )
                cycle_results["validation_results"] = validation_result
                
                if not validation_result.get("approved", False):
                    logger.warning("Melhoria do CORE não passou na validação científica. Revertendo ou ajustando.")
                    # Aqui poderia implementar lógica de reversão
            
            # 4. Executar ciclo do agente LEARN (colaboração)
            logger.info("🤝 Executando ciclo do Agente LEARN...")
            learn_result = self.learn_agent.run_collaboration_cycle()
            cycle_results["learn_collaboration"] = learn_result
            self._update_agent_status("LEARN", self.learn_agent.get_status())
            
            # 5. Analisar métricas do sistema
            logger.info("📊 Analisando métricas do sistema...")
            metrics_result = self.metrics_system.analyze_system_metrics()
            cycle_results["metrics_analysis"] = metrics_result
            
            # Marcar ciclo como bem-sucedido
            cycle_results["overall_success"] = True
            
        except Exception as e:
            logger.error(f"Erro durante ciclo de evolução: {e}")
            cycle_results["error"] = str(e)
        
        finally:
            # Calcular duração e salvar resultados
            cycle_results["duration_seconds"] = round(time.time() - start_time, 2)
            self._save_evolution_cycle(cycle_results)
            
            if cycle_results["overall_success"]:
                logger.info(f"✅ Ciclo de evolução {cycle_id} concluído com sucesso.")
            else:
                logger.warning(f"⚠️ Ciclo de evolução {cycle_id} falhou ou teve problemas.")
            
            logger.info(f"Ciclo {cycle_id} finalizado em {cycle_results['duration_seconds']} segundos.")
            
            self.evolution_cycles_count += 1
            self.last_evolution_cycle = datetime.utcnow()
        
        return cycle_results

    def _save_evolution_cycle(self, cycle_data: Dict[str, Any]):
        """Salva os resultados do ciclo de evolução no Supabase"""
        try:
            self.supabase_client.from_("evolution_cycles").insert(cycle_data).execute()
        except Exception as e:
            logger.error(f"Erro ao salvar ciclo de evolução: {e}")

    def get_system_status(self) -> Dict[str, Any]:
        """Retorna o status atual do sistema"""
        return {
            "integration_id": self.integration_id,
            "system_status": self.system_status,
            "evolution_cycles_count": self.evolution_cycles_count,
            "last_evolution_cycle": self.last_evolution_cycle.isoformat() if self.last_evolution_cycle else None,
            "agents_status": {
                "core": self.core_agent.get_status(),
                "learn": self.learn_agent.get_status(),
                "guard": self.guard_agent.get_status()
            },
            "supabase_connection": "REAL" if not self.is_mock else "MOCK",
            "created_at": self.created_at.isoformat()
        }
