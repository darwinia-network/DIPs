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
  - Users can engage in staking/unstaking through this contract, which will issue an ERC20 token with the ERC20Votes extension upon staking. This token cannot be transferred but serves as the governance token of RingDAO.
- **Deposit Contract**: Implement a deposit contract that replicates the functionality of the original deposit pallet, converting deposits into ERC721 NFT tokens. Users can use this NFT for further staking/unstaking in the RING staking contract.
  - The Deposit NFT can be transferred.
- **Governance Integration**: RING, Deposit NFTs, staked RING, and Deposit NFTs in the staking contract can participate in the governance of RingDAO.
- **Runtime**: Due to the limitations of the Polkadot-SDK framework, session rotation and reward distribution logic will still need to remain on the runtime pallet side.

### Details
#### RING Staking Pallet
- Add a `RewardToRing` interface to transfer the runtime-minted/distributed reward to the contract.
- Add an `ElectionResultProvider` interface to receive the election result from the contract.
  - Apply the election result to the session pallet.
  - Handle zero addresses as described in the RING staking contract section.
- During the migration stage, rewards need to be distributed to both the runtime and the contract.
  - Proper handling is required to distinguish whether the collator comes from the runtime or the contract.

#### RING Staking Contract
- Provide a `createNominationPool()` interface for collators to create a nomination pool.
  - Each collator can create only one pool to participate in staking.
- Provide `stake()` and `unstake()` interfaces for users to participate in staking and nominate a collator.
  - Support RING and Deposit NFT.
- Provide a `claim()` interface for users to withdraw staking rewards.
- Provide a `collate()` interface for collators to change the commission.
- Provide a `distributeReward()` interface to distribute staking rewards to collators and nominators.
  - Only the runtime can call this function.
- Provide a `getTopCollators(n)` interface for the runtime to query the top `n` collators based on stakers' votes.
  - The election result will be yielded in `[H160; n]`. If `n` is greater than the actual collator count, the result will be padded with zero addresses, which the runtime needs to filter out.

#### Deposit Contract
- Provide a `migrate()` interface for users to migrate deposits from the old deposit pallet to this contract.
  - Only the runtime can call this function.
- Provide a `deposit()` interface for users to deposit RING with a specified duration.
  - In return, users will receive a set number of KTONs as a reward.
  - As a voucher, the user will receive a Deposit NFT.
- Provide a `claim()` interface for users to withdraw RING.
  - If on time, the Deposit NFT will be burned.
  - If prematurely, a penalty of 3x KTON is required.

#### Governance Integration
- Implement an ERC20 token that includes the ERC20Votes extension.
  - Grant `Minter Role` and `Burner Role` to the RING Staking Contract.
  - Wrap RING and Deposit NFTs into this token.
  - The token cannot be transferred.
- Create a flexible DAO using the Aragon DAO framework.

### Additional
#### EVM Transaction Fee
Any call that needs to be dispatched inside the pallet to the EVM contract requires a transaction fee due to the Frontier framework limitation. To prevent the transaction fee from affecting the original pallet accounts' balance, the Treasury pallet account will be used as the EVM transaction sender. All fees will be paid by the Treasury as a system expenditure.

#### Migration Strategy
To ensure a smooth protocol update, a migration curve has been implemented. Our goal is to minimize any impact on the rights of current staking users. Users have **2** months to transition from runtime staking to EVM staking. During this period, staking will operate in a hybrid mode. We will gradually decrease the runtime staker seats and increase the EVM staker seats following this curve. Over time, all stakers will be elected from the EVM side.

## Copyright
Copyright and related rights waived via [CC0](../LICENSE).
