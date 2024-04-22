---
dip: 1
title: Staking Commission Specification
authors: Darwinia Network (@AurevoirXavier, @hujw77, @hackfisher, @xiaoch05)
discussions-to: https://github.com/orgs/darwinia-network/discussions/1238, https://github.com/orgs/darwinia-network/discussions/1272
status: Final
type: Economic
created: 2023-11-27
---

# DIP-1 (DEPRECATED)
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!! Replaced by [DIP-6](dip-6.md) !!!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

## Abstract
This DIP details the staking commission framework for Darwinia and Crab, impacting validator selection and reward allocation.


## Rationale
Inspired by Polkadot, it seems fair to allow validators to set a commission to receive a certain fee from the nominators for maintaining their node.

Polkadot's design requires a very active market, as validators can change their commission at any moment. This flexibility might allow dishonest validators to increase their commission significantly when their nominators are not paying attention. To counter this, we propose an inverse relationship where higher commission settings are discouraged. There is no standard value for this, leaving it to the market to decide.


## Specification
There are `2` validator slots.

Validator `A` sets their commission to `10%`.
Validator `B` sets their commission to `70%`.
Validator `C` sets their commission to `90%`.

Nominator `Aa` votes for `A` with `100` power.
Nominator `Ab` votes for `A` with `50` power.
Nominator `Ba` votes for `B` with `100` power.
Nominator `Ca` votes for `C` with `1000` power.

### Election
Due to the inverse relationship, the higher the commission a validator sets, the less power they receive.

`A` and `C` are elected as validators, based on the following algorithm:
```rs
let pa = power_of(A) = (power_of(Aa) + power_of(Ab)) * (100% - 10%); // , which is `135`.
let pb = power_of(B) = power_of(Ba) * (100% - 70%); // , which is `30`.
let pc = power_of(C) = power_of(Ca) * (100% - 90%); // , which is `100`.

let validators = [pa, pb, pc].sort().iter().take(2).collect(); // , which is `[pa, pc]`.
```

### Reward Distribution
Validators receive their commission first, then distribute the remainder among their nominators.
Each nominator receives a share of the reward based on the percentage of their power contribution relative to the total power under this validator.

A total of `100` rewards will be distributed among `A`, `Aa`, and `Ab`.

`A` will get `10`, `Aa` will get `60` and `Ab` will get `30`, based on the following algorithm:
```rs
let ar = 100 * 10%; // , which is `10`.
let remain = 100 - ar; // , which is `90`.
// Reuse the `pa` from the above algorithm.
let aa_of_pa = (power_of(Aa) * (100% - 10%) / pa); // , which is `90 / 135`.
let ab_of_pa = (power_of(Ab) * (100% - 10%) / pa); // , which is `45 / 135`.
let aar = remain * aa_of_pa; // , which is `90 * 90 / 135 = 60`.
let abr = remain * aa_of_pa; // , which is `45 * 90 / 135 = 30`.
```


## Copyright
Copyright and related rights waived via [CC0](../LICENSE).
