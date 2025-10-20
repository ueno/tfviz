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
$ python visualize.py -o out.mermaid tlsfuzzer/scripts/test-tls13-obsolete-curves.py "sanity - HRR support"
```

```mermaid
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
    alt
        Server-->>Client: Connection closed
    end
```

## License

GPL2-or-later

---

*Co-authored by Claude*
