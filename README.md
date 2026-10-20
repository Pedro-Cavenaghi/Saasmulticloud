# IHMInvest

Aplicação web de página única para projetar investimentos e consolidar resultados de AWS Lambda, Azure Functions e Google Cloud Functions.

## Estrutura

- `frontend-app/ihminvest-frontend.html` — interface, gráfico, chamadas HTTP e fallback local.
- `aws-lambda/` — implementação AWS (ainda não configurada).
- `azure-functions/` — implementação Azure (ainda não configurada).
- `google-functions/` — implementação Google Cloud (ainda não configurada).
- `Atividade 04 - Ecossistema SaaS Multicloud Integrado.pdf` — enunciado da atividade.
- `IHMInvest Fluxo.docx` — fluxo da aplicação.

## Executar

Abra o HTML no navegador para usar os cálculos locais. Para chamadas às APIs, sirva o frontend por HTTP (por exemplo, com Live Server no VS Code) e configure os endpoints no objeto `API_ENDPOINTS`, no fim de `frontend-app/ihminvest-frontend.html`.

O frontend envia requisições `POST` JSON em paralelo, com timeout de 8 segundos. Cada módulo mostra o provedor, o estado da chamada e a latência real. Se a URL estiver vazia ou a chamada falhar, somente aquele módulo usa o cálculo local; falhas de serviço aparecem como “Serviço temporariamente indisponível”.

## Contratos HTTP esperados

Todas as respostas devem ser JSON com valores numéricos:

| Provedor | Entrada | Resposta |
|---|---|---|
| AWS Lambda | `initial`, `monthly`, `annualRate` (decimal), `months` | `balance`, `invested`, `profit` |
| Azure Functions | `balance`, `usdRate`, `eurRate` | `usd`, `eur`, `usdRate`, `eurRate` |
| Google Cloud Functions | `balance`, `inflation` (decimal), `months` | `real` |

As funções precisam aceitar `POST` com `Content-Type: application/json` e permitir por CORS a origem usada pelo frontend. Atualmente, as três pastas de funções estão vazias e os endpoints não estão configurados.

As projeções são estimativas e não constituem recomendação financeira.
