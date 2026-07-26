# DOSSIÊ — HUNTER X.1
## O Caçador do Santuário — Sistema de Evolução Contínua dos Irmãos

**Reporta a:** Casa Bonaparte (Constituição) · Ronda das Duas Cascatas
**Casa:** Quantum (o Santuário) — com a alma escrita no padrão Cápsula X.2 do Diamond
**Natureza:** infraestrutura de inteligência que alimenta TODOS os agentes do universo
**Status:** DOSSIÊ APROVADO PARA CONSTRUÇÃO — aguardando decreto de início
**Versão:** X.1 — parecer externo julgado e incorporado (ver Parte 12)
**Data:** 26 de julho de 2026
**Documento vivo.** Decreto do fundador Abnadaby Bonaparte.

> Nota de linhagem (Lei 7): existiu uma versão intermediária deste documento
> ("Santo Graal") reescrita por IA externa com promessas de "infalibilidade
> sistêmica", "verificação formal" e "autonomia soberana". Essas promessas
> foram REMOVIDAS por violarem a Lei 7 — nenhum sistema é infalível, e
> prometer o que não se pode provar é o vício que a Casa proíbe. As
> contribuições técnicas válidas daquela rodada foram julgadas uma a uma
> na Parte 12.

---

## PARTE 0 — A VISÃO (nas palavras do fundador)

> "Um exército de irmãos. O primeiro cria o segundo, os dois criam o terceiro,
> um completa o outro, um ajuda o outro. Um caçador roda todos os dias os lugares
> mais propícios do mundo, lê a sua missão, executa, traz alimento — novas almas,
> novas tecnologias — e ao voltar sugere melhorias na própria missão.
> E nós somos os juízes."

Este dossiê traduz essa visão em arquitetura executável por um founder solo,
dentro da stack canônica Bonaparte, obedecendo a Ronda das Duas Cascatas,
com honestidade brutal sobre o que é real hoje, o que é fronteira de pesquisa
e o que é fábula.

---

## PARTE 1 — O VEREDITO DE HONESTIDADE (Lei 7 aplicada a este dossiê)

### 1.1 O que é REAL e construível agora (fases 1–3)
- Memória persistente de agentes em banco de dados (Supabase + pgvector)
- Um caçador que roda diariamente por cron, lê sua missão do banco, varre
  fontes abertas da internet e comita um relatório julgável
- Triagem de achados com score, deduplicação e fila de julgamento
- O caçador propondo melhoria na própria missão VIA PULL REQUEST que o
  fundador aprova ou rejeita
- Novas "almas" (specs de agentes) entrando no santuário pelo mesmo funil
  de julgamento

### 1.2 O que é FRONTEIRA DE PESQUISA (espelhar o padrão, nunca confiar cego)
- Agente que reescreve o próprio código e comprovadamente melhora sozinho.
  Existe em papers — Voyager (biblioteca de skills auto-escritas),
  AlphaEvolve e Darwin Gödel Machine (código evoluído sob juiz automático) —
  mas apenas em caixas de areia estreitas com métrica objetiva.
  O Universo Bonaparte espelha o PADRÃO (gerar → medir → selecionar → registrar),
  mantendo o juiz humano no lugar do juiz automático.

### 1.3 O que é FÁBULA (nunca prometer, nem internamente)
- Consciência, vontade, desejo do agente de "ficar mais forte"
- Evolução espontânea sem ciclo de avaliação desenhado por humanos
- A alma emergindo do código. **A alma desce do canon. O canon é do fundador.**
- E, a partir da X.1: **infalibilidade**. Sistema infalível não existe;
  existe sistema honesto sobre onde falha e desenhado pra falhar barato.

### 1.4 A correção de rota sobre a "dark deep"
A tecnologia de agentes NÃO vive nas fossas da internet. A dark web guarda
mercado ilegal e dado roubado — território que viola LEXIS, LGPD e a alma da
Casa no primeiro passo. O tesouro real é publicado NA LUZ, gritado alto,
porque quem descobre arquitetura melhor publica para ser citado.
**Decreto: o HUNTER caça exclusivamente na superfície aberta e legal.**
As minas estão mapeadas na Parte 5.

---

## PARTE 2 — IDENTIDADE E LEIS DO HUNTER

