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

# Importações SUNA existentes
try:
    from ...config.settings import get_setting, SUPABASE_URL, SUPABASE_KEY
except ImportError:
    # Fallback para desenvolvimento
    SUPABASE_URL = os.getenv('SUPABASE_URL', '')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY', '')
    get_setting = lambda key, default=None: os.getenv(key, default)

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
        # Definir valores padrão
        kwargs.setdefault('name', 'CORE')
        kwargs.setdefault('type', 'self_improving')
        super().__init__(**kwargs)
        
        # Aplicar configurações específicas
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

@dataclass
class LearnAgentConfig(AgentConfig):
    """Configuração específica do agente LEARN"""
    min_collaboration_synergy: float = 30.0
    max_learning_sessions: int = 5
    collaboration_timeout: int = 180
    synergy_threshold: float = 0.5
    auto_collaboration_enabled: bool = True
    
    def __init__(self, **kwargs):
        # Definir valores padrão
        kwargs.setdefault('name', 'LEARN')
        kwargs.setdefault('type', 'collaborative')
        super().__init__(**kwargs)
        
        # Aplicar configurações específicas
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

@dataclass
class GuardAgentConfig(AgentConfig):
    """Configuração específica do agente GUARD"""
    max_critical_incidents: int = 0
    threat_threshold: float = 0.7
    auto_containment: bool = True
    security_scan_interval: int = 60
    containment_timeout: int = 30
    
    def __init__(self, **kwargs):
        # Definir valores padrão
        kwargs.setdefault('name', 'GUARD')
        kwargs.setdefault('type', 'security')
        super().__init__(**kwargs)
        
        # Aplicar configurações específicas
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

@dataclass
class MetricsConfig:
    """Configuração do sistema de métricas"""
    enabled: bool = True
    retention_days: int = 30
    analysis_window_hours: int = 24
    collection_interval_minutes: int = 15
    alert_thresholds: Dict[str, float] = None
    
    def __post_init__(self):
        if self.alert_thresholds is None:
            self.alert_thresholds = {
                'performance_drop': 0.2,
                'security_score': 0.7,
                'collaboration_synergy': 0.3
            }

@dataclass
class ValidationConfig:
    """Configuração do sistema de validação"""
    enabled: bool = True
    min_improvement_percentage: float = 20.0
    significance_level: float = 0.05
    min_sample_size: int = 5
    reproducibility_threshold: float = 0.8
    auto_validation: bool = True

@dataclass
class IntegrationConfig:
    """Configuração principal do sistema de integração"""
    system_name: str = "SUNA-ALSHAM"
    version: str = "1.0.0"
    evolution_interval_minutes: int = 60
    max_concurrent_evolutions: int = 3
    auto_start: bool = True
    debug_mode: bool = False
    
    # Configurações dos componentes
    core_agent: CoreAgentConfig = None
    learn_agent: LearnAgentConfig = None
    guard_agent: GuardAgentConfig = None
    metrics: MetricsConfig = None
    validation: ValidationConfig = None
    
    def __post_init__(self):
        if self.core_agent is None:
            self.core_agent = CoreAgentConfig()
        if self.learn_agent is None:
            self.learn_agent = LearnAgentConfig()
        if self.guard_agent is None:
            self.guard_agent = GuardAgentConfig()
        if self.metrics is None:
            self.metrics = MetricsConfig()
        if self.validation is None:
            self.validation = ValidationConfig()

