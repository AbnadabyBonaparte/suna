-- SUNA-ALSHAM Integration Migration
-- Adiciona tabelas e funcionalidades para agentes auto-evolutivos
-- Data: 2025-07-19
-- Versão: 1.0.0

-- =====================================================
-- EXTENSÕES NECESSÁRIAS
-- =====================================================

-- Habilitar extensões UUID se não estiverem ativas
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- =====================================================
-- TABELAS SUNA-ALSHAM
-- =====================================================

-- Tabela para métricas de performance dos agentes auto-evolutivos
CREATE TABLE IF NOT EXISTS performance_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    agent_id UUID NOT NULL,
    metric_type VARCHAR(100) NOT NULL,
    current_value DECIMAL(10,6) NOT NULL,
    baseline_value DECIMAL(10,6) DEFAULT 0.0,
    improvement_percentage DECIMAL(8,3) DEFAULT 0.0,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tabela para interações entre agentes
CREATE TABLE IF NOT EXISTS agent_interactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    initiator_agent_id UUID NOT NULL,
    target_agent_ids JSONB NOT NULL DEFAULT '[]',
    interaction_type VARCHAR(100) NOT NULL,
    synergy_score DECIMAL(8,3) DEFAULT 0.0,
    duration_seconds DECIMAL(10,3) DEFAULT 0.0,
    outcomes JSONB DEFAULT '{}',
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tabela para sessões de aprendizado colaborativo
CREATE TABLE IF NOT EXISTS learning_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID UNIQUE NOT NULL,
    initiator_agent_id UUID NOT NULL,
    participating_agents JSONB NOT NULL DEFAULT '[]',
    session_type VARCHAR(100) DEFAULT 'collaborative_learning',
    average_synergy DECIMAL(8,3) DEFAULT 0.0,
    learning_outcomes JSONB DEFAULT '{}',
    duration_seconds DECIMAL(10,3) DEFAULT 0.0,
    success BOOLEAN DEFAULT FALSE,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tabela para logs de segurança dos agentes
CREATE TABLE IF NOT EXISTS security_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    agent_id UUID NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    severity VARCHAR(20) DEFAULT 'LOW',
    security_score DECIMAL(8,6) DEFAULT 1.0,
    threats_detected INTEGER DEFAULT 0,
    containment_actions INTEGER DEFAULT 0,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    details JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tabela para ações de contenção de segurança
CREATE TABLE IF NOT EXISTS containment_actions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    action_id UUID UNIQUE NOT NULL,
    agent_id UUID NOT NULL,
    threat_id UUID,
    action_type VARCHAR(100) NOT NULL,
    executed_at TIMESTAMPTZ DEFAULT NOW(),
    success BOOLEAN DEFAULT FALSE,
    details TEXT,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tabela para resultados de validação científica