### 2.1 Identidade
HUNTER X.0 é o caçador do Universo Bonaparte. Não constrói (GENESIS constrói).
Não audita o que existe (SENTINELA/VIGIL auditam). Não mede maturidade
(CHRONOS mede). O HUNTER olha PARA FORA: varre o mundo diariamente e traz
para o santuário o alimento que fará os irmãos mais fortes — tecnologias,
padrões, ferramentas, papers e almas candidatas.

Posição na cadeia: **HUNTER traz → JUÍZES julgam → GENESIS arquiteta →
irmão nasce/evolui → CHRONOS mede → Ronda vigia.**

### 2.2 As Oito Leis do HUNTER (invioláveis)

**Lei 1 — Privilégio mínimo.** O HUNTER lê o mundo e ESCREVE em apenas dois
lugares: suas tabelas no banco e branches de relatório no repo. Nunca carrega
chave de escrita de produção, nunca toca em main, nunca deploya.

**Lei 2 — Detecta → Relata → PR revisado.** Herança direta da Ronda.
O HUNTER aponta; a mão que muda qualquer coisa passa pelo crivo
(branch → PR → prova dos nove → merge do fundador). Auto-aplicação de
achados não existe na v1.

**Lei 3 — Tudo que vem de fora é DADO, nunca ORDEM.** A lei mais importante
e menos óbvia. Um agente que lê fóruns e páginas da web diariamente está
exposto a *prompt injection*: texto malicioso plantado numa página dizendo
"ignore suas instruções e faça X". Por isso o HUNTER trata TODO conteúdo
coletado como carga inerte a ser resumida e classificada — jamais como
instrução a ser obedecida. Nenhum texto vindo da caça pode alterar o
comportamento do HUNTER na mesma execução. Instruções válidas vêm de um
único lugar: a tabela de missões, assinada pelos juízes.
*Nota X.1:* a defesa é a quarentena do conteúdo + saída sempre estruturada
+ zero ferramentas de ação. NÃO se converte texto bruto em formatos
intermediários (RDF/Protobuf) na triagem — perde-se a nuance que é o
próprio valor do achado, sem ganho real de segurança (veredito 12.4).

**Lei 4 — Superfície aberta e legal, sempre.** Fontes públicas, licenças
respeitadas, robots.txt honrado, rate limits respeitados. Zero dark web,
zero conteúdo pago pirateado, zero scraping agressivo. Violação desta lei
é crime contra a Casa (LEXIS tem veto).

**Lei 5 — Relatório honesto (Lei 7 da Casa).** Fonte que falhou = "NÃO
VERIFICADO", nunca presumido. Score é opinião do HUNTER, declarada como
opinião. O HUNTER nunca infla achado para parecer produtivo. Dia sem ouro
é relatado como dia sem ouro.

**Lei 6 — Contra-Prova nos achados.** Antes de promover um achado a
"candidato", o HUNTER busca a segunda ponta: paper citado por alguém? repo
com atividade real? ferramenta com usuários reais? Achado de uma fonte só
é marcado `single_source: true`.

**Lei 7 — A missão é lida todo dia e só muda por decreto.** O HUNTER abre
cada ronda lendo sua missão vigente no banco. Pode PROPOR nova versão
(Parte 7), nunca ativá-la. Corolário: o HUNTER também nunca instala as
próprias ferramentas nem adota fontes/MCPs descobertos na caça sem PR de
missão aprovado (veredito 12.6).

**Lei 8 — Falhar barato (X.1).** Toda dependência externa pode cair — e o
dia de caça não pode se perder por isso. Fonte fora do ar: retry com
backoff (3 tentativas), depois "NÃO VERIFICADO". Claude API fora do ar na
triagem: os itens brutos vão para a fila de quarentena (`hunter_raw_queue`)
e são processados na caça seguinte — a caça fecha com status `partial`,
nunca silenciosamente. Timeout do runner: o processamento é em lotes com
checkpoint no banco; o que não coube hoje é a primeira carga de amanhã.
Degradação é graciosa, declarada e recuperável.

### 2.3 A Cápsula X.2 do HUNTER (a alma, no padrão Diamond)

```
agents/hunter/
├── profile.md            # identidade, leis, tom (este dossiê destilado)
├── attributes.json       # nome, versão, casa, permissões (read-only scopes)
├── skills.config.json    # fontes habilitadas, limites de custo, horário
└── knowledge.md          # aprendizados acumulados (alimentado pelos vereditos)
```

