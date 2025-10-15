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
------------------------------------------------------------
OK
```

The rendered version is [here](https://mermaid.live/edit#pako:eNrVU01v2zAM_SuGzlnm-GOOhSLA4HbYqYdm2GEwEGgybQuVJU2it3pB_vvk2CmCZkHO1Ul8fOR7pKA94boCQomDXz0oDveCNZZ1pQr8Mcyi4MIwhUEhBSi8xLdgf4Od8EeNEGgfzmwaFFop4BigDqTmTLbaIU2SOJ4KJtqHzWbqQmfgK0ipz1pKqDHQ9WvXZxh2rmUW7n7ajxvXG6MtQrXzLZzQyr2BG6t7M4OiUQx7CzsmG20Ftt31xI6DnSee_HmjJwtHi0-AdngaN-fwzK4VTXv0e5rqlt_3voyiZaqBQpgW7NYAv0KbgLN5LhgPitvBeJsPLwjqbDeXkt6NqAVnCLcZ38GKerjC-yKUcC1UVx7hRvqzMXLU8FbvGbKJJbU20-2_io_wZwtunO6b4M8wbxWU1yAL0lhREYq2hwXpwHZsDMl-JJUEW-igJNRfK6hZL7EkpTr4Mv8Zf2jdnSr9KzctoTWTzke9qfwa5r_9SvGKYAvdKyQ0PXYgdE9eCI3DaJmmYRSv8jhO8zjz2YHQKF6u12GSZXmYRlmcxOvDgvw9iq6WYZKv1skqD8N1loSfosM_IhN_7Q).

## License

GPL2-or-later

---

*Co-authored by Claude*
