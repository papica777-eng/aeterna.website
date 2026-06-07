# AETERNA K2 Smart Contracts Mainnet Deployment Pipeline

This repository hosts the production-ready Soroban deployment pipeline for the AETERNA K2 smart contracts:

- **k2_kinetic_router** (Kinetic router and liquidator proxy)
- **k2_incentives** (Incentives and liquidity rewards engine)
- **k2_treasury** (Protocol treasury and fee management)

## Deployment

The contracts are built, optimized, and deployed to Stellar Mainnet/Futurenet using the GitHub Actions workflow located in `.github/workflows/mainnet-deploy.yml`.

To trigger a deployment, navigate to the **Actions** tab in GitHub, select the **AETERNA Trinity Mainnet Deploy** workflow, and run it manually with the target network and audit justification.

---
*AETERNA Protocol Core — Dimitar Prodromov*
