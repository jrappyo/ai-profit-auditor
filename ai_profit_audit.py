import argparse

def calculate_3x_profitability(p_in, p_out, t_avg, c_fixed, v_human, m_saved):
    """
    Calculates the profitability ratio of an AI feature based on the 3x Value Rule.
    Assumes a standard 80/20 input-to-output token distribution.
    """
    c_in = (t_avg * 0.8) * (p_in / 1_000_000)
    c_out = (t_avg * 0.2) * (p_out / 1_000_000)
    cv = c_in + c_out + c_fixed

    vh = (v_human / 60) * m_saved

    ratio = vh / cv if cv > 0 else 0

    return cv, vh, ratio

def main():
    parser = argparse.ArgumentParser(description="AI Feature Profitability Audit (3x Value Rule)")
    parser.add_argument("--pin", type=float, default=5.00, help="Cost per 1M Input Tokens ($)")
    parser.add_argument("--pout", type=float, default=15.00, help="Cost per 1M Output Tokens ($)")
    parser.add_argument("--tavg", type=int, default=2500, help="Avg Total Tokens per Request")
    parser.add_argument("--cfixed", type=float, default=0.002, help="Fixed per-request costs (Vector DB, etc.)")
    parser.add_argument("--vhuman", type=float, default=60.00, help="Hourly rate of the human user ($)")
    parser.add_argument("--msaved", type=float, default=5.0, help="Minutes saved per successful action")

    args = parser.parse_args()

    cv, vh, ratio = calculate_3x_profitability(
        args.pin, args.pout, args.tavg, args.cfixed, args.vhuman, args.msaved
    )

    print("-" * 40)
    print(" AI FEATURE PROFITABILITY AUDIT")
    print("-" * 40)
    print(f" Variable Cost per Request (Cv):  ${cv:.4f}")
    print(f" Value Created per Request (Vh):  ${vh:.4f}")
    print(f" Profitability Ratio (R):         {ratio:.2f}x")
    print("-" * 40)

    if ratio >= 3.0:
        print(" VERDICT: GREEN LIGHT (Sustainable Product)")
    elif ratio >= 1.5:
        print(" VERDICT: YELLOW LIGHT (Needs Optimization)")
    else:
        print(" VERDICT: RED LIGHT (Broken Unit Economics)")
    print("-" * 40)

if __name__ == "__main__":
    main()
