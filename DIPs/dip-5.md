---
dip: 5
title: KTON Staking
authors: Darwinia Network (@AurevoirXavier, @hackfisher, @hujw77)
discussions-to: https://github.com/orgs/darwinia-network/discussions/1393
status: Final
type: Economic
created: 2024-01-29
---


# DIP-5
## Abstract
This DIP articulates the enhancement of the staking models.
The modification aims to segregate the operational logic, thereby refining the models' lucidity and user comprehensibility.

1. The proposal introduces the configuration of an independent staking mechanism for the *KTON* asset, thus establishing distinct and focused staking processes for each token.
2. It mandates that the election or selection of collators will be exclusively undertaken utilizing the *RING* currency.
3. The proposal outlines a reward distribution system with a set inflation rate of `20%` for both *RING* and *KTON* stakers, together accounting for a total inflation allocation of `40%`.
   This setup is similar to the prior scheme in which `Power` stakers shared a collective inflation reward of `40%`, with the notable difference being that *KTON* will not be utilized for elections.
4. Additionally, the proposal recommends the removal of the abstract `Power` concept from the staking vernacular, thereby streamlining and simplifying the staking framework.

The envisioned restructuring is projected to enhance the staking models' efficiency, transparency, and user engagement.


## Rationale
The incumbent collator hybrid staking system within the Darwinia network has precipitated several complexities.
The amalgamation of divergent incentivization objectives has rendered the system opaque and challenging to comprehend.
Moreover, the binding of these incentives has resulted in restricted strategic actions, epitomizing suboptimal design.

To address these issues, this proposal underscores the necessity to decouple the *KTON* from the collator staking framework. Subsequently, the reformed collator staking would consist exclusively of the *RING*.
This separation is anticipated to amplify the visibility of the *KTON* staking, thereby augmenting the potency of its incentives.

As a corollary of these changes, Collators will cease to partake in the commission distributions deriving from *KTON* stakes.
Nevertheless, given that the quintessential function of Collators is to sustain network liveness, the commission incentives derived from *RING* stakes are deemed to be wholly adequate.

Furthermore, this proposal advocates for the dispensation of the convoluted and laborious-to-communicate `Power` concept presently embedded in the collator staking paradigm.
The clarity of nomenclature and conceptualization is paramount, as it facilitates community discourse and the elucidation of perspectives.

It is imperative to reiterate that the economic incentives for both the *RING* and *KTON* pools are envisioned to be preserved at their current magnitude, thereby circumventing discussions pertinent to the quantum of incentives.


## Specification
These changes are designed to streamline the staking process and enhance their efficiency:

1. Decouple *KTON* staking from collator staking.
   1. Eliminate the Stake trait implementation for the *KTON* asset, thereby discontinuing its direct association with collator staking.
   2. Remove all *KTON*-related attributes from the Ledger structure, ensuring that it solely reflects *RING*-related staking activities.
   3. Discard the `KtonPool` storage entry, effectively obviating the need for maintaining a separate pool for *KTON* within the staking pallet.
   4. Convert existing Power attributes to *RING* votes to align with the new staking paradigm focused exclusively on *RING*.
   5. Expunge all *KTON*-specific parameters from extrinsic definitions, thus simplifying the interface and interactions with the staking system.
2. Institute *RING*-based elections.
   1. Abrogate the concept of Power in the context of election mechanics, replacing it with a straightforward *RING*-centric approach.
   2. Overhaul the election voting algorithm to accommodate the new framework that privileges *RING* as the sole medium for voting and election processes.
3. Implement *KTON* staking module.
   1. Deploy the *KTON Staker* contract.
   2. Periodically allocate the RING inflation rewards into the *KTON Staker* contract.
   3. Users must personally manually stake their KTON tokens to the *KTON Staker* contract in order to obtain rewards.
   4. Users must manually claim the rewards.
   5. There is no lock-up period for the staking, and the rewards are solely based on the amount and duration of the user's staking.
   6. By implementing the `StakingRewards` contract based on the Synthetix standard contract, it significantly alleviates the burden of auditing.

These amendments aim to fortify the transparency and simplicity of the staking mechanism, ensuring that stakeholders can engage with the system with greater clarity and confidence.

### Additional
#### Migration Strategy
To ensure a smooth protocol update, we've implemented a migration curve.
Our goal is to minimize any impact on the rights of current staking users as much as possible.
Users have **1** month to transition from V1 to V2.
We will gradually decrease the original KTON staking reward by applying this curve.
All power and reward calculations will be influenced by this curve.
Over time, the V1 reward share will decrease from **100%** to **0%**.

