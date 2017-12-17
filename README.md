## Audience

You're using AWS, managing certificates through ACM, and DNS through Route53.

You want to create an ACM certificate using DNS validation, since you may not have email configured for the domain. And you want to automatically create the associated CNAME records for DNS validation in Route53. This mimics the "Create record in Route 53" button in the AWS Console (see [DNS validation reference](http://docs.aws.amazon.com/acm/latest/userguide/gs-acm-validate-dns.html)).

## Overview

Creates an ACM certificate for a given domain name, with optional subject alternative names, with DNS validation.

Immediately creates the associated CNAME records for DNS validation in Route53. Returns the ARN for the ACM certificate.

## Usage

    create-and-validate-acm-certificate.py \
        --hosted_zone_name <hosted zone domain> \
        --domain <domain> \
        --subject-alternative-names \
            <alternate name> \
            <another alternate name>
