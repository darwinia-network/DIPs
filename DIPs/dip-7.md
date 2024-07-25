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
  - Support for LSTs will align with standard practices in other ecosystems, such as implementing a liquid RING staking contract. Users can engage in staking/unstaking through this contract, which will issue an ERC20 stRING token upon staking. This token can be transferred, traded, or used to add liquidity in DEXes. Developers within the ecosystem can also create customized versions.
- **Deposit Contract**: Implement a deposit contract that replicates the functionality of the original deposit pallet, converting deposits into ERC721 NFT tokens. Users can use this NFT for further staking/unstaking in the RING staking contract.
  - Similar to the liquid RING staking contract, a liquid deposit contract will be developed to allow users to obtain an NFT voucher that can be transferred or traded while staking.
- **Governance Integration**: For participation in the next-generation governance system, the liquid RING staking token and liquid deposit token will be highly conducive, merely requiring configuration of voting weights in the governor contract.
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
- TODO: Detailed implementation.
  - Provide a `getTopCollators(n)` interface for runtime to query the top `n` collators based on stakers' votes.
  - The election result will be yielded in `[H160; n]`. If `n` is greater than the actual collator count, the result will be padded with zero addresses, which the runtime needs to filter out.

#### Deposit Contract
- TODO: Detailed implementation.

### Additional
#### Migration Strategy
To ensure a smooth protocol update, a migration curve has been implemented. Our goal is to minimize any impact on the rights of current staking users. Users have **2** months to transition from runtime staking to EVM staking. During this period, staking will operate in a hybrid mode. We will gradually decrease the runtime staker seats and increase the EVM staker seats following this curve. Over time, all stakers will be elected from the EVM side.


## Copyright
Copyright and related rights waived via [CC0](../LICENSE).
