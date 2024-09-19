---
dip: 4
title: Governance V2
authors: Darwinia Network (@AurevoirXavier)
discussions-to: None
relate-to: [DIP-8](dip-8.md)
status: Final
type: Governance
created: 2024-09-18
---

# DIP-4

## Abstract

This DIP proposes the introduction of GovernanceV2, also known as OpenGov, to the Darwinia Network.

For more information, please refer to the official OpenGov [wiki](https://wiki.polkadot.network/docs/learn-polkadot-opengov).

## Rationale

**In V1:**
- Only one proposal could be voted on at a time, which is inconvenient for a community-driven project like the Darwinia Network. A more flexible governance system is needed to support multiple simultaneous proposals.
- The council holds excessive power in the governance process. A more decentralized governance system is required to enhance community involvement in decision-making.
- The technical committee has limited functionality within the current governance framework. A more comprehensive governance system is necessary to increase the technical committee's effectiveness.

**With V2:**
- Multiple proposals across different tracks can be voted on simultaneously, enhancing the efficiency and flexibility of the governance process.
- The introduction of tracks allows for more granular control over pass requirements.
- The council can be removed, and its responsibilities delegated to different tracks, thereby ensuring a more decentralized governance structure.
- The technical committee can function similarly to a fellowship within Polkadot, enabling it to whitelist proposals and expedite the governance process.

## Specification

Seven tracks will be configured for the Darwinia Network.

The first one is `Root`, which remains essentially the same as in V1. Every passed proposal will be executed with the root origin.

The remaining tracks are defined as follows:

```rs
pub enum Origin {
	/// Origin able to dispatch a whitelisted call.
	WhitelistedCaller,
	/// General admin
	GeneralAdmin,
	/// Origin able to cancel referenda.
	ReferendumCanceller,
	/// Origin able to kill referenda.
	ReferendumKiller,
	/// Origin able to spend up to 4M RING from the treasury at once.
	MediumSpender,
	/// Origin able to spend up to 20M RING from the treasury at once.
	BigSpender,
}
```

The specific spending limits are implemented through the following code:

```rs
macro_rules! decl_ensure {
	(
		$vis:vis type $name:ident: EnsureOrigin<Success = $success_type:ty> {
			$( $item:ident = $success:expr, )*
		}
	) => {
		$vis struct $name;
		impl<O: Into<Result<Origin, O>> + From<Origin>>
			EnsureOrigin<O> for $name
		{
			type Success = $success_type;
			fn try_origin(o: O) -> Result<Self::Success, O> {
				o.into().and_then(|o| match o {
					$(
						Origin::$item => Ok($success),
					)*
					r => Err(O::from(r)),
				})
			}
			#[cfg(feature = "runtime-benchmarks")]
			fn try_successful_origin() -> Result<O, ()> {
				// By convention the more privileged origins go later, so for greatest chance
				// of success, we want the last one.
				let _result: Result<O, ()> = Err(());
				$(
					let _result: Result<O, ()> = Ok(O::from(Origin::$item));
				)*
				_result
			}
		}
	}
}
decl_ensure! {
	pub type Spender: EnsureOrigin<Success = Balance> {
		MediumSpender = 4_000_000 * UNIT,
		BigSpender = 20_000_000 * UNIT,
	}
}
```

## Copyright

Copyright and related rights waived via [CC0](../LICENSE).