```rs
/// A curve helps to migrate to staking v2 smoothly.
pub struct MigrationCurve<T>(PhantomData<T>);
impl<T> Get<Perquintill> for MigrationCurve<T>
where
	T: Config,
{
	fn get() -> Perquintill {
		// substrate
		use sp_runtime::traits::SaturatedConversion;

		let x = (<frame_system::Pallet<T>>::block_number() - <MigrationStartBlock<T>>::get())
			.saturated_into::<u64>()
			.max(1);
		let month_in_blocks = 30 * 24 * 60 * 60 / 12;

		Perquintill::one() - Perquintill::from_rational(x, month_in_blocks)
	}
}

#[test]
fn migration_curves_should_work() {
	ExtBuilder::default().build().execute_with(|| {
		System::set_block_number(10);
		<MigrationStartBlock<Runtime>>::put(10);

		assert_eq!(
			vec![0, 1, 7, 14, 21, 29, 30, 31, 999]
				.into_iter()
				.map(|x| {
					System::set_block_number(10 + x * 24 * 60 * 60 / 12);

					format!("{:?}", <MigrationCurve<Runtime>>::get())
				})
				.collect::<Vec<_>>(),
			[
				"99.9995370370370371%",
				"96.6666666666666667%",
				"76.6666666666666667%",
				"53.3333333333333334%",
				"30%",
				"3.3333333333333334%",
				"0%",
				"0%",
				"0%"
			]
		);
	});
}
```

#### Notification mechanism
KTON staking rewards will be minted via the staking module.
Currently, minting occurs on the Substrate framework.
An EVM call is necessary to inform the contract that the reward has been issued.
However, because an EVM transaction incurs fees, we're using a treasury account to send this notification in order to maintain protocol simplicity.

```rs
/// KTON staker contact notification interface.
pub trait KtonStakerNotification {
	/// Notify the KTON staker contract.
	fn notify(_: Balance) {}
}
impl KtonStakerNotification for () {}
/// KTON staker contact notifier.
pub struct KtonStakerNotifier<T>(PhantomData<T>);
impl<T> KtonStakerNotification for KtonStakerNotifier<T>
where
	T: Config + darwinia_ethtx_forwarder::Config,
	T::RuntimeOrigin: Into<Result<ForwardEthOrigin, T::RuntimeOrigin>> + From<ForwardEthOrigin>,
	<T as frame_system::Config>::AccountId: Into<H160>,
{
	fn notify(amount: Balance) {
		// KTONStakingRewards
		// 0x000000000419683a1a03AbC21FC9da25fd2B4dD7
		let staking_reward =
			H160([0, 0, 0, 0, 4, 25, 104, 58, 26, 3, 171, 194, 31, 201, 218, 37, 253, 43, 77, 215]);

		let reward_distr = T::KtonRewardDistributionContract::get().into();
		// https://github.com/darwinia-network/kton-staker/blob/175f0ec131d4aef3bf64cfb2fce1d262e7ce9140/src/RewardsDistribution.sol#L11
		#[allow(deprecated)]
		let function = Function {
			name: "distributeRewards".into(),
			inputs: vec![
				Param {
					name: "ktonStakingRewards".into(),
					kind: ParamType::Address,
					internal_type: None,
				},
				Param { name: "reward".into(), kind: ParamType::Uint(256), internal_type: None },
			],
			outputs: vec![Param {
				name: "success or not".into(),
				kind: ParamType::Bool,
				internal_type: None,
			}],
			constant: None,
			state_mutability: StateMutability::Payable,
		};

		let request = ForwardRequest {
			tx_type: TxType::LegacyTransaction,
			action: TransactionAction::Call(reward_distr),
			value: U256::zero(),
			input: function
				.encode_input(&[Token::Address(staking_reward), Token::Uint(amount.into())])
				.unwrap_or_default(),
			gas_limit: U256::from(1_000_000),
		};
		// Treasury account.
		let sender = H160([
			109, 111, 100, 108, 100, 97, 47, 116, 114, 115, 114, 121, 0, 0, 0, 0, 0, 0, 0, 0,
		]);

		if let Err(e) = <darwinia_ethtx_forwarder::Pallet<T>>::forward_transact(
			ForwardEthOrigin::ForwardEth(sender).into(),
			request,
		) {
			log::error!("[pallet::staking] failed to notify KTON staker contract due to {e:?}");
		}
	}
}
```

## Copyright
Copyright and related rights waived via [CC0](../LICENSE).
