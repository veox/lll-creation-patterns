# Interacting with `lll-creation-patterns` contracts

## Introduction

For a high-level overview of how these work and why they might be
useful, see [the `contracts` `README`][contracts-readme].

[contracts-readme]: ../contracts/README.md

The contracts described below have been deployed to the same address on
ETH-mainnet/Ropsten/Rinkeby/Kovan, and have this address registered on
mainnet ENS as `<contract-name>.veoxxoev.eth` for easy look-up.

The [`furiate`][furiate] script was used to do this; transaction data
can be seen [here][schedule].

[furiate]: https://gitlab.com/veox/furiate
[schedule]: https://gitlab.com/veox/furiate/blob/5dd6b3b2c62141a19e30f501e833ee145bc3edf8/schedule.py

A locally-compiled `lllc` from `solidity` release v0.4.21 was used to
compile the contracts.


## `collapser` (demo payload)

Source code: [`collapser.lll`][collapser-src] in `lll-contracts` repo.

[collapser-src]: https://gitlab.com/veox/lll-contracts/blob/c419bd68c2c15115c50ccd28d9d9163117658505/contracts/collapser.lll

This "contract" is used throught the examples below; it's actually just
two instructions at runtime: `ADDRESS SELFDESTRUCT`, or two bytes: `0x30ff`.

On any call, such a contract will remove itself from the state, together
with any ether that might have been sent to it.


## `stamping-press` (with `collapser` as static payload)

Address: `0xb20ad6089B9BEDCF6dDaadc4D9A56AD86694359a`
ENS: `stamping-press.veoxxoev.eth`
Source code: [`stamping-press-collapser.lll`][spc-src]
ABI: [`stamping-press-collapser.lll.abi`][spc-abi]
Solidity interface: [`stamping-press-collapser.solidity`][spc-sol]

[spc-src]:
[spc-abi]:
[spc-sol]:

On any invocation of the `stamp()` function, this contract will deploy a
new `collapser`. An event to that effect will be emitted, and the
newly-created contract's address returned by the `stamping-press`.

EtherScan will not display these, but you can look at the ["internal
transactions"][tx13it] tab to see the where your precious `collapser`
went.

[tx13it]: https://etherscan.io/tx/0xb1c0f5aeb16c16276a8bc84686a53be2174a3eaabb2c0b4d2c99157e4f7424c9#internal


## `cloning-vat` 

Address: `0xC533fFbdcc952069f710dc3f6FA08510125Bcd49`
ENS: `cloning-vat.veoxxoev.eth`
Source code: [../contracts/cloning-vat.lll]
ABI: [../contracts/cloning-vat.lll.abi]
Solidity interface: [../contracts/cloning-vat.solidity]

TODO


## `cannery`

Address: `0x25d62DA8E032c5cba01c351c7868f4b1a0E0949e`
ENS: `cannery.veoxxoev.eth`
Source code: [../contracts/cannery.lll]
ABI: [../contracts/cannery.lll.abi]
Solidity interface: [../contracts/cannery.solidity]

TODO


## A canned `collapser`

Address: `0x1e77625c9818c25d4f4FA6b40D24Ef231D1740eF`
ENS: `canned-collapser.veoxxoev.eth`
Source code: N/A
ABI: N/A
Solidity interface: N/A

TODO


## `can-opener`

Address: `0xC9d28DcA3CD8cCFDF583643837E3C637Bc59A789`
ENS: `can-opener.veoxxoev.eth`
Source code: [../contracts/can-opener.lll]
ABI: [../contracts/can-opener.lll.abi]
Solidity interface: [../contracts/can-opener.solidity]

TODO
