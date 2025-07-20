"""
SUNA-ALSHAM Configuration Module
Carrega e valida as configurações do sistema a partir de variáveis de ambiente.
"""

import os
from dataclasses import dataclass, field
from typing import List

def _get_env_bool(name: str, default: bool) -> bool:
    return os.getenv(name, str(default)).lower() in ('true', '1', 't')

@dataclass
class CoreAgentConfig:
    enabled: bool = field(default_factory=lambda: _get_env_bool("SUNA_ALSHAM_CORE_ENABLED", True))
    min_improvement_percentage: float = field(default_factory=lambda: float(os.getenv("SUNA_ALSHAM_CORE_MIN_IMPROVEMENT", 20.0)))

@dataclass
class LearnAgentConfig:
    enabled: bool = field(default_factory=lambda: _get_env_bool("SUNA_ALSHAM_LEARN_ENABLED", True))
    min_synergy_score: float = field(default_factory=lambda: float(os.getenv("SUNA_ALSHAM_LEARN_MIN_SYNERGY", 30.0)))

@dataclass
class GuardAgentConfig:
    enabled: bool = field(default_factory=lambda: _get_env_bool("SUNA_ALSHAM_GUARD_ENABLED", True))
    max_critical_incidents: int = field(default_factory=lambda: int(os.getenv("SUNA_ALSHAM_GUARD_MAX_INCIDENTS", 0)))

@dataclass
class MetricsConfig:
    enabled: bool = field(default_factory=lambda: _get_env_bool("SUNA_ALSHAM_METRICS_ENABLED", True))
    retention_days: int = field(default_factory=lambda: int(os.getenv("SUNA_ALSHAM_METRICS_RETENTION_DAYS", 30)))

@dataclass
class ValidationConfig:
    enabled: bool = field(default_factory=lambda: _get_env_bool("SUNA_ALSHAM_VALIDATION_ENABLED", True))
    significance_level: float = field(default_factory=lambda: float(os.getenv("SUNA_ALSHAM_VALIDATION_SIGNIFICANCE", 0.05)))

@dataclass
class IntegrationConfig:
    system_name: str = "SUNA-ALSHAM"
    version: str = "1.0.0"
    auto_start: bool = field(default_factory=lambda: _get_env_bool("SUNA_ALSHAM_AUTO_START", True))
    evolution_interval_minutes: int = field(default_factory=lambda: int(os.getenv("SUNA_ALSHAM_EVOLUTION_INTERVAL", 60)))
    debug_mode: bool = field(default_factory=lambda: _get_env_bool("SUNA_ALSHAM_DEBUG", False))
    
    core_agent: CoreAgentConfig = field(default_factory=CoreAgentConfig)
    learn_agent: LearnAgentConfig = field(default_factory=LearnAgentConfig)
    guard_agent: GuardAgentConfig = field(default_factory=GuardAgentConfig)
    metrics: MetricsConfig = field(default_factory=MetricsConfig)
    validation: ValidationConfig = field(default_factory=ValidationConfig)

# Esta é a classe principal que estava faltando ou com nome errado
class SUNAAlshamConfig:
    """
    Classe principal para carregar e fornecer a configuração do sistema.
    """
    def __init__(self, config_file: str = None):
        # O argumento config_file é mantido para compatibilidade, mas não é usado
        # pois a configuração é totalmente baseada em variáveis de ambiente.
        self.config = IntegrationConfig()

    def get_config(self) -> IntegrationConfig:
        return self.config

    def reload_config(self):
        self.config = IntegrationConfig()
        return self.config