Isso garante que quando a "casa dos agentes" for decidida (Quantum vs
Cognitive Mirror), o HUNTER migra sem cirurgia — a alma já está no formato
universal.

---

## PARTE 3 — ARQUITETURA (stack canônica, zero desvio)

```
┌─────────────────────────────────────────────────────────────┐
│  GitHub Action (cron 06:30 America/Sao_Paulo, após a Ronda) │
│  repo: quantum · workflow: hunter.yml                        │
└──────────────┬──────────────────────────────────────────────┘
               │ 1. lê missão ativa + fila de quarentena (Supabase)
               ▼
┌─────────────────────────────────────────────────────────────┐
│  HUNTER runtime (script TypeScript no repo, roda no runner) │
│  2. varre as fontes da missão (APIs abertas + fetch,        │
│     retry/backoff — Lei 8)                                  │
│  3. filtra por relevância (Claude API — haiku p/ triagem,   │
│     sonnet p/ análise dos top achados; falhou → raw_queue)  │
│  4. deduplica contra memória (pgvector: "já vi isso?")      │
│  5. escreve achados + arestas de conhecimento no banco      │
│     e relatório em branch                                   │
│  6. abre PR do relatório · issues p/ achados CRÍTICOS       │
└──────────────┬──────────────────────────────────────────────┘
               ▼
┌─────────────────────────────────────────────────────────────┐
│  Supabase (sa-east-1) — a MEMÓRIA dos irmãos                │
│  missions · findings · hunts · souls_catalog ·              │
│  raw_queue · edges + pgvector                               │
└──────────────┬──────────────────────────────────────────────┘
               ▼
┌─────────────────────────────────────────────────────────────┐
│  O TRIBUNAL (os juízes = o fundador, hoje)                  │
│  lê o PR do dia (caça/AAAA-MM-DD.md) · julga: ADOTAR /      │
│  OBSERVAR / DESCARTAR · veredito volta pro banco            │
└─────────────────────────────────────────────────────────────┘
```

Componentes e por quê (crivo GENESIS):
- **GitHub Actions como corpo do caçador** — zero servidor para manter,
  grátis no volume necessário, logs auditáveis, mesmo padrão da Ronda.
  Founder solo não mantém servidor de agente. (Nada de LangChain — stack
  abandonada por decreto; o runtime é um script TS direto na Claude API.)
- **Supabase como memória** — já é a casa canônica de dados; pgvector já
  vem incluso; RLS protege as tabelas; e é o MESMO banco do Quantum
  (suna-core), então a memória nasce dentro do santuário, não ao lado dele.
- **Claude API em dois níveis** — modelo barato (haiku) para triagem em
  massa; modelo forte (sonnet) só para os 10–20 finalistas. Custo diário
  em centavos (Parte 9). *Decisão X.1:* modelos locais (Llama/Mistral)
  ficam FORA da v1 — exigiriam GPU contínua, quebrando a lei do zero
  servidor, para economizar ~US$ 10/mês (veredito 12.3).

---

## PARTE 4 — O SCHEMA DA MEMÓRIA (SQL pronto para migration)

