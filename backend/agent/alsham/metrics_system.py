"""
SUNA-ALSHAM Metrics System
Sistema para coleta, armazenamento e análise de métricas de performance.
"""
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from collections import defaultdict

# Correção: Importa a classe de configuração correta
from .config import MetricsConfig

class MetricsSystem:
    """
    Gerencia as métricas de saúde e performance do sistema SUNA-ALSHAM.
    """
    def __init__(self, config: Optional[MetricsConfig] = None):
        self.system_id = str(uuid.uuid4())
        
        # Correção: Usa dataclass diretamente
        self.config = config if config else MetricsConfig()
        self.enabled = self.config.enabled
        self.retention_days = self.config.retention_days

        # Armazenamento em memória (em um sistema real, usaria um banco de dados de séries temporais)
        self.metrics_storage: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self.system_health_score = 100.0

    def collect_performance_metric(self, agent_id: str, metric_name: str, value: float, metadata: Optional[Dict] = None):
        """Coleta uma métrica de performance para um agente específico."""
        if not self.enabled:
            return

        metric_record = {
            "timestamp": datetime.utcnow(),
            "agent_id": agent_id,
            "metric_name": metric_name,
            "value": value,
            "metadata": metadata or {}
        }
        self.metrics_storage[metric_name].append(metric_record)
        self._prune_old_metrics()

    def _prune_old_metrics(self):
        """Remove métricas mais antigas que o período de retenção."""
        retention_limit = datetime.utcnow() - timedelta(days=self.retention_days)
        for metric_name in self.metrics_storage:
            self.metrics_storage[metric_name] = [
                m for m in self.metrics_storage[metric_name] if m["timestamp"] > retention_limit
            ]

    def get_performance_metrics(self, agent_id: str, metric_name: str) -> Dict[str, Any]:
        """Recupera e sumariza métricas para um agente."""
        agent_metrics = [
            m["value"] for m in self.metrics_storage.get(metric_name, [])
            if m["agent_id"] == agent_id
        ]
        
        if not agent_metrics:
            return {"count": 0, "avg": 0, "max": 0, "min": 0, "sum": 0}

        return {
            "count": len(agent_metrics),
            "avg": sum(agent_metrics) / len(agent_metrics),
            "max": max(agent_metrics),
            "min": min(agent_metrics),
            "sum": sum(agent_metrics)
        }

    def analyze_system_health(self) -> Dict[str, Any]:
        """Analisa a saúde geral do sistema com base nas métricas coletadas."""
        # Lógica de análise de saúde simulada
        total_metrics = sum(len(v) for v in self.metrics_storage.values())
        if total_metrics > 10:
            self.system_health_score = 95.0
        else:
            self.system_health_score = 85.0
            
        return self.get_system_health()

    def get_system_health(self) -> Dict[str, Any]:
        """Retorna o status de saúde do sistema."""
        return {
            "health_score": self.system_health_score,
            "total_metrics_collected": sum(len(v) for v in self.metrics_storage.values()),
            "status": "healthy" if self.system_health_score > 70 else "warning"
        }
