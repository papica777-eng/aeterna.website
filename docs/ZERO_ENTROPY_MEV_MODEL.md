# AETERNA K2: Zero-Entropy MEV Model

## The Problem: Predatory MEV in DeFi
Traditional lending protocols rely on instantaneous spot prices from Automated Market Makers (AMMs) to calculate user Health Factors. This creates a massive vulnerability: **Flash-Loan Attacks**.
A malicious actor (bot/sniper) can borrow millions in a single transaction, artificially crash the spot price of an asset in an AMM, trigger a false liquidation of healthy user positions, and seize the liquidation bonus in the exact same ledger block.

## The Solution: Zero-Entropy Pricing (TWAP + Oracle Shielding)

K2 Kinetic Router completely neutralizes single-block price manipulation through a **Zero-Entropy** design:

1. **Time-Weighted Average Price (TWAP)**
   Instead of looking at the *current* spot price of XLM/USDC, K2 only evaluates Health Factors based on the average price over a trailing window (e.g., 30 minutes). 
   - *Result:* An attacker must manipulate the price and *hold* it there for 30 minutes, burning millions in arbitrage losses, making the attack mathematically unprofitable.

2. **Decoupled Liquidation Execution**
   By ensuring that price ingestion occurs independently from the AMM state of the exact current ledger, flash-loan manipulators cannot compute deterministic outcomes. The entropy (unpredictability) of the attack's success approaches zero, deterring sniper bots natively.

3. **Safe-Math Thresholds**
   Every liquidation computation checks absolute upper boundaries before execution (`checked_mul` and `checked_div`). Even if an oracle were to malfunction and send a bizarre price string, the math primitives panic securely (`unwrap_or_else(|| panic!("Math overflow"))`), terminating the transaction and protecting the vault.

### Verdict
Through TWAP integration and Safe-Math rust primitives, K2 guarantees that liquidations are executed **only** during genuine market shifts, ensuring absolute safety for institutional capital.
