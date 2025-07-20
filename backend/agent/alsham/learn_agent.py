"""
SUNA-ALSHAM LEARN Agent
Agente responsável pela aprendizagem colaborativa e otimização de sinergia.
"""
import uuid
import time
from datetime import datetime
from typing import Dict, Any, Optional, List

# Correção: Importa a classe de configuração correta
from .config import LearnAgentConfig

class LearnAgent:
    """
    Agente LEARN: Focado em aprender com os outros agentes e melhorar a colaboração.
    """
    def __init__(self, config: Optional[LearnAgentConfig] = None):
        self.agent_id = str(uuid.uuid4())
        self.name = "LEARN"
        self.status = "initializing"
        self.version = "1.0.0"
        self.created_at = datetime.utcnow()
        self.last_collaboration_time: Optional[datetime] = None
        
        # Correção: Usa dataclass diretamente
        self.config = config if config else LearnAgentConfig()
        self.enabled = self.config.enabled
        self.min_synergy_score = self.config.min_synergy_score

        self.synergy_score = 50.0 # Sinergia inicial
        self.status = "active" if self.enabled else "disabled"

    def get_status(self) -> Dict[str, Any]:
        """Retorna o status atual do agente."""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "status": self.status,
            "version": self.version,
            "synergy_score": self.synergy_score,
            "last_collaboration": self.last_collaboration_time.isoformat() if self.last_collaboration_time else "N/A"
        }

    def run_collaboration_cycle(self, other_agents_status: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Executa um ciclo de aprendizagem colaborativa.
        Simula a análise do estado de outros agentes para melhorar a sinergia.
        """
        if not self.enabled:
            return {"success": False, "message": "LEARN Agent is disabled."}

        start_time = time.time()
        
        # Simulação de análise e aprendizado
        time.sleep(1)
        performance_sum = sum(agent.get("performance", 0) for agent in other_agents_status)
        security_sum = sum(agent.get("security_score", 0) for agent in other_agents_status)
        
        # Fórmula simulada para sinergia
        new_synergy = (performance_sum * 50) + (security_sum * 50)
        new_synergy = min(max(new_synergy, 0), 100) # Normaliza entre 0 e 100

        self.synergy_score = new_synergy
        self.last_collaboration_time = datetime.utcnow()
        duration = time.time() - start_time

        return {
            "success": True,
            "message": "Collaboration cycle completed.",
            "synergy_score": self.synergy_score,
            "analyzed_agents": len(other_agents_status),
            "duration_seconds": duration
        }

    def load_state(self, state: Dict[str, Any]):
        """Carrega o estado do agente a partir de um dicionário."""
        self.agent_id = state.get("agent_id", self.agent_id)
        self.version = state.get("version", self.version)
        self.synergy_score = state.get("synergy_score", self.synergy_score)
        last_collab_str = state.get("last_collaboration")
        if last_collab_str and last_collab_str != "N/A":
            self.last_collaboration_time = datetime.fromisoformat(last_collab_str)
