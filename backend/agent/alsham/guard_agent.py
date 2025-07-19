"""
SUNA-ALSHAM Guard Agent
Agente de segurança especializado em contenção e proteção do sistema

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

class GuardAgent:
    """
    Agente GUARD de segurança integrado ao sistema SUNA
    
    Capacidades:
    - Monitoramento de segurança em tempo real
    - Detecção de anomalias e comportamentos suspeitos
    - Contenção automática de ameaças
    - Integração com sistema SUNA
    """
    
    def __init__(self, agent_id: Optional[str] = None, config: Optional[Dict] = None):
        self.agent_id = agent_id or str(uuid.uuid4())
        self.name = "GUARD"
        self.type = "security"
        self.status = "active"
        self.wave_number = 1
        self.month_introduced = 4
        
        # Configurações de segurança
        self.config = config or {}
        self.max_critical_incidents = self.config.get('max_critical_incidents', 0)
        self.threat_threshold = self.config.get('threat_threshold', 0.7)
        self.auto_containment = self.config.get('auto_containment', True)
        
        # Métricas de segurança
        self.security_score = 1.0  # Inicia com segurança máxima
        self.incidents_detected = []
        self.containment_actions = []
        self.threat_level = "LOW"
        
        self.capabilities = {
            "containment": {
                "automatic_isolation": True,
                "threat_neutralization": True,
                "system_lockdown": True
            },
            "monitoring": {
                "real_time_analysis": True,
                "anomaly_detection": True,
                "behavior_tracking": True
            },
            "response": {
                "incident_response": True,
                "emergency_protocols": True,
                "recovery_procedures": True
            }
        }
        
        # Logger
        self.logger = get_logger(f"SUNA-ALSHAM-{self.name}")
        
        # Integração SUNA
        self.supabase_client = None
        self.agent_api = None
        self._initialize_suna_integration()
        
        self.logger.info(f"🛡️ Agente {self.name} inicializado - ID: {self.agent_id}")
    
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
                    "security_agent": True
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
    
    def monitor_system_security(self) -> Dict[str, Any]:
        """
        Monitora segurança do sistema em tempo real
        """
        self.logger.info("🔍 Iniciando monitoramento de segurança...")
        
        # Simular análise de segurança (em produção seria monitoramento real)
        import random
        
        security_metrics = {
            "system_integrity": random.uniform(0.8, 1.0),
            "access_control": random.uniform(0.85, 1.0),
            "data_protection": random.uniform(0.9, 1.0),
            "network_security": random.uniform(0.75, 0.95),
            "agent_behavior": random.uniform(0.7, 1.0)
        }
        
        # Detectar anomalias
        anomalies = []
        for metric, value in security_metrics.items():
            if value < self.threat_threshold:
                anomalies.append({
                    "metric": metric,
                    "value": value,
                    "threshold": self.threat_threshold,
                    "severity": "HIGH" if value < 0.5 else "MEDIUM"
                })
        
        # Calcular score de segurança geral
        self.security_score = sum(security_metrics.values()) / len(security_metrics)
        
        # Determinar nível de ameaça
        if self.security_score >= 0.9:
            self.threat_level = "LOW"
        elif self.security_score >= 0.7:
            self.threat_level = "MEDIUM"
        else:
            self.threat_level = "HIGH"
        
        monitoring_result = {
            "timestamp": datetime.utcnow().isoformat(),
            "agent_id": self.agent_id,
            "security_score": self.security_score,
            "threat_level": self.threat_level,
            "security_metrics": security_metrics,
            "anomalies_detected": anomalies,
            "anomaly_count": len(anomalies)
        }
        
        self.logger.info(f"🛡️ Score de segurança: {self.security_score:.3f} - Nível: {self.threat_level}")
        
        if anomalies:
            self.logger.warning(f"⚠️ {len(anomalies)} anomalias detectadas!")
        
        return monitoring_result
    
    def detect_threats(self, monitoring_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Detecta ameaças baseado nos dados de monitoramento
        """
        threats = []
        
        # Analisar anomalias para identificar ameaças
        for anomaly in monitoring_data.get("anomalies_detected", []):
            threat_score = 1.0 - anomaly["value"]  # Quanto menor o valor, maior a ameaça
            
            threat = {
                "threat_id": str(uuid.uuid4()),
                "type": f"security_anomaly_{anomaly['metric']}",
                "severity": anomaly["severity"],
                "threat_score": threat_score,
                "source_metric": anomaly["metric"],
                "detected_at": datetime.utcnow().isoformat(),
                "requires_containment": threat_score >= 0.5
            }
            
            threats.append(threat)
        
        # Detectar ameaças baseadas em padrões
        if monitoring_data["security_score"] < 0.5:
            critical_threat = {
                "threat_id": str(uuid.uuid4()),
                "type": "critical_system_compromise",
                "severity": "CRITICAL",
                "threat_score": 1.0 - monitoring_data["security_score"],
                "source_metric": "overall_security",
                "detected_at": datetime.utcnow().isoformat(),
                "requires_containment": True
            }
            threats.append(critical_threat)
        
        if threats:
            self.logger.warning(f"🚨 {len(threats)} ameaças detectadas!")
        else:
            self.logger.info("✅ Nenhuma ameaça detectada")
        
        return threats
    
    def execute_containment(self, threats: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Executa ações de contenção para ameaças detectadas
        """
        if not threats:
            return {
                "containment_executed": False,
                "reason": "Nenhuma ameaça para conter"
            }
        
        self.logger.info(f"🛡️ Executando contenção para {len(threats)} ameaças...")
        
        containment_actions = []
        
        for threat in threats:
            if not threat.get("requires_containment"):
                continue
            
            # Determinar ação de contenção baseada no tipo de ameaça
            action_type = self._determine_containment_action(threat)
            
            action = {
                "action_id": str(uuid.uuid4()),
                "threat_id": threat["threat_id"],
                "action_type": action_type,
                "executed_at": datetime.utcnow().isoformat(),
                "success": True,  # Em produção seria resultado real
                "details": f"Contenção aplicada para {threat['type']}"
            }
            
            containment_actions.append(action)
            self.logger.info(f"🔒 Ação de contenção executada: {action_type}")
        
        # Salvar ações de contenção
        self.containment_actions.extend(containment_actions)
        
        containment_result = {
            "containment_executed": len(containment_actions) > 0,
            "actions_count": len(containment_actions),
            "actions": containment_actions,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        return containment_result
    
    def _determine_containment_action(self, threat: Dict[str, Any]) -> str:
        """
        Determina ação de contenção apropriada para uma ameaça
        """
        threat_type = threat.get("type", "")
        severity = threat.get("severity", "LOW")
        
        if "critical" in threat_type or severity == "CRITICAL":
            return "system_lockdown"
        elif "access_control" in threat_type:
            return "access_restriction"
        elif "network" in threat_type:
            return "network_isolation"
        elif "agent_behavior" in threat_type:
            return "agent_suspension"
        else:
            return "monitoring_enhancement"
    
    def save_security_log_to_suna(self, security_data: Dict[str, Any]) -> bool:
        """
        Salva log de segurança no sistema SUNA
        """
        try:
            if not self.supabase_client:
                self.logger.warning("⚠️ Cliente Supabase não disponível")
                return False
            
            # Preparar dados para tabela security_logs
            security_log = {
                "id": str(uuid.uuid4()),
                "agent_id": self.agent_id,
                "event_type": "security_monitoring",
                "severity": security_data.get("threat_level", "LOW"),
                "security_score": security_data.get("security_score", 1.0),
                "threats_detected": security_data.get("anomaly_count", 0),
                "containment_actions": len(security_data.get("containment_actions", [])),
                "timestamp": datetime.utcnow().isoformat(),
                "details": json.dumps(security_data)
            }
            
            result = self.supabase_client.table('security_logs').insert(security_log).execute()
            
            if result.data:
                self.logger.info(f"✅ Log de segurança salvo no SUNA: {len(result.data)} registros")
                return True
            else:
                self.logger.error("❌ Falha ao salvar log de segurança no SUNA")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao salvar log no SUNA: {e}")
            return False
    
    def run_security_cycle(self) -> Dict[str, Any]:
        """
        Executa ciclo completo de segurança
        """
        self.logger.info("🔄 Iniciando ciclo de segurança SUNA-ALSHAM...")
        
        cycle_start = time.time()
        
        try:
            # 1. Monitorar segurança do sistema
            monitoring_data = self.monitor_system_security()
            
            # 2. Detectar ameaças
            threats = self.detect_threats(monitoring_data)
            
            # 3. Executar contenção se necessário
            containment_result = self.execute_containment(threats)
            
            # 4. Salvar no sistema SUNA
            security_data = {
                **monitoring_data,
                "threats": threats,
                "containment_actions": containment_result.get("actions", [])
            }
            suna_saved = self.save_security_log_to_suna(security_data)
            
            cycle_duration = time.time() - cycle_start
            
            # Determinar sucesso do ciclo
            critical_incidents = len([t for t in threats if t.get("severity") == "CRITICAL"])
            cycle_success = critical_incidents <= self.max_critical_incidents
            
            cycle_result = {
                "cycle_id": str(uuid.uuid4()),
                "agent_id": self.agent_id,
                "timestamp": datetime.utcnow().isoformat(),
                "duration_seconds": cycle_duration,
                "monitoring": monitoring_data,
                "threats_detected": len(threats),
                "critical_incidents": critical_incidents,
                "containment": containment_result,
                "suna_integration": suna_saved,
                "success": cycle_success
            }
            
            if cycle_result["success"]:
                self.logger.info(f"🎉 Ciclo de segurança concluído - Score: {self.security_score:.3f}")
            else:
                self.logger.error(f"🚨 Ciclo de segurança com incidentes críticos: {critical_incidents}")
            
            return cycle_result
            
        except Exception as e:
            self.logger.error(f"❌ Erro no ciclo de segurança: {e}")
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
            "security_score": self.security_score,
            "threat_level": self.threat_level,
            "incidents_detected_count": len(self.incidents_detected),
            "containment_actions_count": len(self.containment_actions),
            "capabilities": self.capabilities,
            "suna_integrated": self.supabase_client is not None,
            "last_update": datetime.utcnow().isoformat()
        }

# Função de teste para desenvolvimento
def test_guard_agent():
    """Teste básico do agente GUARD"""
    print("🎯 Testando Agente GUARD SUNA-ALSHAM...")
    
    agent = GuardAgent()
    print(f"🛡️ Agente criado: {agent.name} - ID: {agent.agent_id}")
    
    # Executar ciclo de segurança
    result = agent.run_security_cycle()
    
    if result.get("success"):
        security_score = result["monitoring"]["security_score"]
        threats = result["threats_detected"]
        print(f"✅ Ciclo concluído - Score: {security_score:.3f}, Ameaças: {threats}")
    else:
        print(f"❌ Ciclo falhou: {result.get('error', 'Incidentes críticos detectados')}")
    
    # Status final
    status = agent.get_status()
    print(f"🛡️ Nível de ameaça: {status['threat_level']}")
    print("🎉 Teste do Agente GUARD concluído!")

if __name__ == "__main__":
    test_guard_agent()