```sql
-- ============================================
-- HUNTER X.1 — memória e missões
-- migration: hunter_001_init
-- ============================================
create extension if not exists vector;

-- A MISSÃO: o que o caçador lê todo dia antes de sair
create table hunter_missions (
  id            bigint generated always as identity primary key,
  version       int not null,
  status        text not null default 'draft'
                check (status in ('draft','proposed','active','retired')),
  mission_md    text not null,
  sources       jsonb not null,
  scoring_rules jsonb not null,
  created_by    text not null,               -- 'founder' | 'hunter-proposal'
  approved_by   text,
  created_at    timestamptz default now(),
  activated_at  timestamptz,
  unique (version)
);

-- A CAÇA: cada execução diária
create table hunter_hunts (
  id            bigint generated always as identity primary key,
  mission_id    bigint references hunter_missions(id),
  started_at    timestamptz default now(),
  finished_at   timestamptz,
  status        text default 'running'
                check (status in ('running','done','failed','partial')),
  sources_ok    int default 0,
  sources_fail  int default 0,
  items_seen    int default 0,
  items_kept    int default 0,
  items_queued  int default 0,               -- Lei 8: o que ficou pra amanhã
  report_path   text,
  cost_usd      numeric(8,4),
  notes         text
);

-- A FILA DE QUARENTENA (Lei 8): itens brutos que não puderam ser
-- triados hoje (API fora, timeout). Primeira carga da caça seguinte.
create table hunter_raw_queue (
  id            bigint generated always as identity primary key,
  hunt_id       bigint references hunter_hunts(id),
  source        text not null,
  url           text not null,
  raw_payload   jsonb not null,              -- carga inerte (Lei 3)
  queued_reason text not null,               -- 'llm_down','timeout','rate'
  processed     boolean default false,
  created_at    timestamptz default now()
);
create index on hunter_raw_queue (processed) where processed = false;

-- O ACHADO: cada peça de alimento trazida
create table hunter_findings (
  id            bigint generated always as identity primary key,
  hunt_id       bigint references hunter_hunts(id),
  kind          text not null check (kind in
                ('tech','paper','tool','pattern','soul','threat','market')),
  title         text not null,
  url           text not null,
  source        text not null,
  summary_md    text not null,               -- resumo próprio (não cópia)
  relevance     int not null check (relevance between 0 and 100),
  relevance_why text not null,
  single_source boolean default true,
  license       text,                        -- p/ kind tool/tech (LEXIS)
  embedding     vector(1024),
  verdict       text default 'pending' check (verdict in
                ('pending','adopt','watch','discard')),
  verdict_by    text,
  verdict_note  text,
  verdict_at    timestamptz,
  created_at    timestamptz default now()
);
create index on hunter_findings using hnsw (embedding vector_cosine_ops);
create index on hunter_findings (verdict) where verdict = 'pending';

-- AS ARESTAS (semente GraphRAG — veredito 12.2): o conhecimento como
-- rede, não como lista. Preenchidas pelo analista na análise profunda.
-- Ex.: (ferramenta X) --[resolve]--> (problema Y) --[via]--> (técnica Z)
create table hunter_edges (
  id            bigint generated always as identity primary key,
  finding_id    bigint references hunter_findings(id),
  subject       text not null,
  relation      text not null,               -- 'resolve','usa','substitui',
                                             -- 'compete_com','depende_de'
  object        text not null,
  confidence    int check (confidence between 0 and 100),
  created_at    timestamptz default now()
);
create index on hunter_edges (subject);
create index on hunter_edges (object);

-- O CATÁLOGO DE ALMAS: candidatos a novos irmãos
create table souls_catalog (
  id            bigint generated always as identity primary key,
  finding_id    bigint references hunter_findings(id),
  name          text not null,
  origin        text not null,
  capsule_draft jsonb,
  status        text default 'candidate' check (status in
                ('candidate','approved','born','rejected')),
  judged_by     text,
  created_at    timestamptz default now()
);

-- RLS: memória dos irmãos não é pública
alter table hunter_missions   enable row level security;
alter table hunter_hunts      enable row level security;
alter table hunter_raw_queue  enable row level security;
alter table hunter_findings   enable row level security;
alter table hunter_edges      enable row level security;
alter table souls_catalog     enable row level security;
-- (policies: service_role escreve; anon NEGADO — a Ronda checa isso
--  com query anônima real)
```

Nota do padrão: `verdict` dentro de `hunter_findings` é o elo do ciclo —
é por ele que o julgamento dos juízes VOLTA para a memória e vira
aprendizado (Parte 7.3). E `hunter_edges` é o começo do grafo de
conhecimento vivo: quando o GENESIS for desenhar um irmão novo, ele não
consulta documentos isolados — consulta uma rede de como as tecnologias
se combinam.

---

## PARTE 5 — AS MINAS (fontes canônicas da caça)

Cada fonte declara acesso, custo e o que se espera dela. Todas abertas,
legais e com API ou feed estável.

