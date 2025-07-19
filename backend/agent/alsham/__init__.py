"""
SUNA-ALSHAM Integration Module
Sistema de Agentes Auto-Evolutivos integrado ao SUNA

Este módulo contém os agentes auto-evolutivos:
- CORE: Agente auto-melhorável
- LEARN: Agente colaborativo
- GUARD: Agente de segurança

Integração com infraestrutura SUNA existente.
"""

from .core_agent import CoreAgent
from .learn_agent import LearnAgent
from .guard_agent import GuardAgent
from .metrics_system import MetricsSystem
from .validation_system import ValidationSystem
from .integration import SUNAAlshamIntegration

__version__ = "1.0.0"
__author__ = "SUNA-ALSHAM Team"

__all__ = [
    "CoreAgent",
    "LearnAgent", 
    "GuardAgent",
    "MetricsSystem",
    "ValidationSystem",
    "SUNAAlshamIntegration"
]
