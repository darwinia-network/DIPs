---
dip: 0
title: Staking Power Specification
authors: Darwinia Network (@AurevoirXavier, @hackfisher)
discussions-to: None
relate-to: DIP-5
status: Superseded
type: Economic
created: 2023-11-28
---

# DIP-0 (SUPERSEDED)

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!! Replaced by [DIP-5](dip-5.md) !!!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


## Abstract

This DIP explicates the staking power specification applicable to Darwinia and Crab.

## Rationale

Darwinia's initial design recognizes the existence of two tokens.
To incorporate these two tokens in staking, a unified measuring unit is indispensable.

## Specification

Power is a composite unit of RINGs and KTONs.

There is a constant total of `1` billion power, with `50%` allocated to RINGs and `50%` to KTONs.

A RING pool exists, where all staked RINGs are held to share the `50%` power. The same applies to the KTON pool.

```rs
const TOTAL_POWER: u32 = 1_000_000_000;
const HALF_POWER: u32 = TOTAL_POWER / 2;

// Initially, there are no stakers.
static mut ring_pool = 0;
static mut kton_pool = 0;

// The power of a staker is the sum of their RINGs' power and their KTONs' power.
fn power_of(staker) {
	(staker.ring / ring_pool  + staker.kton / kton_pool) * HALF_POWER
}

// Staker `S1` stakes `25` RINGs.
ring_pool += 25; // , which becomes `25`.
assert_eq!(power_of(S1), HALF_POWER);

// Staker `S1` stakes `25` KTONs.
kton_pool += 25; // , which becomes `25`;
assert_eq!(power_of(S1), TOTAL_POWER);

// Staker `S2` stakes `75` RINGs.
ring_pool += 75; // , which becomes `100`.
assert_eq!(power_of(S1), 25 / 100 * HALF_POWER + HALF_POWER);
assert_eq!(power_of(S2), 75 / 100 * HALF_POWER);

// Staker `S2` stakes `25` KTONs.
kton_pool += 25; // , which becomes `50`.
assert_eq!(power_of(S1), 25 / 100 * HALF_POWER + 25 / 50 * HALF_POWER);
assert_eq!(power_of(S2), 75 / 100 * HALF_POWER + 25 / 50 * HALF_POWER);
```

## Copyright

Copyright and related rights waived via [CC0](../LICENSE).
