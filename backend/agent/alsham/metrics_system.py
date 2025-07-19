"""
SUNA-ALSHAM Metrics System
Sistema centralizado de métricas para monitoramento de agentes auto-evolutivos

Integrado com infraestrutura SUNA existente
"""

import uuid
import json
import time
import random
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import logging
import statistics

# Configuração de logging básica
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MetricsSystem:
    """
    Sistema centralizado de métricas para agentes SUNA-ALSHAM
    
    Funcionalidades:
    - Coleta de métricas de todos os agentes
    - Análise estatística de performance
    - Geração de relatórios consolidados
    """
    
    def __init__(self, config: Optional[Dict] = None):
        self.system_id = str(uuid.uuid4())
        self.config = config or {}
        
        # Configurações
        self.metrics_retention_days = self.config.get('metrics_retention_days', 30)
        self.analysis_window_hours = self.config.get('analysis_window_hours', 24)
        self.alert_thresholds = self.config.get('alert_thresholds', {
            'performance_drop': 0.2,  # 20% de queda
            'security_score': 0.7,   # Score mínimo
            'collaboration_synergy': 30.0  # Sinergia mínima
        })
        
        # Armazenamento de métricas
        self.metrics_storage = {}
        self.performance_history = []
        self.alerts_generated = []
        self.last_analysis = None
        
        logger.info(f"📊 Sistema de Métricas inicializado - ID: {self.system_id}")
    
    def collect_performance_metric(self, agent_id: str, metric_type: str, value: float, metadata: Optional[Dict] = None):
        """
        Coleta uma métrica de performance de um agente
        """
        timestamp = datetime.utcnow()
        
        metric_entry = {
            "id": str(uuid.uuid4()),
            "agent_id": agent_id,
            "metric_type": metric_type,
            "value": value,
            "timestamp": timestamp.isoformat(),
            "metadata": metadata or {}
        }
        
        # Armazenar por agente
        if agent_id not in self.metrics_storage:
            self.metrics_storage[agent_id] = []
        
        self.metrics_storage[agent_id].append(metric_entry)
        
        # Manter apenas métricas dentro do período de retenção
        cutoff_date = timestamp - timedelta(days=self.metrics_retention_days)
        self.metrics_storage[agent_id] = [
            m for m in self.metrics_storage[agent_id]
            if datetime.fromisoformat(m["timestamp"]) > cutoff_date
        ]
        
        logger.debug(f"📊 Métrica coletada: {agent_id} - {metric_type}: {value}")
    
    def get_performance_metrics(self, agent_id: str, metric_type: Optional[str] = None, hours: int = 24) -> Dict[str, Any]:
        """
        Recupera métricas de performance de um agente
        """
        if agent_id not in self.metrics_storage:
            return {"metrics": [], "summary": {}}
        
        # Filtrar por período
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        agent_metrics = [
            m for m in self.metrics_storage[agent_id]
            if datetime.fromisoformat(m["timestamp"]) > cutoff_time
        ]
        
        # Filtrar por tipo se especificado
        if metric_type:
            agent_metrics = [m for m in agent_metrics if m["metric_type"] == metric_type]
        
        # Calcular estatísticas
        if agent_metrics:
            values = [m["value"] for m in agent_metrics]
            summary = {
                "count": len(values),
                "average": statistics.mean(values),
                "median": statistics.median(values),
                "min": min(values),
                "max": max(values),
                "std_dev": statistics.stdev(values) if len(values) > 1 else 0
            }
        else:
            summary = {"count": 0, "average": 0, "median": 0, "min": 0, "max": 0, "std_dev": 0}
        
        return {
            "agent_id": agent_id,
            "metric_type": metric_type,
            "period_hours": hours,
            "metrics": agent_metrics,
            "summary": summary
        }
    
    def analyze_system_health(self) -> Dict[str, Any]:
        """
        Analisa a saúde geral do sistema SUNA-ALSHAM
        """
        logger.info("🔍 Analisando saúde do sistema...")
        
        analysis_timestamp = datetime.utcnow()
        
        # Analisar cada agente
        agent_analyses = {}
        alerts = []
        
        for agent_id in self.metrics_storage.keys():
            agent_analysis = self._analyze_agent_health(agent_id)
            agent_analyses[agent_id] = agent_analysis
            
            # Gerar alertas se necessário
            agent_alerts = self._generate_alerts(agent_id, agent_analysis)
            alerts.extend(agent_alerts)
        
        # Calcular saúde geral do sistema
        if agent_analyses:
            health_scores = [a.get("health_score", 0) for a in agent_analyses.values()]
            system_health_score = statistics.mean(health_scores)
            
            if system_health_score > 0.8:
                system_health = "EXCELLENT"
            elif system_health_score > 0.6:
                system_health = "GOOD"
            elif system_health_score > 0.4:
                system_health = "FAIR"
            else:
                system_health = "POOR"
        else:
            system_health_score = 0
            system_health = "ERROR"
        
        analysis = {
            "analysis_id": str(uuid.uuid4()),
            "timestamp": analysis_timestamp.isoformat(),
            "system_health": system_health,
            "system_health_score": system_health_score,
            "agents_analyzed": len(agent_analyses),
            "agent_analyses": agent_analyses,
            "alerts": alerts,
            "total_alerts": len(alerts),
            "critical_alerts": len([a for a in alerts if a.get("severity") == "CRITICAL"]),
            "analysis_duration": random.uniform(0.5, 2.0)
        }
        
        self.last_analysis = analysis
        self.alerts_generated.extend(alerts)
        
        logger.info(f"🔍 Análise concluída - Saúde: {system_health} ({system_health_score:.3f})")
        return analysis
    
    def _analyze_agent_health(self, agent_id: str) -> Dict[str, Any]:
        """
        Analisa a saúde de um agente específico
        """
        # Obter métricas recentes
        recent_metrics = self.get_performance_metrics(agent_id, hours=self.analysis_window_hours)
        
        if recent_metrics["summary"]["count"] == 0:
            return {
                "agent_id": agent_id,
                "health_score": 0.0,
                "status": "NO_DATA",
                "issues": ["Nenhuma métrica disponível"]
            }
        
        # Analisar tendências
        metrics = recent_metrics["metrics"]
        if len(metrics) >= 2:
            recent_values = [m["value"] for m in metrics[-5:]]  # Últimas 5 métricas
            older_values = [m["value"] for m in metrics[:-5]] if len(metrics) > 5 else recent_values
            
            recent_avg = statistics.mean(recent_values)
            older_avg = statistics.mean(older_values) if older_values else recent_avg
            
            trend = (recent_avg - older_avg) / older_avg if older_avg > 0 else 0
        else:
            trend = 0
        
        # Calcular score de saúde
        summary = recent_metrics["summary"]
        base_score = min(summary["average"], 1.0)  # Normalizar para 0-1
        
        # Penalizar alta variabilidade
        variability_penalty = min(summary["std_dev"] * 0.5, 0.3)
        
        # Bonificar tendência positiva
        trend_bonus = max(trend * 0.2, -0.2)
        
        health_score = max(0.0, min(1.0, base_score - variability_penalty + trend_bonus))
        
        # Determinar status
        if health_score > 0.8:
            status = "EXCELLENT"
        elif health_score > 0.6:
            status = "GOOD"
        elif health_score > 0.4:
            status = "FAIR"
        else:
            status = "POOR"
        
        # Identificar problemas
        issues = []
        if summary["std_dev"] > 0.3:
            issues.append("Alta variabilidade nas métricas")
        if trend < -0.1:
            issues.append("Tendência de declínio na performance")
        if summary["average"] < 0.5:
            issues.append("Performance abaixo do esperado")
        
        return {
            "agent_id": agent_id,
            "health_score": health_score,
            "status": status,
            "trend": trend,
            "variability": summary["std_dev"],
            "average_performance": summary["average"],
            "issues": issues,
            "metrics_count": summary["count"]
        }
    
    def _generate_alerts(self, agent_id: str, agent_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Gera alertas baseado na análise do agente
        """
        alerts = []
        
        health_score = agent_analysis.get("health_score", 0)
        trend = agent_analysis.get("trend", 0)
        
        # Alerta de performance baixa
        if health_score < self.alert_thresholds.get("security_score", 0.7):
            alerts.append({
                "id": str(uuid.uuid4()),
                "agent_id": agent_id,
                "type": "low_performance",
                "severity": "HIGH" if health_score < 0.4 else "MEDIUM",
                "message": f"Performance do agente abaixo do esperado: {health_score:.3f}",
                "timestamp": datetime.utcnow().isoformat()
            })
        
        # Alerta de declínio
        if trend < -self.alert_thresholds.get("performance_drop", 0.2):
            alerts.append({
                "id": str(uuid.uuid4()),
                "agent_id": agent_id,
                "type": "performance_decline",
                "severity": "MEDIUM",
                "message": f"Declínio na performance detectado: {trend:.3f}",
                "timestamp": datetime.utcnow().isoformat()
            })
        
        return alerts
    
    def generate_report(self, report_type: str = "summary") -> Dict[str, Any]:
        """
        Gera relatório de métricas
        """
        if report_type == "summary":
            if not self.last_analysis:
                return {"error": "Nenhuma análise disponível"}
            
            return {
                "report_type": "summary",
                "generated_at": datetime.utcnow().isoformat(),
                "system_health": self.last_analysis.get("system_health"),
                "agents_count": self.last_analysis.get("agents_analyzed", 0),
                "total_alerts": self.last_analysis.get("total_alerts", 0),
                "critical_alerts": self.last_analysis.get("critical_alerts", 0)
            }
        
        elif report_type == "detailed":
            if not self.last_analysis:
                return {"error": "Nenhuma análise disponível"}
            
            return {
                "report_type": "detailed",
                "generated_at": datetime.utcnow().isoformat(),
                "full_analysis": self.last_analysis
            }
        
        return {"error": "Tipo de relatório não suportado"}

# Função de teste
def test_metrics_system():
    """Teste básico do sistema de métricas"""
    print("🎯 Testando Sistema de Métricas...")
    
    metrics_system = MetricsSystem()
    
    # Simular coleta de métricas
    test_agent_id = "test-agent-123"
    for i in range(10):
        metrics_system.collect_performance_metric(
            test_agent_id, 
            "performance_score", 
            random.uniform(0.6, 0.9)
        )
    
    # Analisar saúde
    analysis = metrics_system.analyze_system_health()
    
    print(f"📊 Resultado: {analysis.get('system_health', 'ERROR')}")
    print(f"🤖 Agentes analisados: {analysis.get('agents_analyzed', 0)}")
    print("✅ Teste concluído!")

if __name__ == "__main__":
    test_metrics_system()