CREATE TABLE IF NOT EXISTS validation_results (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    validation_id UUID UNIQUE NOT NULL,
    agent_id UUID NOT NULL,
    validation_type VARCHAR(100) NOT NULL,
    overall_passed BOOLEAN DEFAULT FALSE,
    confidence_score DECIMAL(8,6) DEFAULT 0.0,
    validation_criteria JSONB DEFAULT '{}',
    recommendations JSONB DEFAULT '[]',
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tabela para métricas do sistema SUNA-ALSHAM
CREATE TABLE IF NOT EXISTS system_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    system_id UUID NOT NULL,
    cycle_type VARCHAR(100) NOT NULL,
    duration_seconds DECIMAL(10,3) DEFAULT 0.0,
    successful_agents INTEGER DEFAULT 0,
    total_agents INTEGER DEFAULT 0,
    success BOOLEAN DEFAULT FALSE,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    results JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tabela para critérios de sucesso dos agentes
CREATE TABLE IF NOT EXISTS success_criteria (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    agent_id UUID NOT NULL,
    criteria_type VARCHAR(100) NOT NULL,
    threshold_value DECIMAL(10,6) NOT NULL,
    current_value DECIMAL(10,6) DEFAULT 0.0,
    is_met BOOLEAN DEFAULT FALSE,
    last_evaluated TIMESTAMPTZ DEFAULT NOW(),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tabela para rastreamento de marcos (milestones)
CREATE TABLE IF NOT EXISTS milestone_tracking (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    milestone_id UUID UNIQUE NOT NULL,
    agent_id UUID,
    system_id UUID,
    milestone_type VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    target_date TIMESTAMPTZ,
    completed_date TIMESTAMPTZ,
    is_completed BOOLEAN DEFAULT FALSE,
    progress_percentage DECIMAL(5,2) DEFAULT 0.0,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tabela para capacidades emergentes dos agentes
CREATE TABLE IF NOT EXISTS emergent_capabilities (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    capability_id UUID UNIQUE NOT NULL,
    agent_id UUID NOT NULL,
    capability_name VARCHAR(200) NOT NULL,
    capability_type VARCHAR(100) NOT NULL,
    emergence_date TIMESTAMPTZ DEFAULT NOW(),
    strength_score DECIMAL(8,6) DEFAULT 0.0,
    validation_status VARCHAR(50) DEFAULT 'pending',
    description TEXT,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tabela para trilha de auditoria detalhada
CREATE TABLE IF NOT EXISTS audit_trail (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    entity_type VARCHAR(100) NOT NULL,
    entity_id UUID NOT NULL,
    action VARCHAR(100) NOT NULL,
    actor_id UUID,
    actor_type VARCHAR(100),
    old_values JSONB DEFAULT '{}',
    new_values JSONB DEFAULT '{}',
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    ip_address INET,
    user_agent TEXT,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- =====================================================
-- ÍNDICES PARA PERFORMANCE
-- =====================================================

-- Índices para performance_metrics
CREATE INDEX IF NOT EXISTS idx_performance_metrics_agent_id ON performance_metrics(agent_id);
CREATE INDEX IF NOT EXISTS idx_performance_metrics_timestamp ON performance_metrics(timestamp);
CREATE INDEX IF NOT EXISTS idx_performance_metrics_metric_type ON performance_metrics(metric_type);

-- Índices para agent_interactions
CREATE INDEX IF NOT EXISTS idx_agent_interactions_initiator ON agent_interactions(initiator_agent_id);
CREATE INDEX IF NOT EXISTS idx_agent_interactions_timestamp ON agent_interactions(timestamp);
CREATE INDEX IF NOT EXISTS idx_agent_interactions_type ON agent_interactions(interaction_type);

-- Índices para learning_sessions
CREATE INDEX IF NOT EXISTS idx_learning_sessions_initiator ON learning_sessions(initiator_agent_id);
CREATE INDEX IF NOT EXISTS idx_learning_sessions_timestamp ON learning_sessions(timestamp);
CREATE INDEX IF NOT EXISTS idx_learning_sessions_success ON learning_sessions(success);

-- Índices para security_logs
CREATE INDEX IF NOT EXISTS idx_security_logs_agent_id ON security_logs(agent_id);
CREATE INDEX IF NOT EXISTS idx_security_logs_timestamp ON security_logs(timestamp);
CREATE INDEX IF NOT EXISTS idx_security_logs_severity ON security_logs(severity);

-- Índices para validation_results
CREATE INDEX IF NOT EXISTS idx_validation_results_agent_id ON validation_results(agent_id);
CREATE INDEX IF NOT EXISTS idx_validation_results_timestamp ON validation_results(timestamp);
CREATE INDEX IF NOT EXISTS idx_validation_results_passed ON validation_results(overall_passed);

-- Índices para system_metrics
CREATE INDEX IF NOT EXISTS idx_system_metrics_system_id ON system_metrics(system_id);
CREATE INDEX IF NOT EXISTS idx_system_metrics_timestamp ON system_metrics(timestamp);
CREATE INDEX IF NOT EXISTS idx_system_metrics_success ON system_metrics(success);

-- Índices para audit_trail
CREATE INDEX IF NOT EXISTS idx_audit_trail_entity ON audit_trail(entity_type, entity_id);
CREATE INDEX IF NOT EXISTS idx_audit_trail_timestamp ON audit_trail(timestamp);
CREATE INDEX IF NOT EXISTS idx_audit_trail_actor ON audit_trail(actor_id);

-- =====================================================
-- TRIGGERS PARA AUDITORIA AUTOMÁTICA
-- =====================================================

-- Função para trigger de auditoria
CREATE OR REPLACE FUNCTION audit_trigger_function()
RETURNS TRIGGER AS $$
BEGIN
    -- Inserir registro de auditoria para UPDATE
    IF TG_OP = 'UPDATE' THEN
        INSERT INTO audit_trail (
            entity_type,
            entity_id,
            action,
            old_values,
            new_values,
            timestamp
        ) VALUES (
            TG_TABLE_NAME,
            COALESCE(NEW.id, OLD.id),
            'UPDATE',
            to_jsonb(OLD),
            to_jsonb(NEW),
            NOW()
        );
        RETURN NEW;
    END IF;
    
    -- Inserir registro de auditoria para DELETE
    IF TG_OP = 'DELETE' THEN
        INSERT INTO audit_trail (
            entity_type,
            entity_id,
            action,
            old_values,
            timestamp
        ) VALUES (
            TG_TABLE_NAME,
            OLD.id,
            'DELETE',
            to_jsonb(OLD),
            NOW()
        );
        RETURN OLD;
    END IF;
    
    -- Inserir registro de auditoria para INSERT
    IF TG_OP = 'INSERT' THEN
        INSERT INTO audit_trail (
            entity_type,
            entity_id,
            action,
            new_values,
            timestamp
        ) VALUES (
            TG_TABLE_NAME,
            NEW.id,
            'INSERT',
            to_jsonb(NEW),
            NOW()
        );
        RETURN NEW;
    END IF;
    
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Aplicar triggers de auditoria nas tabelas principais
CREATE TRIGGER audit_performance_metrics
    AFTER INSERT OR UPDATE OR DELETE ON performance_metrics
    FOR EACH ROW EXECUTE FUNCTION audit_trigger_function();

CREATE TRIGGER audit_agent_interactions
    AFTER INSERT OR UPDATE OR DELETE ON agent_interactions
    FOR EACH ROW EXECUTE FUNCTION audit_trigger_function();

CREATE TRIGGER audit_validation_results
    AFTER INSERT OR UPDATE OR DELETE ON validation_results
    FOR EACH ROW EXECUTE FUNCTION audit_trigger_function();

-- =====================================================
-- TRIGGERS PARA UPDATED_AT
-- =====================================================

-- Função para atualizar updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Aplicar trigger de updated_at onde necessário
CREATE TRIGGER update_success_criteria_updated_at
    BEFORE UPDATE ON success_criteria
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_milestone_tracking_updated_at
    BEFORE UPDATE ON milestone_tracking
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_emergent_capabilities_updated_at
    BEFORE UPDATE ON emergent_capabilities
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- VIEWS PARA RELATÓRIOS
-- =====================================================

-- View para métricas consolidadas de agentes
CREATE OR REPLACE VIEW agent_performance_summary AS
SELECT 
    a.id as agent_id,
    a.name as agent_name,
    a.type as agent_type,
    COUNT(pm.id) as total_metrics,
    AVG(pm.current_value) as avg_performance,
    MAX(pm.current_value) as max_performance,
    MIN(pm.current_value) as min_performance,
    AVG(pm.improvement_percentage) as avg_improvement,
    COUNT(CASE WHEN pm.improvement_percentage > 0 THEN 1 END) as positive_improvements,
    MAX(pm.timestamp) as last_metric_date
FROM agents a
LEFT JOIN performance_metrics pm ON a.id = pm.agent_id
WHERE a.status = 'active'
GROUP BY a.id, a.name, a.type;

-- View para status de segurança
CREATE OR REPLACE VIEW security_status_summary AS
SELECT 
    a.id as agent_id,
    a.name as agent_name,
    COUNT(sl.id) as total_security_events,
    AVG(sl.security_score) as avg_security_score,
    MIN(sl.security_score) as min_security_score,
    SUM(sl.threats_detected) as total_threats,
    SUM(sl.containment_actions) as total_containments,
    COUNT(CASE WHEN sl.severity = 'CRITICAL' THEN 1 END) as critical_incidents,
    MAX(sl.timestamp) as last_security_check
FROM agents a
LEFT JOIN security_logs sl ON a.id = sl.agent_id
WHERE a.status = 'active'
GROUP BY a.id, a.name;

-- View para colaboração entre agentes
CREATE OR REPLACE VIEW collaboration_summary AS
SELECT 
    a.id as agent_id,
    a.name as agent_name,
    COUNT(ai.id) as total_interactions,
    AVG(ai.synergy_score) as avg_synergy,
    MAX(ai.synergy_score) as max_synergy,
    COUNT(CASE WHEN ai.synergy_score >= 30.0 THEN 1 END) as successful_collaborations,
    AVG(ai.duration_seconds) as avg_interaction_duration,
    MAX(ai.timestamp) as last_interaction
FROM agents a
LEFT JOIN agent_interactions ai ON a.id = ai.initiator_agent_id
WHERE a.status = 'active'
GROUP BY a.id, a.name;

-- =====================================================
-- FUNÇÕES UTILITÁRIAS
-- =====================================================

-- Função para calcular score de saúde do sistema
CREATE OR REPLACE FUNCTION calculate_system_health_score()
RETURNS DECIMAL(8,6) AS $$
DECLARE
    avg_performance DECIMAL(8,6);
    avg_security DECIMAL(8,6);
    avg_collaboration DECIMAL(8,6);
    health_score DECIMAL(8,6);
BEGIN
    -- Calcular performance média
    SELECT AVG(avg_performance) INTO avg_performance
    FROM agent_performance_summary
    WHERE avg_performance IS NOT NULL;
    
    -- Calcular segurança média
    SELECT AVG(avg_security_score) INTO avg_security
    FROM security_status_summary
    WHERE avg_security_score IS NOT NULL;
    
    -- Calcular colaboração média (normalizada)
    SELECT AVG(avg_synergy / 100.0) INTO avg_collaboration
    FROM collaboration_summary
    WHERE avg_synergy IS NOT NULL;
    
    -- Calcular score final (pesos: 40% performance, 40% security, 20% collaboration)
    health_score := COALESCE(avg_performance, 0.0) * 0.4 + 
                   COALESCE(avg_security, 1.0) * 0.4 + 
                   COALESCE(avg_collaboration, 0.0) * 0.2;
    
    RETURN health_score;
END;
$$ LANGUAGE plpgsql;

-- Função para limpar dados antigos (manutenção)
CREATE OR REPLACE FUNCTION cleanup_old_data(retention_days INTEGER DEFAULT 30)
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER := 0;
    cutoff_date TIMESTAMPTZ;
BEGIN
    cutoff_date := NOW() - INTERVAL '1 day' * retention_days;
    
    -- Limpar métricas antigas
    DELETE FROM performance_metrics WHERE created_at < cutoff_date;
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    
    -- Limpar logs de segurança antigos
    DELETE FROM security_logs WHERE created_at < cutoff_date;
    GET DIAGNOSTICS deleted_count = deleted_count + ROW_COUNT;
    
    -- Limpar interações antigas
    DELETE FROM agent_interactions WHERE created_at < cutoff_date;
    GET DIAGNOSTICS deleted_count = deleted_count + ROW_COUNT;
    
    -- Limpar auditoria antiga (manter mais tempo)
    DELETE FROM audit_trail WHERE created_at < (cutoff_date - INTERVAL '30 days');
    GET DIAGNOSTICS deleted_count = deleted_count + ROW_COUNT;
    
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

-- =====================================================
-- POLÍTICAS DE SEGURANÇA (RLS)
-- =====================================================

-- Habilitar RLS nas tabelas sensíveis
ALTER TABLE performance_metrics ENABLE ROW LEVEL SECURITY;
ALTER TABLE security_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE validation_results ENABLE ROW LEVEL SECURITY;

-- Política básica: usuários autenticados podem ver todos os dados
CREATE POLICY "Allow authenticated users" ON performance_metrics
    FOR ALL TO authenticated USING (true);

CREATE POLICY "Allow authenticated users" ON security_logs
    FOR ALL TO authenticated USING (true);

CREATE POLICY "Allow authenticated users" ON validation_results
    FOR ALL TO authenticated USING (true);

-- =====================================================
-- DADOS INICIAIS (SEED DATA)
-- =====================================================

-- Inserir critérios de sucesso padrão para agentes SUNA-ALSHAM
INSERT INTO success_criteria (agent_id, criteria_type, threshold_value, metadata) VALUES
    (uuid_generate_v4(), 'min_improvement_percentage', 20.0, '{"description": "Melhoria mínima de performance para agentes CORE"}'),
    (uuid_generate_v4(), 'min_collaboration_synergy', 30.0, '{"description": "Sinergia mínima para colaboração entre agentes"}'),
    (uuid_generate_v4(), 'max_critical_incidents', 0.0, '{"description": "Máximo de incidentes críticos de segurança permitidos"}'),
    (uuid_generate_v4(), 'min_security_score', 0.7, '{"description": "Score mínimo de segurança do sistema"}')
ON CONFLICT DO NOTHING;

-- =====================================================
-- COMENTÁRIOS PARA DOCUMENTAÇÃO
-- =====================================================

COMMENT ON TABLE performance_metrics IS 'Métricas de performance dos agentes auto-evolutivos SUNA-ALSHAM';
COMMENT ON TABLE agent_interactions IS 'Registro de interações e colaborações entre agentes';
COMMENT ON TABLE learning_sessions IS 'Sessões de aprendizado colaborativo entre agentes';
COMMENT ON TABLE security_logs IS 'Logs de eventos de segurança e monitoramento';
COMMENT ON TABLE validation_results IS 'Resultados de validação científica das melhorias';
COMMENT ON TABLE system_metrics IS 'Métricas gerais do sistema SUNA-ALSHAM';
COMMENT ON TABLE emergent_capabilities IS 'Capacidades emergentes descobertas pelos agentes';
COMMENT ON TABLE audit_trail IS 'Trilha de auditoria completa do sistema';

COMMENT ON FUNCTION calculate_system_health_score() IS 'Calcula score de saúde geral do sistema baseado em métricas dos agentes';
COMMENT ON FUNCTION cleanup_old_data(INTEGER) IS 'Remove dados antigos para manutenção do banco';

-- =====================================================
-- FINALIZAÇÃO
-- =====================================================

-- Atualizar estatísticas do banco
ANALYZE;

-- Log de conclusão
DO $$
BEGIN
    RAISE NOTICE 'SUNA-ALSHAM Integration Migration completed successfully at %', NOW();
    RAISE NOTICE 'Tables created: 11 main tables + views and functions';
    RAISE NOTICE 'Indexes created: Performance optimized';
    RAISE NOTICE 'Triggers created: Audit trail and updated_at automation';
    RAISE NOTICE 'Security: Row Level Security enabled on sensitive tables';
END $$;