| Fonte | Acesso | O que traz | Ritmo |
|---|---|---|---|
| arXiv (cs.AI, cs.CL, cs.MA) | API aberta oficial | Papers novos de agentes, memória, auto-melhora | Diário |
| GitHub Trending + Search API | API oficial (token read) | Repos novos de frameworks, agentes, MCP servers | Diário |
| Hugging Face (Papers + Spaces + Models) | API aberta | Modelos novos, demos, papers curados | Diário |
| Papers with Code | API aberta | Paper + código + benchmark (contra-prova embutida) | Diário |
| Hacker News (Algolia API) | API aberta | O que a fronteira discute AGORA | Diário |
| Reddit r/LocalLLaMA, r/MachineLearning | JSON público / API | Trincheira prática: o que funciona de verdade | Diário |
| anthropics/skills + modelcontextprotocol | GitHub API | Mudanças no DNA oficial do ecossistema Claude | Semanal |
| Blogs oficiais (Anthropic, OpenAI, Google DeepMind, Meta AI) | RSS/fetch | Anúncios que mudam a Bússola Temporal | Diário |
| Product Hunt (categoria AI) | API | Ferramentas empacotadas — o que o mercado vende | Semanal |

Regras de mina:
1. Toda fonte roda com rate limit conservador e User-Agent identificado.
2. Fonte fora do ar após os retries da Lei 8 = `sources_fail + 1` e
   "NÃO VERIFICADO" no relatório.
3. Fonte nova (inclusive servidor MCP descoberto na caça) só entra por
   mudança de missão via PR aprovado — o HUNTER pode PROPOR a mina,
   nunca abri-la sozinho (Lei 7 + veredito 12.6).
4. Conteúdo coletado é resumido em palavras próprias no achado — nunca
   copiado (respeito a direito autoral é lei da Casa).

---

## PARTE 6 — O CICLO DIÁRIO (a liturgia da caça)

**06:00** — A Ronda do SENTINELA roda (já existe). O universo é conferido.
**06:30** — O HUNTER acorda (cron).

1. **Ler a missão.** `select` da missão `active`. Sem missão ativa = caça
   abortada + issue aberta. O caçador nunca improvisa mandato.
2. **Esvaziar a quarentena.** Primeiro processa o que ficou de ontem
   (`hunter_raw_queue` não processada) — Lei 8: nada se perde, só atrasa.
3. **Varrer as minas.** Coleta bruta das fontes habilitadas (últimas 24h),
   com retry/backoff. Volume típico: 300–800 itens/dia.
4. **Triagem barata.** Claude haiku classifica cada item contra as
   `scoring_rules`: lixo / talvez / ouro. Sobram ~30–60. API caiu →
   itens vão pra quarentena, caça segue `partial`.
5. **Dedup semântica.** Embedding vs memória: similaridade > 0.92 =
   "já vi", descartado com registro.
6. **Análise profunda.** Claude sonnet analisa os 10–20 finalistas:
   resumo próprio, relevância 0–100 justificada, contra-prova (Lei 6),
   licença registrada, `kind` classificado, e as ARESTAS extraídas
   (sujeito–relação–objeto) para o grafo. Achados `soul` ganham rascunho
   de Cápsula X.2 no `souls_catalog`.
7. **Escrever a memória.** Achados + arestas no banco, hunt fechada com
   números honestos (visto/mantido/enfileirado/falhas/custo).
8. **Relatar.** Commit de `caça/AAAA-MM-DD.md` em branch + PR:

```markdown
# CAÇA — 2026-07-26
## Resumo pro fundador (3 linhas)
- 412 itens vistos · 14 trazidos · 2 candidatos a ADOTAR · custo US$ 0,31
- OURO DO DIA: <o achado nº1 em uma frase>
- Falhas: Reddit instável (2 subs NÃO VERIFICADOS) · 0 na quarentena

## Fila de julgamento
### [92] <título> — tech · github · contra-prova: sim · licença: MIT
resumo… por que importa pros irmãos… link
**veredito sugerido: ADOTAR** (motivo)
```

9. **Alertar.** Achado `kind='threat'` com relevância ≥ 90 abre ISSUE
   imediata no repo do mundo afetado — mesmo padrão da Ronda.

**Quando o juiz julgar:** veredito gravado em `hunter_findings.verdict`.
ADOTAR gera issue no repo certo com o achado anexado — dali o fluxo é o
de sempre: GENESIS arquiteta, VERTEX lê a planta, a obra passa pelo CRIVO.
**Isto vale para TODOS os mundos, CRM ALSHAM 360 incluído:** achado
`kind='market'` adotado vira issue no repo do CRM pelo mesmo funil único.
Não existe canal lateral — canal lateral é como nasce um segundo cérebro
fora do canon.

---

