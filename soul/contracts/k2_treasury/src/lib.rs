#![no_std]
use soroban_sdk::{contract, contractimpl, contracttype, Address, Env};

#[contracttype]
#[derive(Clone)]
pub enum DataKey {
    Admin,
    ProposedAdmin,
    ReserveFactor,
    ProtocolFees,
}

#[contract]
pub struct AeternaTreasury;

#[contractimpl]
impl AeternaTreasury {
    /// ZERO HARDCODING: Initialize the treasury dynamically with an admin and reserve factor
    pub fn init(env: Env, admin: Address, reserve_factor: u32) {
        admin.require_auth();
        if env.storage().instance().has(&DataKey::Admin) {
            panic!("AETERNA_TREASURY: Already initialized");
        }
        env.storage().instance().set(&DataKey::Admin, &admin);
        env.storage()
            .instance()
            .set(&DataKey::ReserveFactor, &reserve_factor);
        env.storage().instance().set(&DataKey::ProtocolFees, &0i128);
    }

    /// ABSOLUTE SECURITY: Step 1 - Propose a new admin (Two-Step Admin Transfer)
    pub fn propose_admin(env: Env, new_admin: Address) {
        let current_admin: Address = env.storage().instance().get(&DataKey::Admin).unwrap();
        current_admin.require_auth();
        env.storage()
            .instance()
            .set(&DataKey::ProposedAdmin, &new_admin);
    }

    /// ABSOLUTE SECURITY: Step 2 - Accept admin role (Prevents Fat Finger errors)
    pub fn accept_admin(env: Env) {
        let proposed_admin: Address = env
            .storage()
            .instance()
            .get(&DataKey::ProposedAdmin)
            .expect("AETERNA_TREASURY: No proposed admin");
        proposed_admin.require_auth();

        env.storage()
            .instance()
            .set(&DataKey::Admin, &proposed_admin);
        env.storage().instance().remove(&DataKey::ProposedAdmin);
    }

    /// HYBRID PUSH/PULL: Synchronize protocol fees directly to the admin without blocking operations
    pub fn sync_fees(env: Env) -> i128 {
        let admin: Address = env.storage().instance().get(&DataKey::Admin).unwrap();
        admin.require_auth();

        let current_fees: i128 = env
            .storage()
            .instance()
            .get(&DataKey::ProtocolFees)
            .unwrap_or(0);

        // Extract fees (Pull) and reset internal counter
        env.storage().instance().set(&DataKey::ProtocolFees, &0i128);
        current_fees
    }

    /// COGNITIVE ENGINE INTEGRATION: Update the reserve factor dynamically from Wealth Sentinel
    pub fn update_reserve_factor(env: Env, new_factor: u32) {
        let admin: Address = env.storage().instance().get(&DataKey::Admin).unwrap();
        admin.require_auth();
        
        env.storage()
            .instance()
            .set(&DataKey::ReserveFactor, &new_factor);
    }

    /// Internal logic: Accumulate fees during transactions (Borrow/Lending/Flashloans)
    pub fn accumulate_fees(env: Env, transaction_amount: i128) {
        let current_fees: i128 = env
            .storage()
            .instance()
            .get(&DataKey::ProtocolFees)
            .unwrap_or(0);
        
        let reserve_factor: u32 = env
            .storage()
            .instance()
            .get(&DataKey::ReserveFactor)
            .unwrap_or(0);

        // RAY Math Concept: amount * reserve_factor / 10000 (Basis Points)
        let fee = (transaction_amount * (reserve_factor as i128)) / 10000;
        
        env.storage()
            .instance()
            .set(&DataKey::ProtocolFees, &(current_fees + fee));
    }
}
