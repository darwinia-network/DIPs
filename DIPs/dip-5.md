---
dip: 5
title: KTON Staking
authors: Darwinia Network
discussions-to: https://github.com/orgs/darwinia-network/discussions/1393
status: Final
type: Economic
created: 2024-1-29
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
The incumbent collator hybrid staking system within the Darwinia network has precipitated several complexities. The amalgamation of divergent incentivization objectives has rendered the system opaque and challenging to comprehend. Moreover, the binding of these incentives has resulted in restricted strategic actions, epitomizing suboptimal design.

To address these issues, this proposal underscores the necessity to decouple the *KTON* from the collator staking framework. Subsequently, the reformed collator staking would consist exclusively of the *RING*. This separation is anticipated to amplify the visibility of the *KTON* staking, thereby augmenting the potency of its incentives.

As a corollary of these changes, Collators will cease to partake in the commission distributions deriving from *KTON* stakes. Nevertheless, given that the quintessential function of Collators is to sustain network liveness, the commission incentives derived from *RING* stakes are deemed to be wholly adequate.

Furthermore, this proposal advocates for the dispensation of the convoluted and laborious-to-communicate `Power` concept presently embedded in the collator staking paradigm. The clarity of nomenclature and conceptualization is paramount, as it facilitates community discourse and the elucidation of perspectives.

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
   1. TBD.

These amendments aim to fortify the transparency and simplicity of the staking mechanism, ensuring that stakeholders can engage with the system with greater clarity and confidence.


## Copyright
Copyright and related rights waived via [CC0](../LICENSE).
