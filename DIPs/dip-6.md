---
dip: 6
title: Flexible and Secure Staking System
authors: Darwinia Network (@AurevoirXavier, @hackfisher)
discussions-to: https://github.com/orgs/darwinia-network/discussions/1455
status: Final
type: Security
created: 2024-04-10
---


# DIP-6
## Abstract
Restrict the rate of entry and exit in collator staking while eliminating the unstaking period to offer a more flexible staking system.


## Rationale
1. Unlike the Darwinia1 solochain model, under the relaychain parachain model,
   security is upheld by validators on the relaychain side. Collators are solely responsible for block collection;
   therefore, the original mechanism for maintaining network security should be updated accordingly.
2. Currently, there is no staking slash mechanism in place, rendering the unbonding duration largely irrelevant.
   This should be replaced by a different mechanism. However, should a staking slashing mechanism be implemented in the future,
   reintroduction of the unbonding duration should be reconsidered.
3. Introducing a rate-limited mechanism can mitigate potential instability in token prices affecting network stability
   if the unbonding duration is removed. Other factors also play a role. Similar mechanisms are employed by Ethereum to maintain network stability.
   Essentially, this involves determining a **maximum amount** and setting it as the upper limit.
   Withdrawals within **a specific time period** must not exceed this limit in order to minimize impact on collator elections.
4. Before transitioning to another governance model, limitations exist within *OpenGov*. When users lock their tokens in other DApps,
   they are unable to utilize those tokens to vote in referenda and contribute to a healthy community.
   This proposed mechanism addresses this issue specifically within the staking module, allowing users to withdraw their tokens immediately to participate in referenda.


## Specification
TODO:
- How to determine the **maximum amount**?
- What will be the duration of **the specific time period**?
- Other details.


## Copyright
Copyright and related rights waived via [CC0](../LICENSE).
