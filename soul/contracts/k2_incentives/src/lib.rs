#![no_std]
use soroban_sdk::{contract, contractimpl, contracttype, Address, Env};

#[contracttype]
#[derive(Clone)]
pub enum DataKey {
    Admin,
    AuthorizedRouter,
    TotalSupply,
    UserBalance(Address),
}

#[contract]
pub struct K2Incentives;

#[contractimpl]
impl K2Incentives {
    /// Initialize the Incentives engine with an Admin
    pub fn init(env: Env, admin: Address) {
        admin.require_auth();
        if env.storage().instance().has(&DataKey::Admin) {
            panic!("K2_INCENTIVES: Already initialized");
        }
        env.storage().instance().set(&DataKey::Admin, &admin);
        env.storage().instance().set(&DataKey::TotalSupply, &0i128);
    }

    /// Set the authorized router (The only entity allowed to mint rewards)
    pub fn set_router(env: Env, router: Address) {
        let admin: Address = env.storage().instance().get(&DataKey::Admin).unwrap();
        admin.require_auth();
        env.storage().instance().set(&DataKey::AuthorizedRouter, &router);
    }

    /// ABSOLUTE SECURITY: `require_auth` protects reward distribution
    pub fn handle_action(env: Env, user: Address, reward_amount: i128) {
        // Only the Authorized Router can trigger handle_action
        let router: Address = env
            .storage()
            .instance()
            .get(&DataKey::AuthorizedRouter)
            .expect("K2_INCENTIVES: Router not set");
        router.require_auth();

        if reward_amount <= 0 {
            panic!("K2_INCENTIVES: Invalid reward");
        }

        // Mint cognitive fuel to user
        let current_balance: i128 = env
            .storage()
            .instance()
            .get(&DataKey::UserBalance(user.clone()))
            .unwrap_or(0);
        env.storage()
            .instance()
            .set(&DataKey::UserBalance(user), &(current_balance + reward_amount));

        // Update total supply
        let total_supply: i128 = env
            .storage()
            .instance()
            .get(&DataKey::TotalSupply)
            .unwrap_or(0);
        env.storage()
            .instance()
            .set(&DataKey::TotalSupply, &(total_supply + reward_amount));
    }
}
