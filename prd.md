# PRD: AI Profitability Auditor

## 1. Problem Statement
Product and engineering teams routinely ship generative AI features without a clear understanding of the underlying unit economics. Unlike traditional SaaS where the marginal cost of a feature is near zero, AI features incur a direct Cost of Goods Sold (COGS) for every transaction (compute tokens, vector retrieval, orchestration). This leads to a dangerous dynamic: shipping features that look successful in user engagement but actively degrade the company's gross margins.

## 2. Target Audience
* **Product Engineers:** Evaluating architectural trade-offs, model selection, and caching strategies.
* **Product Managers:** Grooming the backlog, writing specifications, and prioritizing features based on actual ROI rather than novelty.

## 3. Core Hypothesis
If we provide a zero-friction CLI tool that calculates the unit profitability of an AI feature *before* development begins, teams will possess the operational discipline to kill unprofitable ideas early or optimize their architecture to meet standard SaaS margin requirements.

## 4. The Standard: The 3x Value Rule
To justify the infrastructure, latency, and maintenance overhead, an AI feature must generate hard business value (time saved, labor displaced, direct revenue) that is at least 3x its variable cost.

## 5. Functional Requirements (v1.0)
* **Variable CLI Inputs:** The script must accept arguments for token costs, average token usage, fixed retrieval costs, and human labor rates.
* **Cost Calculation (Cv):** Calculate the fully loaded per-request cost, assuming a standard 80/20 input-to-output token distribution.
* **Value Calculation (Vh):** Calculate the monetary value of the time saved by the human user per successful action.
* **Ratio Output (R):** Display the Vh / Cv ratio clearly.
* **Decision Matrix:** Output a definitive "Green Light," "Yellow Light," or "Red Light" to enforce a Go/No-Go decision.

## 6. Out of Scope (v1.0)
* Real-time API integration with LLM provider pricing pages.
* Web-based GUI.
* Database integration for historical cost tracking.
