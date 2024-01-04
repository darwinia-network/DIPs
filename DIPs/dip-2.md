---
dip: 2
title: Seamless Account Integration Between EVM and Substrate
authors: Darwinia Network (@AurevoirXavier, @boundless-forest, @hackfisher)
status: Final
type: Core
created: 2023-12-13
---


# DIP-2
## Abstract
To facilitate Ethereum integration, Substrate-based chains are transitioning to `H160` account addresses, using `ECDSA` for signatures.
This change streamlines the user experience by consolidating address types and wallets.

## Rationale
Ethereum-like and Substrate-based chains differ significantly in their account format.

Ethereum uses `H160` for its account addresses, while Substrate opts for `H256`.

With the EVM being a superior feature, more Substrate-based chains are incorporating it into their systems to tap into Ethereum's ecosystem
Darwinia is doing the same.

However, this creates an issue where users and developers must juggle two distinct address types and wallets.

To avoid this disconnect, we've decided to adopt `H160` as the native account address type for Substrate.

With this improvement, users only need to interact with one type of account and wallet.


## Specification
Utilize `ECDSA` as the signature algorithm for Substrate native runtime.

```rs
/// Alias to 512-bit hash when used in the context of a transaction signature on the chain.
pub type Signature = fp_account::EthereumSignature;

/// Some way of identifying an account on the chain.
/// We intentionally make it equivalent to the public key of our transaction signing scheme.
pub type AccountId = <<Signature as sp_runtime::traits::Verify>::Signer as sp_runtime::traits::IdentifyAccount>::AccountId;
```

The address is 20 bytes long, and the public key no longer has a corresponding SS58 address.

All pallet addresses have been truncated to 20 bytes; simply remove the trailing zeros, which are 12 bytes long.


## Copyright
Copyright and related rights waived via [CC0](../LICENSE).
