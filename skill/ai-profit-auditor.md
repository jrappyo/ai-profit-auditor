# AI Feature Profitability Audit (3x Value Rule)

Run a unit economics audit on an AI feature to determine if it clears the 3x Value Rule — the minimum threshold for sustainable AI product margins.

## How to use

You can invoke this with arguments or let Claude walk you through it interactively.

**With arguments:** `/ai-profit-auditor $ARGUMENTS`

Accepted arguments (all optional, defaults shown):
- `pin=5.00` — Cost per 1M input tokens ($)
- `pout=15.00` — Cost per 1M output tokens ($)
- `tavg=2500` — Average total tokens per request
- `cfixed=0.002` — Fixed per-request costs (vector DB, orchestration, etc.)
- `vhuman=60.00` — Hourly rate of the human user ($)
- `msaved=5.0` — Minutes saved per successful AI action

**Example:** `/ai-profit-auditor pin=3.00 pout=12.00 msaved=8`

---

## Instructions for Claude

When this skill is invoked:

1. **Parse any arguments** from `$ARGUMENTS`. If arguments are missing or not provided, use the defaults listed above. Do NOT ask the user for every input — just run with defaults and show them what was assumed.

2. **Calculate using this exact logic:**

   ```
   c_in  = (tavg × 0.8) × (pin  / 1,000,000)   # input token cost (80% of tokens)
   c_out = (tavg × 0.2) × (pout / 1,000,000)   # output token cost (20% of tokens)
   Cv    = c_in + c_out + cfixed                 # total variable cost per request
   Vh    = (vhuman / 60) × msaved               # dollar value of time saved
   R     = Vh / Cv                               # profitability ratio
   ```

3. **Output this report** (formatted cleanly in a code block):

   ```
   ----------------------------------------
    AI FEATURE PROFITABILITY AUDIT
   ----------------------------------------
    Inputs Assumed:
      Token Cost (In/Out):   $X.XX / $X.XX per 1M
      Avg Tokens/Request:    X,XXX
      Fixed Cost/Request:    $X.XXXX
      Human Rate:            $XX.XX/hr
      Minutes Saved:         X.X min
   ----------------------------------------
    Variable Cost (Cv):      $X.XXXX
    Value Created (Vh):      $X.XXXX
    Profitability Ratio (R): X.XXx
   ----------------------------------------
    VERDICT: [GREEN / YELLOW / RED] LIGHT
    [One-line interpretation]
   ----------------------------------------
   ```

   Verdict thresholds:
   - R >= 3.0 → GREEN LIGHT — "Sustainable product. Ship it."
   - R >= 1.5 → YELLOW LIGHT — "Marginal. Needs optimization before scale."
   - R < 1.5  → RED LIGHT — "Broken unit economics. Do not ship at scale."

4. **After the report**, add a short "Optimization Levers" section (3–5 bullets) suggesting the highest-impact changes the PM could make to improve the ratio — based on the actual numbers (e.g., if Cv is high relative to Vh, focus on token reduction; if Vh is low, focus on use-case selection).

5. If the user provides arguments in any reasonable format (key=value, plain numbers in order, natural language like "assume $80/hr rate"), parse them sensibly and note what you interpreted.
