"""
SUNA-ALSHAM Integration System
Sistema principal de integração dos agentes auto-evolutivos com SUNA

Orquestra todos os componentes SUNA-ALSHAM e integra com infraestrutura SUNA
"""

import uuid
import json
import time
import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import logging

# Importações SUNA-ALSHAM
from .core_agent import CoreAgent
from .learn_agent import LearnAgent
from .guard_agent import GuardAgent
from .metrics_system import MetricsSystem
from .validation_system import ValidationSystem

# Importações SUNA existentes
try:
    from ...services.supabase import DBConnection
    from ...utils.logger import get_logger
    from ...services import redis
    from .config import get_config
except ImportError:
    # Fallback para desenvolvimento
    logging.basicConfig(level=logging.INFO)
    get_logger = lambda name: logging.getLogger(name)
    
    # Mock para desenvolvimento
    class redis:
        @staticmethod
        async def set(*args, **kwargs): pass
        @staticmethod
        async def get(*args, **kwargs): return None
    
    class DBConnection:
        def __init__(self): pass
    
    def get_config():
        return {}

class SUNAAlshamIntegration:
    """
    Sistema principal de integração SUNA-ALSHAM
    
    Funcionalidades:
    - Orquestração de todos os agentes auto-evolutivos
    - Integração com sistema SUNA existente
    - Coordenação de ciclos de evolução
    - Monitoramento e validação centralizados
    """
    
    def __init__(self, config: Optional[Dict] = None):
        self.integration_id = str(uuid.uuid4())
        self.config = {**get_config(), **(config or {})}
        
        # Configurações do sistema
        self.evolution_interval_minutes = self.config.get('evolution_interval_minutes', 60)
        self.max_concurrent_evolutions = self.config.get('max_concurrent_evolutions', 3)
        self.auto_start = self.config.get('auto_start', True)
        
        # Estado do sistema
        self.is_running = False
        self.agents = {}
        self.evolution_cycles = []
        self.system_metrics = {}
        
        # Componentes do sistema
        self.metrics_system = MetricsSystem(self.config.get('metrics', {}))
        self.validation_system = ValidationSystem(self.config.get('validation', {}))
        
        # Logger SUNA
        self.logger = get_logger("SUNA-ALSHAM-INTEGRATION")
        
        # Integração SUNA
        self.db_connection = None
        
        self.logger.info(f"🚀 Sistema SUNA-ALSHAM inicializado - ID: {self.integration_id}")
    
    async def initialize_suna_integration(self):
        """Inicializa integração com infraestrutura SUNA"""
        try:
            self.db_connection = DBConnection()
            
            # Registrar sistema no SUNA
            await self._register_system_in_suna()
            
            # Inicializar agentes
            await self._initialize_agents()
            
            self.logger.info("✅ Integração SUNA inicializada com sucesso")
        except Exception as e:
            self.logger.warning(f"⚠️ Integração SUNA parcial: {e}")
    
    async def _register_system_in_suna(self):
        """Registra sistema SUNA-ALSHAM no SUNA principal"""
        try:
            if not self.db_connection:
                return
            
            # Registrar no Redis para controle de estado
            await redis.set(
                f"suna_alsham:system:{self.integration_id}",
                json.dumps({
                    "status": "active",
                    "started_at": datetime.utcnow().isoformat(),
                    "config": self.config
                }),
                ex=3600  # 1 hora de TTL
            )
            
            self.logger.info(f"✅ Sistema SUNA-ALSHAM registrado: {self.integration_id}")
                    
        except Exception as e:
            self.logger.error(f"❌ Erro ao registrar sistema no SUNA: {e}")
    
    async def _initialize_agents(self):
        """Inicializa todos os agentes SUNA-ALSHAM"""
        try:
            # Inicializar agente CORE
            core_agent = CoreAgent(config=self.config.get('core_agent', {}))
            await core_agent.initialize_suna_integration()
            self.agents['core'] = core_agent
            
            # Inicializar agente LEARN
            learn_agent = LearnAgent(config=self.config.get('learn_agent', {}))
            self.agents['learn'] = learn_agent
            
            # Inicializar agente GUARD
            guard_agent = GuardAgent(config=self.config.get('guard_agent', {}))
            self.agents['guard'] = guard_agent
            
            self.logger.info(f"✅ {len(self.agents)} agentes SUNA-ALSHAM inicializados")
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao inicializar agentes: {e}")
    
    async def start_system(self):
        """Inicia o sistema SUNA-ALSHAM"""
        if self.is_running:
            self.logger.warning("⚠️ Sistema já está em execução")
            return
        
        try:
            self.is_running = True
            
            # Inicializar integração se necessário
            if not self.db_connection:
                await self.initialize_suna_integration()
            
            # Iniciar ciclo de evolução se configurado
            if self.auto_start:
                asyncio.create_task(self._evolution_cycle_loop())
            
            self.logger.info("🚀 Sistema SUNA-ALSHAM iniciado com sucesso")
            
        except Exception as e:
            self.is_running = False
            self.logger.error(f"❌ Erro ao iniciar sistema: {e}")
            raise
    
    async def stop_system(self):
        """Para o sistema SUNA-ALSHAM"""
        try:
            self.is_running = False
            
            # Limpar estado no Redis
            await redis.set(
                f"suna_alsham:system:{self.integration_id}",
                json.dumps({
                    "status": "stopped",
                    "stopped_at": datetime.utcnow().isoformat()
                }),
                ex=300  # 5 minutos de TTL
            )
            
            self.logger.info("🛑 Sistema SUNA-ALSHAM parado")
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao parar sistema: {e}")
    
    async def _evolution_cycle_loop(self):
        """Loop principal de ciclos de evolução"""
        while self.is_running:
            try:
                await self._run_evolution_cycle()
                await asyncio.sleep(self.evolution_interval_minutes * 60)
            except Exception as e:
                self.logger.error(f"❌ Erro no ciclo de evolução: {e}")
                await asyncio.sleep(60)  # Aguardar 1 minuto antes de tentar novamente
    
    async def _run_evolution_cycle(self):
        """Executa um ciclo completo de evolução"""
        cycle_id = str(uuid.uuid4())
        cycle_start = datetime.utcnow()
        
        self.logger.info(f"🔄 Iniciando ciclo de evolução: {cycle_id}")
        
        try:
            # 1. Coletar métricas de todos os agentes
            metrics = await self._collect_system_metrics()
            
            # 2. Executar evolução dos agentes (limitado por max_concurrent_evolutions)
            evolution_tasks = []
            for agent_name, agent in list(self.agents.items())[:self.max_concurrent_evolutions]:
                if hasattr(agent, 'run_evolution_cycle'):
                    task = asyncio.create_task(agent.run_evolution_cycle())
                elif hasattr(agent, 'run_collaboration_cycle'):
                    task = asyncio.create_task(agent.run_collaboration_cycle())
                elif hasattr(agent, 'run_security_cycle'):
                    task = asyncio.create_task(agent.run_security_cycle())
                else:
                    continue
                evolution_tasks.append((agent_name, task))
            
            # 3. Aguardar conclusão das evoluções
            evolution_results = {}
            for agent_name, task in evolution_tasks:
                try:
                    result = await task
                    evolution_results[agent_name] = result
                except Exception as e:
                    self.logger.error(f"❌ Erro na evolução do agente {agent_name}: {e}")
                    evolution_results[agent_name] = {"error": str(e)}
            
            # 4. Validar melhorias
            validation_results = await self._validate_evolution_results(evolution_results)
            
            # 5. Registrar ciclo
            cycle_data = {
                "cycle_id": cycle_id,
                "started_at": cycle_start.isoformat(),
                "completed_at": datetime.utcnow().isoformat(),
                "metrics": metrics,
                "evolution_results": evolution_results,
                "validation_results": validation_results
            }
            
            self.evolution_cycles.append(cycle_data)
            
            # Manter apenas os últimos 100 ciclos
            if len(self.evolution_cycles) > 100:
                self.evolution_cycles = self.evolution_cycles[-100:]
            
            self.logger.info(f"✅ Ciclo de evolução concluído: {cycle_id}")
            
        except Exception as e:
            self.logger.error(f"❌ Erro no ciclo de evolução {cycle_id}: {e}")
    
    async def _collect_system_metrics(self) -> Dict[str, Any]:
        """Coleta métricas de todo o sistema"""
        try:
            system_metrics = {}
            
            for agent_name, agent in self.agents.items():
                try:
                    if hasattr(agent, 'get_status'):
                        agent_metrics = agent.get_status()
                    else:
                        agent_metrics = {"status": "unknown"}
                    system_metrics[agent_name] = agent_metrics
                except Exception as e:
                    self.logger.warning(f"⚠️ Erro ao coletar métricas do agente {agent_name}: {e}")
                    system_metrics[agent_name] = {"error": str(e)}
            
            # Métricas do sistema
            system_metrics["system"] = {
                "total_agents": len(self.agents),
                "running_agents": sum(1 for agent in self.agents.values() if getattr(agent, 'status', None) == "active"),
                "total_cycles": len(self.evolution_cycles),
                "uptime_minutes": (datetime.utcnow() - datetime.fromisoformat(
                    self.evolution_cycles[0]["started_at"] if self.evolution_cycles else datetime.utcnow().isoformat()
                )).total_seconds() / 60
            }
            
            return system_metrics
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao coletar métricas do sistema: {e}")
            return {}
    
    async def _validate_evolution_results(self, evolution_results: Dict[str, Any]) -> Dict[str, Any]:
        """Valida os resultados das evoluções"""
        try:
            validation_results = {}
            
            for agent_name, result in evolution_results.items():
                if "error" not in result and result.get("success"):
                    # Extrair dados de melhoria do resultado
                    improvement_data = {
                        "old_performance": result.get("old_performance", 0.0),
                        "new_performance": result.get("new_performance", 0.0),
                        "improvement_percentage": result.get("improvement_percentage", 0.0),
                        "timestamp": result.get("timestamp", datetime.utcnow().isoformat())
                    }
                    
                    validation = self.validation_system.validate_improvement(
                        self.agents[agent_name].agent_id, improvement_data
                    )
                    validation_results[agent_name] = validation
                else:
                    validation_results[agent_name] = {"overall_passed": False, "reason": "evolution_error"}
            
            return validation_results
            
        except Exception as e:
            self.logger.error(f"❌ Erro na validação dos resultados: {e}")
            return {}
    
    async def get_system_status(self) -> Dict[str, Any]:
        """Retorna status completo do sistema"""
        try:
            status = {
                "integration_id": self.integration_id,
                "is_running": self.is_running,
                "agents": {
                    name: {
                        "agent_id": getattr(agent, 'agent_id', 'unknown'),
                        "status": getattr(agent, 'status', 'unknown'),
                        "current_performance": getattr(agent, 'current_performance', 0.0)
                    }
                    for name, agent in self.agents.items()
                },
                "total_evolution_cycles": len(self.evolution_cycles),
                "last_cycle": self.evolution_cycles[-1] if self.evolution_cycles else None,
                "system_metrics": await self._collect_system_metrics()
            }
            
            return status
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao obter status do sistema: {e}")
            return {"error": str(e)}
    
    async def trigger_manual_evolution(self, agent_name: Optional[str] = None) -> Dict[str, Any]:
        """Dispara evolução manual de um agente específico ou todos"""
        try:
            if agent_name:
                if agent_name not in self.agents:
                    raise ValueError(f"Agente '{agent_name}' não encontrado")
                
                agent = self.agents[agent_name]
                
                # Executar ciclo apropriado baseado no tipo do agente
                if hasattr(agent, 'run_evolution_cycle'):
                    result = await agent.run_evolution_cycle()
                elif hasattr(agent, 'run_collaboration_cycle'):
                    result = agent.run_collaboration_cycle()
                elif hasattr(agent, 'run_security_cycle'):
                    result = agent.run_security_cycle()
                else:
                    result = {"error": "Método de evolução não encontrado"}
                
                if "error" not in result and result.get("success"):
                    improvement_data = {
                        "old_performance": result.get("old_performance", 0.0),
                        "new_performance": result.get("new_performance", 0.0),
                        "improvement_percentage": result.get("improvement_percentage", 0.0),
                        "timestamp": result.get("timestamp", datetime.utcnow().isoformat())
                    }
                    validation = self.validation_system.validate_improvement(agent.agent_id, improvement_data)
                else:
                    validation = {"overall_passed": False, "reason": "evolution_error"}
                
                return {
                    "agent": agent_name,
                    "evolution_result": result,
                    "validation": validation
                }
            else:
                # Evoluir todos os agentes
                results = {}
                for name, agent in self.agents.items():
                    try:
                        if hasattr(agent, 'run_evolution_cycle'):
                            result = await agent.run_evolution_cycle()
                        elif hasattr(agent, 'run_collaboration_cycle'):
                            result = agent.run_collaboration_cycle()
                        elif hasattr(agent, 'run_security_cycle'):
                            result = agent.run_security_cycle()
                        else:
                            result = {"error": "Método de evolução não encontrado"}
                        
                        if "error" not in result and result.get("success"):
                            improvement_data = {
                                "old_performance": result.get("old_performance", 0.0),
                                "new_performance": result.get("new_performance", 0.0),
                                "improvement_percentage": result.get("improvement_percentage", 0.0),
                                "timestamp": result.get("timestamp", datetime.utcnow().isoformat())
                            }
                            validation = self.validation_system.validate_improvement(agent.agent_id, improvement_data)
                        else:
                            validation = {"overall_passed": False, "reason": "evolution_error"}
                        
                        results[name] = {
                            "evolution_result": result,
                            "validation": validation
                        }
                    except Exception as e:
                        results[name] = {"error": str(e)}
                
                return results
                
        except Exception as e:
            self.logger.error(f"❌ Erro na evolução manual: {e}")
            return {"error": str(e)}

