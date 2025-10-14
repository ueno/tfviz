# tfviz

tfviz is a script to visualize tlsfuzzer test scripts as a sequence
diagram in the [Mermaid](https://mermaid.js.org/) format.

## Usage

```console
$ git clone --depth=1 https://github.com/tlsfuzzer/tlsfuzzer.git
$ git clone --depth=1 https://github.com/tlsfuzzer/tlslite-ng.git
$ PYTHONPATH=.:tlsfuzzer:tlslite-ng python visualize.py <tlsfuzzer-script-path> <probe-name>
```

## Example

```console
$ python visualize.py tlsfuzzer/scripts/test-tls13-obsolete-curves.py "sanity - HRR support"
sanity - HRR support ...
------------------------------------------------------------
sequenceDiagram
    participant Client
    participant Server
    Note over Client: Connect to localhost:4433
    Client->>Server: ClientHello [key_share, supported_versions, supported_groups, signature_algorithms, signature_algorithms_cert]
    Server->>Client: HelloRetryRequest [key_share, supported_versions]
    Client->>Server: ClientHello [key_share, supported_versions, supported_groups, signature_algorithms, signature_algorithms_cert]
    Server->>Client: ChangeCipherSpec
    Server->>Client: ServerHello
    Server->>Client: EncryptedExtensions
    Server->>Client: Certificate
    Server->>Client: CertificateVerify
    Server->>Client: Finished
    Client->>Server: Finished
    Client->>Server: ApplicationData
    Server->>Client: NewSessionTicket
------------------------------------------------------------
OK
```

The rendered version is [here](https://mermaid.live/edit#pako:eNrNU8FunDAQ_RU0Z7qC4s2CD5EikqqnHLJVDy3RyjKzYAVs1x7a0NX-ew1sqkoV2mt88jy_mfdmbJ9AmhqBg8cfA2qJ90o0TvSVjsKywpGSygpNUdkp1PQ_vkf3E92CPxrCyITwwuZRabRGSRGZqDNSdK3xxBnLsiVhoX24vV2q8AvwGbvORN9fcDz4VjiMIz9YaxxhfQg0r4z2_2KNM4OdENVoQYPDg-ga4xS1_Qp6kOjoeTGxaAcTb6Zn-SckNz5NU_F0xcrze26mbIVusFS2Rbe3KFdoCzB7XWE8aOlGGxw-vBLq2faaZLCjjkoKwuuMr-jUcVzhfVJa-RbrlQFfOb6ztps0gtV7QWJF4xF_7dFP_XxR8gXDE4cYGqdq4OQGjKFH14sphNNUogJqsccKeNjWeBRDRxVU-hzSwo_4Zkz_lhlusmmBH0XnQzTYOvR7-WB_UYe6RleaQRPwdDfXAH6CV-Afi5tNmmV5WmzzJNnlaQwjcJZsWLbbpiljLCnS_BzD71kz2eQ7VkwruSm2LE2K8x-hhle-).

## License

GPL2-or-later

---

*Co-authored by Claude*
