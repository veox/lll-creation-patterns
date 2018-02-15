# Approaches to the Factory pattern for Ethereum contracts

## Stamping press

The straightforward Factory. Used in Solidity programs with the `new`
keyword.

A contract's runtime bytecode contains the deployment bytecode (and, by
extension, runtime) of a yet another contract.

On receiving input, the "outer layer" contract can create (optionally
parametrised) copies of this nested contract.

If the copies are to be non-identical, then the "outer layer" must know
their interface: that is, it must contain code that is not strictly
required for its own operation, but is dependent on the implementation
of the nested contract.

**Upside:** simple to implement and understand.

**Downside:** for whatever kind of contract that one would
like to be deploying, they'll need to have a separate `stamping-press`.
If a change needs to be made to the nested contract template, then a
new `stamping-press` will have to be deployed.

**Philosophical dead-end:**

> Recursion is the mother of recursion.

If, instead of making objects (`o`), one needs to make factories that
can make objects (`Fo`), then they can nest their desired factory in a
yet another "outer layer" factory (`FFo`), and be done with it.

However, on the next step attempting to do the same, it becomes
apparent that the third-layer indirection `FFFo` has the same interface
(`F(F..)`) as the second-layer indirection `FFo` (`F(F.)`), only with a
bigger nested payload.

In other words, `FFFo` handles its payload in the same way as `FFo` -
they have the same basic function - yet, for some reason, they are not
the same contract!

## Cloning vat

The honeybadger Factory.

Takes an account address as input and creates a copy of that account's
runtime bytecode as a new contract.

**Upside:** extremely simple to implement and understand.

**More upsides:**

No runtime? _Don't care._ Runtime makes no sense without the init code?
_Don't care._ Even if that makes it insecure? _Don't care._ Runtime
makes no sense without the storage it was handling? _Don't care._

**Downside:** needs additional steps if created contract needs
customisation (such as access controls), which likely requires
an additional contract that can perform creation (by use of the
`cloning-vat`) immediately followed by initialisation, in the same
externally-originating call.

By extension, this requires initialisation code to be present in the
target, even if it will only be used once, and then disabled.

**More downsides:**

See "more upsides" above. _Don't care._

**Philosophically re-invigorating:**

A `cloning-vat` handles just fine being given its own address as the
target, and creating a perfect copy of itself. It can also be given
a `stamping-press` as input, or any other factory for that matter.

## Cannery (and can opener)



## Assembly line (a.k.a. sequencer)

TODO

* keeps code blocks as data in storage
* receives blueprint/sequence
* creates external contracts out of code blocks, concatenating them
  according to the blueprint/sequence

`+` may be useful for one-shot "transactional" contracts

## Garden

TODO

* (optionally?) `STATICCALL`s into a
* `DELEGATECALL` into an external contract that
* runs its code to deploy a yet another external contract

`+` pass entire storage as "call data"
`-` storage operations are expensive