# Instância global do sistema SUNA-ALSHAM
suna_alsham_system = None

async def initialize_suna_alsham():
    """Inicializa o sistema SUNA-ALSHAM globalmente"""
    global suna_alsham_system
    
    if suna_alsham_system is None:
        suna_alsham_system = SUNAAlshamIntegration()
        await suna_alsham_system.initialize_suna_integration()
        
        # Auto-start se configurado
        if suna_alsham_system.auto_start:
            await suna_alsham_system.start_system()
    
    return suna_alsham_system

async def get_suna_alsham_system():
    """Retorna instância do sistema SUNA-ALSHAM"""
    global suna_alsham_system
    
    if suna_alsham_system is None:
        return await initialize_suna_alsham()
    
    return suna_alsham_system

# Função de teste para desenvolvimento
async def test_suna_alsham_integration():
    """Teste básico do sistema de integração"""
    print("🎯 Testando Sistema de Integração SUNA-ALSHAM...")
    
    integration = SUNAAlshamIntegration()
    await integration.initialize_suna_integration()
    
    print(f"🚀 Sistema criado - ID: {integration.integration_id}")
    print(f"🤖 Agentes inicializados: {len(integration.agents)}")
    
    # Obter status
    status = await integration.get_system_status()
    print(f"📊 Status: {status.get('is_running', False)}")
    
    print("🎉 Teste do Sistema de Integração concluído!")

if __name__ == "__main__":
    asyncio.run(test_suna_alsham_integration())
