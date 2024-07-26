---
dip: 7
title: EVM Staking
authors: Darwinia Network (@AurevoirXavier, @hackfisher, @hujw77)
discussions-to: https://github.com/orgs/darwinia-network/discussions/1481
status: Final
type: Core
created: 2024-06-30
---

# DIP-7

## Abstract
This proposal aims to migrate the original collator staking and deposit functionalities from pallets to EVM contracts.


## Rationale
1. **Standardization**: Standardizing Collator Staking and Deposit ensures better compatibility with ERC20 and ERC721 standards. This integration will enhance our infrastructure and ecosystem interactions, making the system more accommodating to Liquidity Staking Tokens (LSTs). Additionally, it allows transforming deposits into NFTs, which can be transferred and traded in the NFT market.
2. **Governance**: As a prerequisite to the next-generation governance system, transitioning Collator Staking and Deposit to smart contracts will facilitate the adoption of standardized governance models like those provided by Tally/OpenZeppelin Governor contracts. This shift will make on-chain governance more intelligent and standardized.


## Specification
- **RING Staking Contract**: Implement a RING staking contract where users can stake/unstake RING and nominate collators.
  - User can engage in staking/unstaking through this contract, which will issue an ERC20 token with ERC20Votes extension upon staking. This token can not be transferred, but it is the governance token of RingDAO.
- **Deposit Contract**: Implement a deposit contract that replicates the functionality of the original deposit pallet, converting deposits into ERC721 NFT tokens. Users can use this NFT for further staking/unstaking in the RING staking contract.
  - The Deposit NFT can be transferred.
- **Governance Integration**: RING, Deposit NFT, staked RING and Deposit NFT in staking contract can participate the governance of RingDAO.
- **Runtime**: Due to the limitations of the Polkadot-SDK framework, session rotation and reward distribution logic will still need to remain on the runtime pallet side.

### Detail
#### RING Staking Pallet
- Add a `RewardToRing` interface to transfer the runtime-minted/distributed reward to the contract.
- Add an `ElectionResultProvider` interface to receive the election result from the contract.
  - Apply the election result to the session pallet.
  - Handle the zero addresses as described in the below RING staking contract part.
- During the migration stage, rewards need to be distributed to both the runtime and the contract.
  - Proper handling is required to distinguish whether the collator comes from the runtime or the contract.

#### RING Staking Contract
- Provide `createNominationPool()` interface for collator create a nomination pool.
  - One collator only could create one pool to participate staking.
- Provide `stake()` and `unstake()` interface for user participate staking, while also nominating a collator.
  - Support RING and Deposit NFT.
- Provide `claim()` interface for user to withdraw staking rewards.
- Provide `collate()` interface for collator change the commision.
- Provide `distributeReward()` interface to distribute staking reward for collator and nominators.
  - Only runtime could call this function.
- Provide a `getTopCollators(n)` interface for runtime to query the top `n` collators based on stakers' votes.
  - The election result will be yielded in `[H160; n]`. If `n` is greater than the actual collator count, the result will be padded with zero addresses, which the runtime needs to filter out.

#### Deposit Contract
- Provide `migrate()` interface for user migrate Deposit from old deposit pallet to this contract.
  - Only runtime could call this function.
- Provide `deposit()` interface for user deposit RING with months.
  - In return, a set number of KTONs reward to users.
  - As a voucher, the user will receive a Deposit NFT.
- Prvode `claim()` interface for user withdraw RING.
  - If on time, the Deposit NFT will be burned. 
  - If prematurely, a penalty of 3x KTON is required.

#### Governance Integration
- Implement an ERC20 token that includes the ERC20Votes extension.
  - Grant `Minter Roler` and `Burner Role` to RING Staking Contract.
  - Wrapp RING and Deposit NFT to this token.
  - Could not be transferred.
- Create a flexible DAO using the Aragon DAO framework.

### Additional
#### Migration Strategy
To ensure a smooth protocol update, a migration curve has been implemented. Our goal is to minimize any impact on the rights of current staking users. Users have **2** months to transition from runtime staking to EVM staking. During this period, staking will operate in a hybrid mode. We will gradually decrease the runtime staker seats and increase the EVM staker seats following this curve. Over time, all stakers will be elected from the EVM side.


## Copyright
Copyright and related rights waived via [CC0](../LICENSE).