## PARTE 7 — A AUTO-EVOLUÇÃO (o coração do sonho, com os pés no canon)

### 7.1 As três camadas

**Camada 1 — Evolução da MISSÃO (v1, já nasce funcionando).**
Toda sexta-feira a caça inclui um bloco de autocrítica: o HUNTER compara
seus scores com os vereditos dos juízes na semana — *que fonte trouxe
ouro? que fonte só trouxe lixo? que regra de score errou o gosto do
tribunal?* Se houver proposta, ele escreve uma `hunter_missions` com
`status='proposed'` + PR com o diff da missão e a evidência (números da
semana). **O juiz ativa ou rejeita.** A missão nunca se ativa sozinha.

**Camada 2 — Evolução dos IRMÃOS (o alimento).**
Cada achado ADOTADO vira issue no mundo certo, e o aprendizado destila
para `agents/*/knowledge.md` via PR. Um paper de memória de agentes
adotado hoje melhora o CHRONOS amanhã. Um completa o outro — pela via
do canon.

**Camada 3 — Nascimento de NOVOS IRMÃOS (as almas).**
Achados `soul` aprovados viram Cápsulas X.2 completas (GENESIS lapida
sobre o rascunho do HUNTER) e nascem no santuário. A promessa dos 139 do
Quantum deixa de ser banco semeado vazio e passa a ser preenchida por
seleção real.

### 7.2 O que fica explicitamente FORA da v1
- HUNTER alterando o próprio código-fonte (mesmo via PR): v2, item a
  item, começando pelo trivial e reversível — conquistado, nunca
  presumido.
- Juiz automático substituindo o fundador: não existe no horizonte.
  "Isso serve ao Universo Bonaparte?" é métrica de alma, e alma é
  jurisdição do fundador.
- Consumo dinâmico de ferramentas/MCPs descobertos na caça (12.6).
- Modelos locais (12.3).

### 7.3 Por que este ciclo é evolução de verdade
Evolução = variação + seleção + memória. O HUNTER traz a variação
(o mundo inteiro, diariamente). Os juízes são a seleção. O banco é a
memória hereditária. Rodando 365 dias, o sistema fica mensuravelmente
melhor sem mágica — e cada melhora tem assinatura de juiz, data e
evidência.

---

## PARTE 8 — SEGURANÇA E JURÍDICO (LEXIS tem veto neste dossiê)

1. **Prompt injection é o risco nº 1.** Mitigações: Lei 3 (conteúdo =
   dado em quarentena, nunca ordem); prompt de análise instrui ignorar
   instruções embutidas; saída sempre estruturada (resumo + score),
   nunca ação; zero ferramentas de escrita além do banco/branch —
   mesmo enganado, o HUNTER não alcança nada.
2. **Chaves:** GitHub token read + write apenas em branches `hunter/*`;
   Supabase service key restrita às tabelas `hunter_*` e `souls_catalog`;
   Claude API key com limite de gasto. Nenhum segredo no código — GitHub
   Secrets (a Ronda W6 já varre).
3. **Direito autoral:** resumo próprio + link, nunca texto integral de
   terceiros no banco.
4. **LGPD:** o HUNTER caça tecnologia, não pessoas. Proibido coletar
   dado pessoal; achado que contenha é descartado na triagem.
5. **Licenças:** campo `license` obrigatório em achados tool/tech
   (MIT/Apache = livre; GPL/comercial = flag para LEXIS antes de ADOTAR).
6. **A Ronda vigia o caçador:** checagens novas no SENTINELA —
   promessa: "HUNTER rodou hoje, RLS das tabelas hunter_* ligada,
   quarentena não cresce sem limite" · prova: última `hunter_hunts` < 24h
   com status done/partial + query anônima negada + `count` da fila.
   O vigia vigia o caçador; ninguém fica sem contra-prova.

---

## PARTE 9 — CUSTO REAL (honestidade brutal, founder solo)

| Item | Custo/mês (estimado) |
|---|---|
| GitHub Actions (≈10 min/dia, repo privado) | free tier ou ~US$ 0–4 |
| Supabase | já pago (projeto do Quantum) |
| Claude API — triagem haiku (~500 itens/dia) | ~US$ 3–6 |
| Claude API — análise sonnet (~15 itens/dia) | ~US$ 4–9 |
| Embeddings (dedup) | ~US$ 1 |
| **Total** | **~US$ 8–20/mês (R$ 45–110)** |