class SUNAAlshamConfig:
    """
    Classe principal de configuração SUNA-ALSHAM
    Integra com sistema de configuração SUNA existente
    """
    
    def __init__(self, config_file: Optional[str] = None):
        self.config_file = config_file
        self._config = None
        self._load_configuration()
    
    def _load_configuration(self):
        """Carrega configuração de múltiplas fontes"""
        
        # 1. Configuração padrão
        default_config = IntegrationConfig()
        
        # 2. Configuração de arquivo (se especificado)
        file_config = self._load_from_file() if self.config_file else {}
        
        # 3. Configuração de variáveis de ambiente
        env_config = self._load_from_environment()
        
        # 4. Mesclar configurações (prioridade: env > file > default)
        merged_config = self._merge_configs(
            asdict(default_config),
            file_config,
            env_config
        )
        
        # 5. Criar objeto de configuração final
        self._config = self._create_config_object(merged_config)
    
    def _load_from_file(self) -> Dict[str, Any]:
        """Carrega configuração de arquivo JSON"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"⚠️ Erro ao carregar arquivo de configuração: {e}")
        return {}
    
    def _load_from_environment(self) -> Dict[str, Any]:
        """Carrega configuração de variáveis de ambiente"""
        env_config = {}
        
        # Configurações gerais
        if os.getenv('SUNA_ALSHAM_EVOLUTION_INTERVAL'):
            env_config['evolution_interval_minutes'] = int(os.getenv('SUNA_ALSHAM_EVOLUTION_INTERVAL'))
        
        if os.getenv('SUNA_ALSHAM_AUTO_START'):
            env_config['auto_start'] = os.getenv('SUNA_ALSHAM_AUTO_START').lower() == 'true'
        
        if os.getenv('SUNA_ALSHAM_DEBUG'):
            env_config['debug_mode'] = os.getenv('SUNA_ALSHAM_DEBUG').lower() == 'true'
        
        # Configurações do agente CORE
        core_config = {}
        if os.getenv('SUNA_ALSHAM_CORE_MIN_IMPROVEMENT'):
            core_config['min_improvement_percentage'] = float(os.getenv('SUNA_ALSHAM_CORE_MIN_IMPROVEMENT'))
        
        if os.getenv('SUNA_ALSHAM_CORE_ENABLED'):
            core_config['enabled'] = os.getenv('SUNA_ALSHAM_CORE_ENABLED').lower() == 'true'
        
        if core_config:
            env_config['core_agent'] = core_config
        
        # Configurações do agente LEARN
        learn_config = {}
        if os.getenv('SUNA_ALSHAM_LEARN_MIN_SYNERGY'):
            learn_config['min_collaboration_synergy'] = float(os.getenv('SUNA_ALSHAM_LEARN_MIN_SYNERGY'))
        
        if os.getenv('SUNA_ALSHAM_LEARN_ENABLED'):
            learn_config['enabled'] = os.getenv('SUNA_ALSHAM_LEARN_ENABLED').lower() == 'true'
        
        if learn_config:
            env_config['learn_agent'] = learn_config
        
        # Configurações do agente GUARD
        guard_config = {}
        if os.getenv('SUNA_ALSHAM_GUARD_MAX_INCIDENTS'):
            guard_config['max_critical_incidents'] = int(os.getenv('SUNA_ALSHAM_GUARD_MAX_INCIDENTS'))
        
        if os.getenv('SUNA_ALSHAM_GUARD_ENABLED'):
            guard_config['enabled'] = os.getenv('SUNA_ALSHAM_GUARD_ENABLED').lower() == 'true'
        
        if guard_config:
            env_config['guard_agent'] = guard_config
        
        # Configurações de métricas
        metrics_config = {}
        if os.getenv('SUNA_ALSHAM_METRICS_RETENTION_DAYS'):
            metrics_config['retention_days'] = int(os.getenv('SUNA_ALSHAM_METRICS_RETENTION_DAYS'))
        
        if os.getenv('SUNA_ALSHAM_METRICS_ENABLED'):
            metrics_config['enabled'] = os.getenv('SUNA_ALSHAM_METRICS_ENABLED').lower() == 'true'
        
        if metrics_config:
            env_config['metrics'] = metrics_config
        
        # Configurações de validação
        validation_config = {}
        if os.getenv('SUNA_ALSHAM_VALIDATION_SIGNIFICANCE'):
            validation_config['significance_level'] = float(os.getenv('SUNA_ALSHAM_VALIDATION_SIGNIFICANCE'))
        
        if os.getenv('SUNA_ALSHAM_VALIDATION_ENABLED'):
            validation_config['enabled'] = os.getenv('SUNA_ALSHAM_VALIDATION_ENABLED').lower() == 'true'
        
        if validation_config:
            env_config['validation'] = validation_config
        
        return env_config
    
    def _merge_configs(self, *configs: Dict[str, Any]) -> Dict[str, Any]:
        """Mescla múltiplas configurações recursivamente"""
        result = {}
        
        for config in configs:
            for key, value in config.items():
                if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                    result[key] = self._merge_configs(result[key], value)
                else:
                    result[key] = value
        
        return result
    
    def _create_config_object(self, config_dict: Dict[str, Any]) -> IntegrationConfig:
        """Cria objeto de configuração a partir de dicionário"""
        try:
            # Criar configurações dos agentes
            core_config = CoreAgentConfig(**config_dict.get('core_agent', {}))
            learn_config = LearnAgentConfig(**config_dict.get('learn_agent', {}))
            guard_config = GuardAgentConfig(**config_dict.get('guard_agent', {}))
            metrics_config = MetricsConfig(**config_dict.get('metrics', {}))
            validation_config = ValidationConfig(**config_dict.get('validation', {}))
            
            # Criar configuração principal
            main_config = {k: v for k, v in config_dict.items() 
                          if k not in ['core_agent', 'learn_agent', 'guard_agent', 'metrics', 'validation']}
            
            return IntegrationConfig(
                **main_config,
                core_agent=core_config,
                learn_agent=learn_config,
                guard_agent=guard_config,
                metrics=metrics_config,
                validation=validation_config
            )
            
        except Exception as e:
            print(f"⚠️ Erro ao criar configuração: {e}")
            return IntegrationConfig()  # Retorna configuração padrão
    
    @property
    def config(self) -> IntegrationConfig:
        """Retorna configuração atual"""
        return self._config
    
    def get_agent_config(self, agent_name: str) -> Optional[AgentConfig]:
        """Retorna configuração de um agente específico"""
        agent_name = agent_name.upper()
        
        if agent_name == 'CORE':
            return self._config.core_agent
        elif agent_name == 'LEARN':
            return self._config.learn_agent
        elif agent_name == 'GUARD':
            return self._config.guard_agent
        else:
            return None
    
    def get_database_config(self) -> Dict[str, str]:
        """Retorna configuração do banco de dados"""
        return {
            'url': SUPABASE_URL,
            'key': SUPABASE_KEY,
            'schema': 'public'
        }
    
    def get_logging_config(self) -> Dict[str, Any]:
        """Retorna configuração de logging"""
        level = 'DEBUG' if self._config.debug_mode else 'INFO'
        
        return {
            'level': level,
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'handlers': ['console', 'file'] if self._config.debug_mode else ['console']
        }
    
    def save_to_file(self, filename: str):
        """Salva configuração atual em arquivo"""
        try:
            config_dict = asdict(self._config)
            with open(filename, 'w') as f:
                json.dump(config_dict, f, indent=2, default=str)
            print(f"✅ Configuração salva em: {filename}")
        except Exception as e:
            print(f"❌ Erro ao salvar configuração: {e}")
    
    def validate_config(self) -> List[str]:
        """Valida configuração atual e retorna lista de problemas"""
        issues = []
        
        # Validar configurações gerais
        if self._config.evolution_interval_minutes < 1:
            issues.append("Intervalo de evolução deve ser >= 1 minuto")
        
        if self._config.max_concurrent_evolutions < 1:
            issues.append("Máximo de evoluções concorrentes deve ser >= 1")
        
        # Validar configurações dos agentes
        if self._config.core_agent.min_improvement_percentage < 0:
            issues.append("Melhoria mínima do CORE deve ser >= 0%")
        
        if self._config.learn_agent.min_collaboration_synergy < 0:
            issues.append("Sinergia mínima do LEARN deve ser >= 0%")
        
        if self._config.guard_agent.max_critical_incidents < 0:
            issues.append("Máximo de incidentes críticos deve ser >= 0")
        
        # Validar configurações de métricas
        if self._config.metrics.retention_days < 1:
            issues.append("Retenção de métricas deve ser >= 1 dia")
        
        # Validar configurações de validação
        if not (0 < self._config.validation.significance_level < 1):
            issues.append("Nível de significância deve estar entre 0 e 1")
        
        # Validar conexão com banco
        if not SUPABASE_URL or not SUPABASE_KEY:
            issues.append("Configurações do Supabase não encontradas")
        
        return issues
    
    def __str__(self) -> str:
        """Representação string da configuração"""
        return f"SUNAAlshamConfig(system={self._config.system_name}, version={self._config.version})"

# Instância global de configuração
_global_config = None

def get_config(config_file: Optional[str] = None) -> SUNAAlshamConfig:
    """
    Retorna instância global de configuração SUNA-ALSHAM
    """
    global _global_config
    
    if _global_config is None:
        _global_config = SUNAAlshamConfig(config_file)
    
    return _global_config

def reload_config(config_file: Optional[str] = None):
    """
    Recarrega configuração global
    """
    global _global_config
    _global_config = SUNAAlshamConfig(config_file)

# Funções de conveniência
def get_agent_config(agent_name: str) -> Optional[AgentConfig]:
    """Retorna configuração de um agente específico"""
    return get_config().get_agent_config(agent_name)

def get_database_config() -> Dict[str, str]:
    """Retorna configuração do banco de dados"""
    return get_config().get_database_config()

def is_debug_mode() -> bool:
    """Verifica se está em modo debug"""
    return get_config().config.debug_mode
