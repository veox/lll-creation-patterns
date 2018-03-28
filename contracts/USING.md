# Interacting with `lll-creation-patterns` contracts

## Introduction

For a high-level overview of how these work and why they might be
useful, see [the `contracts` `README`][contracts-readme].

[contracts-readme]: ../contracts/README.md

The contracts described below have been deployed to the same addresses
across multiple chains (ETH-mainnet/Ropsten/Rinkeby/Kovan), and have
these addresses registered on mainnet ENS as
`<contract-name>.veoxxoev.eth` for convenience.

The [`furiate`][furiate] script was used to do this; transaction data
can be seen [here][schedule].

[furiate]: https://gitlab.com/veox/furiate
[schedule]: https://gitlab.com/veox/furiate/blob/d9eb4d2d75f3601a081bf8f830fd4cd12f8177ce/schedule.py

A locally-compiled `lllc` from `solidity` release v0.4.21 was used to
compile the contracts.


## `collapser` (demo payload)

* Source code: [`collapser.lll`][collapser-src] in `lll-contracts` repo.

[collapser-src]: https://gitlab.com/veox/lll-contracts/blob/c419bd68c2c15115c50ccd28d9d9163117658505/contracts/collapser.lll

This "contract" is used throughout the examples below; it's actually just
two instructions at runtime: `ADDRESS SELFDESTRUCT`, or two bytes: `0x30ff`.

On any call, such a contract will remove itself from the state, together
with any ether that might have been sent to it.


## `stamping-press` (with `collapser` as static payload)

* Address: `0xb20ad6089B9BEDCF6dDaadc4D9A56AD86694359a`
* ENS: `stamping-press.veoxxoev.eth`
* Source code: [`stamping-press-collapser.lll`][spc-src]
* ABI: [`stamping-press-collapser.lll.abi`][spc-abi]
* Solidity interface: [`stamping-press-collapser.solidity`][spc-sol]

[spc-src]: https://gitlab.com/veox/lll-creation-patterns/blob/923e322130ff611ebd2bbd16320d96f2b466844b/contracts/stamping-press/stamping-press-collapser.lll
[spc-abi]: https://gitlab.com/veox/lll-creation-patterns/blob/923e322130ff611ebd2bbd16320d96f2b466844b/contracts/stamping-press/stamping-press-collapser.lll.abi
[spc-sol]: https://gitlab.com/veox/lll-creation-patterns/blob/923e322130ff611ebd2bbd16320d96f2b466844b/contracts/stamping-press/stamping-press-collapser.solidity

On any invocation of the `stamp()` function, this contract will deploy a
new `collapser`. An event to that effect will be emitted, and the
newly-created contract's address returned by the `stamping-press`.

(EtherScan will not display these, but you can look at the ["internal
transactions"][tx13it] tab to see the where your precious `collapser`
went.)

[tx21it]: https://etherscan.io/tx/0xd3f3896f740332925372f29832337eada5604cf7c50c4b75d2656c03aa686aee#internal


## `cloning-vat` 

* Address: `0xC533fFbdcc952069f710dc3f6FA08510125Bcd49`
* ENS: `cloning-vat.veoxxoev.eth`
* Source code: [`cloning-vat.lll`][cv-src]
* ABI: [`cloning-vat.lll.abi`][cv-abi]
* Solidity interface: [`cloning-vat.solidity`][cv-sol]

[cv-src]: https://gitlab.com/veox/lll-creation-patterns/blob/923e322130ff611ebd2bbd16320d96f2b466844b/contracts/cloning-vat/cloning-vat.lll
[cv-abi]: https://gitlab.com/veox/lll-creation-patterns/blob/923e322130ff611ebd2bbd16320d96f2b466844b/contracts/cloning-vat/cloning-vat.lll.abi
[cv-sol]: https://gitlab.com/veox/lll-creation-patterns/blob/923e322130ff611ebd2bbd16320d96f2b466844b/contracts/cloning-vat/cloning-vat.solidity

Having deployed a `collapser` as shown above, one can use the
`cloning-vat` to make an exact copy of it:

* either by calling the `clone(address)` function, supplying the
  `collapser`'s address; or
* calling the `cloning-vat` with just the address (20 bytes) provided,
  as shown [in this transaction][tx4].

[tx4]: https://etherscan.io/tx/0xd495220ffbe8ff84807d08bba1da095f9fb87a49487597f5e1f5dbb6813b5a73

Just as `stamping-press` did, `cloning-vat` will emit an event, and return
the newly-cloned contract's address.

None of the above is particularly exciting (unless you enjoy whack-a-mole).
However, if you followed the examples, it serves to demonstrate deploying some
"standard contracts" without having to bother with compilation, connecting to
a node, submitting the bytecode...


## `cannery`

* Address: `0x25d62DA8E032c5cba01c351c7868f4b1a0E0949e`
* ENS: `cannery.veoxxoev.eth`
* Source code: [`cannery.lll`][cannery-src]
* ABI: [`cannery.lll.abi`][cannery-abi]
* Solidity interface: [`cannery.solidity`][cannery-sol]

[cannery-src]: https://gitlab.com/veox/lll-creation-patterns/blob/923e322130ff611ebd2bbd16320d96f2b466844b/contracts/cannery/cannery.lll
[cannery-abi]: https://gitlab.com/veox/lll-creation-patterns/blob/923e322130ff611ebd2bbd16320d96f2b466844b/contracts/cannery/cannery.lll.abi
[cannery-sol]: https://gitlab.com/veox/lll-creation-patterns/blob/923e322130ff611ebd2bbd16320d96f2b466844b/contracts/cannery/cannery.solidity

TODO


## A canned `collapser`

* Address: `0x1e77625c9818c25d4f4FA6b40D24Ef231D1740eF`
* ENS: `canned-collapser.veoxxoev.eth`
* Source code: N/A
* ABI: always REVERTs
* Solidity interface: N/A

The contract created by `cannery` above.


## `can-opener`

* Address: `0xC9d28DcA3CD8cCFDF583643837E3C637Bc59A789`
* ENS: `can-opener.veoxxoev.eth`
* Source code: [`can-opener.lll`][co-src]
* ABI: [`can-opener.lll.abi`][co-abi]
* Solidity interface: [`can-opener.solidity`][co-sol]

[co-src]: https://gitlab.com/veox/lll-creation-patterns/blob/923e322130ff611ebd2bbd16320d96f2b466844b/contracts/cannery/can-opener.lll
[co-abi]: https://gitlab.com/veox/lll-creation-patterns/blob/923e322130ff611ebd2bbd16320d96f2b466844b/contracts/cannery/can-opener.lll.abi
[co-sol]: https://gitlab.com/veox/lll-creation-patterns/blob/923e322130ff611ebd2bbd16320d96f2b466844b/contracts/cannery/can-opener.solidity

TODO