-- Migration: 20250719000000_suna_alsham_integration.sql
-- Descrição: Criação das tabelas necessárias para a integração SUNA-ALSHAM

-- Tabela para armazenar o estado dos agentes (CORE, LEARN, GUARD)
CREATE TABLE IF NOT EXISTS public.agents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL UNIQUE,
    type TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'inactive',
    config JSONB NOT NULL DEFAULT '{}'::jsonb,
    state JSONB NOT NULL DEFAULT '{}'::jsonb,
    last_updated TIMESTAMPTZ DEFAULT NOW()
);

-- Tabela para registrar os ciclos de evolução do sistema SUNA-ALSHAM
CREATE TABLE IF NOT EXISTS public.evolution_cycles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    cycle_id TEXT NOT NULL UNIQUE,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    core_evolution JSONB,
    learn_collaboration JSONB,
    guard_security JSONB,
    metrics_analysis JSONB,
    validation_results JSONB,
    overall_success BOOLEAN NOT NULL,
    duration_seconds NUMERIC,
    error TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tabela para armazenar métricas de performance e saúde do sistema
CREATE TABLE IF NOT EXISTS public.system_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    agent_id TEXT,
    metric_name TEXT NOT NULL,
    value NUMERIC NOT NULL,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Índices para otimização de consultas
CREATE INDEX IF NOT EXISTS idx_agents_name ON public.agents (name);
CREATE INDEX IF NOT EXISTS idx_evolution_cycles_timestamp ON public.evolution_cycles (timestamp);
CREATE INDEX IF NOT EXISTS idx_system_metrics_agent_id ON public.system_metrics (agent_id);
CREATE INDEX IF NOT EXISTS idx_system_metrics_metric_name ON public.system_metrics (metric_name);

-- Comentários para documentação
COMMENT ON TABLE public.agents IS 'Armazena o estado e configuração dos agentes auto-evolutivos SUNA-ALSHAM.';
COMMENT ON COLUMN public.agents.name IS 'Nome único do agente (ex: CORE, LEARN, GUARD).';
COMMENT ON TABLE public.evolution_cycles IS 'Registra cada ciclo de evolução executado pelo sistema SUNA-ALSHAM.';
COMMENT ON TABLE public.system_metrics IS 'Armazena métricas de performance e saúde coletadas dos agentes e do sistema.';

-- Opcional: Adicionar RLS (Row Level Security) para segurança, se aplicável ao seu projeto
-- ALTER TABLE public.agents ENABLE ROW LEVEL SECURITY;
-- CREATE POLICY "Enable read access for all users" ON public.agents FOR SELECT USING (TRUE);

-- Opcional: Adicionar função para gerar UUIDs se não estiver disponível
-- CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Fim da migração
