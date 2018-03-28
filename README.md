# lll-creation-patterns

Various ways to implement Ethereum contract copying, at different degrees
of homogeneity, using LLL.

For a high-level description, see [`contracts/README`][readme]. For
something more hands-on, see [`contracts/USING`][using].

[readme]: contracts/README.md
[using]: contracts/USING.md

See [`lll-contracts`](https://gitlab.com/veox/lll-contracts), for some
more simple examples.

[Populus](https://github.com/ethereum/populus/) is used for development.
Although `requirements.txt` specifies `populus==2.1.0`, the actual version
required is the one in [my `populus/lll-to-merge`
branch](https://github.com/veox/populus/tree/lll-to-merge), at least until
[`ethereum/populus` PR 408](https://github.com/ethereum/populus/pull/408)
is merged.

## License

Blanket-covered by GPLv3 (see [`LICENSE.txt`](LICENSE.txt)).
