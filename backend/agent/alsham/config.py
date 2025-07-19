"""
SUNA-ALSHAM Configuration
Configurações específicas para agentes auto-evolutivos

Integra com sistema de configuração SUNA existente
"""

import os
import json
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from datetime import timedelta

@dataclass
class AgentConfig:
    """Configuração base para agentes"""
    name: str
    type: str
    enabled: bool = True
    max_iterations: int = 10
    timeout_seconds: int = 300
    retry_attempts: int = 3
    
@dataclass
class CoreAgentConfig(AgentConfig):
    """Configuração específica do agente CORE"""
    min_improvement_percentage: float = 20.0
    max_performance_iterations: int = 5
    baseline_performance: float = 0.0
    performance_threshold: float = 0.8
    auto_improvement_enabled: bool = True
    
    def __init__(self, **kwargs):
        kwargs.setdefault('name', 'CORE')
        kwargs.setdefault('type', 'self_improving')
        super().__init__(**kwargs)

@dataclass
class LearnAgentConfig(AgentConfig):
    """Configuração específica do agente LEARN"""
    min_collaboration_synergy: float = 30.0
    max_learning_sessions: int = 5
    collaboration_threshold: float = 0.7
    
    def __init__(self, **kwargs):
        kwargs.setdefault('name', 'LEARN')
        kwargs.setdefault('type', 'collaborative')
        super().__init__(**kwargs)

@dataclass
class GuardAgentConfig(AgentConfig):
    """Configuração específica do agente GUARD"""
    max_critical_incidents: int = 0
    threat_threshold: float = 0.3
    containment_enabled: bool = True
    
    def __init__(self, **kwargs):
        kwargs.setdefault('name', 'GUARD')
        kwargs.setdefault('type', 'security')
        super().__init__(**kwargs)

# Configuração global
SUNA_ALSHAM_CONFIG = {
    "system_name": "SUNA-ALSHAM",
    "version": "1.0.0",
    "auto_start": os.getenv('SUNA_ALSHAM_AUTO_START', 'false').lower() == 'true',
    "evolution_interval": int(os.getenv('SUNA_ALSHAM_EVOLUTION_INTERVAL', '60')),
    "agents": {
        "core": CoreAgentConfig(),
        "learn": LearnAgentConfig(), 
        "guard": GuardAgentConfig()
    }
}

def get_config():
    """Retorna configuração SUNA-ALSHAM"""
    return SUNA_ALSHAM_CONFIG
