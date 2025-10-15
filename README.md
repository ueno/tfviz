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
    Client->>Server: ClientHello
    Note left of Client: key_share<br/>supported_versions<br/>supported_groups<br/>signature_algorithms<br/>signature_algorithms_cert
    Server->>Client: HelloRetryRequest
    Note right of Server: key_share<br/>supported_versions
    Client->>Server: ClientHello
    Note left of Client: key_share<br/>supported_versions<br/>supported_groups<br/>signature_algorithms<br/>signature_algorithms_cert
    Server->>Client: ChangeCipherSpec
    Server->>Client: ServerHello
    Server->>Client: EncryptedExtensions
    Server->>Client: Certificate
    Server->>Client: CertificateVerify
    Server->>Client: Finished
    Client->>Server: Finished
    Client->>Server: ApplicationData
    loop
        Server->>Client: NewSessionTicket
    end
    Server->>Client: ApplicationData
    Client->>Server: Alert(warning, close_notify)
    Server->>Client: Alert
------------------------------------------------------------
OK
```

The rendered version is [here](https://mermaid.live/edit#pako:eNrVVMtu2zAQ_BWBpxZQ3FiSX0RhIHBS9NIc4qKHQoDBSCuJCEWyS6qJavjfQ4lyYMQRfC5P5OxwdnZJ7J5kKgdCiYE_DcgMbjkrkdWpDNzSDC3PuGbSBhvBQdpzfAv4F9Dj98pCoNxxYNNgo6SEzAZWBUJlTFTKWJokcewveNrVeu1V6AB8ByHUiaSAwgaqeFN9gnZnKobw9RG_rE2jtUIL-c5JGK6keQeXqBo9gLyUzDYIOyZKhdxW9XhglwEOFXt_zujRQm_xASy2D13njD2xi7yser_Hqi75_d-bsamYLGHDdQW41ZCN0DxwUs8Z405m2Gpn8-7FgjzpzXlK54YXPGMWLjN-AfKiHeF945KbCvKRR7gQvtFadDmc1VtmmWcJpbTffZjxHp63YLrqfvLsCYaugsxHHH6Y49yJcAV_emYouSzDIBPKwE4q14P285iw6N-UhKREnhNqsYGQ1IA1645k391Lia2ghpRQt82hYI2wKQl9yOnDjXDfxYe7v5mSVB6cpJsOv5Wqj6ru25UVoQUTxp0anbt3GYbNG4quB4Ab1UhL6DRa9CKE7skLoXEUTaJkPl_Es2W8WiZJSFpCr5JFNJnHsziZJbNlBx9C8q9PO53Ml9fTxXQ1X10vllHi1CDnVuEPP_H6wXd4Be9et6M).

## License

GPL2-or-later

---

*Co-authored by Claude*
