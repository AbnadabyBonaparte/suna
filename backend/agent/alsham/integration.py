"""
SUNA-ALSHAM Integration Module
Módulo principal de integração e orquestração dos agentes auto-evolutivos

Gerencia o ciclo de vida, comunicação e persistência dos agentes CORE, LEARN e GUARD.
Integrado com infraestrutura SUNA existente (Supabase, Redis, etc.).
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

# Importações Supabase (simuladas para este exemplo)
# Em um ambiente real, você usaria o cliente Supabase real
# from supabase import create_client, Client

# Configuração de logging básica
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SupabaseClientMock:
    """
    Mock de cliente Supabase para simular operações de banco de dados.
    Em um ambiente real, isso seria substituído pelo cliente Supabase real.
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

        def insert(self, data: Dict):
            self.db[self.table_name].append(data)
            logger.debug(f"MOCK Supabase: Inserido em {self.table_name}: {data.get('id', data.get('name'))}")
            return self

        def select(self, columns: str = "*"):
            return self

        def eq(self, column: str, value: Any):
            self.filter_column = column
            self.filter_value = value
            return self

        def execute(self):
            if hasattr(self, 'filter_column'):
                results = [item for item in self.db[self.table_name] if item.get(self.filter_column) == self.filter_value]
                del self.filter_column
                del self.filter_value
                return {'data': results, 'error': None}
            return {'data': self.db[self.table_name], 'error': None}

        def update(self, data: Dict):
            if hasattr(self, 'filter_column'):
                updated_count = 0
                for item in self.db[self.table_name]:
                    if item.get(self.filter_column) == self.filter_value:
                        item.update(data)
                        updated_count += 1
                del self.filter_column
                del self.filter_value
                logger.debug(f"MOCK Supabase: Atualizado {updated_count} registros em {self.table_name}")
                return self
            logger.warning("MOCK Supabase: Update sem filtro. Nenhuma ação realizada.")
            return self


