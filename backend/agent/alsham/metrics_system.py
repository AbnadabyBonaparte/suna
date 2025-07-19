"""
SUNA-ALSHAM Metrics System
Sistema centralizado de métricas para monitoramento de agentes auto-evolutivos

Integrado com infraestrutura SUNA existente
"""

import uuid
import json
import time
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import logging
import statistics

# Importações SUNA existentes
try:
    from ...supabase import get_supabase_client
    from ...utils.logger import get_logger
except ImportError:
    # Fallback para desenvolvimento
    logging.basicConfig(level=logging.INFO)
    get_logger = lambda name: logging.getLogger(name)

class MetricsSystem:
    """
    Sistema centralizado de métricas para agentes SUNA-ALSHAM
    
    Funcionalidades:
    - Coleta de métricas de todos os agentes
    - Análise estatística de performance
    - Geração de relatórios consolidados
    - Integração com sistema SUNA
    """
    
    def __init__(self, config: Optional[Dict] = None):
        self.system_id = str(uuid.uuid4())
        self.config = config or {}
        
        # Configurações
        self.metrics_retention_days = self.config.get('metrics_retention_days', 30)
        self.analysis_window_hours = self.config.get('analysis_window_hours', 24)
        self.alert_thresholds = self.config.get('alert_thresholds', {
            'performance_drop': 0.2,  # 20% de queda
            'security_score': 0.7,   # Score mínimo de segurança
            'collaboration_synergy': 0.3  # Sinergia mínima
        })
        
        # Cache de métricas
        self.metrics_cache = {}
        self.last_analysis = None
        self.metrics_history = []
        
        # Logger
        self.logger = get_logger("SUNA-ALSHAM-METRICS")
        
        # Integração SUNA
        self.supabase_client = None
        self._initialize_suna_integration()
        
        self.logger.info(f"📊 Sistema de Métricas inicializado - ID: {self.system_id}")
    
    def _initialize_suna_integration(self):
        """Inicializa integração com infraestrutura SUNA"""
        try:
            self.supabase_client = get_supabase_client()
            self.logger.info("✅ Integração SUNA inicializada com sucesso")
        except Exception as e:
            self.logger.warning(f"⚠️ Integração SUNA parcial: {e}")
    
    def collect_agent_metrics(self, agent_id: str, time_window_hours: int = 24) -> Dict[str, Any]:
        """
        Coleta métricas de um agente específico
        """
        self.logger.info(f"📊 Coletando métricas do agente {agent_id}...")
        
        try:
            if not self.supabase_client:
                self.logger.warning("⚠️ Cliente Supabase não disponível")
                return {}
            
            # Calcular janela de tempo
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(hours=time_window_hours)
            
            # Coletar métricas de performance
            performance_metrics = self._collect_performance_metrics(agent_id, start_time, end_time)
            
            # Coletar métricas de interação (para agentes colaborativos)
            interaction_metrics = self._collect_interaction_metrics(agent_id, start_time, end_time)
            
            # Coletar métricas de segurança
            security_metrics = self._collect_security_metrics(agent_id, start_time, end_time)
            
            # Consolidar métricas
            consolidated_metrics = {
                "agent_id": agent_id,
                "collection_timestamp": end_time.isoformat(),
                "time_window_hours": time_window_hours,
                "performance": performance_metrics,
                "interactions": interaction_metrics,
                "security": security_metrics
            }
            
            # Atualizar cache
            self.metrics_cache[agent_id] = consolidated_metrics
            
            self.logger.info(f"✅ Métricas coletadas para agente {agent_id}")
            return consolidated_metrics
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao coletar métricas: {e}")
            return {}
    
    def _collect_performance_metrics(self, agent_id: str, start_time: datetime, end_time: datetime) -> Dict[str, Any]:
        """Coleta métricas de performance de um agente"""
        try:
            result = self.supabase_client.table('performance_metrics').select("*").eq('agent_id', agent_id).gte('timestamp', start_time.isoformat()).lte('timestamp', end_time.isoformat()).execute()
            
            if not result.data:
                return {"metrics_count": 0, "average_performance": 0.0}
            
            # Analisar métricas
            performance_values = [record['current_value'] for record in result.data if record.get('current_value') is not None]
            improvement_values = [record['improvement_percentage'] for record in result.data if record.get('improvement_percentage') is not None]
            
            metrics = {
                "metrics_count": len(result.data),
                "average_performance": statistics.mean(performance_values) if performance_values else 0.0,
                "max_performance": max(performance_values) if performance_values else 0.0,
                "min_performance": min(performance_values) if performance_values else 0.0,
                "performance_std": statistics.stdev(performance_values) if len(performance_values) > 1 else 0.0,
                "average_improvement": statistics.mean(improvement_values) if improvement_values else 0.0,
                "total_improvements": len([v for v in improvement_values if v > 0]),
                "last_performance": performance_values[-1] if performance_values else 0.0
            }
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao coletar métricas de performance: {e}")
            return {"error": str(e)}
    
    def _collect_interaction_metrics(self, agent_id: str, start_time: datetime, end_time: datetime) -> Dict[str, Any]:
        """Coleta métricas de interação de um agente"""
        try:
            result = self.supabase_client.table('agent_interactions').select("*").eq('initiator_agent_id', agent_id).gte('timestamp', start_time.isoformat()).lte('timestamp', end_time.isoformat()).execute()
            
            if not result.data:
                return {"interactions_count": 0, "average_synergy": 0.0}
            
            # Analisar interações
            synergy_values = [record['synergy_score'] for record in result.data if record.get('synergy_score') is not None]
            duration_values = [record['duration_seconds'] for record in result.data if record.get('duration_seconds') is not None]
            
            metrics = {
                "interactions_count": len(result.data),
                "average_synergy": statistics.mean(synergy_values) if synergy_values else 0.0,
                "max_synergy": max(synergy_values) if synergy_values else 0.0,
                "min_synergy": min(synergy_values) if synergy_values else 0.0,
                "average_duration": statistics.mean(duration_values) if duration_values else 0.0,
                "successful_interactions": len([v for v in synergy_values if v >= 30.0]),  # Threshold de sucesso
                "last_synergy": synergy_values[-1] if synergy_values else 0.0
            }
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao coletar métricas de interação: {e}")
            return {"error": str(e)}
    
    def _collect_security_metrics(self, agent_id: str, start_time: datetime, end_time: datetime) -> Dict[str, Any]:
        """Coleta métricas de segurança de um agente"""
        try:
            result = self.supabase_client.table('security_logs').select("*").eq('agent_id', agent_id).gte('timestamp', start_time.isoformat()).lte('timestamp', end_time.isoformat()).execute()
            
            if not result.data:
                return {"security_events": 0, "average_security_score": 1.0}
            
            # Analisar logs de segurança
            security_scores = [record['security_score'] for record in result.data if record.get('security_score') is not None]
            threat_counts = [record['threats_detected'] for record in result.data if record.get('threats_detected') is not None]
            containment_counts = [record['containment_actions'] for record in result.data if record.get('containment_actions') is not None]
            
            metrics = {
                "security_events": len(result.data),
                "average_security_score": statistics.mean(security_scores) if security_scores else 1.0,
                "min_security_score": min(security_scores) if security_scores else 1.0,
                "total_threats_detected": sum(threat_counts) if threat_counts else 0,
                "total_containment_actions": sum(containment_counts) if containment_counts else 0,
                "security_incidents": len([s for s in security_scores if s < 0.7]),  # Threshold de incidente
                "last_security_score": security_scores[-1] if security_scores else 1.0
            }
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao coletar métricas de segurança: {e}")
            return {"error": str(e)}
    
    def collect_performance_metric(self, agent_id: str, metric_type: str, value: float, metadata: Optional[Dict] = None) -> bool:
        """
        Coleta métrica de performance de um agente
        """
        try:
            metric_data = {
                "id": str(uuid.uuid4()),
                "agent_id": agent_id,
                "metric_type": metric_type,
                "value": value,
                "metadata": json.dumps(metadata or {}),
                "timestamp": datetime.utcnow().isoformat()
            }
            
            # Salvar métrica no histórico local
            self.metrics_history.append(metric_data)
            
            # Salvar no SUNA se disponível
            if self.supabase_client:
                result = self.supabase_client.table('system_metrics').insert(metric_data).execute()
                if result.data:
                    self.logger.info(f"📊 Métrica salva: {metric_type} = {value}")
                    return True
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao coletar métrica: {e}")
            return False
    
    def get_performance_metrics(self, agent_id: str) -> Dict[str, Any]:
        """
        Retorna métricas de performance de um agente
        """
        try:
            # Verificar cache primeiro
            if agent_id in self.metrics_cache:
                cached_metrics = self.metrics_cache[agent_id]
                cache_time = datetime.fromisoformat(cached_metrics["collection_timestamp"].replace('Z', '+00:00'))
                
                # Se cache é recente (menos de 5 minutos), usar cache
                if (datetime.utcnow() - cache_time.replace(tzinfo=None)) < timedelta(minutes=5):
                    return cached_metrics.get("performance", {})
            
            # Coletar métricas atualizadas
            metrics = self.collect_agent_metrics(agent_id, 1)  # Última hora
            return metrics.get("performance", {})
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao obter métricas: {e}")
            return {}
    
    def analyze_system_health(self) -> Dict[str, Any]:
        """
        Analisa saúde geral do sistema SUNA-ALSHAM
        """
        self.logger.info("🔍 Analisando saúde do sistema...")
        
        try:
            if not self.supabase_client:
                return {
                    "system_health": "UNKNOWN",
                    "reason": "Cliente Supabase não disponível"
                }
            
            # Obter lista de agentes ativos
            agents_result = self.supabase_client.table('agents').select("id, name, type").eq('status', 'active').execute()
            
            if not agents_result.data:
                return {
                    "system_health": "UNKNOWN",
                    "reason": "Nenhum agente ativo encontrado"
                }
            
            # Coletar métricas de todos os agentes
            system_metrics = {}
            for agent in agents_result.data:
                agent_id = agent['id']
                agent_metrics = self.collect_agent_metrics(agent_id, self.analysis_window_hours)
                system_metrics[agent_id] = {
                    "name": agent['name'],
                    "type": agent['type'],
                    "metrics": agent_metrics
                }
            
            # Analisar saúde geral
            health_analysis = self._analyze_health_indicators(system_metrics)
            
            # Gerar alertas se necessário
            alerts = self._generate_alerts(system_metrics)
            
            analysis_result = {
                "analysis_timestamp": datetime.utcnow().isoformat(),
                "system_health": health_analysis["overall_health"],
                "agents_analyzed": len(system_metrics),
                "health_indicators": health_analysis,
                "alerts": alerts,
                "system_metrics": system_metrics
            }
            
            self.last_analysis = analysis_result
            
            self.logger.info(f"✅ Análise concluída - Saúde: {health_analysis['overall_health']}")
            return analysis_result
            
        except Exception as e:
            self.logger.error(f"❌ Erro na análise de saúde: {e}")
            return {
                "system_health": "ERROR",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def _analyze_health_indicators(self, system_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Analisa indicadores de saúde do sistema"""
        
        # Coletar indicadores de todos os agentes
        performance_scores = []
        security_scores = []
        collaboration_scores = []
        
        for agent_id, agent_data in system_metrics.items():
            metrics = agent_data.get("metrics", {})
            
            # Performance
            perf = metrics.get("performance", {})
            if perf.get("average_performance"):
                performance_scores.append(perf["average_performance"])
            
            # Segurança
            sec = metrics.get("security", {})
            if sec.get("average_security_score"):
                security_scores.append(sec["average_security_score"])
            
            # Colaboração (para agentes colaborativos)
            inter = metrics.get("interactions", {})
            if inter.get("average_synergy"):
                collaboration_scores.append(inter["average_synergy"] / 100.0)  # Normalizar para 0-1
        
        # Calcular indicadores gerais
        avg_performance = statistics.mean(performance_scores) if performance_scores else 0.0
        avg_security = statistics.mean(security_scores) if security_scores else 1.0
        avg_collaboration = statistics.mean(collaboration_scores) if collaboration_scores else 0.0
        
        # Determinar saúde geral
        health_score = (avg_performance * 0.4 + avg_security * 0.4 + avg_collaboration * 0.2)
        
        if health_score >= 0.8:
            overall_health = "EXCELLENT"
        elif health_score >= 0.6:
            overall_health = "GOOD"
        elif health_score >= 0.4:
            overall_health = "FAIR"
        else:
            overall_health = "POOR"
        
        return {
            "overall_health": overall_health,
            "health_score": health_score,
            "average_performance": avg_performance,
            "average_security": avg_security,
            "average_collaboration": avg_collaboration,
            "agents_with_metrics": len(performance_scores)
        }
    
    def _generate_alerts(self, system_metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Gera alertas baseados nos thresholds configurados"""
        
        alerts = []
        
        for agent_id, agent_data in system_metrics.items():
            agent_name = agent_data.get("name", "Unknown")
            metrics = agent_data.get("metrics", {})
            
            # Alerta de performance baixa
            perf = metrics.get("performance", {})
            if perf.get("last_performance", 1.0) < self.alert_thresholds["performance_drop"]:
                alerts.append({
                    "type": "PERFORMANCE_LOW",
                    "severity": "HIGH",
                    "agent_id": agent_id,
                    "agent_name": agent_name,
                    "message": f"Performance baixa detectada: {perf['last_performance']:.3f}",
                    "timestamp": datetime.utcnow().isoformat()
                })
            
            # Alerta de segurança
            sec = metrics.get("security", {})
            if sec.get("last_security_score", 1.0) < self.alert_thresholds["security_score"]:
                alerts.append({
                    "type": "SECURITY_RISK",
                    "severity": "CRITICAL",
                    "agent_id": agent_id,
                    "agent_name": agent_name,
                    "message": f"Score de segurança baixo: {sec['last_security_score']:.3f}",
                    "timestamp": datetime.utcnow().isoformat()
                })
            
            # Alerta de colaboração baixa
            inter = metrics.get("interactions", {})
            if inter.get("last_synergy", 0.0) < self.alert_thresholds["collaboration_synergy"] * 100:
                alerts.append({
                    "type": "COLLABORATION_LOW",
                    "severity": "MEDIUM",
                    "agent_id": agent_id,
                    "agent_name": agent_name,
                    "message": f"Sinergia de colaboração baixa: {inter['last_synergy']:.1f}%",
                    "timestamp": datetime.utcnow().isoformat()
                })
        
        return alerts
    
    def generate_report(self, format_type: str = "summary") -> Dict[str, Any]:
        """
        Gera relatório do sistema
        """
        self.logger.info(f"📋 Gerando relatório do sistema ({format_type})...")
        
        # Executar análise se não foi feita recentemente
        if not self.last_analysis or self._analysis_is_stale():
            self.analyze_system_health()
        
        if format_type == "summary":
            return self._generate_summary_report()
        elif format_type == "detailed":
            return self._generate_detailed_report()
        else:
            return {"error": f"Formato de relatório não suportado: {format_type}"}
    
    def _analysis_is_stale(self) -> bool:
        """Verifica se a análise está desatualizada"""
        if not self.last_analysis:
            return True
        
        last_time = datetime.fromisoformat(self.last_analysis["analysis_timestamp"].replace('Z', '+00:00'))
        return (datetime.utcnow() - last_time.replace(tzinfo=None)) > timedelta(hours=1)
    
    def _generate_summary_report(self) -> Dict[str, Any]:
        """Gera relatório resumido"""
        if not self.last_analysis:
            return {"error": "Nenhuma análise disponível"}
        
        health = self.last_analysis["health_indicators"]
        alerts = self.last_analysis["alerts"]
        
        return {
            "report_type": "summary",
            "generated_at": datetime.utcnow().isoformat(),
            "system_health": health["overall_health"],
            "health_score": health["health_score"],
            "agents_monitored": health["agents_with_metrics"],
            "active_alerts": len(alerts),
            "critical_alerts": len([a for a in alerts if a["severity"] == "CRITICAL"]),
            "performance_avg": health["average_performance"],
            "security_avg": health["average_security"],
            "collaboration_avg": health["average_collaboration"]
        }
    
    def _generate_detailed_report(self) -> Dict[str, Any]:
        """Gera relatório detalhado"""
        if not self.last_analysis:
            return {"error": "Nenhuma análise disponível"}
        
        return {
            "report_type": "detailed",
            "generated_at": datetime.utcnow().isoformat(),
            "full_analysis": self.last_analysis
        }

# Função de teste para desenvolvimento
def test_metrics_system():
    """Teste básico do sistema de métricas"""
    print("🎯 Testando Sistema de Métricas SUNA-ALSHAM...")
    
    metrics_system = MetricsSystem()
    print(f"📊 Sistema criado - ID: {metrics_system.system_id}")
    
    # Analisar saúde do sistema
    health_analysis = metrics_system.analyze_system_health()
    
    if health_analysis.get("system_health") != "ERROR":
        health = health_analysis["system_health"]
        agents = health_analysis["agents_analyzed"]
        alerts = len(health_analysis["alerts"])
        print(f"✅ Análise concluída - Saúde: {health}, Agentes: {agents}, Alertas: {alerts}")
    else:
        print(f"❌ Análise falhou: {health_analysis.get('error', 'Erro desconhecido')}")
    
    # Gerar relatório
    report = metrics_system.generate_report("summary")
    print(f"📋 Relatório gerado: {report.get('system_health', 'N/A')}")
    print("🎉 Teste do Sistema de Métricas concluído!")

if __name__ == "__main__":
    test_metrics_system()
