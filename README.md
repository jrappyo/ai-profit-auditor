# AI Feature Profitability Audit

A lightweight framework and CLI tool for product engineers to evaluate the unit economics of proposed AI features using the **3x Value Rule**.

## The Problem
Traditional SaaS models operate on high gross margins (typically 80% or more) because the marginal cost of a new user is near zero. Generative AI features break this model. Every user prompt incurs a direct Cost of Goods Sold (COGS) in the form of compute tokens. Without strict operational discipline, AI features can easily destroy product margins.

## The Solution: The 3x Value Rule
To ensure sustainable unit economics, an AI feature must generate measurable business value that is at least three times greater than its fully loaded variable cost.

R = Vh / Cv

Where:
* **R** is the Profitability Ratio.
* **Vh** is the Hard Value Created (e.g., labor arbitrage, time saved).
* **Cv** is the Unit Variable Cost (API costs, retrieval overhead).

A ratio of R >= 3.0 indicates a viable, scalable product feature.

## Usage
Run the Python script from your terminal to audit a feature during planning or grooming sessions.

### Basic Command
`python ai_profit_audit.py`

### Advanced Command (Custom Variables)
`python ai_profit_audit.py --pin 2.50 --pout 10.00 --tavg 4000 --vhuman 75.00 --msaved 10.0`

### Arguments
* `--pin`: Cost per 1M Input Tokens (USD). Default is 5.00.
* `--pout`: Cost per 1M Output Tokens (USD). Default is 15.00.
* `--tavg`: Average Total Tokens per Request. Default is 2500.
* `--cfixed`: Fixed per-request costs for infrastructure. Default is 0.002.
* `--vhuman`: Fully loaded hourly rate of the human user (USD). Default is 60.00.
* `--msaved`: Minutes saved per successful AI action. Default is 5.0.

## Output Matrix
The script will return one of three verdicts:
* **GREEN LIGHT (R >= 3.0):** Sustainable unit economics. Proceed to scale.
* **YELLOW LIGHT (1.5 <= R < 3.0):** Feature is at risk. Optimize prompts, implement semantic caching, or route to a smaller model.
* **RED LIGHT (R < 1.5):** Broken unit economics. Do not ship without a fundamental architectural pivot.
