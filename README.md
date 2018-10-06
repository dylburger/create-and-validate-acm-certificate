## Audience

You're using AWS, managing certificates through ACM, and DNS through Route53.

You want to create an ACM certificate using DNS validation, since you may not have email configured for the domain. And you want to automatically create the associated CNAME records for DNS validation in Route53. This mimics the "Create record in Route 53" button in the AWS Console (see [DNS validation reference](http://docs.aws.amazon.com/acm/latest/userguide/gs-acm-validate-dns.html)).

NOTE: this script was created for a single use case and may not function as intended for more general use. However, please feel free to modify it or submit PRs.

## Overview

Creates an ACM certificate for a given domain name, with optional subject alternative names, using DNS validation.

Immediately creates the associated CNAME records for DNS validation in Route53. The script assumes that a Route 53 hosted zone tied to the domain exists (e.g. if you're creating a new certificate for www.test.com, the script will create validation records in the test.com hosted zone).

It will take a few minutes after you run the script for the certificate to be fully validated and issued.

By default, this creates ACM certificates in `us-east-1`, so that the certificates can be used by Cloudfront. You can pass in a custom region (see Usage section below).

## Usage

### Python Module

If you want to install as a python package, run:

`pip install git+https://github.com/dylburger/create-and-validate-acm-certificate`

Then, in your script:

```python
from create_and_validate_acm_cert import DNSValidatedACMCertClient

cert_client = DNSValidatedACMCertClient(domain='www.domain.com') # defaults to using the 'default` aws profile on your machine and the 'us-east-1' aws region.
arn = cert_client.request_certificate()
# Create DNS validation records
cert_client.create_domain_validation_records(arn)
# Wait for certificate to get to validation state before continuing
cert_client.wait_for_certificate_validation(certificate_arn=arn, sleep_time=5, timeout=600)
```

### Command Line

First, you'll need to install the dependencies in `requirements.txt`:

    pip install -r requirements.txt

Then, run the `request-certificate.py` script:

    python request-certificate.py \
        --domain <domain> \
        --subject_alternative_names \
            <alternate name> \
            <another alternate name>

You can also pass a custom AWS profile name, or region:

    python request-certificate.py \
        --profile personal \
        --region us-east-1 \
        --domain <domain> \
        --subject_alternative_names \
            <alternate name> \
            <another alternate name>

## Credits

I'm very grateful to the contributors of these libraries:

* [`tldextract`](https://github.com/john-kurkowski/tldextract) helps parse the TLD and domain portions of hosts.
* [`boto3`](https://github.com/boto/boto3) makes working with the AWS API easy.
