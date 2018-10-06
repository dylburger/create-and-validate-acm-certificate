import argparse
import time
from create_and_validate_acm_cert import DNSValidatedACMCertClient

WAIT_TIME = 10


def configure_argument_parser():
    """ Configures options for our argument parser,
        returns parsed arguments
    """
    default_profile = 'default'
    default_region = 'us-east-1'

    parser = argparse.ArgumentParser()

    # Help strings from ACM.Client Boto 3 docs
    parser.add_argument(
        '--profile',
        default=default_profile,
        help="The name tied to your boto profile (default: '%s')" %
        (default_profile),
    )

    parser.add_argument(
        '--region',
        default=default_region,
        help=
        "The region in which you want to create your certificate (default: '%s')"
        % (default_region),
    )

    parser.add_argument(
        '--domain',
        required=True,
        help=
        'The fully qualified domain name (FQDN) of the site you want to secure with an ACM Certificate',
    )

    parser.add_argument(
        '--subject_alternative_names',
        nargs='+',
        default=[],
        help=
        'Additional FQDNs to be included in the Subject Alternative Name extension of the ACM Certificate',
    )

    return parser.parse_args()


args = configure_argument_parser()

cert_client = DNSValidatedACMCertClient(args.domain, args.profile, args.region)
arn = cert_client.request_certificate(args.subject_alternative_names)
print("Certificate created. ARN: %s" % arn)

# We must wait a few seconds until the metadata we need to perform DNS validation is ready
print("Waiting for %s seconds for DNS validation records to be created..." %
      WAIT_TIME)
time.sleep(WAIT_TIME)

# Create the DNS validation records in Route 53
cert_client.create_domain_validation_records(arn)