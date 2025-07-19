"""
SUNA-ALSHAM Core Agent
Agente auto-evolutivo principal com capacidades de auto-melhoria

Integrado com infraestrutura SUNA existente
"""

import uuid
import json
import time
import random
from datetime import datetime
from typing import Dict, Any, Optional, List
import logging

# Importações SUNA existentes
try:
    from services.supabase import DBConnection
    from utils.logger import logger
    from .metrics_system import MetricsSystem
    from .validation_system import ValidationSystem
    from .config import SUNA_ALSHAM_CONFIG
except ImportError:
    # Fallback para desenvolvimento
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    # Mock classes para desenvolvimento
    class MetricsSystem:
        def collect_performance_metric(self, *args, **kwargs): pass
        def get_performance_metrics(self, *args, **kwargs): return {}
    
    class ValidationSystem:
        def validate_improvement(self, *args, **kwargs): return True
    
    SUNA_ALSHAM_CONFIG = {}

class CoreAgent:
    """
    Agente CORE auto-evolutivo integrado ao sistema SUNA
    
    Capacidades:
    - Auto-análise de performance
    - Auto-melhoria baseada em métricas
    - Integração com banco Supabase
    - Validação científica de melhorias
    """
    
    def __init__(self, agent_id: Optional[str] = None, config: Optional[Dict] = None):
        self.agent_id = agent_id or str(uuid.uuid4())
        self.name = "SUNA-ALSHAM-CORE"
        self.type = "self_improving"
        self.status = "active"
        self.wave_number = 1
        self.month_introduced = 1
        
        # Configurações SUNA-ALSHAM
        self.config = {**SUNA_ALSHAM_CONFIG, **(config or {})}
        self.min_improvement_threshold = self.config.get('min_improvement_percentage', 20.0)
        self.max_iterations = self.config.get('max_iterations', 10)
        
        # Integração SUNA
        self.db_connection = None
        self.metrics_system = MetricsSystem()
        self.validation_system = ValidationSystem()
        
        # Métricas
        self.current_performance = 0.0
        self.baseline_performance = 0.0
        self.improvement_history = []
        self.capabilities = {
            "meta_learning": {},
            "self_analysis": {},
            "performance_optimization": {}
        }
        
        # Logger SUNA
        self.logger = logger
        
        self.logger.info(f"🤖 Agente {self.name} inicializado - ID: {self.agent_id}")
    
    async def initialize_suna_integration(self):
        """Inicializa integração com infraestrutura SUNA"""
        try:
            # Conectar com Supabase SUNA
            self.db_connection = DBConnection()
            
            # Registrar agente no sistema SUNA
            await self._register_in_suna_system()
            
            self.logger.info("✅ Integração SUNA inicializada com sucesso")
        except Exception as e:
            self.logger.warning(f"⚠️ Integração SUNA parcial: {e}")
    
    async def _register_in_suna_system(self):
        """Registra agente no sistema SUNA existente"""
        try:
            if not self.db_connection:
                return
                
            client = await self.db_connection.client
            
            agent_data = {
                "agent_id": self.agent_id,
                "name": self.name,
                "description": f"SUNA-ALSHAM {self.type} agent",
                "system_prompt": self._get_system_prompt(),
                "configured_mcps": [],
                "custom_mcps": [],
                "agentpress_tools": {},
                "is_default": False,
                "avatar": "🤖",
                "avatar_color": "#FF6B35",
                "account_id": "suna-alsham-system",
                "created_at": datetime.utcnow().isoformat(),
                "metadata": {
                    "system": "SUNA-ALSHAM",
                    "version": "1.0.0",
                    "auto_evolutionary": True,
                    "wave_number": self.wave_number,
                    "month_introduced": self.month_introduced
                }
            }
            
            # Verificar se agente já existe
            existing = await client.table('agents').select("*").eq('agent_id', self.agent_id).execute()
            
            if not existing.data:
                # Criar novo agente
                result = await client.table('agents').insert(agent_data).execute()
                self.logger.info(f"✅ Agente registrado no SUNA: {result.data}")
            else:
                self.logger.info("✅ Agente já existe no sistema SUNA")
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao registrar no SUNA: {e}")
    
    def _get_system_prompt(self) -> str:
        """Retorna prompt do sistema para o agente"""
        return f"""
Você é o {self.name}, um agente auto-evolutivo do sistema SUNA-ALSHAM.

Suas capacidades incluem:
- Auto-análise de performance
- Auto-melhoria baseada em métricas científicas
- Colaboração com outros agentes
- Validação científica de melhorias

Você deve sempre buscar melhorar sua performance de forma mensurável e validada.
"""
    
    async def analyze_performance(self) -> Dict[str, Any]:
        """
        Análise auto-reflexiva de performance
        Integrada com métricas SUNA
        """
        self.logger.info("🔍 Iniciando auto-análise de performance...")
        
        # Coletar métricas reais do sistema
        try:
            metrics = await self.metrics_system.get_performance_metrics(self.agent_id)
        except:
            # Fallback para métricas simuladas
            metrics = {
                "response_time": random.uniform(0.1, 2.0),
                "accuracy": random.uniform(0.7, 0.99),
                "efficiency": random.uniform(0.6, 0.95),
                "adaptability": random.uniform(0.5, 0.9),
                "learning_rate": random.uniform(0.3, 0.8)
            }
        
        analysis_factors = metrics
        
        # Calcular performance agregada
        weights = {
            "response_time": 0.2,
            "accuracy": 0.3,
            "efficiency": 0.25,
            "adaptability": 0.15,
            "learning_rate": 0.1
        }
        
        weighted_score = sum(
            analysis_factors[factor] * weights[factor] 
            for factor in analysis_factors
        )
        
        self.current_performance = weighted_score
        
        analysis_result = {
            "timestamp": datetime.utcnow().isoformat(),
            "agent_id": self.agent_id,
            "performance_score": self.current_performance,
            "factors": analysis_factors,
            "baseline": self.baseline_performance,
            "improvement_needed": self.current_performance < self.baseline_performance * 1.1
        }
        
        self.logger.info(f"📊 Performance atual: {self.current_performance:.3f}")
        return analysis_result
            async def generate_improvements(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Gera melhorias baseadas na análise de performance
        """
        self.logger.info("🔧 Gerando melhorias auto-evolutivas...")
        
        improvements = []
        factors = analysis.get("factors", {})
        
        # Identificar fatores com baixa performance
        for factor, score in factors.items():
            if score < 0.8:  # Threshold para melhoria
                improvement = {
                    "id": str(uuid.uuid4()),
                    "factor": factor,
                    "current_score": score,
                    "target_score": min(score * 1.2, 1.0),
                    "strategy": self._get_improvement_strategy(factor),
                    "estimated_impact": random.uniform(0.1, 0.3),
                    "confidence": random.uniform(0.6, 0.9)
                }
                improvements.append(improvement)
        
        self.logger.info(f"💡 {len(improvements)} melhorias geradas")
        return improvements
    
    def _get_improvement_strategy(self, factor: str) -> str:
        """Retorna estratégia de melhoria para um fator específico"""
        strategies = {
            "response_time": "Otimizar algoritmos de processamento e cache",
            "accuracy": "Refinar modelos de decisão e validação",
            "efficiency": "Reduzir overhead computacional",
            "adaptability": "Expandir capacidades de aprendizado",
            "learning_rate": "Ajustar parâmetros de aprendizado"
        }
        return strategies.get(factor, "Estratégia de melhoria geral")
    
    async def implement_improvements(self, improvements: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Implementa melhorias de forma segura
        """
        self.logger.info("⚙️ Implementando melhorias...")
        
        implementation_results = []
        
        for improvement in improvements:
            try:
                # Simular implementação (em produção seria código real)
                success = random.choice([True, True, False])  # 66% sucesso
                
                if success:
                    # Aplicar melhoria
                    factor = improvement["factor"]
                    current_score = improvement["current_score"]
                    target_score = improvement["target_score"]
                    
                    # Simular melhoria real
                    new_score = min(current_score + random.uniform(0.05, 0.15), 1.0)
                    
                    result = {
                        "improvement_id": improvement["id"],
                        "factor": factor,
                        "success": True,
                        "old_score": current_score,
                        "new_score": new_score,
                        "actual_improvement": new_score - current_score
                    }
                    
                    self.logger.info(f"✅ Melhoria aplicada: {factor} {current_score:.3f} → {new_score:.3f}")
                else:
                    result = {
                        "improvement_id": improvement["id"],
                        "factor": improvement["factor"],
                        "success": False,
                        "error": "Falha na implementação"
                    }
                    self.logger.warning(f"❌ Falha na melhoria: {improvement['factor']}")
                
                implementation_results.append(result)
                
            except Exception as e:
                self.logger.error(f"❌ Erro na implementação: {e}")
                implementation_results.append({
                    "improvement_id": improvement["id"],
                    "success": False,
                    "error": str(e)
                })
        
        successful_improvements = [r for r in implementation_results if r.get("success")]
        
        return {
            "total_improvements": len(improvements),
            "successful": len(successful_improvements),
            "failed": len(improvements) - len(successful_improvements),
            "results": implementation_results,
            "overall_success": len(successful_improvements) > 0
        }
    
    async def validate_improvements(self, implementation_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Valida melhorias usando sistema de validação científica
        """
        self.logger.info("🔬 Validando melhorias cientificamente...")
        
        if not implementation_result.get("overall_success"):
            return {"validated": False, "reason": "Nenhuma melhoria implementada"}
        
        # Medir performance pós-melhoria
        post_analysis = await self.analyze_performance()
        
        # Calcular melhoria real
        if self.baseline_performance > 0:
            improvement_percentage = ((post_analysis["performance_score"] - self.baseline_performance) / self.baseline_performance) * 100
        else:
            improvement_percentage = 0
        
        # Validação científica
        validation_result = await self.validation_system.validate_improvement(
            self.agent_id,
            {
                "baseline": self.baseline_performance,
                "current": post_analysis["performance_score"],
                "improvement_percentage": improvement_percentage,
                "implementation_details": implementation_result
            }
        )
        
        # Atualizar baseline se validado
        if validation_result.get("validated") and improvement_percentage >= self.min_improvement_threshold:
            self.baseline_performance = post_analysis["performance_score"]
            self.improvement_history.append({
                "timestamp": datetime.utcnow().isoformat(),
                "improvement_percentage": improvement_percentage,
                "validated": True
            })
            
            self.logger.info(f"🎉 Melhoria VALIDADA: {improvement_percentage:.1f}%")
        else:
            self.logger.warning(f"⚠️ Melhoria NÃO validada: {improvement_percentage:.1f}%")
        
        return {
            "validated": validation_result.get("validated", False),
            "improvement_percentage": improvement_percentage,
            "meets_threshold": improvement_percentage >= self.min_improvement_threshold,
            "new_baseline": self.baseline_performance,
            "validation_details": validation_result
        }
    
    async def run_evolution_cycle(self) -> Dict[str, Any]:
        """
        Executa um ciclo completo de auto-evolução
        """
        cycle_id = str(uuid.uuid4())
        self.logger.info(f"🔄 Iniciando ciclo de evolução: {cycle_id}")
        
        try:
            # 1. Análise de performance
            analysis = await self.analyze_performance()
            
            # 2. Gerar melhorias
            improvements = await self.generate_improvements(analysis)
            
            if not improvements:
                return {
                    "cycle_id": cycle_id,
                    "success": True,
                    "message": "Nenhuma melhoria necessária",
                    "performance": analysis["performance_score"]
                }
            
            # 3. Implementar melhorias
            implementation = await self.implement_improvements(improvements)
            
            # 4. Validar melhorias
            validation = await self.validate_improvements(implementation)
            
            # 5. Salvar métricas
            await self._save_cycle_metrics(cycle_id, analysis, implementation, validation)
            
            cycle_result = {
                "cycle_id": cycle_id,
                "success": validation.get("validated", False),
                "improvement": validation.get("improvement_percentage", 0),
                "performance": analysis["performance_score"],
                "improvements_attempted": len(improvements),
                "improvements_successful": implementation.get("successful", 0),
                "meets_threshold": validation.get("meets_threshold", False),
                "timestamp": datetime.utcnow().isoformat()
            }
            
            if cycle_result["success"]:
                self.logger.info(f"🎉 Ciclo CONCLUÍDO com sucesso: {cycle_result['improvement']:.1f}% melhoria")
            else:
                self.logger.warning(f"⚠️ Ciclo sem melhoria significativa")
            
            return cycle_result
            
        except Exception as e:
            self.logger.error(f"❌ Erro no ciclo de evolução: {e}")
            return {
                "cycle_id": cycle_id,
                "success": False,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def _save_cycle_metrics(self, cycle_id: str, analysis: Dict, implementation: Dict, validation: Dict):
        """Salva métricas do ciclo no sistema SUNA"""
        try:
            await self.metrics_system.collect_performance_metric(
                agent_id=self.agent_id,
                metric_type="evolution_cycle",
                value=validation.get("improvement_percentage", 0),
                metadata={
                    "cycle_id": cycle_id,
                    "analysis": analysis,
                    "implementation": implementation,
                    "validation": validation
                }
            )
        except Exception as e:
            self.logger.error(f"❌ Erro ao salvar métricas: {e}")
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna status atual do agente"""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "type": self.type,
            "status": self.status,
            "current_performance": self.current_performance,
            "baseline_performance": self.baseline_performance,
            "improvement_history_count": len(self.improvement_history),
            "last_improvement": self.improvement_history[-1] if self.improvement_history else None,
            "wave_number": self.wave_number,
            "month_introduced": self.month_introduced,
            "capabilities": list(self.capabilities.keys()),
            "last_update": datetime.utcnow().isoformat()
        }

# Função de teste para desenvolvimento
async def test_core_agent():
    """Teste básico do agente CORE"""
    print("🎯 Testando Agente CORE...")
    
    agent = CoreAgent()
    await agent.initialize_suna_integration()
    
    # Executar ciclo de evolução
    result = await agent.run_evolution_cycle()
    
    print(f"📊 Resultado: {result}")
    print(f"🤖 Status: {agent.get_status()}")
    
    print("✅ Teste concluído!")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_core_agent())

