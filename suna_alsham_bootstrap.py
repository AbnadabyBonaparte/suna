"""
SUNA-ALSHAM Bootstrap Script - VERSÃO FINAL CORRIGIDA
Script principal para inicializar e executar o sistema SUNA-ALSHAM em produção.
CORREÇÃO: Método start_system() em vez de start()
"""

import os
import time
import logging
from datetime import datetime, timedelta
from typing import Optional

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("SUNA_ALSHAM_BOOTSTRAP")

def run_bootstrap():
    """
    Função principal de bootstrap do sistema SUNA-ALSHAM
    """
    logger.info("🚀 Iniciando bootstrap do sistema SUNA-ALSHAM...")
    
    try:
        # Importar e inicializar a integração SUNA-ALSHAM
        from backend.agent.alsham.integration import SUNAAlshamIntegration
        
        # Criar instância da integração
        integration = SUNAAlshamIntegration()
        
        # CORREÇÃO: Usar start_system() em vez de start()
        integration.start_system()
        
        logger.info("SUNA-ALSHAM Integration inicializada. Entrando em loop de evolução.")
        
        # Loop principal de evolução
        evolution_interval_minutes = int(os.getenv('SUNA_ALSHAM_EVOLUTION_INTERVAL', '60'))
        
        while True:
            try:
                logger.info(f"Aguardando {evolution_interval_minutes} minutos para o próximo ciclo de evolução...")
                time.sleep(evolution_interval_minutes * 60)  # Converter para segundos
                
                # Executar ciclo de evolução
                logger.info(f"Executando ciclo de evolução em {datetime.utcnow().isoformat()}...")
                cycle_result = integration.run_evolution_cycle()
                
                if cycle_result.get('overall_success', False):
                    logger.info(f"✅ Ciclo de evolução {cycle_result.get('cycle_id')} concluído com sucesso.")
                else:
                    logger.warning(f"⚠️ Ciclo de evolução {cycle_result.get('cycle_id')} falhou ou teve problemas.")
                
            except KeyboardInterrupt:
                logger.info("🛑 Interrupção detectada. Finalizando sistema SUNA-ALSHAM...")
                break
            except Exception as e:
                logger.error(f"❌ Erro durante ciclo de evolução: {e}")
                logger.info("🔄 Continuando com próximo ciclo...")
                continue
                
    except Exception as e:
        logger.error(f"❌ Erro ao inicializar SUNA-ALSHAM Integration: {e}")
        logger.info("🔄 Tentando novamente em 30 segundos...")
        time.sleep(30)
        run_bootstrap()  # Tentar novamente

def main():
    """
    Função principal do script
    """
    logger.info("🌟 SUNA-ALSHAM Bootstrap iniciado")
    
    # Verificar variáveis de ambiente essenciais
    required_vars = ['SUPABASE_URL', 'SUPABASE_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.warning(f"⚠️ Variáveis de ambiente faltando: {missing_vars}")
        logger.info("🔧 Sistema continuará com configurações padrão/mock")
    
    # Executar bootstrap
    run_bootstrap()

if __name__ == "__main__":
    main()
