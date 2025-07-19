import os
import unittest
import json
import time
from datetime import datetime, timedelta

# Adiciona o diretório raiz do projeto ao PYTHONPATH
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__)))
if project_root not in os.sys.path:
    os.sys.path.insert(0, project_root)

# Importa os módulos SUNA-ALSHAM
from backend.agent.alsham.config import SUNAAlshamConfig
from backend.agent.alsham.core_agent import CoreAgent
from backend.agent.alsham.learn_agent import LearnAgent
from backend.agent.alsham.guard_agent import GuardAgent
from backend.agent.alsham.metrics_system import MetricsSystem
from backend.agent.alsham.validation_system import ValidationSystem
from backend.agent.alsham.integration import SUNAAlshamIntegration, SupabaseClientMock

class TestSUNAAlshamIntegration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Configura variáveis de ambiente para os testes
        os.environ["SUPABASE_URL"] = "http://test.supabase.com"
        os.environ["SUPABASE_KEY"] = "test_key"
        os.environ["SUNA_ALSHAM_AUTO_START"] = "true"
        os.environ["SUNA_ALSHAM_EVOLUTION_INTERVAL"] = "1" # 1 minuto para testes
        os.environ["SUNA_ALSHAM_DEBUG"] = "true"

    def setUp(self ):
        # Reinicia o mock do Supabase para cada teste
        self.integration = SUNAAlshamIntegration()
        self.integration.supabase = SupabaseClientMock(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])
        self.integration.start()

    def tearDown(self):
        self.integration.stop()

    def test_01_initialization(self):
        print("\n--- Teste 01: Inicialização do Sistema ---")
        self.assertIsInstance(self.integration, SUNAAlshamIntegration)
        self.assertIsInstance(self.integration.core_agent, CoreAgent)
        self.assertIsInstance(self.integration.learn_agent, LearnAgent)
        self.assertIsInstance(self.integration.guard_agent, GuardAgent)
        self.assertIsInstance(self.integration.metrics_system, MetricsSystem)
        self.assertIsInstance(self.integration.validation_system, ValidationSystem)
        self.assertTrue(self.integration.is_running)
        print("Inicialização bem-sucedida.")

    def test_02_agent_status(self):
        print("\n--- Teste 02: Status dos Agentes ---")
        core_status = self.integration.core_agent.get_status()
        self.assertIn("name", core_status)
        self.assertEqual(core_status["name"], "CORE")
        print(f"Status CORE: {core_status}")

        learn_status = self.integration.learn_agent.get_status()
        self.assertIn("name", learn_status)
        self.assertEqual(learn_status["name"], "LEARN")
        print(f"Status LEARN: {learn_status}")

        guard_status = self.integration.guard_agent.get_status()
        self.assertIn("name", guard_status)
        self.assertEqual(guard_status["name"], "GUARD")
        print(f"Status GUARD: {guard_status}")
        print("Status dos agentes verificados.")

    def test_03_run_evolution_cycle(self):
        print("\n--- Teste 03: Execução de um Ciclo de Evolução ---")
        cycle_result = self.integration.run_evolution_cycle()
        self.assertIsNotNone(cycle_result)
        self.assertTrue(cycle_result.get("overall_success"), f"Ciclo de evolução falhou: {cycle_result.get("error")}")
        self.assertIn("core_evolution", cycle_result)
        self.assertIn("learn_collaboration", cycle_result)
        self.assertIn("guard_security", cycle_result)
        self.assertIn("metrics_analysis", cycle_result)
        self.assertIn("validation_results", cycle_result)
        print(f"Ciclo de evolução concluído com sucesso. ID: {cycle_result.get("cycle_id")}")

    def test_04_metrics_collection(self):
        print("\n--- Teste 04: Coleta de Métricas ---")
        # Executa um ciclo para garantir que métricas sejam coletadas
        self.integration.run_evolution_cycle()
        
        # Verifica se as métricas foram coletadas para o CORE
        core_metrics = self.integration.metrics_system.get_performance_metrics(self.integration.core_agent.agent_id, "performance_improvement")
        self.assertGreater(core_metrics["summary"]["count"], 0)
        print(f"Métricas do CORE coletadas: {core_metrics["summary"]}")

        # Verifica se as métricas foram coletadas para o GUARD
        guard_metrics = self.integration.metrics_system.get_performance_metrics(self.integration.guard_agent.agent_id, "security_score")
        self.assertGreater(guard_metrics["summary"]["count"], 0)
        print(f"Métricas do GUARD coletadas: {guard_metrics["summary"]}")
        print("Coleta de métricas verificada.")

    def test_05_validation_system(self):
        print("\n--- Teste 05: Sistema de Validação ---")
        # Simula uma melhoria para validação
        improvement_data = {
            "old_performance": 0.7,
            "new_performance": 0.85,
            "improvement_percentage": 21.4,
            "context": {"test": "validation"}
        }
        validation_result = self.integration.validation_system.validate_improvement(
            self.integration.core_agent.agent_id, improvement_data
        )
        self.assertIsNotNone(validation_result)
        self.assertTrue(validation_result.get("overall_passed"), "Validação científica deveria ter passado.")
        self.assertGreaterEqual(validation_result.get("confidence_score", 0), 0.7)
        print(f"Validação científica bem-sucedida. Confiança: {validation_result.get("confidence_score")}")

        # Simula uma melhoria que não passa
        bad_improvement_data = {
            "old_performance": 0.7,
            "new_performance": 0.71,
            "improvement_percentage": 1.4,
            "context": {"test": "bad_validation"}
        }
        bad_validation_result = self.integration.validation_system.validate_improvement(
            self.integration.core_agent.agent_id, bad_improvement_data
        )
        self.assertFalse(bad_validation_result.get("overall_passed"), "Validação científica não deveria ter passado.")
        print("Validação de melhoria insuficiente corretamente rejeitada.")
        print("Sistema de validação verificado.")

    def test_06_data_persistence(self):
        print("\n--- Teste 06: Persistência de Dados (Mock Supabase) ---")
        # Executa um ciclo para garantir que dados sejam persistidos
        cycle_result = self.integration.run_evolution_cycle()
        self.assertTrue(cycle_result.get("overall_success"))

        # Verifica se o estado dos agentes foi salvo
        agents_in_db = self.integration.supabase.from_("agents").select("*").execute().get("data")
        self.assertGreaterEqual(len(agents_in_db), 3) # CORE, LEARN, GUARD
        print(f"Agentes encontrados no DB: {len(agents_in_db)}")

        # Verifica se o ciclo de evolução foi salvo
        cycles_in_db = self.integration.supabase.from_("evolution_cycles").select("*").execute().get("data")
        self.assertGreater(len(cycles_in_db), 0)
        print(f"Ciclos de evolução encontrados no DB: {len(cycles_in_db)}")

        # Verifica se as métricas do sistema foram salvas
        metrics_in_db = self.integration.supabase.from_("system_metrics").select("*").execute().get("data")
        self.assertGreater(len(metrics_in_db), 0)
        print(f"Métricas do sistema encontradas no DB: {len(metrics_in_db)}")
        print("Persistência de dados verificada.")

    def test_07_system_status_reporting(self):
        print("\n--- Teste 07: Relatório de Status do Sistema ---")
        status_report = self.integration.get_system_status()
        self.assertIn("system_id", status_report)
        self.assertTrue(status_report["is_running"])
        self.assertIn("core_agent_status", status_report)
        self.assertIn("metrics_system_stats", status_report)
        self.assertIn("validation_system_stats", status_report)
        print("Relatório de status do sistema gerado com sucesso.")
        # print(json.dumps(status_report, indent=2))

if __name__ == '__main__':
    unittest.main(argv=["first-arg-is-ignored"], exit=False)
