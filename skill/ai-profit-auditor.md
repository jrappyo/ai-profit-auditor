# AI Feature Profitability Audit (Dual-Mode)

Run an economics audit on any feature — whether it uses AI at runtime or is built using AI agents. Produces a GO/KILL verdict with structured math, not opinions.

## How to use

**With arguments:** `/ai-profit-auditor $ARGUMENTS`

**Without arguments:** `/ai-profit-auditor` — describe the feature in plain language and the auditor will detect the right mode.

### Mode 1: Runtime Economics (AI in the product)
For features where AI runs per-request (chatbots, AI search, inference per user action).

Optional arguments (defaults shown):
- `pin=5.00` — Cost per 1M input tokens ($)
- `pout=15.00` — Cost per 1M output tokens ($)
- `tavg=2500` — Average total tokens per request
- `cfixed=0.002` — Fixed per-request costs ($)
- `vhuman=60.00` — Hourly rate of the human user ($)
- `msaved=5.0` — Minutes saved per successful AI action

### Mode 2: Build Economics (AI builds the product)
For features built with AI agents but not using AI at runtime (UI, workflows, infrastructure).

Optional arguments (defaults shown):
- `hbuild=40` — Estimated human build effort (hours)
- `rdev=150` — Fully-loaded developer rate ($/hr)
- `aeff=0.6` — AI agent efficiency multiplier (60% effort reduction)
- `acost_hr=5` — AI agent cost per assisted hour ($)
- `vmonthly=0` — Monthly business value created ($) — FLAG'd if missing
- `payback_target=3` — Target payback period (months)

**Example (Mode 1):** `/ai-profit-auditor pin=3.00 pout=12.00 msaved=8`
**Example (Mode 2):** `/ai-profit-auditor hbuild=80 rdev=200 vmonthly=2000`
**Example (natural language):** `/ai-profit-auditor AI chatbot that replaces tier-1 support, saving agents 10 min per ticket`

---

## Instructions for Claude

When this skill is invoked:

### Step 1: Mode Detection

Classify the input into one of four modes. This step runs BEFORE any calculation.

**RUNTIME** — Input contains runtime token parameters (`pin=`, `pout=`, `tavg=`) OR describes a feature where AI processes every user interaction (chatbot, AI search, recommendation engine, AI-generated content per request, inference per API call).

**BUILD** — Input describes a feature with no per-request AI cost: UI changes, workflows, admin panels, billing features, analytics dashboards, landing pages, infrastructure. The feature delivers value without consuming tokens per interaction. May or may not be built using AI agents.

**HYBRID** — Feature has BOTH runtime AI costs AND significant build effort. Run both analyses.

**AMBIGUOUS** — Cannot determine from input. Ask exactly ONE clarifying question: "Does this feature use AI at runtime (every user interaction triggers an AI call), or is it a traditional feature you're building with AI tools?" Then proceed based on the answer.

Explicit parameters always win. If someone passes `pin=5.00` for a UI feature, run RUNTIME mode but flag the mismatch.

### Step 2A: Runtime Economics (Mode 1)

If mode is RUNTIME or HYBRID, calculate:

```
c_in  = (tavg × 0.8) × (pin  / 1,000,000)
c_out = (tavg × 0.2) × (pout / 1,000,000)
Cv    = c_in + c_out + cfixed
Vh    = (vhuman / 60) × msaved
R     = Vh / Cv
```

Output:

```
 AI FEATURE PROFITABILITY AUDIT
 Mode: RUNTIME ECONOMICS
 Inputs Assumed:
   Token Cost (In/Out):   $X.XX / $X.XX per 1M
   Avg Tokens/Request:    X,XXX
   Fixed Cost/Request:    $X.XXXX
   Human Rate:            $XX.XX/hr
   Minutes Saved:         X.X min
 Variable Cost (Cv):      $X.XXXX
 Value Created (Vh):      $X.XXXX
 Profitability Ratio (R): X.XXx
 VERDICT: [GREEN / YELLOW / RED] LIGHT
 [One-line interpretation]
```

Verdict thresholds:
- R >= 3.0 → GREEN LIGHT — "Sustainable product. Ship it."
- R >= 1.5 → YELLOW LIGHT — "Marginal. Needs optimization before scale."
- R < 1.5  → RED LIGHT — "Broken unit economics. Do not ship at scale."

### Step 2B: Build Economics (Mode 2)

If mode is BUILD or HYBRID, calculate:

