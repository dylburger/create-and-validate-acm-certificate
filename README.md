## Audience

You're using AWS, managing certificates through ACM, and DNS through Route53.

You want to create an ACM certificate using DNS validation, since you may not have email configured for the domain. And you want to automatically create the associated CNAME records for DNS validation in Route53. This mimics the "Create record in Route 53" button in the AWS Console (see [DNS validation reference](http://docs.aws.amazon.com/acm/latest/userguide/gs-acm-validate-dns.html)).

NOTE: this script was created for a single use case and may not function as intended for more general use. However, please feel free to modify it or submit PRs.

## Overview

Creates an ACM certificate for a given domain name, with optional subject alternative names, with DNS validation.

Immediately creates the associated CNAME records for DNS validation in Route53.

By default, this creates ACM certificates in `us-east-1`, so that the certificates can be used by Cloudfront. You can pass in a custom region (see Usage section below).

## Usage

    python request-certificate.py \
        --domain <domain> \
        --subject-alternative-names \
            <alternate name> \
            <another alternate name>

You can also pass a custom AWS profile name, or region:

    python request-certificate.py \
        --profile personal \
        --region us-east-1 \
        --domain <domain> \
        --subject-alternative-names \
            <alternate name> \
            <another alternate name>
