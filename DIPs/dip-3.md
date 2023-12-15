---
dip: 3
title: Introduce EIP-1559 to Reform the Network Fee Market
authors: Darwinia Network
discussions-to: https://github.com/orgs/darwinia-network/discussions/1163
status: Final
type: Economic
created: 2023-12-14
---


# DIP-3
## Abstract
This DIP suggests implementing `EIP-1559` within the Darwinia Network to transform its fee structure.

Under this proposal, all transaction fees would be burned, while tips would be awarded directly to block authors.
This aligns with our future inflation strategy, motivates collators, and paves the way for practical applications of *RING* and *KTON* tokens.
The result is a more predictable, sustainable, and user-centric ecosystem.


## Rationale
### Reasons
1. By adopting `EIP-1559`, which replaces the gas auction system with a base fee plus a priority fee,
   users will benefit from more predictable transaction costs while also reducing network congestion during peak times.
   This improvement serves both individual users and the network overall.

### Future Objectives
1. To align with our upcoming inflation model,
   the burning mechanism of `EIP-1559` for part of the transaction fees is consistent with Darwinia's strategy to revamp its inflation system.
   This approach aims to maintain long-term token value stability and promote sustainable development of the network.
3. To better balance responsibilities and rewards within the relay chain-parachain structure, where collators play a more indirect role in security,
   it's logical to adjust block production incentives to reflect their updated contribution to consensus maintenance and network protection.
4. To enhance utility for *RING* and *KTON* tokens, introducing tangible use cases is essential.
   Doing so encourages wider token engagement within network activities and increases their practical value.

### References
- https://eips.ethereum.org/EIPS/eip-1559


## Specification
Integrate this within `DealWithFees` and pass the struct to `pallet-transaction` to enable the updated transaction fee model.
```rs
impl pallet_transaction_payment::Config for Runtime {
	type OnChargeTransaction =
		pallet_transaction_payment::CurrencyAdapter<Balances, DealWithFees<Runtime>>;
	..
}

/// EIP-1559 like configuration.
///
/// Burn the base fee and allocate the tips to the block producer.
pub struct DealWithFees<R>(core::marker::PhantomData<R>);
impl<R> frame_support::traits::OnUnbalanced<pallet_balances::NegativeImbalance<R>>
	for DealWithFees<R>
where
	R: pallet_authorship::Config + pallet_balances::Config,
{
	fn on_unbalanceds<B>(
		mut fees_then_tips: impl Iterator<Item = pallet_balances::NegativeImbalance<R>>,
	) {
		// substrate
		use frame_support::traits::Currency;

		if fees_then_tips.next().is_some() {
			if let Some(tips) = fees_then_tips.next() {
				if let Some(author) = <pallet_authorship::Pallet<R>>::author() {
					// Tip the block producer here.
					<pallet_balances::Pallet<R>>::resolve_creating(&author, tips);
				}

				// Burn the tips here. (IMPOSSIBLE CASE)
			}
		}

		// Burn the base fee here.
	}
}
```


## Copyright
Copyright and related rights waived via [CC0](../LICENSE).