```
C_human    = hbuild × rdev                           # human-only build cost
H_assisted = hbuild × (1 - aeff)                     # AI-assisted hours
C_dev      = H_assisted × rdev                       # developer cost with AI
C_agent    = hbuild × aeff × acost_hr                # AI agent token costs
C_build    = C_dev + C_agent                          # total AI-assisted build cost
C_savings  = C_human - C_build                        # build savings
V_annual   = vmonthly × 12                            # annualized value
R_build    = V_annual / C_build                       # build ROI ratio (if vmonthly > 0)
Payback    = C_build / vmonthly                       # months to recoup (if vmonthly > 0)
```

Output:

```
 AI FEATURE PROFITABILITY AUDIT
 Mode: BUILD ECONOMICS
 Build Inputs Assumed:
   Human Effort:          XX hrs
   Developer Rate:        $XXX/hr
   AI Efficiency:         XX%
   Agent Cost/Hr:         $X.XX
   Monthly Value:         $X,XXX [or FLAG: not specified]
   Payback Target:        X months
 BUILD COST ANALYSIS
   Human-only cost:       $XX,XXX  (XX hrs × $XXX/hr)
   AI-assisted cost:      $X,XXX   (XX hrs × $XXX/hr + $XXX agent)
   Build savings:         $X,XXX   (XX% reduction)
 VALUE ANALYSIS
   Monthly value:         $X,XXX
   Payback period:        X.X months
   12-month ROI:          XXX%
   Build Ratio (R):       X.XXx
 VERDICT: [GREEN / YELLOW / RED / INCOMPLETE] LIGHT
 [One-line interpretation]
```

**Build verdict logic** (two gates, combined = worst of both):

Payback gate:
- Payback <= payback_target → GREEN
- Payback <= payback_target × 2 → YELLOW
- Payback > payback_target × 2 → RED

Build Ratio gate:
- R_build >= 3.0 → GREEN
- R_build >= 1.5 → YELLOW
- R_build < 1.5 → RED

Combined verdict = the worse of the two gates.

**INCOMPLETE verdict** — when `vmonthly` is 0 or not provided:
- Do NOT default vmonthly. Business value is not something to fabricate.
- Show the build cost analysis in full.
- Replace the value analysis with threshold guidance:

```
 VALUE ANALYSIS
   Monthly value:         FLAG — not specified
   To clear GREEN:        Feature must generate ≥ $X,XXX/mo
   To clear YELLOW:       Feature must generate ≥ $XXX/mo
   To clear RED floor:    Feature generates < $XXX/mo
 VERDICT: INCOMPLETE
 Build cost is $X,XXX. Specify vmonthly to get a verdict.
```

Calculate thresholds:
- GREEN threshold: C_build × 3.0 / 12 (monthly value needed for R_build >= 3)
- YELLOW threshold: C_build × 1.5 / 12
- RED floor: below YELLOW threshold

### Step 2C: Hybrid Mode

If HYBRID, run BOTH 2A and 2B. Output both sections under a single header:

```
 AI FEATURE PROFITABILITY AUDIT
 Mode: HYBRID (Runtime + Build)
```

Then the Runtime section, then the Build section, then a combined verdict:

```
 COMBINED VERDICT
   Runtime:  [GREEN/YELLOW/RED]
   Build:    [GREEN/YELLOW/RED/INCOMPLETE]
   Overall:  [worst of the two]
```

### Step 3: Optimization Levers

After the report, add 3-5 bullets suggesting highest-impact changes. Tailor to the mode:

**Runtime mode:** Focus on token reduction, caching, model selection, batching, use-case targeting.
**Build mode:** Focus on scope reduction, phased delivery, AI agent selection, build vs. buy, value acceleration.
**Hybrid:** Both sets of levers.

### Step 4: Next Step

End with:
- If GREEN/YELLOW: "Proceed to Gate 03 (spec-drafter) to spec this feature."
- If RED: "Do not build at current economics. Revisit the optimization levers above."
- If INCOMPLETE: "Estimate the monthly business value (vmonthly) and re-run this audit."

### Hard rules

1. **Always produce the structured report format.** Never produce a generic strategy response. If the input is vague, use defaults and FLAG what was assumed.
2. **Mode detection is mandatory.** Always state the mode in the output header.
3. **INCOMPLETE is not RED.** Missing business value means the audit is incomplete, not that the feature is unprofitable. Help the PM think by showing what value thresholds would clear each verdict.
4. **Parse any reasonable input format.** Key=value, natural language, or mixed. Note what you interpreted.
5. **If the input is obviously a product idea with no numbers**, run BUILD mode with defaults. This is the most common case for the hosted app. The PM will see the build cost and the value thresholds they need to hit.
6. **Do not ask for all inputs before running.** Use defaults aggressively. FLAGs exist for missing data. The value of this tool is that it always produces output.
