# CVE-2026-30081 — Security Advisory

![CVE](https://img.shields.io/badge/CVE-2026--30081-red) ![CWE](https://img.shields.io/badge/CWE--319-Cleartext%20Transmission-orange) ![Severity](https://img.shields.io/badge/Severity-HIGH-critical)

> CVE-2026-30081 has been officially published by MITRE.

---

## Vulnerability Overview

| Field            | Value                                                       |
| :--------------- | :---------------------------------------------------------- |
| **CVE ID**       | CVE-2026-30081                                              |
| **CWE**          | CWE-319: Cleartext Transmission of Sensitive Information    |
| **Device Model** | QN-I-470                                                    |
| **Firmware**     | 6.1.1.B1                                                    |
| **Severity**     | HIGH                                                        |
| **Vendor**       | Quantum Networks                                            |

---

##  Vulnerability Description

The administrative web interface of the affected Quantum Networks router (QN-I-470, firmware 6.1.1.B1) transmits authentication credentials in cleartext over the network.

When an administrator authenticates to the web-based management interface over HTTP, the supplied username and password are sent without any transport-layer encryption. As a result, an adjacent network attacker with access to the same broadcast domain can passively intercept network traffic and recover valid administrative credentials.

Successful credential disclosure enables complete compromise of the affected device.

---

##  Impact

An attacker capable of intercepting network traffic on the same local network can:

- Obtain valid administrative credentials
- Gain full administrative control over the affected router
- Modify critical network configuration, including routing, DNS, and firewall settings
- Perform traffic interception, redirection, or manipulation
- Establish persistent or stealthy access to the network infrastructure

> Given that the affected device functions as a network gateway, successful exploitation may enable network-wide attacks against connected systems, significantly increasing the overall impact.


---

##  References

1. [OWASP Top 10 — A02:2021 Cryptographic Failures](https://owasp.org/Top10/A02_2021-Cryptographic_Failures/)
2. [CWE-319: Cleartext Transmission of Sensitive Information](https://cwe.mitre.org/data/definitions/319.html)

---