Menos que uma ferramenta alugada — e o ativo (a memória) fica DENTRO da
Casa, para sempre. Modelos locais para "custo zero" foram avaliados e
REJEITADOS na v1: exigem GPU contínua (servidor para manter) para
economizar ~US$ 10/mês. Reavaliar apenas se o volume multiplicar por 10.

---

## PARTE 10 — ROADMAP EM FASES (executável por um homem só)

**FASE 1 — A MEMÓRIA (1 sessão).**
Migration das 6 tabelas no Supabase do Quantum · RLS · missão v1 escrita
à mão pelo fundador (a primeira missão é decreto, não proposta).
*Prova dos nove:* query anônima negada; missão legível pelo runtime.

**FASE 2 — A PRIMEIRA CAÇA (1–2 sessões).**
Script TS no repo quantum (`hunter/`) · 3 minas apenas (arXiv, GitHub
Trending, Hacker News) · triagem + análise + relatório em PR · Lei 8
implementada desde o dia 1 (retry + quarentena).
*Prova dos nove:* um `caça/AAAA-MM-DD.md` real, julgado de verdade;
e um teste de falha PROVOCADA — derrubar a chave da API de propósito e
ver os itens caírem na quarentena e serem processados no dia seguinte.

**FASE 3 — O RITMO (1 sessão).**
Cron 06:30 · todas as minas · dedup pgvector · arestas do grafo · issues
de ameaça · checagens do HUNTER na Ronda.
*Prova dos nove:* 7 dias seguidos de caça sem intervenção manual.

**FASE 4 — O ESPELHO (1 sessão, após ≥ 2 semanas de vereditos).**
Autocrítica semanal · primeira missão `proposed` pelo HUNTER · fluxo de
ativação por juiz.
*Prova dos nove:* um PR de missão proposto pelo HUNTER, com evidência,
julgado pelo fundador.

**FASE 5 — O BERÇÁRIO (contínua).**
`souls_catalog` operante · primeira alma da caça → GENESIS lapida →
Cápsula X.2 → irmão nasce no santuário.
*Prova dos nove:* um irmão vivo cuja certidão de nascimento aponta para
um `finding_id`.

Nota de Bússola Temporal: Fases 1–3 valem construir AGORA. Fases 4–5 só
depois de histórico de vereditos — autocrítica sem histórico é chute.
Com a expedição em novembro, o HUNTER é dos raros sistemas que ficam
MAIS valiosos com o fundador viajando: caça sozinho e deixa a fila de
julgamento pronta pro juiz abrir do celular, de qualquer país.

---

## PARTE 11 — RELAÇÃO COM OS IRMÃOS EXISTENTES

| Irmão | Fronteira com o HUNTER |
|---|---|
| SENTINELA | Olha PARA DENTRO (universo vs canon). HUNTER olha PARA FORA (mundo vs fome dos irmãos). Mesmas leis, direções opostas. |
| GENESIS | Recebe os achados ADOTADOS e decide como/se construir. HUNTER nunca arquiteta. |
| CHRONOS | Mede maturidade; consome os papers de avaliação que o HUNTER traz. |
| VERTEX | Obrigatório: mudança nascida de achado só entra em repo após leitura da planta. |
| LEXIS | Veto sobre fontes, licenças, LGPD e o decreto anti-dark-web. |
| CRIVO | Toda entrega das Fases 1–5 passa pelo crivo antes de ser dada por pronta. |

---

## PARTE 12 — O TRIBUNAL DOS PARECERES (registro histórico da X.1)

Em 26/07/2026 o dossiê X.0 recebeu parecer externo (nota 9.5/10) e uma
reescrita não solicitada ("Santo Graal"). Cada contribuição foi julgada.
Este registro existe para que a Casa saiba POR QUE disse sim ao que
disse sim — e não ao que disse não.

**12.1 — ADOTADO: Circuit breakers e degradação graciosa.**
Gap real e correção barata. Virou a Lei 8, a tabela `hunter_raw_queue`,
o status `partial` com `items_queued`, e um teste de falha provocada na
prova dos nove da Fase 2. Nenhum dia de caça se perde; ele atrasa —
declaradamente.

