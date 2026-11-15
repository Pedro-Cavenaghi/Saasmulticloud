# IHMInvest

Aplicação web de página única (SPA) para projeção de investimentos e consolidação de resultados em arquitetura Serverless Multicloud (Vercel, Azure Functions e Google Cloud Functions).

## 🚀 Arquitetura e Tecnologias

- **Frontend:** SPA desenvolvida em HTML5/JavaScript com gráficos dinâmicos, hospedada no **Railway**.
- **Função 01 (Cálculo de Juros Compostos):** Hospedada via Serverless Functions na **Vercel** (substituindo a AWS Lambda).
- **Função 02 (Conversão de Moedas - USD/EUR):** Hospedada no **Azure Functions**.
- **Função 03 (Ajuste de Inflação - IPCA):** Hospedada no **Google Cloud Functions**.

---

## 📁 Estrutura do Repositório

- `frontend-app/ihminvest-frontend.html` — Interface de usuário, gráficos, lógica de chamadas HTTP assíncronas e camada de fallback local.
- `api/juros.py` — Função Serverless em Python (Vercel) para o cálculo de juros compostos.
- `azure-functions/` — Código-fonte e configurações da função Azure.
- `google-functions/` — Código-fonte e configurações da função Google Cloud.
- `Atividade 04 - Ecossistema SaaS Multicloud Integrado.pdf` — Enunciado da atividade acadêmica.
- `IHMInvest Fluxo.docx` — Documentação do fluxo da aplicação.

---

## ⚙️ Como Executar e Configurar

1. **Frontend:** Pode ser acessado diretamente pelo link de produção no Railway ou executado localmente via servidor HTTP (ex: *Live Server* no VS Code).
2. **Endpoints:** As URLs de produção da Vercel, Azure e GCP devem estar configuradas no objeto `API_ENDPOINTS` localizado no final de `frontend-app/ihminvest-frontend.html`.

### Comportamento de Resiliência
O frontend envia requisições POST JSON em paralelo com timeout de 8 segundos. Cada módulo exibe o provedor, o status da requisição e a latência real. Caso uma URL esteja vazia ou ocorra falha de rede, o sistema ativa automaticamente o **fallback local** para garantir que a interface permaneça funcional, exibindo o aviso de indisponibilidade pontual do serviço.

---

## 🔌 Contratos HTTP Esperados

As requisições utilizam o método `POST` com `Content-Type: application/json` e suporte a CORS (`Access-Control-Allow-Origin: *`):

- **Vercel (Juros Compostos):**
  - *Entrada:* `initial`, `monthly`, `annualRate` (decimal), `months`
  - *Resposta:* `balance`, `invested`, `profit`
- **Azure Functions (Conversão):**
  - *Entrada:* `balance`, `usdRate`, `eurRate`
  - *Resposta:* `usd`, `eur`, `usdRate`, `eurRate`
- **Google Cloud Functions (Inflação):**
  - *Entrada:* `balance`, `inflation` (decimal), `months`
  - *Resposta:* `real` *(Nota: A taxa de inflação é injetada automaticamente pelo frontend através da constante `ESTIMATED_INFLATION_RATE` em 4,5% a.a.)*

---

> *As projeções exibidas são estimativas matemáticas para fins acadêmicos e não constituem recomendação financeira.*
