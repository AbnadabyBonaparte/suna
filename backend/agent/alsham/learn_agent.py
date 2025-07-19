"""
SUNA-ALSHAM Learn Agent
Agente colaborativo especializado em aprendizado e sinergia entre agentes

Integrado com infraestrutura SUNA existente
"""

import uuid
import json
import time
from datetime import datetime
from typing import Dict, Any, Optional, List
import logging

# Importações SUNA existentes
try:
    from ..api import AgentAPI
    from ...supabase import get_supabase_client
    from ...utils.logger import get_logger
except ImportError:
    # Fallback para desenvolvimento
    logging.basicConfig(level=logging.INFO)
    get_logger = lambda name: logging.getLogger(name)

class LearnAgent:
    """
    Agente LEARN colaborativo integrado ao sistema SUNA
    
    Capacidades:
    - Aprendizado colaborativo entre agentes
    - Análise de sinergia e interações
    - Otimização de workflows colaborativos
    - Integração com sistema SUNA
    """
    
    def __init__(self, agent_id: Optional[str] = None, config: Optional[Dict] = None):
        self.agent_id = agent_id or str(uuid.uuid4())
        self.name = "LEARN"
        self.type = "collaborative"
        self.status = "active"
        self.wave_number = 1
        self.month_introduced = 3
        
        # Configurações
        self.config = config or {}
        self.min_collaboration_synergy = self.config.get('min_collaboration_synergy', 30.0)
        self.max_learning_sessions = self.config.get('max_learning_sessions', 5)
        
        # Métricas de colaboração
        self.collaboration_score = 0.0
        self.learning_sessions = []
        self.agent_interactions = []
        self.synergy_metrics = {}
        
        self.capabilities = {
            "collaboration": {
                "multi_agent_coordination": True,
                "knowledge_sharing": True,
                "workflow_optimization": True
            },
            "learning": {
                "pattern_recognition": True,
                "adaptive_strategies": True,
                "performance_correlation": True
            }
        }
        
        # Logger
        self.logger = get_logger(f"SUNA-ALSHAM-{self.name}")
        
        # Integração SUNA
        self.supabase_client = None
        self.agent_api = None
        self._initialize_suna_integration()
        
        self.logger.info(f"🤖 Agente {self.name} inicializado - ID: {self.agent_id}")
    
    def _initialize_suna_integration(self):
        """Inicializa integração com infraestrutura SUNA"""
        try:
            # Conectar com Supabase SUNA
            self.supabase_client = get_supabase_client()
            
            # Conectar com API SUNA
            self.agent_api = AgentAPI()
            
            # Registrar agente no sistema SUNA
            self._register_in_suna_system()
            
            self.logger.info("✅ Integração SUNA inicializada com sucesso")
        except Exception as e:
            self.logger.warning(f"⚠️ Integração SUNA parcial: {e}")
    
    def _register_in_suna_system(self):
        """Registra agente no sistema SUNA existente"""
        try:
            agent_data = {
                "id": self.agent_id,
                "name": self.name,
                "type": self.type,
                "status": self.status,
                "wave_number": self.wave_number,
                "month_introduced": self.month_introduced,
                "capabilities": json.dumps(self.capabilities),
                "created_at": datetime.utcnow().isoformat(),
                "metadata": json.dumps({
                    "system": "SUNA-ALSHAM",
                    "version": "1.0.0",
                    "collaborative": True
                })
            }
            
            if self.supabase_client:
                # Verificar se agente já existe
                existing = self.supabase_client.table('agents').select("*").eq('id', self.agent_id).execute()
                
                if not existing.data:
                    # Criar novo agente
                    result = self.supabase_client.table('agents').insert(agent_data).execute()
                    self.logger.info(f"✅ Agente registrado no SUNA: {result.data}")
                else:
                    self.logger.info("✅ Agente já existe no sistema SUNA")
                    
        except Exception as e:
            self.logger.error(f"❌ Erro ao registrar no SUNA: {e}")
    
    def discover_agents(self) -> List[Dict[str, Any]]:
        """
        Descobre outros agentes no sistema SUNA para colaboração
        """
        self.logger.info("🔍 Descobrindo agentes para colaboração...")
        
        try:
            if not self.supabase_client:
                self.logger.warning("⚠️ Cliente Supabase não disponível")
                return []
            
            # Buscar agentes ativos no sistema
            result = self.supabase_client.table('agents').select("*").eq('status', 'active').execute()
            
            available_agents = []
            for agent_data in result.data:
                if agent_data['id'] != self.agent_id:  # Excluir a si mesmo
                    available_agents.append({
                        "id": agent_data['id'],
                        "name": agent_data['name'],
                        "type": agent_data['type'],
                        "capabilities": json.loads(agent_data.get('capabilities', '{}')),
                        "wave_number": agent_data.get('wave_number', 1),
                        "month_introduced": agent_data.get('month_introduced', 1)
                    })
            
            self.logger.info(f"🤖 Encontrados {len(available_agents)} agentes para colaboração")
            return available_agents
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao descobrir agentes: {e}")
            return []
    
    def analyze_collaboration_potential(self, target_agent: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analisa potencial de colaboração com outro agente
        """
        self.logger.info(f"🔍 Analisando potencial de colaboração com {target_agent['name']}...")
        
        # Análise de compatibilidade de capacidades
        my_capabilities = set(self.capabilities.keys())
        target_capabilities = set(target_agent.get('capabilities', {}).keys())
        
        # Calcular sinergia baseada em complementaridade
        common_capabilities = my_capabilities.intersection(target_capabilities)
        unique_capabilities = my_capabilities.symmetric_difference(target_capabilities)
        
        # Métricas de sinergia
        compatibility_score = len(common_capabilities) / max(len(my_capabilities), 1) * 100
        complementarity_score = len(unique_capabilities) / max(len(my_capabilities.union(target_capabilities)), 1) * 100
        
        # Análise temporal (agentes da mesma onda colaboram melhor)
        temporal_alignment = 100 if target_agent.get('wave_number') == self.wave_number else 50
        
        # Score final de colaboração
        collaboration_potential = (compatibility_score * 0.4 + 
                                 complementarity_score * 0.4 + 
                                 temporal_alignment * 0.2)
        
        analysis = {
            "target_agent_id": target_agent['id'],
            "target_agent_name": target_agent['name'],
            "compatibility_score": compatibility_score,
            "complementarity_score": complementarity_score,
            "temporal_alignment": temporal_alignment,
            "collaboration_potential": collaboration_potential,
            "common_capabilities": list(common_capabilities),
            "unique_capabilities": list(unique_capabilities),
            "recommended": collaboration_potential >= self.min_collaboration_synergy
        }
        
        self.logger.info(f"📊 Potencial de colaboração: {collaboration_potential:.1f}%")
        return analysis
    
    def initiate_learning_session(self, target_agents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Inicia sessão de aprendizado colaborativo
        """
        self.logger.info(f"🎓 Iniciando sessão de aprendizado com {len(target_agents)} agentes...")
        
        session_id = str(uuid.uuid4())
        session_start = time.time()
        
        # Analisar cada agente
        collaboration_analyses = []
        total_synergy = 0.0
        
        for agent in target_agents:
            analysis = self.analyze_collaboration_potential(agent)
            collaboration_analyses.append(analysis)
            
            if analysis['recommended']:
                total_synergy += analysis['collaboration_potential']
        
        # Calcular sinergia média
        avg_synergy = total_synergy / max(len(target_agents), 1)
        
        # Simular aprendizado colaborativo
        learning_outcomes = self._simulate_collaborative_learning(collaboration_analyses)
        
        session_duration = time.time() - session_start
        
        session_data = {
            "session_id": session_id,
            "initiator_agent_id": self.agent_id,
            "timestamp": datetime.utcnow().isoformat(),
            "duration_seconds": session_duration,
            "participating_agents": [agent['id'] for agent in target_agents],
            "collaboration_analyses": collaboration_analyses,
            "average_synergy": avg_synergy,
            "learning_outcomes": learning_outcomes,
            "success": avg_synergy >= self.min_collaboration_synergy
        }
        
        # Salvar sessão
        self.learning_sessions.append(session_data)
        
        if session_data['success']:
            self.logger.info(f"✅ Sessão de aprendizado concluída - Sinergia: {avg_synergy:.1f}%")
        else:
            self.logger.warning(f"⚠️ Sessão de aprendizado com baixa sinergia: {avg_synergy:.1f}%")
        
        return session_data
    
    def _simulate_collaborative_learning(self, analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Simula processo de aprendizado colaborativo
        """
        # Em produção, isso seria aprendizado real baseado em interações
        import random
        
        learning_gains = {
            "knowledge_transfer": random.uniform(0.1, 0.3),
            "workflow_optimization": random.uniform(0.05, 0.25),
            "capability_enhancement": random.uniform(0.08, 0.2),
            "pattern_recognition": random.uniform(0.06, 0.18)
        }
        
        # Calcular ganho total baseado nas análises
        recommended_collaborations = [a for a in analyses if a['recommended']]
        collaboration_multiplier = len(recommended_collaborations) / max(len(analyses), 1)
        
        total_learning_gain = sum(learning_gains.values()) * collaboration_multiplier
        
        return {
            "learning_gains": learning_gains,
            "collaboration_multiplier": collaboration_multiplier,
            "total_learning_gain": total_learning_gain,
            "new_patterns_discovered": random.randint(1, 5),
            "workflow_improvements": random.randint(0, 3)
        }
    
    def save_interaction_to_suna(self, interaction_data: Dict[str, Any]) -> bool:
        """
        Salva interação colaborativa no sistema SUNA
        """
        try:
            if not self.supabase_client:
                self.logger.warning("⚠️ Cliente Supabase não disponível")
                return False
            
            # Preparar dados para tabela agent_interactions
            interaction_record = {
                "id": str(uuid.uuid4()),
                "initiator_agent_id": self.agent_id,
                "target_agent_ids": json.dumps(interaction_data.get('participating_agents', [])),
                "interaction_type": "collaborative_learning",
                "synergy_score": interaction_data.get('average_synergy', 0.0),
                "duration_seconds": interaction_data.get('duration_seconds', 0.0),
                "outcomes": json.dumps(interaction_data.get('learning_outcomes', {})),
                "timestamp": datetime.utcnow().isoformat(),
                "metadata": json.dumps(interaction_data)
            }
            
            result = self.supabase_client.table('agent_interactions').insert(interaction_record).execute()
            
            if result.data:
                self.logger.info(f"✅ Interação salva no SUNA: {len(result.data)} registros")
                return True
            else:
                self.logger.error("❌ Falha ao salvar interação no SUNA")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao salvar interação no SUNA: {e}")
            return False
    
    def run_collaboration_cycle(self) -> Dict[str, Any]:
        """
        Executa ciclo completo de colaboração
        """
        self.logger.info("🔄 Iniciando ciclo de colaboração SUNA-ALSHAM...")
        
        cycle_start = time.time()
        
        try:
            # 1. Descobrir agentes disponíveis
            available_agents = self.discover_agents()
            
            if not available_agents:
                return {
                    "success": False,
                    "reason": "Nenhum agente disponível para colaboração",
                    "timestamp": datetime.utcnow().isoformat()
                }
            
            # 2. Iniciar sessão de aprendizado
            learning_session = self.initiate_learning_session(available_agents)
            
            # 3. Salvar no sistema SUNA
            suna_saved = self.save_interaction_to_suna(learning_session)
            
            cycle_duration = time.time() - cycle_start
            
            cycle_result = {
                "cycle_id": str(uuid.uuid4()),
                "agent_id": self.agent_id,
                "timestamp": datetime.utcnow().isoformat(),
                "duration_seconds": cycle_duration,
                "agents_discovered": len(available_agents),
                "learning_session": learning_session,
                "suna_integration": suna_saved,
                "success": learning_session.get("success", False)
            }
            
            if cycle_result["success"]:
                synergy = learning_session.get("average_synergy", 0)
                self.logger.info(f"🎉 Ciclo de colaboração concluído - Sinergia: {synergy:.1f}%")
            else:
                self.logger.warning("⚠️ Ciclo de colaboração com limitações")
            
            return cycle_result
            
        except Exception as e:
            self.logger.error(f"❌ Erro no ciclo de colaboração: {e}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def get_status(self) -> Dict[str, Any]:
        """
        Retorna status completo do agente
        """
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "type": self.type,
            "status": self.status,
            "collaboration_score": self.collaboration_score,
            "learning_sessions_count": len(self.learning_sessions),
            "agent_interactions_count": len(self.agent_interactions),
            "capabilities": self.capabilities,
            "suna_integrated": self.supabase_client is not None,
            "last_update": datetime.utcnow().isoformat()
        }

# Função de teste para desenvolvimento
def test_learn_agent():
    """Teste básico do agente LEARN"""
    print("🎯 Testando Agente LEARN SUNA-ALSHAM...")
    
    agent = LearnAgent()
    print(f"🤖 Agente criado: {agent.name} - ID: {agent.agent_id}")
    
    # Executar ciclo de colaboração
    result = agent.run_collaboration_cycle()
    
    if result.get("success"):
        synergy = result["learning_session"].get("average_synergy", 0)
        print(f"✅ Ciclo concluído - Sinergia: {synergy:.1f}%")
    else:
        print(f"❌ Ciclo falhou: {result.get('error', result.get('reason', 'Erro desconhecido'))}")
    
    # Status final
    status = agent.get_status()
    print(f"📊 Sessões de aprendizado: {status['learning_sessions_count']}")
    print("🎉 Teste do Agente LEARN concluído!")

if __name__ == "__main__":
    test_learn_agent()
