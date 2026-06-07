#![no_std]
use soroban_sdk::{contract, contractimpl, contracttype, Address, Env};

#[contracttype]
#[derive(Clone)]
pub enum DataKey {
    Admin,
    CollateralCap,
    UserCollateral(Address),
    UserDebt(Address),
}

#[contract]
pub struct KineticRouter;

#[contractimpl]
impl KineticRouter {
    /// ZERO HARDCODING: Initialize Router with admin and collateral cap
    pub fn init(env: Env, admin: Address, collateral_cap: i128) {
        admin.require_auth();
        if env.storage().instance().has(&DataKey::Admin) {
            panic!("K2_ROUTER: Already initialized");
        }
        env.storage().instance().set(&DataKey::Admin, &admin);
        env.storage()
            .instance()
            .set(&DataKey::CollateralCap, &collateral_cap);
    }

    /// Provide liquidity / Deposit Collateral
    pub fn deposit_collateral(env: Env, user: Address, amount: i128) {
        user.require_auth();

        if amount <= 0 {
            panic!("K2_ROUTER: Invalid amount");
        }

        let cap: i128 = env.storage().instance().get(&DataKey::CollateralCap).unwrap_or(0);
        let current_collat: i128 = env
            .storage()
            .instance()
            .get(&DataKey::UserCollateral(user.clone()))
            .unwrap_or(0);

        // VULNERABILITY PATCHED: Collateral Cap Check
        if current_collat + amount > cap {
            panic!("K2_ROUTER: collateral_cap_triggered");
        }

        env.storage()
            .instance()
            .set(&DataKey::UserCollateral(user), &(current_collat + amount));
    }

    /// Borrow assets / Accrue Debt
    pub fn borrow(env: Env, user: Address, amount: i128) {
        user.require_auth();

        if amount <= 0 {
            panic!("K2_ROUTER: Invalid amount");
        }

        let current_collat: i128 = env
            .storage()
            .instance()
            .get(&DataKey::UserCollateral(user.clone()))
            .unwrap_or(0);
        
        let current_debt: i128 = env
            .storage()
            .instance()
            .get(&DataKey::UserDebt(user.clone()))
            .unwrap_or(0);

        let new_debt = current_debt + amount;

        // Verify Health Factor (RAY Math Representation: HF must be > 1.0 represented as > 10000 Basis Points)
        // For simplicity: Collateral / Debt > 1.25 (12500)
        let health_factor = (current_collat * 10000) / new_debt;
        if health_factor < 12500 {
            panic!("K2_ROUTER: health_factor_too_low");
        }

        env.storage()
            .instance()
            .set(&DataKey::UserDebt(user), &new_debt);
    }

    /// Liquidate an undercollateralized position
    pub fn liquidate(env: Env, liquidator: Address, target: Address) {
        liquidator.require_auth();

        let current_collat: i128 = env
            .storage()
            .instance()
            .get(&DataKey::UserCollateral(target.clone()))
            .unwrap_or(0);
        
        let current_debt: i128 = env
            .storage()
            .instance()
            .get(&DataKey::UserDebt(target.clone()))
            .unwrap_or(0);

        if current_debt == 0 {
            panic!("K2_ROUTER: Target has no debt");
        }

        let health_factor = (current_collat * 10000) / current_debt;
        // Liquidation Condition: Health factor drops below 1.0 (10000 bps)
        if health_factor >= 10000 {
            panic!("K2_ROUTER: Position is healthy");
        }

        // Execute Liquidation: Liquidator pays off debt, gets collateral (Implementation simplified)
        env.storage()
            .instance()
            .set(&DataKey::UserDebt(target.clone()), &0i128);
        env.storage()
            .instance()
            .set(&DataKey::UserCollateral(target), &0i128);
        
        // Add collateral to liquidator
        let liquidator_collat: i128 = env
            .storage()
            .instance()
            .get(&DataKey::UserCollateral(liquidator.clone()))
            .unwrap_or(0);
        env.storage()
            .instance()
            .set(&DataKey::UserCollateral(liquidator), &(liquidator_collat + current_collat));
    }
}
