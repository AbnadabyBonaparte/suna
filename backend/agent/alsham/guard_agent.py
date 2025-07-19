"""
SUNA-ALSHAM Guard Agent
Agente de segurança especializado em contenção e proteção do sistema

Integrado com infraestrutura SUNA existente
"""

import uuid
import json
import time
import random
from datetime import datetime
from typing import Dict, Any, Optional, List
import logging

# Configuração de logging básica
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GuardAgent:
    """
    Agente GUARD de segurança integrado ao sistema SUNA
    
    Capacidades:
    - Monitoramento de segurança em tempo real
    - Detecção de anomalias e comportamentos suspeitos
    - Contenção automática de ameaças
    """
    
    def __init__(self, agent_id: Optional[str] = None, config: Optional[Dict] = None):
        self.agent_id = agent_id or str(uuid.uuid4())
        self.name = "SUNA-ALSHAM-GUARD"
        self.type = "security"
        self.status = "active"
        self.wave_number = 1
        self.month_introduced = 4
        
        # Configurações de segurança
        self.config = config or {}
        self.max_critical_incidents = self.config.get('max_critical_incidents', 0)
        self.threat_threshold = self.config.get('threat_threshold', 0.3)
        self.containment_enabled = self.config.get('containment_enabled', True)
        
        # Métricas de segurança
        self.security_score = 1.0
        self.threat_level = "LOW"
        self.incidents_detected = []
        self.containment_actions = []
        
        # Capacidades
        self.capabilities = {
            "threat_detection": True,
            "anomaly_analysis": True,
            "automatic_containment": True,
            "security_monitoring": True,
            "incident_response": True
        }
        
        logger.info(f"🛡️ Agente GUARD inicializado - ID: {self.agent_id}")
    
    def run_security_cycle(self) -> Dict[str, Any]:
        """
        Executa um ciclo completo de monitoramento de segurança
        """
        cycle_id = str(uuid.uuid4())
        logger.info(f"🔒 Iniciando ciclo de segurança: {cycle_id}")
        
        try:
            # 1. Monitoramento do sistema
            monitoring_result = self.monitor_system()
            
            # 2. Detecção de ameaças
            threats_detected = self.detect_threats(monitoring_result)
            
            # 3. Análise de anomalias
            anomaly_analysis = self.analyze_anomalies(monitoring_result)
            
            # 4. Ações de contenção (se necessário)
            containment_result = self.execute_containment(threats_detected)
            
            # 5. Atualizar métricas de segurança
            self.update_security_metrics(monitoring_result, threats_detected)
            
            # Verificar se há incidentes críticos
            critical_incidents = len([t for t in threats_detected if t.get("severity") == "CRITICAL"])
            
            cycle_result = {
                "cycle_id": cycle_id,
                "timestamp": datetime.utcnow().isoformat(),
                "monitoring": monitoring_result,
                "threats_detected": len(threats_detected),
                "critical_incidents": critical_incidents,
                "anomalies_found": len(anomaly_analysis.get("anomalies", [])),
                "containment_actions": len(containment_result.get("actions", [])),
                "security_score": self.security_score,
                "threat_level": self.threat_level,
                "success": critical_incidents <= self.max_critical_incidents
            }
            
            if cycle_result["success"]:
                logger.info(f"✅ Ciclo de segurança bem-sucedido: {cycle_id}")
            else:
                logger.warning(f"⚠️ Incidentes críticos detectados: {critical_incidents}")
                
            return cycle_result
            
        except Exception as e:
            logger.error(f"❌ Erro no ciclo de segurança: {e}")
            return {
                "cycle_id": cycle_id,
                "success": False,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def monitor_system(self) -> Dict[str, Any]:
        """
        Monitora o sistema em busca de atividades suspeitas
        """
        logger.info("👁️ Monitorando sistema...")
        
        # Simular métricas de monitoramento
        system_metrics = {
            "cpu_usage": random.uniform(0.1, 0.9),
            "memory_usage": random.uniform(0.2, 0.8),
            "network_activity": random.uniform(0.1, 0.7),
            "disk_io": random.uniform(0.1, 0.6),
            "active_processes": random.randint(50, 200),
            "network_connections": random.randint(10, 100)
        }
        
        # Calcular score de segurança baseado nas métricas
        security_indicators = {
            "resource_usage_normal": all(v < 0.85 for v in [
                system_metrics["cpu_usage"], 
                system_metrics["memory_usage"]
            ]),
            "network_activity_normal": system_metrics["network_activity"] < 0.8,
            "process_count_normal": system_metrics["active_processes"] < 180,
            "connection_count_normal": system_metrics["network_connections"] < 90
        }
        
        normal_indicators = sum(security_indicators.values())
        security_score = normal_indicators / len(security_indicators)
        
        monitoring_result = {
            "timestamp": datetime.utcnow().isoformat(),
            "system_metrics": system_metrics,
            "security_indicators": security_indicators,
            "security_score": security_score,
            "monitoring_duration": random.uniform(1.0, 3.0)
        }
        
        logger.info(f"👁️ Monitoramento concluído - Score: {security_score:.3f}")
        return monitoring_result
    
    def detect_threats(self, monitoring_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Detecta ameaças baseado nos dados de monitoramento
        """
        logger.info("🚨 Detectando ameaças...")
        
        threats = []
        system_metrics = monitoring_data.get("system_metrics", {})
        
        # Detectar uso anômalo de recursos
        if system_metrics.get("cpu_usage", 0) > 0.9:
            threats.append({
                "id": str(uuid.uuid4()),
                "type": "resource_abuse",
                "severity": "HIGH",
                "description": "Uso anômalo de CPU detectado",
                "metric_value": system_metrics["cpu_usage"],
                "threshold": 0.9
            })
        
        if system_metrics.get("memory_usage", 0) > 0.85:
            threats.append({
                "id": str(uuid.uuid4()),
                "type": "memory_leak",
                "severity": "MEDIUM",
                "description": "Possível vazamento de memória",
                "metric_value": system_metrics["memory_usage"],
                "threshold": 0.85
            })
        
        # Detectar atividade de rede suspeita
        if system_metrics.get("network_activity", 0) > 0.8:
            threats.append({
                "id": str(uuid.uuid4()),
                "type": "network_anomaly",
                "severity": "HIGH",
                "description": "Atividade de rede suspeita",
                "metric_value": system_metrics["network_activity"],
                "threshold": 0.8
            })
        
        # Simular detecção aleatória de ameaças críticas (raro)
        if random.random() < 0.05:  # 5% de chance
            threats.append({
                "id": str(uuid.uuid4()),
                "type": "critical_security_breach",
                "severity": "CRITICAL",
                "description": "Possível violação de segurança crítica detectada",
                "metric_value": 1.0,
                "threshold": 0.0
            })
        
        logger.info(f"🚨 {len(threats)} ameaças detectadas")
        return threats
    
    def analyze_anomalies(self, monitoring_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analisa anomalias nos padrões do sistema
        """
        logger.info("🔍 Analisando anomalias...")
        
        anomalies = []
        system_metrics = monitoring_data.get("system_metrics", {})
        
        # Detectar padrões anômalos
        for metric, value in system_metrics.items():
            if isinstance(value, (int, float)):
                # Simular detecção de anomalia baseada em desvio
                if value > 0.8 or value < 0.05:
                    anomalies.append({
                        "metric": metric,
                        "value": value,
                        "anomaly_type": "statistical_outlier",
                        "confidence": random.uniform(0.6, 0.95)
                    })
        
        analysis = {
            "timestamp": datetime.utcnow().isoformat(),
            "anomalies": anomalies,
            "anomaly_count": len(anomalies),
            "analysis_confidence": sum(a["confidence"] for a in anomalies) / len(anomalies) if anomalies else 1.0
        }
        
        logger.info(f"🔍 {len(anomalies)} anomalias encontradas")
        return analysis
    
    def execute_containment(self, threats: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Executa ações de contenção para ameaças detectadas
        """
        if not threats or not self.containment_enabled:
            return {"actions": [], "containment_success": True}
        
        logger.info("🛡️ Executando contenção...")
        
        containment_actions = []
        
        for threat in threats:
            severity = threat.get("severity", "LOW")
            threat_type = threat.get("type", "unknown")
            
            # Determinar ação de contenção baseada na severidade
            if severity == "CRITICAL":
                action = {
                    "threat_id": threat["id"],
                    "action_type": "emergency_shutdown",
                    "description": "Desligamento de emergência do componente afetado",
                    "success": random.random() > 0.1  # 90% de sucesso
                }
            elif severity == "HIGH":
                action = {
                    "threat_id": threat["id"],
                    "action_type": "resource_throttling",
                    "description": "Limitação de recursos do processo suspeito",
                    "success": random.random() > 0.05  # 95% de sucesso
                }
            else:
                action = {
                    "threat_id": threat["id"],
                    "action_type": "monitoring_increase",
                    "description": "Aumento do nível de monitoramento",
                    "success": True
                }
            
            containment_actions.append(action)
            
            if action["success"]:
                logger.info(f"✅ Contenção bem-sucedida: {action['action_type']}")
            else:
                logger.error(f"❌ Falha na contenção: {action['action_type']}")
        
        # Salvar ações no histórico
        self.containment_actions.extend(containment_actions)
        
        containment_result = {
            "timestamp": datetime.utcnow().isoformat(),
            "actions": containment_actions,
            "total_actions": len(containment_actions),
            "successful_actions": len([a for a in containment_actions if a["success"]]),
            "containment_success": all(a["success"] for a in containment_actions)
        }
        
        logger.info(f"🛡️ {len(containment_actions)} ações de contenção executadas")
        return containment_result
    
    def update_security_metrics(self, monitoring_data: Dict[str, Any], threats: List[Dict[str, Any]]):
        """
        Atualiza métricas de segurança baseado nos resultados
        """
        # Atualizar score de segurança
        base_score = monitoring_data.get("security_score", 1.0)
        threat_penalty = len(threats) * 0.1
        
        self.security_score = max(0.0, base_score - threat_penalty)
        
        # Atualizar nível de ameaça
        critical_threats = len([t for t in threats if t.get("severity") == "CRITICAL"])
        high_threats = len([t for t in threats if t.get("severity") == "HIGH"])
        
        if critical_threats > 0:
            self.threat_level = "CRITICAL"
        elif high_threats > 2:
            self.threat_level = "HIGH"
        elif high_threats > 0 or len(threats) > 3:
            self.threat_level = "MEDIUM"
        else:
            self.threat_level = "LOW"
        
        # Salvar incidentes
        for threat in threats:
            incident = {
                "timestamp": datetime.utcnow().isoformat(),
                "threat": threat,
                "security_score_at_detection": self.security_score
            }
            self.incidents_detected.append(incident)
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna status atual do agente"""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "type": self.type,
            "status": self.status,
            "security_score": self.security_score,
            "threat_level": self.threat_level,
            "incidents_detected_count": len(self.incidents_detected),
            "containment_actions_count": len(self.containment_actions),
            "capabilities": list(self.capabilities.keys()),
            "wave_number": self.wave_number,
            "month_introduced": self.month_introduced,
            "last_update": datetime.utcnow().isoformat()
        }

# Função de teste
def test_guard_agent():
    """Teste básico do agente GUARD"""
    print("🎯 Testando Agente GUARD...")
    
    agent = GuardAgent()
    result = agent.run_security_cycle()
    
    print(f"📊 Resultado: {result.get('success', False)}")
    print(f"🤖 Status: {agent.get_status()}")
    print("✅ Teste concluído!")

if __name__ == "__main__":
    test_guard_agent()