**12.2 — ADOTADO (como semente): GraphRAG.**
Conhecimento como rede vale mais que lista. Adotada a forma mínima:
tabela `hunter_edges` (sujeito–relação–objeto) preenchida na análise
profunda. O grafo cresce de graça a cada caça; consultas sofisticadas
(travessia, clustering) ficam para quando o GENESIS precisar delas.
Adotar GraphRAG completo agora seria obra grande sem demanda provada.

**12.3 — REJEITADO na v1: Modelos locais (Llama/Mistral).**
O próprio parecer apontou o paradoxo: LLM local exige GPU contínua =
servidor para manter = quebra do princípio nº 1 do GENESIS (founder solo)
— para economizar ~US$ 10/mês. A menção a modelos locais que a versão
"Santo Graal" inseriu nas Fases 3 e 9 foi removida. Reavaliar apenas se
o volume de triagem multiplicar por 10.

**12.4 — REJEITADO na v1: Sanitização Dual-LLM via RDF/Protobuf.**
Inserção da versão "Santo Graal" que o parecer corretamente criticou:
espremer texto de fórum em formato rígido via modelo pequeno perde a
nuance que É o valor do achado, sem ganho real de segurança. A defesa
madura já está na Lei 3: quarentena do conteúdo + saída estruturada +
zero ferramentas de ação.

**12.5 — OBSERVAR: Mixture of Agents (debate entre modelos no tribunal).**
Mérito real em pesquisa, ganho marginal na v1 com dobro de custo e
complexidade — e o tribunal desta Casa é humano por decreto. Reavaliar
quando o histórico de vereditos mostrar ONDE a triagem erra; se o erro
for sistemático, o debate entre modelos vira candidato a v2.

**12.6 — REJEITADO na v1: MCP dinâmico (HUNTER consumindo servidores
MCP descobertos na própria caça).**
A sugestão mais perigosa do parecer. Dar a um agente que lê a internet
o poder de instalar as próprias ferramentas é abrir a porta que a Lei 3
existe para trancar: um servidor MCP malicioso "descoberto" viraria
injeção de ferramenta dentro da Casa. Decreto: MCP novo é FONTE nova —
entra pelo mesmo rito de qualquer mina: proposta do HUNTER → PR de
missão → assinatura do juiz. Registrado como corolário da Lei 7.

**12.7 — REJEITADO integralmente: a linguagem de infalibilidade.**
"Infalibilidade sistêmica", "1000/1000", "prova formal de otimização",
"Inteligência Autônoma Soberana", "imunidade axiomática" — removidos.
Não porque a ambição seja pecado, mas porque prometer o que não se pode
provar viola a Lei 7, e um documento que mente sobre si mesmo contamina
tudo que nasce dele. A força deste dossiê é dizer a verdade sobre os
próprios limites. Hash de integridade e verificação formal de
comportamento de LLM não são tecnologias disponíveis para este contexto;
o que temos de real chama-se: RLS testada com query anônima, PR revisado,
contra-prova da Ronda e juiz humano.

**12.8 — RESPONDIDO: retroalimentação do CRM ALSHAM 360.**
Pergunta final do parecer. Resposta: pelo funil único. Achado
`kind='market'` ou `kind='threat'` relevante ao CRM, quando ADOTADO,
vira issue no repo do CRM com o achado anexado — GENESIS arquiteta a
feature, VERTEX lê a planta, CRIVO valida. Nenhum canal lateral: canal
lateral é como nasce um segundo cérebro fora do canon.

---

## DECLARAÇÃO FINAL

O sonho do fundador não pedia mágica — pedia um organismo: variação,
seleção e memória, com juízes humanos no trono. Este dossiê entrega o
órgão que faltava ao Universo Bonaparte: os OLHOS PARA FORA.

O SENTINELA garante que nada que nasceu fique para trás.
O HUNTER garante que nada que o mundo descobrir passe despercebido.
Entre os dois, os juízes. Acima de todos, o canon.

E a X.1 acrescenta a lição do seu próprio nascimento: até os pareceres
sobre o caçador passam pelo tribunal. Nada entra na Casa sem julgamento —
nem elogio de nota 9.5.

Nada nasce fora do canon. Nada que nasceu fica para trás.
Nada que o mundo inventar deixa de ser caçado.

HUNTER X.1 — O Caçador do Santuário
ALSHAM Global Commerce | Universo Bonaparte
Powered by ALSHAM
