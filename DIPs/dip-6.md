---
dip: 6
title: Flexible and Secure Staking System
authors: Darwinia Network (@AurevoirXavier, @hackfisher)
discussions-to: https://github.com/orgs/darwinia-network/discussions/1455
status: Final
type: Economic
created: 2024-04-10
---


# DIP-6 (DEPRECATED)
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!! Replaced by [DIP-7](dip-7.md) !!!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

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
   Withdrawals and stakes within **a specific time period** must not exceed this limit in order to minimize impact on collator elections. Also the stake in is the same as the withdrawals.
4. Before transitioning to another governance model, limitations exist within *OpenGov*. When users lock their tokens in other DApps,
   they are unable to utilize those tokens to vote in referenda and contribute to a healthy community.
   This proposed mechanism addresses this issue specifically within the staking module, allowing users to withdraw their tokens immediately to participate in referenda.


## Specification
- The maximum amount is set to `20_000_000` *RING* initially. It can be adjusted any time by governance.
- To keep simplest, the specific time period is using the staking session period.

### Dynamic Rate Limit Strategy
We propose the introduction of a dynamic rate limiter to control the flow of stake both into and out of the system.

**Definitions:**
- `Pos` indicates a positive state.
- `Neg` indicates a negative state.

**Initial State:**
The `RateLimiter` starts in the state `Pos(0)`.

**Example Scenarios:**
1. **Withdrawal Scenario:**
   If a withdrawal of `10_000_000 RING` is made, the state changes to `Neg(10_000_000)`.
   - Remaining `RING` available for withdrawal: `10_000_000`
   - Remaining `RING` available for deposit: `30_000_000`
2. **Deposit Scenario:**
   If a deposit of `30_000_000 RING` follows, the state changes to `Pos(20_000_000)`.
   - Remaining `RING` available for withdrawal: `40_000_000`
   - Remaining `RING` available for deposit: `0`

This strategy allows for flexible management of staking rate limit, adapting dynamically to the current net flow of `RING`, thereby enhancing system stability and efficiency.

```rs
/// Staking rate limiter.
#[derive(Clone, Debug, PartialEq, Encode, Decode, MaxEncodedLen, TypeInfo)]
pub enum RateLimiter {
	/// Positive balance.
	Pos(Balance),
	/// Negative balance.
	Neg(Balance),
}
impl RateLimiter {
	fn flow_in(self, amount: Balance, limit: Balance) -> Option<Self> {
		match self {
			Self::Pos(v) => v.checked_add(amount).filter(|&v| v <= limit).map(Self::Pos),
			Self::Neg(v) =>
				if v >= amount {
					Some(Self::Neg(v - amount))
				} else {
					let v = amount - v;

					if v <= limit {
						Some(Self::Pos(v))
					} else {
						None
					}
				},
		}
	}

	fn flow_out(self, amount: Balance, limit: Balance) -> Option<Self> {
		match self {
			Self::Pos(v) =>
				if v >= amount {
					Some(Self::Pos(v - amount))
				} else {
					let v = amount - v;

					if v <= limit {
						Some(Self::Neg(v))
					} else {
						None
					}
				},
			Self::Neg(v) => v.checked_add(amount).filter(|&new_v| new_v <= limit).map(Self::Neg),
		}
	}
}
impl Default for RateLimiter {
	fn default() -> Self {
		Self::Pos(0)
	}
}

#[test]
fn rate_limiter_should_work() {
	let r = RateLimiter::default();
	let r = r.flow_in(1, 3).unwrap();
	assert_eq!(r, RateLimiter::Pos(1));

	let r = r.flow_in(2, 3).unwrap();
	assert_eq!(r, RateLimiter::Pos(3));
	assert!(r.clone().flow_in(1, 3).is_none());

	let r = r.flow_out(1, 3).unwrap();
	assert_eq!(r, RateLimiter::Pos(2));

	let r = r.flow_out(2, 3).unwrap();
	assert_eq!(r, RateLimiter::Pos(0));

	let r = r.flow_out(1, 3).unwrap();
	assert_eq!(r, RateLimiter::Neg(1));

	let r = r.flow_out(2, 3).unwrap();
	assert_eq!(r, RateLimiter::Neg(3));
	assert!(r.clone().flow_out(1, 3).is_none());

	let r = r.flow_in(1, 3).unwrap();
	assert_eq!(r, RateLimiter::Neg(2));

	let r = r.flow_in(2, 3).unwrap();
	assert_eq!(r, RateLimiter::Neg(0));

	let r = r.flow_in(1, 3).unwrap();
	assert_eq!(r, RateLimiter::Pos(1));

	let r = RateLimiter::Pos(3);
	assert_eq!(r.flow_out(6, 3).unwrap(), RateLimiter::Neg(3));

	let r = RateLimiter::Neg(3);
	assert_eq!(r.flow_in(6, 3).unwrap(), RateLimiter::Pos(3));
}
```


## Copyright
Copyright and related rights waived via [CC0](../LICENSE).