class SUNAAlshamIntegration:
    """
    Classe principal para orquestrar a integração SUNA-ALSHAM.
    Gerencia o ciclo de vida, execução e persistência dos agentes.
    """

    def __init__(self, config_file: Optional[str] = None):
        self.config_loader = SUNAAlshamConfig(config_file)
        self.config: IntegrationConfig = self.config_loader.get_config()
        
        self.system_id = str(uuid.uuid4())
        self.is_running = False
        self.last_evolution_cycle_time: Optional[datetime] = None

        # Inicializar clientes Supabase
        supabase_url = os.getenv("SUPABASE_URL") or self.config.system_name # Fallback para nome do sistema se não houver URL
        supabase_key = os.getenv("SUPABASE_KEY") or self.config.version # Fallback para versão se não houver chave
        
        if not supabase_url or not supabase_key:
            logger.warning("⚠️ Variáveis SUPABASE_URL ou SUPABASE_KEY não configuradas. Usando MOCK Supabase.")
            self.supabase: SupabaseClientMock = SupabaseClientMock(supabase_url, supabase_key)
        else:
            # Em um ambiente real, descomente a linha abaixo e remova o mock
            # self.supabase: Client = create_client(supabase_url, supabase_key)
            self.supabase: SupabaseClientMock = SupabaseClientMock(supabase_url, supabase_key) # Mantendo mock para exemplo

        # Inicializar agentes e sistemas
        self.core_agent = CoreAgent(config=self.config.core_agent)
        self.learn_agent = LearnAgent(config=self.config.learn_agent)
        self.guard_agent = GuardAgent(config=self.config.guard_agent)
        self.metrics_system = MetricsSystem(config=self.config.metrics)
        self.validation_system = ValidationSystem(config=self.config.validation)

        logger.info(f"🚀 SUNA-ALSHAM Integration inicializada - ID: {self.system_id}")
        logger.info(f"Configuração carregada: {self.config.system_name} v{self.config.version}")
        logger.info(f"Intervalo de Evolução: {self.config.evolution_interval_minutes} minutos")

    def start(self):
        """Inicia o sistema de integração SUNA-ALSHAM."""
        if self.is_running:
            logger.info("SUNA-ALSHAM já está em execução.")
            return

        logger.info("Iniciando sistema SUNA-ALSHAM...")
        self.is_running = True
        self._load_agents_from_db()
        self._run_initial_checks()
        logger.info("SUNA-ALSHAM iniciado com sucesso.")

    def stop(self):
        """Para o sistema de integração SUNA-ALSHAM."""
        if not self.is_running:
            logger.info("SUNA-ALSHAM não está em execução.")
            return

        logger.info("Parando sistema SUNA-ALSHAM...")
        self.is_running = False
        logger.info("SUNA-ALSHAM parado.")

    def _load_agents_from_db(self):
        """Carrega o estado dos agentes do Supabase."""
        logger.info("Carregando estado dos agentes do Supabase...")
        try:
            response = self.supabase.from_("agents").select("*").execute()
            if response.get("error"):
                logger.error(f"Erro ao carregar agentes do DB: {response['error']}")
                return
            
            agents_data = response.get("data", [])
            for agent_data in agents_data:
                if agent_data["name"] == "CORE":
                    self.core_agent.load_state(agent_data)
                elif agent_data["name"] == "LEARN":
                    self.learn_agent.load_state(agent_data)
                elif agent_data["name"] == "GUARD":
                    self.guard_agent.load_state(agent_data)
            logger.info(f"Estado de {len(agents_data)} agentes carregado do Supabase.")
        except Exception as e:
            logger.error(f"Exceção ao carregar agentes do DB: {e}")

    def _save_agent_state(self, agent_name: str, state: Dict[str, Any]):
        """Salva o estado de um agente no Supabase."""
        try:
            # Tenta atualizar, se não existir, insere
            response = self.supabase.from_("agents").update(state).eq("name", agent_name).execute()
            if not response.get("data"):
                self.supabase.from_("agents").insert(state).execute()
            logger.debug(f"Estado do agente {agent_name} salvo no Supabase.")
        except Exception as e:
            logger.error(f"Erro ao salvar estado do agente {agent_name} no DB: {e}")

    def _run_initial_checks(self):
        """Executa verificações iniciais e garante o estado dos agentes."""
        logger.info("Executando verificações iniciais...")
        # Exemplo: garantir que os agentes estão registrados no DB
        self._save_agent_state(self.core_agent.name, self.core_agent.get_status())
        self._save_agent_state(self.learn_agent.name, self.learn_agent.get_status())
        self._save_agent_state(self.guard_agent.name, self.guard_agent.get_status())
        logger.info("Verificações iniciais concluídas.")

    def run_evolution_cycle(self) -> Dict[str, Any]:
        """
        Executa um ciclo completo de evolução para os agentes SUNA-ALSHAM.
        Este é o coração do sistema auto-evolutivo.
        """
        cycle_id = str(uuid.uuid4())
        start_time = datetime.utcnow()
        logger.info(f"🔄 Iniciando ciclo de evolução SUNA-ALSHAM: {cycle_id}")

        cycle_results = {
            "cycle_id": cycle_id,
            "timestamp": start_time.isoformat(),
            "core_evolution": None,
            "learn_collaboration": None,
            "guard_security": None,
            "metrics_analysis": None,
            "validation_results": [],
            "overall_success": False,
            "duration_seconds": 0
        }

        try:
            # 1. Executar ciclo do Agente GUARD (Segurança primeiro)
            logger.info("🛡️ Executando ciclo do Agente GUARD...")
            guard_result = self.guard_agent.run_security_cycle()
            cycle_results["guard_security"] = guard_result
            self._save_agent_state(self.guard_agent.name, self.guard_agent.get_status())
            self.metrics_system.collect_performance_metric(
                self.guard_agent.agent_id, "security_score", guard_result.get("security_score", 0.0)
            )
            if not guard_result.get("success"):
                logger.warning("Ciclo do Agente GUARD falhou ou detectou incidentes críticos. Abortando evolução.")
                cycle_results["overall_success"] = False
                return cycle_results # Aborta se a segurança não for garantida

            # 2. Executar ciclo do Agente CORE (Auto-evolução)
            logger.info("🧠 Executando ciclo do Agente CORE...")
            core_result = self.core_agent.run_evolution_cycle()
            cycle_results["core_evolution"] = core_result
            self._save_agent_state(self.core_agent.name, self.core_agent.get_status())
            self.metrics_system.collect_performance_metric(
                self.core_agent.agent_id, "performance_improvement", core_result.get("improvement_percentage", 0.0)
            )

            # 3. Validar melhoria do CORE
            if core_result.get("improvement_percentage", 0) > 0:
                logger.info("🔬 Validando melhoria do Agente CORE...")
                validation_data = {
                    "old_performance": core_result.get("initial_performance", 0),
                    "new_performance": core_result.get("final_performance", 0),
                    "improvement_percentage": core_result.get("improvement_percentage", 0),
                    "context": core_result.get("evolution_context", {})
                }
                validation_result = self.validation_system.validate_improvement(
                    self.core_agent.agent_id, validation_data
                )
                cycle_results["validation_results"].append(validation_result)
                
                if not validation_result.get("overall_passed"):
                    logger.warning("Melhoria do CORE não passou na validação científica. Revertendo ou ajustando.")
                    # Aqui você implementaria a lógica de reversão ou ajuste
                    # self.core_agent.revert_to_previous_state()
                    # self.metrics_system.collect_performance_metric(self.core_agent.agent_id, "reversion_event", 1)

            # 4. Executar ciclo do Agente LEARN (Colaboração)
            logger.info("🤝 Executando ciclo do Agente LEARN...")
            learn_result = self.learn_agent.run_collaboration_cycle(
                [self.core_agent.get_status(), self.guard_agent.get_status()]
            )
            cycle_results["learn_collaboration"] = learn_result
            self._save_agent_state(self.learn_agent.name, self.learn_agent.get_status())
            self.metrics_system.collect_performance_metric(
                self.learn_agent.agent_id, "collaboration_synergy", learn_result.get("synergy_score", 0.0)
            )

            # 5. Análise de Métricas do Sistema
            logger.info("📊 Analisando métricas do sistema...")
            metrics_analysis = self.metrics_system.analyze_system_health()
            cycle_results["metrics_analysis"] = metrics_analysis
            
            # Persistir métricas e resultados do ciclo
            self._persist_cycle_data(cycle_results)

            self.last_evolution_cycle_time = datetime.utcnow()
            cycle_results["overall_success"] = True
            logger.info(f"✅ Ciclo de evolução {cycle_id} concluído com sucesso.")

        except Exception as e:
            logger.error(f"❌ Erro crítico no ciclo de evolução {cycle_id}: {e}", exc_info=True)
            cycle_results["overall_success"] = False
            cycle_results["error"] = str(e)
        finally:
            end_time = datetime.utcnow()
            cycle_results["duration_seconds"] = (end_time - start_time).total_seconds()
            logger.info(f"Ciclo {cycle_id} finalizado em {cycle_results['duration_seconds']:.2f} segundos.")
            return cycle_results

    def _persist_cycle_data(self, cycle_data: Dict[str, Any]):
        """Persiste os resultados de um ciclo de evolução no Supabase."""
        try:
            self.supabase.from_("evolution_cycles").insert(cycle_data).execute()
            logger.debug(f"Dados do ciclo {cycle_data['cycle_id']} persistidos.")

            # Persistir métricas individuais (simplificado)
            metrics_to_save = [
                {
                    "agent_id": self.core_agent.agent_id,
                    "metric_name": "core_performance",
                    "value": cycle_data["core_evolution"].get("final_performance", 0) if cycle_data["core_evolution"] else 0,
                    "timestamp": cycle_data["timestamp"]
                },
                {
                    "agent_id": self.learn_agent.agent_id,
                    "metric_name": "learn_synergy",
                    "value": cycle_data["learn_collaboration"].get("synergy_score", 0) if cycle_data["learn_collaboration"] else 0,
                    "timestamp": cycle_data["timestamp"]
                },
                {
                    "agent_id": self.guard_agent.agent_id,
                    "metric_name": "guard_security_score",
                    "value": cycle_data["guard_security"].get("security_score", 0) if cycle_data["guard_security"] else 0,
                    "timestamp": cycle_data["timestamp"]
                }
            ]
            for metric in metrics_to_save:
                self.supabase.from_("system_metrics").insert(metric).execute()

        except Exception as e:
            logger.error(f"Erro ao persistir dados do ciclo no DB: {e}")

    def get_system_status(self) -> Dict[str, Any]:
        """Retorna o status atual do sistema de integração."""
        return {
            "system_id": self.system_id,
            "is_running": self.is_running,
            "last_evolution_cycle": self.last_evolution_cycle_time.isoformat() if self.last_evolution_cycle_time else "N/A",
            "config": self.config.system_name,
            "core_agent_status": self.core_agent.get_status(),
            "learn_agent_status": self.learn_agent.get_status(),
            "guard_agent_status": self.guard_agent.get_status(),
            "metrics_system_stats": self.metrics_system.get_system_health(), # Usar método existente
            "validation_system_stats": self.validation_system.get_validation_statistics()
        }

# Função de teste
def test_suna_alsham_integration():
    """Teste básico do sistema de integração SUNA-ALSHAM."""
    print("🎯 Testando Integração SUNA-ALSHAM...")
    
    # Configurar variáveis de ambiente para o mock Supabase
    os.environ["SUPABASE_URL"] = "http://mock.supabase.com"
    os.environ["SUPABASE_KEY"] = "mock_key"
    os.environ["SUNA_ALSHAM_AUTO_START"] = "true"
    os.environ["SUNA_ALSHAM_EVOLUTION_INTERVAL"] = "1"

    integration = SUNAAlshamIntegration( )
    integration.start()
    
    # Executar um ciclo de evolução
    print("\n--- Executando Ciclo de Evolução ---")
    cycle_result = integration.run_evolution_cycle()
    print(f"Resultado do Ciclo: {cycle_result.get('overall_success')}")
    
    # Verificar status do sistema
    print("\n--- Status do Sistema ---")
    status = integration.get_system_status()
    print(json.dumps(status, indent=2))
    
    integration.stop()
    print("\n✅ Teste de Integração SUNA-ALSHAM concluído!")

if __name__ == "__main__":
    test_suna_alsham_integration()
