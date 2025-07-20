"""
SUNA-ALSHAM GUARD Agent
Agente responsável pela segurança, validação e monitoramento do sistema.
"""
import uuid
import time
from datetime import datetime
from typing import Dict, Any, Optional

# Correção: Importa a classe de configuração correta
from .config import GuardAgentConfig

class GuardAgent:
    """
    Agente GUARD: Atua como um sistema imunológico, garantindo a estabilidade e segurança.
    """
    def __init__(self, config: Optional[GuardAgentConfig] = None):
        self.agent_id = str(uuid.uuid4())
        self.name = "GUARD"
        self.status = "initializing"
        self.version = "1.0.0"
        self.created_at = datetime.utcnow()
        self.last_security_scan: Optional[datetime] = None
        
        # Correção: Usa dataclass diretamente
        self.config = config if config else GuardAgentConfig()
        self.enabled = self.config.enabled
        self.max_critical_incidents = self.config.max_critical_incidents

        self.security_score = 99.0 # Pontuação de segurança inicial
        self.incidents_detected = 0
        self.status = "active" if self.enabled else "disabled"

    def get_status(self) -> Dict[str, Any]:
        """Retorna o status atual do agente."""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "status": self.status,
            "version": self.version,
            "security_score": self.security_score,
            "incidents_detected": self.incidents_detected,
            "last_scan": self.last_security_scan.isoformat() if self.last_security_scan else "N/A"
        }

    def run_security_cycle(self) -> Dict[str, Any]:
        """
        Executa um ciclo de verificação de segurança.
        Simula a detecção de anomalias e vulnerabilidades.
        """
        if not self.enabled:
            return {"success": False, "message": "GUARD Agent is disabled."}

        start_time = time.time()
        
        # Simulação de scan de segurança
        time.sleep(1.5)
        # Simula uma pequena chance de encontrar um incidente não-crítico
        import random
        if random.random() < 0.05:
            self.incidents_detected += 1
            self.security_score = max(self.security_score - 1, 0)

        self.last_security_scan = datetime.utcnow()
        duration = time.time() - start_time
        
        cycle_success = self.incidents_detected <= self.max_critical_incidents

        return {
            "success": cycle_success,
            "message": "Security cycle completed.",
            "security_score": self.security_score,
            "new_incidents": 0, # Simulado
            "duration_seconds": duration
        }

    def load_state(self, state: Dict[str, Any]):
        """Carrega o estado do agente a partir de um dicionário."""
        self.agent_id = state.get("agent_id", self.agent_id)
        self.version = state.get("version", self.version)
        self.security_score = state.get("security_score", self.security_score)
        self.incidents_detected = state.get("incidents_detected", self.incidents_detected)
        last_scan_str = state.get("last_scan")
        if last_scan_str and last_scan_str != "N/A":
            self.last_security_scan = datetime.fromisoformat(last_scan_str)
