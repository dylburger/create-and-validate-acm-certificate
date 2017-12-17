import argparse
import boto3
import time

WAIT_TIME = 10


def configure_argument_parser():
    """ Configures options for our argument parser,
        returns parsed arguments
    """
    default_profile = 'default'
    default_region = 'us-east-1'

    parser = argparse.ArgumentParser()

    # Help strings from ACM.CLient Boto 3 docs
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
        '--hosted_zone_name',
        required=True,
        help=
        "The domain name of the hosted zone in which you want to create the Route53 records",
    )

    parser.add_argument(
        '--domain',
        required=True,
        help=
        'The fully qualified domain name (FQDN) of the site you want to secure with an ACM Certificate',
    )

    parser.add_argument(
        '--subject_alternative_names',
        required=True,
        nargs='+',
        help=
        'Additional FQDNs to be included in the Subject Alternative Name extension of the ACM Certificate',
    )

    return parser.parse_args()


def response_succeeded(response):
    """ Given a Boto response,
        return True if the response was successful
    """
    return response.get('ResponseMetadata', {}).get('HTTPStatusCode') == 200


def get_certificate_arn(response):
    """ Given an ACM Boto response,
        return the ACM Certificate ARN
    """
    return response.get('CertificateArn')


def request_certificate(client, domain, subject_alternative_names):
    """ Given a domain name, subject alternative names and an ACM client object,
        request a certificate and return the certificate ARN
    """
    response = client.request_certificate(
        DomainName=domain,
        ValidationMethod='DNS',
        SubjectAlternativeNames=subject_alternative_names)

    if response_succeeded(response):
        return get_certificate_arn(response)


def get_resource_record_data(r):
    """ Given a ResourceRecord dictionary from an ACM certificate response,
        return the type, name and value of the record
    """
    return (r.get('Type'), r.get('Name'), r.get('Value'))


def get_hosted_zone_id_of_domain(client, domain):
    """ Given a domain,
        return the HostedZoneId of the zone
    """

    def domain_matches_hosted_zone(domain, zone):
        print("Does %s match %s" % (domain, zone))
        return "%s." % zone.get('Name') == domain

    response = client.list_hosted_zones()
    target_record = list(
        filter(lambda zone: domain_matches_hosted_zone(domain, zone),
               response.get('HostedZones')))
    print("Target record: %s" % target_record)

    return target_record[0].get('Id')


def create_dns_record(client, hosted_zone_id, record_type, record_name,
                      record_value):
    """ Given a record type, name and value,
        create a DNS record in Route 53 and return the response
    """
    print("Creating record for hosted zone %s, type %s, name %s, value %s" %
          (hosted_zone_id, record_type, record_name, record_value))
    client.change_resource_record_sets(HostedZoneId=hosted_zone_id)


def create_domain_validation_records(acm_client, route_53_client,
                                     hosted_zone_name, arn):
    """ Given an ACM certificate ARN,
        return the response
    """
    certificate_metadata = acm_client.describe_certificate(CertificateArn=arn)
    domain_validation_records = certificate_metadata.get('Certificate', {}).get(
        'DomainValidationOptions', [])

    print("Retrieving HostedZoneId for hosted zone name %s" % hosted_zone_name)
    hosted_zone_id = get_hosted_zone_id_of_domain(route_53_client,
                                                  hosted_zone_name)

    for record in domain_validation_records:
        record_type, record_name, record_value = get_resource_record_data(
            record.get('ResourceRecord'))
        create_record_response = create_dns_record(route_53_client,
                                                   hosted_zone_id, record_type,
                                                   record_name, record_value)
        print("Response for creating Route 53 record: %s" %
              (create_record_response))


args = configure_argument_parser()
print("Args: ", args)

session = boto3.Session(profile_name=args.profile)
acm_client = session.client('acm', region_name=args.region)
route_53_client = session.client('route53', region_name=args.region)

arn = request_certificate(acm_client, args.domain,
                          args.subject_alternative_names)
print("Certificate ARN: ", arn)

print("Waiting for %s seconds" % WAIT_TIME)
time.sleep(WAIT_TIME)

certificate_metadata = create_domain_validation_records(
    acm_client, route_53_client, args.hosted_zone_name, arn)
print("Metadata: ", certificate_metadata)
