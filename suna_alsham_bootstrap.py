import os
import time
import logging
from datetime import datetime

# Adiciona o diretório raiz do projeto ao PYTHONPATH
# Isso é crucial para que as importações relativas funcionem corretamente
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__)))
if project_root not in os.sys.path:
    os.sys.path.insert(0, project_root)

# Importa a classe de integração SUNA-ALSHAM
try:
    from backend.agent.alsham.integration import SUNAAlshamIntegration
    from backend.agent.alsham.config import SUNAAlshamConfig
except ImportError as e:
    logging.error(f"Erro ao importar módulos SUNA-ALSHAM. Verifique o PYTHONPATH e a estrutura de arquivos: {e}")
    logging.error("Certifique-se de que 'backend/agent/alsham' está acessível.")
    exit(1)

# Configuração de logging
logging.basicConfig(level=logging.INFO, format=
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("SUNA_ALSHAM_BOOTSTRAP")

def run_bootstrap():
    logger.info("🚀 Iniciando bootstrap do sistema SUNA-ALSHAM...")

    # Carregar configuração
    config_loader = SUNAAlshamConfig()
    config = config_loader.get_config()

    if not config.auto_start:
        logger.info("SUNA_ALSHAM_AUTO_START está definido como 'false'. O sistema não será iniciado automaticamente.")
        return

    # Inicializar o sistema de integração
    try:
        integration = SUNAAlshamIntegration()
        integration.start()
    except Exception as e:
        logger.error(f"❌ Erro ao inicializar SUNA-ALSHAM Integration: {e}", exc_info=True)
        exit(1)

    logger.info("SUNA-ALSHAM Integration inicializada. Entrando em loop de evolução.")

    # Loop principal de evolução
    evolution_interval_seconds = config.evolution_interval_minutes * 60
    if evolution_interval_seconds <= 0:
        logger.warning("Intervalo de evolução inválido ou zero. Definindo para 60 minutos (padrão).")
        evolution_interval_seconds = 3600

    while True:
        try:
            logger.info(f"Aguardando {config.evolution_interval_minutes} minutos para o próximo ciclo de evolução...")
            time.sleep(evolution_interval_seconds)

            logger.info(f"Executando ciclo de evolução em {datetime.now().isoformat()}...")
            cycle_result = integration.run_evolution_cycle()
            
            if cycle_result.get("overall_success"):
                logger.info(f"✅ Ciclo de evolução {cycle_result.get("cycle_id")} concluído com sucesso.")
            else:
                logger.warning(f"⚠️ Ciclo de evolução {cycle_result.get("cycle_id")} falhou ou teve problemas.")
                if "error" in cycle_result:
                    logger.error(f"Detalhes do erro: {cycle_result["error"]}")

            # Opcional: Logar o status completo do sistema após cada ciclo
            # status = integration.get_system_status()
            # logger.debug(f"Status atual do sistema: {status}")

        except KeyboardInterrupt:
            logger.info("Detectado Ctrl+C. Encerrando o sistema SUNA-ALSHAM.")
            integration.stop()
            break
        except Exception as e:
            logger.error(f"❌ Erro inesperado durante o loop de evolução: {e}", exc_info=True)
            # Continua o loop mesmo em caso de erro para tentar novamente no próximo intervalo

if __name__ == "__main__":
    run_bootstrap()
