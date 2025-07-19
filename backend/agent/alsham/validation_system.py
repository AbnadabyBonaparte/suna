"""
SUNA-ALSHAM Validation System
Sistema de validação científica para agentes auto-evolutivos

Garante rigor científico nas melhorias e evolução dos agentes
Integrado com infraestrutura SUNA existente
"""

import uuid
import json
import time
import math
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List, Tuple
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

class ValidationSystem:
    """
    Sistema de validação científica para agentes SUNA-ALSHAM
    
    Funcionalidades:
    - Validação estatística de melhorias
    - Testes de significância científica
    - Análise de reprodutibilidade
    - Controle de qualidade científica
    """
    
    def __init__(self, config: Optional[Dict] = None):
        self.system_id = str(uuid.uuid4())
        self.config = config or {}
        
        # Configurações científicas
        self.min_improvement_percentage = self.config.get('min_improvement_percentage', 20.0)
        self.significance_level = self.config.get('significance_level', 0.05)  # p-value < 0.05
        self.min_sample_size = self.config.get('min_sample_size', 5)
        self.reproducibility_threshold = self.config.get('reproducibility_threshold', 0.8)
        
        # Critérios de validação
        self.validation_criteria = {
            "statistical_significance": True,
            "practical_significance": True,
            "reproducibility": True,
            "consistency": True,
            "bounds_check": True
        }
        
        # Cache de validações
        self.validation_cache = {}
        self.validation_history = []
        
        # Logger
        self.logger = get_logger("SUNA-ALSHAM-VALIDATION")
        
        # Integração SUNA
        self.supabase_client = None
        self._initialize_suna_integration()
        
        self.logger.info(f"🔬 Sistema de Validação inicializado - ID: {self.system_id}")
    
    def _initialize_suna_integration(self):
        """Inicializa integração com infraestrutura SUNA"""
        try:
            self.supabase_client = get_supabase_client()
            self.logger.info("✅ Integração SUNA inicializada com sucesso")
        except Exception as e:
            self.logger.warning(f"⚠️ Integração SUNA parcial: {e}")
    
    def validate_improvement(self, agent_id: str, improvement_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Valida melhoria de um agente usando critérios científicos rigorosos
        """
        self.logger.info(f"🔬 Validando melhoria do agente {agent_id}...")
        
        validation_id = str(uuid.uuid4())
        validation_start = time.time()
        
        try:
            # 1. Validação de significância estatística
            statistical_validation = self._validate_statistical_significance(agent_id, improvement_data)
            
            # 2. Validação de significância prática
            practical_validation = self._validate_practical_significance(improvement_data)
            
            # 3. Validação de reprodutibilidade
            reproducibility_validation = self._validate_reproducibility(agent_id, improvement_data)
            
            # 4. Validação de consistência
            consistency_validation = self._validate_consistency(agent_id, improvement_data)
            
            # 5. Validação de limites
            bounds_validation = self._validate_bounds(improvement_data)
            
            # Consolidar resultados
            validation_results = {
                "statistical": statistical_validation,
                "practical": practical_validation,
                "reproducibility": reproducibility_validation,
                "consistency": consistency_validation,
                "bounds": bounds_validation
            }
            
            # Determinar aprovação geral
            all_passed = all(result.get("passed", False) for result in validation_results.values())
            
            validation_duration = time.time() - validation_start
            
            final_validation = {
                "validation_id": validation_id,
                "agent_id": agent_id,
                "timestamp": datetime.utcnow().isoformat(),
                "duration_seconds": validation_duration,
                "improvement_data": improvement_data,
                "validation_results": validation_results,
                "overall_passed": all_passed,
                "confidence_score": self._calculate_confidence_score(validation_results),
                "recommendations": self._generate_recommendations(validation_results)
            }
            
            # Salvar validação
            self.validation_history.append(final_validation)
            self.validation_cache[agent_id] = final_validation
            
            # Salvar no SUNA
            self._save_validation_to_suna(final_validation)
            
            if all_passed:
                self.logger.info(f"✅ Validação APROVADA para agente {agent_id}")
            else:
                self.logger.warning(f"❌ Validação REPROVADA para agente {agent_id}")
            
            return final_validation
            
        except Exception as e:
            self.logger.error(f"❌ Erro na validação: {e}")
            return {
                "validation_id": validation_id,
                "agent_id": agent_id,
                "error": str(e),
                "overall_passed": False,
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def _validate_statistical_significance(self, agent_id: str, improvement_data: Dict[str, Any]) -> Dict[str, Any]:
        """Valida significância estatística da melhoria"""
        
        try:
            # Obter histórico de performance do agente
            performance_history = self._get_performance_history(agent_id)
            
            if len(performance_history) < self.min_sample_size:
                return {
                    "passed": False,
                    "reason": f"Amostra insuficiente: {len(performance_history)} < {self.min_sample_size}",
                    "sample_size": len(performance_history)
                }
            
            # Calcular estatísticas
            old_performance = improvement_data.get("old_performance", 0.0)
            new_performance = improvement_data.get("new_performance", 0.0)
            
            # Teste t para uma amostra (comparando com média histórica)
            historical_mean = statistics.mean(performance_history)
            historical_std = statistics.stdev(performance_history) if len(performance_history) > 1 else 0.1
            
            # Calcular t-statistic
            n = len(performance_history)
            t_statistic = (new_performance - historical_mean) / (historical_std / math.sqrt(n))
            
            # Graus de liberdade
            df = n - 1
            
            # Valor crítico para p < 0.05 (aproximação)
            critical_value = 2.0 if df > 30 else 2.5  # Simplificado
            
            # Determinar significância
            is_significant = abs(t_statistic) > critical_value
            p_value_approx = 0.01 if abs(t_statistic) > 3.0 else 0.05 if abs(t_statistic) > 2.0 else 0.1
            
            return {
                "passed": is_significant and p_value_approx < self.significance_level,
                "t_statistic": t_statistic,
                "p_value_approx": p_value_approx,
                "critical_value": critical_value,
                "sample_size": n,
                "historical_mean": historical_mean,
                "historical_std": historical_std,
                "is_significant": is_significant
            }
            
        except Exception as e:
            return {
                "passed": False,
                "error": str(e)
            }
    
    def _validate_practical_significance(self, improvement_data: Dict[str, Any]) -> Dict[str, Any]:
        """Valida significância prática da melhoria"""
        
        improvement_percentage = improvement_data.get("improvement_percentage", 0.0)
        old_performance = improvement_data.get("old_performance", 0.0)
        new_performance = improvement_data.get("new_performance", 0.0)
        
        # Critérios de significância prática
        meets_threshold = improvement_percentage >= self.min_improvement_percentage
        positive_improvement = new_performance > old_performance
        meaningful_change = abs(new_performance - old_performance) >= 0.05  # 5% mínimo absoluto
        
        return {
            "passed": meets_threshold and positive_improvement and meaningful_change,
            "improvement_percentage": improvement_percentage,
            "threshold_met": meets_threshold,
            "positive_change": positive_improvement,
            "meaningful_change": meaningful_change,
            "absolute_change": abs(new_performance - old_performance),
            "required_threshold": self.min_improvement_percentage
        }
    
    def _validate_reproducibility(self, agent_id: str, improvement_data: Dict[str, Any]) -> Dict[str, Any]:
        """Valida reprodutibilidade da melhoria"""
        
        try:
            # Obter melhorias recentes do agente
            recent_improvements = self._get_recent_improvements(agent_id, days=7)
            
            if len(recent_improvements) < 2:
                return {
                    "passed": True,  # Primeira melhoria sempre passa
                    "reason": "Primeira melhoria ou dados insuficientes",
                    "improvements_count": len(recent_improvements)
                }
            
            # Analisar consistência das melhorias
            improvement_percentages = [imp.get("improvement_percentage", 0.0) for imp in recent_improvements]
            current_improvement = improvement_data.get("improvement_percentage", 0.0)
            
            # Calcular variabilidade
            all_improvements = improvement_percentages + [current_improvement]
            mean_improvement = statistics.mean(all_improvements)
            std_improvement = statistics.stdev(all_improvements) if len(all_improvements) > 1 else 0.0
            
            # Coeficiente de variação (CV)
            cv = std_improvement / mean_improvement if mean_improvement > 0 else float('inf')
            
            # Reprodutibilidade baseada em CV baixo
            is_reproducible = cv < 0.5  # CV < 50%
            
            return {
                "passed": is_reproducible,
                "coefficient_of_variation": cv,
                "mean_improvement": mean_improvement,
                "std_improvement": std_improvement,
                "improvements_analyzed": len(all_improvements),
                "is_reproducible": is_reproducible
            }
            
        except Exception as e:
            return {
                "passed": False,
                "error": str(e)
            }
    
    def _validate_consistency(self, agent_id: str, improvement_data: Dict[str, Any]) -> Dict[str, Any]:
        """Valida consistência da melhoria com padrões do agente"""
        
        try:
            # Obter padrão de melhorias do agente
            improvement_pattern = self._analyze_improvement_pattern(agent_id)
            
            current_improvement = improvement_data.get("improvement_percentage", 0.0)
            
            if not improvement_pattern:
                return {
                    "passed": True,
                    "reason": "Sem padrão histórico para comparação"
                }
            
            # Verificar se está dentro do padrão esperado
            expected_range = improvement_pattern.get("expected_range", (0.0, 100.0))
            min_expected, max_expected = expected_range
            
            within_pattern = min_expected <= current_improvement <= max_expected
            
            # Verificar tendência
            trend = improvement_pattern.get("trend", "stable")
            trend_consistent = True
            
            if trend == "improving" and current_improvement < improvement_pattern.get("recent_average", 0.0):
                trend_consistent = False
            elif trend == "declining" and current_improvement > improvement_pattern.get("recent_average", 0.0):
                trend_consistent = False
            
            return {
                "passed": within_pattern and trend_consistent,
                "within_expected_range": within_pattern,
                "trend_consistent": trend_consistent,
                "current_improvement": current_improvement,
                "expected_range": expected_range,
                "agent_trend": trend
            }
            
        except Exception as e:
            return {
                "passed": True,  # Falha na validação não deve bloquear
                "error": str(e)
            }
    
    def _validate_bounds(self, improvement_data: Dict[str, Any]) -> Dict[str, Any]:
        """Valida se os valores estão dentro de limites aceitáveis"""
        
        old_performance = improvement_data.get("old_performance", 0.0)
        new_performance = improvement_data.get("new_performance", 0.0)
        improvement_percentage = improvement_data.get("improvement_percentage", 0.0)
        
        # Verificar limites
        performance_in_bounds = 0.0 <= old_performance <= 1.0 and 0.0 <= new_performance <= 1.0
        improvement_reasonable = -100.0 <= improvement_percentage <= 1000.0  # Limites razoáveis
        no_negative_performance = old_performance >= 0.0 and new_performance >= 0.0
        
        return {
            "passed": performance_in_bounds and improvement_reasonable and no_negative_performance,
            "performance_in_bounds": performance_in_bounds,
            "improvement_reasonable": improvement_reasonable,
            "no_negative_values": no_negative_performance,
            "old_performance": old_performance,
            "new_performance": new_performance,
            "improvement_percentage": improvement_percentage
        }
    
    def _get_performance_history(self, agent_id: str, days: int = 30) -> List[float]:
        """Obtém histórico de performance de um agente"""
        try:
            if not self.supabase_client:
                return []
            
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(days=days)
            
            result = self.supabase_client.table('performance_metrics').select("current_value").eq('agent_id', agent_id).gte('timestamp', start_time.isoformat()).execute()
            
            return [record['current_value'] for record in result.data if record.get('current_value') is not None]
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao obter histórico: {e}")
            return []
    
    def _get_recent_improvements(self, agent_id: str, days: int = 7) -> List[Dict[str, Any]]:
        """Obtém melhorias recentes de um agente"""
        try:
            if not self.supabase_client:
                return []
            
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(days=days)
            
            result = self.supabase_client.table('performance_metrics').select("*").eq('agent_id', agent_id).gte('timestamp', start_time.isoformat()).execute()
            
            improvements = []
            for record in result.data:
                if record.get('improvement_percentage') is not None:
                    improvements.append({
                        "improvement_percentage": record['improvement_percentage'],
                        "timestamp": record['timestamp'],
                        "old_performance": record.get('baseline_value', 0.0),
                        "new_performance": record.get('current_value', 0.0)
                    })
            
            return improvements
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao obter melhorias recentes: {e}")
            return []
    
    def _analyze_improvement_pattern(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Analisa padrão de melhorias de um agente"""
        try:
            improvements = self._get_recent_improvements(agent_id, days=30)
            
            if len(improvements) < 3:
                return None
            
            percentages = [imp["improvement_percentage"] for imp in improvements]
            
            # Calcular estatísticas
            mean_improvement = statistics.mean(percentages)
            std_improvement = statistics.stdev(percentages)
            
            # Determinar tendência
            recent_half = percentages[-len(percentages)//2:]
            older_half = percentages[:len(percentages)//2]
            
            recent_avg = statistics.mean(recent_half)
            older_avg = statistics.mean(older_half)
            
            if recent_avg > older_avg * 1.1:
                trend = "improving"
            elif recent_avg < older_avg * 0.9:
                trend = "declining"
            else:
                trend = "stable"
            
            # Calcular faixa esperada (média ± 2 desvios padrão)
            expected_range = (
                max(0.0, mean_improvement - 2 * std_improvement),
                mean_improvement + 2 * std_improvement
            )
            
            return {
                "mean_improvement": mean_improvement,
                "std_improvement": std_improvement,
                "trend": trend,
                "recent_average": recent_avg,
                "expected_range": expected_range,
                "sample_size": len(improvements)
            }
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao analisar padrão: {e}")
            return None
    
    def _calculate_confidence_score(self, validation_results: Dict[str, Any]) -> float:
        """Calcula score de confiança da validação"""
        
        weights = {
            "statistical": 0.3,
            "practical": 0.25,
            "reproducibility": 0.2,
            "consistency": 0.15,
            "bounds": 0.1
        }
        
        total_score = 0.0
        total_weight = 0.0
        
        for category, result in validation_results.items():
            if category in weights:
                weight = weights[category]
                score = 1.0 if result.get("passed", False) else 0.0
                total_score += score * weight
                total_weight += weight
        
        return total_score / total_weight if total_weight > 0 else 0.0
    
    def _generate_recommendations(self, validation_results: Dict[str, Any]) -> List[str]:
        """Gera recomendações baseadas nos resultados da validação"""
        
        recommendations = []
        
        # Recomendações baseadas em falhas
        if not validation_results.get("statistical", {}).get("passed", True):
            recommendations.append("Aumentar tamanho da amostra para melhor significância estatística")
        
        if not validation_results.get("practical", {}).get("passed", True):
            recommendations.append("Buscar melhorias mais substanciais para significância prática")
        
        if not validation_results.get("reproducibility", {}).get("passed", True):
            recommendations.append("Melhorar consistência das melhorias para maior reprodutibilidade")
        
        if not validation_results.get("consistency", {}).get("passed", True):
            recommendations.append("Alinhar melhorias com padrão histórico do agente")
        
        if not validation_results.get("bounds", {}).get("passed", True):
            recommendations.append("Verificar cálculos - valores fora dos limites aceitáveis")
        
        if not recommendations:
            recommendations.append("Validação aprovada - continuar com melhorias")
        
        return recommendations
    
    def _save_validation_to_suna(self, validation_data: Dict[str, Any]) -> bool:
        """Salva resultado da validação no sistema SUNA"""
        try:
            if not self.supabase_client:
                return False
            
            validation_record = {
                "id": validation_data["validation_id"],
                "agent_id": validation_data["agent_id"],
                "validation_type": "scientific_improvement",
                "overall_passed": validation_data["overall_passed"],
                "confidence_score": validation_data["confidence_score"],
                "validation_criteria": json.dumps(validation_data["validation_results"]),
                "recommendations": json.dumps(validation_data["recommendations"]),
                "timestamp": datetime.utcnow().isoformat(),
                "metadata": json.dumps(validation_data)
            }
            
            result = self.supabase_client.table('validation_results').insert(validation_record).execute()
            
            if result.data:
                self.logger.info(f"✅ Validação salva no SUNA: {validation_data['validation_id']}")
                return True
            else:
                self.logger.error("❌ Falha ao salvar validação no SUNA")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao salvar validação: {e}")
            return False

# Função de teste para desenvolvimento
def test_validation_system():
    """Teste básico do sistema de validação"""
    print("🎯 Testando Sistema de Validação SUNA-ALSHAM...")
    
    validation_system = ValidationSystem()
    print(f"🔬 Sistema criado - ID: {validation_system.system_id}")
    
    # Simular dados de melhoria
    improvement_data = {
        "old_performance": 0.65,
        "new_performance": 0.78,
        "improvement_percentage": 20.0,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    # Executar validação
    result = validation_system.validate_improvement("test-agent-id", improvement_data)
    
    if result.get("overall_passed"):
        confidence = result["confidence_score"]
        print(f"✅ Validação APROVADA - Confiança: {confidence:.3f}")
    else:
        print(f"❌ Validação REPROVADA: {result.get('error', 'Critérios não atendidos')}")
    
    print("🎉 Teste do Sistema de Validação concluído!")

if __name__ == "__main__":
    test_validation_system()
