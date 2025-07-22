# CHANGELOG
## v2.0.2 (2025-07-22)
### 🐛 Bug Fixes
- Release process ([`ebe97dd`](https://github.com/fligneul/aps2mqtt/commit/ebe97dd1fbd98f8e464065475c92daa715973783), [#32](https://github.com/fligneul/aps2mqtt/pull/32))
### 🧪 Tests
- Add comprehensive test suite ([`66dd84b`](https://github.com/fligneul/aps2mqtt/commit/66dd84b95fa297197863cebe72c0bd605703e323), [#30](https://github.com/fligneul/aps2mqtt/pull/30))
## v2.0.1 (2025-07-19)
### 🐛 Bug Fixes
- ECU handling with timezone ([`39b99aa`](https://github.com/fligneul/aps2mqtt/commit/39b99aa57473d751fc1211e2ecd486fc40739927), [#26](https://github.com/fligneul/aps2mqtt/pull/26))
### 🚀 CI/CD
- Fix release ([`7ed7662`](https://github.com/fligneul/aps2mqtt/commit/7ed7662d6d4463068d3393ed1b39e7971cb586ad))
- Fix not ignored step when no release ([`6582582`](https://github.com/fligneul/aps2mqtt/commit/6582582e4fb483d50b304405669a8171d1d11dd2))
- Rework release workflow and split release and deploy ([`4996595`](https://github.com/fligneul/aps2mqtt/commit/499659539ef83f659c5ef106e7eab841e53cf772), [#29](https://github.com/fligneul/aps2mqtt/pull/29))
### 📝 Documentation
- Update CHANGELOG ([`fac783f`](https://github.com/fligneul/aps2mqtt/commit/fac783fdbc45f79e0fecaa8af9c04aa2fd97700c))
### ♻️ Refactor
- Migrate to pyproject.toml instead of setup.cfg ([`af776c9`](https://github.com/fligneul/aps2mqtt/commit/af776c9213367dc103515073e2a83f8932c1da9d), [#28](https://github.com/fligneul/aps2mqtt/pull/28))
- Migrate project structure to src layout ([`a4e69a1`](https://github.com/fligneul/aps2mqtt/commit/a4e69a19e52e097b85c58e2c8b65bd0f564e6b6e), [#27](https://github.com/fligneul/aps2mqtt/pull/27))
## v2.0.0 (2025-07-17)
### 🚀 CI/CD
- Update commit parser to use conventional style and correct changelog file definition ([`facd0bb`](https://github.com/fligneul/aps2mqtt/commit/facd0bb42bc932dc25a58ebe0d48d273fa454cbd))
### 📝 Documentation
- Update CHANGELOG ([`cd21dce`](https://github.com/fligneul/aps2mqtt/commit/cd21dce88e142c27a18b9f0fbea5469985534c95))
- Update badges ([`97e2709`](https://github.com/fligneul/aps2mqtt/commit/97e270959073e3ba3b217544c023ac5ffcb21de4))
### ✨ Features
- Add mqtt discovery support ([`5d6e52f`](https://github.com/fligneul/aps2mqtt/commit/5d6e52fb8c7f55346cef208b6d12a46a0e4c34ca), [#24](https://github.com/fligneul/aps2mqtt/pull/24))
### 🚨 Breaking Changes
- MQTT topics have been updated to comply with Home Assistant MQTT
## v1.3.0 (2025-07-15)
### 🧹 Chores
- Upgrade dependencies ([`6fbcf4a`](https://github.com/fligneul/aps2mqtt/commit/6fbcf4a6b6f7050352cc767152b9da6041a28669))
- Bump requests from 2.32.0 to 2.32.4 ([`d98758d`](https://github.com/fligneul/aps2mqtt/commit/d98758d92a9d88f409bee3684f6494284ae74a32), [#21](https://github.com/fligneul/aps2mqtt/pull/21))
### 🚀 CI/CD
- Build the docker image during run ([`8dc146f`](https://github.com/fligneul/aps2mqtt/commit/8dc146f7017ac30ced8c8adf9fb5fd05994b8ef9))
- Update deprecated action ([`9d6f4a8`](https://github.com/fligneul/aps2mqtt/commit/9d6f4a8e1870c58208fb57a5791e1cb2080b515e))
### ✨ Features
- Add MQTT message retention and client status topic ([`2943c8d`](https://github.com/fligneul/aps2mqtt/commit/2943c8d9560bab2cd683cb31f5c3c4e422f0836e), [#22](https://github.com/fligneul/aps2mqtt/pull/22))
## v1.2.0 (2023-12-09)
### 🧹 Chores
- Improve exception trace ([`94120e8`](https://github.com/fligneul/aps2mqtt/commit/94120e8243623292ca1ac98717391d5da44b05a9), [#15](https://github.com/fligneul/aps2mqtt/pull/15))
### ✨ Features
- Allow timezone customization ([`30a945f`](https://github.com/fligneul/aps2mqtt/commit/30a945f5883a4de78a3a3a3e8cc68f4d5fba0a9d), [#17](https://github.com/fligneul/aps2mqtt/pull/17))
## v1.1.3 (2023-12-03)
### 🐛 Bug Fixes
- Improve config boolean parsing ([`65aaee5`](https://github.com/fligneul/aps2mqtt/commit/65aaee56a3a66ce591a9c5b25326f1bdbdc7c137), [#14](https://github.com/fligneul/aps2mqtt/pull/14))
### 🧹 Chores
- Add log when no ca_certs is defined ([`ca6b04b`](https://github.com/fligneul/aps2mqtt/commit/ca6b04b06fc1ec28b1ef49a740042cb6eac86f36), [#13](https://github.com/fligneul/aps2mqtt/pull/13))
- Remove private data from log ([`07ac060`](https://github.com/fligneul/aps2mqtt/commit/07ac060252c4cafcbc32b1b8cdbb75d6a58fac8a))
### 🚀 CI/CD
- Allow semantic to bypass protection ([`c886acb`](https://github.com/fligneul/aps2mqtt/commit/c886acb4c0249057821e93f74e7d62ca4dd65448), [#10](https://github.com/fligneul/aps2mqtt/pull/10))
### 📝 Documentation
- Add Docker compose example ([`f513a8a`](https://github.com/fligneul/aps2mqtt/commit/f513a8a15237de90be0a0f828e9406dce4b92ed2))
## v1.1.2 (2023-11-22)
### 🚀 CI/CD
- Fix release.yml ([`75705eb`](https://github.com/fligneul/aps2mqtt/commit/75705ebdaa9c8b567ce3cee77999e8a12ae0db84))
- Deploy on docker ([`d2ffb7b`](https://github.com/fligneul/aps2mqtt/commit/d2ffb7b218fcc3f3e74c9212d25125c8bce4f554), [#8](https://github.com/fligneul/aps2mqtt/pull/8))
### ⚡ Performance Improvements
- Replace numpy for lighter image ([`ea12ed8`](https://github.com/fligneul/aps2mqtt/commit/ea12ed8f3d381e72b6651a4282c9132c2df20187), [#9](https://github.com/fligneul/aps2mqtt/pull/9))
## v1.1.1 (2023-11-19)
### 🐛 Bug Fixes
- Cast import for non string values ([`5dc868b`](https://github.com/fligneul/aps2mqtt/commit/5dc868b6b9780d13f5b66d8fe67a60c502c90be1), [#7](https://github.com/fligneul/aps2mqtt/pull/7))
## v1.1.0 (2023-11-10)
### 🧹 Chores
- Clean code ([`f1ee302`](https://github.com/fligneul/aps2mqtt/commit/f1ee302ca8672313e28db371c2f8e58e37e984af), [#4](https://github.com/fligneul/aps2mqtt/pull/4))
### 🚀 CI/CD
- Enable semantic release ([`8bd6b56`](https://github.com/fligneul/aps2mqtt/commit/8bd6b569bc542dd20b7bbb3d255f805b0e2101a5))
### 📝 Documentation
- Update README ([`9947c03`](https://github.com/fligneul/aps2mqtt/commit/9947c037e9c35ca172a16e81eb6246bd5b730774))
### ✨ Features
- Add TLS/SSL support for broker connection ([`9893dad`](https://github.com/fligneul/aps2mqtt/commit/9893dad8250a353eac3bf87d9c2cbe4b8518c94e), [#5](https://github.com/fligneul/aps2mqtt/pull/5))
- Add TLS/SSL support for broker connection ([`9893dad`](https://github.com/fligneul/aps2mqtt/commit/9893dad8250a353eac3bf87d9c2cbe4b8518c94e), [#5](https://github.com/fligneul/aps2mqtt/pull/5))
## v1.0.0 (2023-11-01)
### ✨ Features
- Release aps2mqtt ([`b9c4cc5`](https://github.com/fligneul/aps2mqtt/commit/b9c4cc5a47bc2d3a8475431f2a8b06027afdc191), [#1](https://github.com/fligneul/aps2mqtt/pull/1))
