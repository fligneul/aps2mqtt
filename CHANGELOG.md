# CHANGELOG

## v2.0.0 (2025-07-17)

### Continuous Integration

- Update commit parser to use conventional style and correct changelog file definition ([`facd0bb`](https://github.com/fligneul/aps2mqtt/commit/facd0bb42bc932dc25a58ebe0d48d273fa454cbd))

### Documentation

- Update badges ([`97e2709`](https://github.com/fligneul/aps2mqtt/commit/97e270959073e3ba3b217544c023ac5ffcb21de4))

- Update CHANGELOG ([`cd21dce`](https://github.com/fligneul/aps2mqtt/commit/cd21dce88e142c27a18b9f0fbea5469985534c95))

### Features

- Add mqtt discovery support ([#24](https://github.com/fligneul/aps2mqtt/pull/24), [`5d6e52f`](https://github.com/fligneul/aps2mqtt/commit/5d6e52fb8c7f55346cef208b6d12a46a0e4c34ca))

### Breaking Changes

- MQTT topics have been updated to comply with Home Assistant MQTT

## v1.3.0 (2025-07-15)

### Chores

- **deps**: Bump requests from 2.32.0 to 2.32.4 (#21) ([#21](https://github.com/fligneul/aps2mqtt/pull/21), [`d98758d`](https://github.com/fligneul/aps2mqtt/commit/d98758d92a9d88f409bee3684f6494284ae74a32))

- **deps**: Upgrade dependencies ([`6fbcf4a`](https://github.com/fligneul/aps2mqtt/commit/6fbcf4a6b6f7050352cc767152b9da6041a28669))

### Continuous Integration

- Build the docker image during run ([`8dc146f`](https://github.com/fligneul/aps2mqtt/commit/8dc146f7017ac30ced8c8adf9fb5fd05994b8ef9))

- Update deprecated action ([`9d6f4a8`](https://github.com/fligneul/aps2mqtt/commit/9d6f4a8e1870c58208fb57a5791e1cb2080b515e))

### Features

- Add MQTT message retention and client status topic (#22) ([#22](https://github.com/fligneul/aps2mqtt/pull/22), [`2943c8d`](https://github.com/fligneul/aps2mqtt/commit/2943c8d9560bab2cd683cb31f5c3c4e422f0836e))


## v1.2.0 (2023-12-09)

### Chore

* chore: improve exception trace (#15) ([`94120e8`](https://github.com/fligneul/aps2mqtt/commit/94120e8243623292ca1ac98717391d5da44b05a9))

### Feature

* feat: allow timezone customization (#17) ([`30a945f`](https://github.com/fligneul/aps2mqtt/commit/30a945f5883a4de78a3a3a3e8cc68f4d5fba0a9d))


## v1.1.3 (2023-12-03)

### Chore

* chore: add log when no ca_certs is defined (#13) ([`ca6b04b`](https://github.com/fligneul/aps2mqtt/commit/ca6b04b06fc1ec28b1ef49a740042cb6eac86f36))

* chore(log): remove private data from log ([`07ac060`](https://github.com/fligneul/aps2mqtt/commit/07ac060252c4cafcbc32b1b8cdbb75d6a58fac8a))

### Ci

* ci(release): allow semantic to bypass protection (#10) ([`c886acb`](https://github.com/fligneul/aps2mqtt/commit/c886acb4c0249057821e93f74e7d62ca4dd65448))

### Documentation

* docs: Add Docker compose example ([`f513a8a`](https://github.com/fligneul/aps2mqtt/commit/f513a8a15237de90be0a0f828e9406dce4b92ed2))

### Fix

* fix: improve config boolean parsing (#14) ([`65aaee5`](https://github.com/fligneul/aps2mqtt/commit/65aaee56a3a66ce591a9c5b25326f1bdbdc7c137))

### Unknown

* [release] 1.1.3

Automatically generated by python-semantic-release ([`d84de5a`](https://github.com/fligneul/aps2mqtt/commit/d84de5af36fc34aa3b3643eb449aa0358c23bcb4))


## v1.1.2 (2023-11-22)

### Ci

* ci: fix release.yml ([`75705eb`](https://github.com/fligneul/aps2mqtt/commit/75705ebdaa9c8b567ce3cee77999e8a12ae0db84))

* ci: deploy on docker (#8) ([`d2ffb7b`](https://github.com/fligneul/aps2mqtt/commit/d2ffb7b218fcc3f3e74c9212d25125c8bce4f554))

### Performance

* perf: replace numpy for lighter image (#9) ([`ea12ed8`](https://github.com/fligneul/aps2mqtt/commit/ea12ed8f3d381e72b6651a4282c9132c2df20187))

### Unknown

* [release] 1.1.2

Automatically generated by python-semantic-release ([`21a539b`](https://github.com/fligneul/aps2mqtt/commit/21a539b0d84f1574b77429b7c02ee552d547f78d))


## v1.1.1 (2023-11-19)

### Fix

* fix: cast import for non string values (#7) ([`5dc868b`](https://github.com/fligneul/aps2mqtt/commit/5dc868b6b9780d13f5b66d8fe67a60c502c90be1))

### Unknown

* [release] 1.1.1

Automatically generated by python-semantic-release ([`c2e2fc3`](https://github.com/fligneul/aps2mqtt/commit/c2e2fc3507ba8bfda179c77eb254d668a8f67d3f))


## v1.1.0 (2023-11-10)

### Chore

* chore: clean code (#4) ([`f1ee302`](https://github.com/fligneul/aps2mqtt/commit/f1ee302ca8672313e28db371c2f8e58e37e984af))

### Ci

* ci: enable semantic release ([`8bd6b56`](https://github.com/fligneul/aps2mqtt/commit/8bd6b569bc542dd20b7bbb3d255f805b0e2101a5))

### Documentation

* docs: update README ([`9947c03`](https://github.com/fligneul/aps2mqtt/commit/9947c037e9c35ca172a16e81eb6246bd5b730774))

### Feature

* feat: add TLS/SSL support for broker connection (#5)

* feat: add TLS/SSL support for broker connection

* doc: Update README for broker secured connection ([`9893dad`](https://github.com/fligneul/aps2mqtt/commit/9893dad8250a353eac3bf87d9c2cbe4b8518c94e))

### Unknown

* [release] 1.1.0

Automatically generated by python-semantic-release ([`709be16`](https://github.com/fligneul/aps2mqtt/commit/709be16aecfde1e6546a18610bcc6bcc1a448450))


## v1.0.0 (2023-11-01)

### Feature

* feat: Release aps2mqtt (#1)

Publish APS ECU data to MQTT broker
Doc up to date
Python whl &amp; PyPI release ([`b9c4cc5`](https://github.com/fligneul/aps2mqtt/commit/b9c4cc5a47bc2d3a8475431f2a8b06027afdc191))

### Unknown

* [release] 1.0.0

Automatically generated by python-semantic-release ([`28c816f`](https://github.com/fligneul/aps2mqtt/commit/28c816fce9c6ce6000a62233f0754c6189821308))

* Initial commit ([`12e516f`](https://github.com/fligneul/aps2mqtt/commit/12e516f9cb0abf424fa12673ecbb473d5199413c))
