# Changelog
## [Unreleased]
### 🧪 Tests
- Add comprehensive test suite ([`66dd84b`](/commit/66dd84b95fa297197863cebe72c0bd605703e323), [#30](/pull/30))
## [v2.0.1] - 2025-07-19
### 🐛 Bug Fixes
- ECU handling with timezone ([`39b99aa`](/commit/39b99aa57473d751fc1211e2ecd486fc40739927), [#26](/pull/26))
### 🚀 CI/CD
- fix release ([`7ed7662`](/commit/7ed7662d6d4463068d3393ed1b39e7971cb586ad))
- fix not ignored step when no release ([`6582582`](/commit/6582582e4fb483d50b304405669a8171d1d11dd2))
- rework release workflow and split release and deploy ([`4996595`](/commit/499659539ef83f659c5ef106e7eab841e53cf772), [#29](/pull/29))
### 📝 Documentation
- update CHANGELOG ([`fac783f`](/commit/fac783fdbc45f79e0fecaa8af9c04aa2fd97700c))
### ♻️ Refactor
- migrate to pyproject.toml instead of setup.cfg ([`af776c9`](/commit/af776c9213367dc103515073e2a83f8932c1da9d), [#28](/pull/28))
- migrate project structure to src layout ([`a4e69a1`](/commit/a4e69a19e52e097b85c58e2c8b65bd0f564e6b6e), [#27](/pull/27))
### Other
## [v2.0.0] - 2025-07-17
### 🚀 CI/CD
- update commit parser to use conventional style and correct changelog file definition ([`facd0bb`](/commit/facd0bb42bc932dc25a58ebe0d48d273fa454cbd))
### 📝 Documentation
- update CHANGELOG ([`cd21dce`](/commit/cd21dce88e142c27a18b9f0fbea5469985534c95))
- update badges ([`97e2709`](/commit/97e270959073e3ba3b217544c023ac5ffcb21de4))
### ✨ Features
- add mqtt discovery support ([`5d6e52f`](/commit/5d6e52fb8c7f55346cef208b6d12a46a0e4c34ca), [#24](/pull/24))
### 🚨 Breaking Changes
- MQTT topics have been updated to comply with Home Assistant MQTT
## [v1.3.0] - 2025-07-15
### 🧹 Chores
- upgrade dependencies ([`6fbcf4a`](/commit/6fbcf4a6b6f7050352cc767152b9da6041a28669))
- bump requests from 2.32.0 to 2.32.4 ([`d98758d`](/commit/d98758d92a9d88f409bee3684f6494284ae74a32), [#21](/pull/21))
### 🚀 CI/CD
- build the docker image during run ([`8dc146f`](/commit/8dc146f7017ac30ced8c8adf9fb5fd05994b8ef9))
- update deprecated action ([`9d6f4a8`](/commit/9d6f4a8e1870c58208fb57a5791e1cb2080b515e))
### ✨ Features
- Add MQTT message retention and client status topic ([`2943c8d`](/commit/2943c8d9560bab2cd683cb31f5c3c4e422f0836e), [#22](/pull/22))
### Other
## [v1.2.0] - 2023-12-09
### 🧹 Chores
- improve exception trace ([`94120e8`](/commit/94120e8243623292ca1ac98717391d5da44b05a9), [#15](/pull/15))
### ✨ Features
- allow timezone customization ([`30a945f`](/commit/30a945f5883a4de78a3a3a3e8cc68f4d5fba0a9d), [#17](/pull/17))
## [v1.1.3] - 2023-12-03
### 🐛 Bug Fixes
- improve config boolean parsing ([`65aaee5`](/commit/65aaee56a3a66ce591a9c5b25326f1bdbdc7c137), [#14](/pull/14))
### 🧹 Chores
- add log when no ca_certs is defined ([`ca6b04b`](/commit/ca6b04b06fc1ec28b1ef49a740042cb6eac86f36), [#13](/pull/13))
- remove private data from log ([`07ac060`](/commit/07ac060252c4cafcbc32b1b8cdbb75d6a58fac8a))
### 🚀 CI/CD
- allow semantic to bypass protection ([`c886acb`](/commit/c886acb4c0249057821e93f74e7d62ca4dd65448), [#10](/pull/10))
### 📝 Documentation
- Add Docker compose example ([`f513a8a`](/commit/f513a8a15237de90be0a0f828e9406dce4b92ed2))
## [v1.1.2] - 2023-11-22
### 🚀 CI/CD
- fix release.yml ([`75705eb`](/commit/75705ebdaa9c8b567ce3cee77999e8a12ae0db84))
- deploy on docker ([`d2ffb7b`](/commit/d2ffb7b218fcc3f3e74c9212d25125c8bce4f554), [#8](/pull/8))
### ⚡ Performance Improvements
- replace numpy for lighter image ([`ea12ed8`](/commit/ea12ed8f3d381e72b6651a4282c9132c2df20187), [#9](/pull/9))
## [v1.1.1] - 2023-11-19
### 🐛 Bug Fixes
- cast import for non string values ([`5dc868b`](/commit/5dc868b6b9780d13f5b66d8fe67a60c502c90be1), [#7](/pull/7))
## [v1.1.0] - 2023-11-10
### 🧹 Chores
- clean code ([`f1ee302`](/commit/f1ee302ca8672313e28db371c2f8e58e37e984af), [#4](/pull/4))
### 🚀 CI/CD
- enable semantic release ([`8bd6b56`](/commit/8bd6b569bc542dd20b7bbb3d255f805b0e2101a5))
### 📝 Documentation
- update README ([`9947c03`](/commit/9947c037e9c35ca172a16e81eb6246bd5b730774))
### ✨ Features
- add TLS/SSL support for broker connection ([`9893dad`](/commit/9893dad8250a353eac3bf87d9c2cbe4b8518c94e), [#5](/pull/5))
- add TLS/SSL support for broker connection ([`9893dad`](/commit/9893dad8250a353eac3bf87d9c2cbe4b8518c94e), [#5](/pull/5))
## [v1.0.0] - 2023-11-01
### ✨ Features
- Release aps2mqtt ([`b9c4cc5`](/commit/b9c4cc5a47bc2d3a8475431f2a8b06027afdc191), [#1](/pull/1))
### Other
