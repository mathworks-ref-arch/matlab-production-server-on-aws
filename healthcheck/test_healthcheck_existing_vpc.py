# Health check Test for MATLAB Production Server Reference Architecture AWS on Linux where existing VPC is used for stack creation.
# Copyright 2022-26 The MathWorks, Inc.
import refarch_testtools.deploy as deploy
import refarch_testtools.git_utils as git_utils
import sys
import requests
import datetime
import urllib.request
import random
from datetime import date
import time


def main(keypairname, password, SSLCertificateARN, region, platform, git_token):
    # Reference architectures in production.
    ref_arch_name = 'matlab-production-server-on-aws'
    branch_name = git_utils.get_current_branch()
    
    ipAddress = requests.get("https://api.ipify.org").text + "/32"
    vpc_parameters = [{"ParameterKey": "AllowPublicIP",
                       "ParameterValue": "Yes"}]
    
    # Deploy a stack for creating VPC with 2 subnets
    existing_template_url = "https://matlab-production-server-templates.s3.amazonaws.com/mw-aws-payg-vpc-stack-cf.yml"
    existingstack = deploy.deploy_stack(existing_template_url, vpc_parameters, region, "existingvpc")
    time.sleep(90)
    
    vpc_id = deploy.get_stack_output_value(existingstack, 'VPCID')
    subnet1 = deploy.get_stack_output_value(existingstack, 'Subnet1')
    subnet2 = deploy.get_stack_output_value(existingstack, 'Subnet2')
    
    # With a GitHub token
    headers = {
        'Authorization': f'token {git_token}'
    }
    
    # Use GitHub API which has clearer rate limits
    api_url = f"https://api.github.com/repos/mathworks-ref-arch/{ref_arch_name}/contents/releases?ref={branch_name}"
    res = requests.get(api_url, headers=headers)
    
    if res.status_code != 200:
        print(f"Error fetching releases from GitHub API: {res.status_code}")
        print(f"Response: {res.text}")
        # Clean up VPC before raising exception
        deploy.delete_stack(existingstack)
        raise Exception(f"Failed to fetch releases from GitHub API")
    
    files = res.json()
    # Extract release names from file names and sort to get latest
    releases = sorted([f['name'] for f in files if f['name'].startswith('R')], reverse=True)
    
    if len(releases) < 2:
        print(f"Warning: Found only {len(releases)} release(s). Expected at least 2.")
    
    # Get the two latest releases
    latest_releases = releases[:2]
    
    for matlab_release in latest_releases:
        print(f"Testing Health Check Release: {matlab_release}\n")
        
        # Parameters for all releases
        parameters = [{'ParameterKey': 'KeyPairName', 'ParameterValue': keypairname},
                      {'ParameterKey': 'SSLCertificateARN', 'ParameterValue': SSLCertificateARN},
                      {'ParameterKey': 'ClientIPAddress', 'ParameterValue': ipAddress},
                      {'ParameterKey': 'WorkerSystem', 'ParameterValue': platform},
                      {'ParameterKey': 'Username', 'ParameterValue': 'admin'},
                      {'ParameterKey': 'Password', 'ParameterValue': password},
                      {'ParameterKey': 'ConfirmPassword', 'ParameterValue': password},
                      {'ParameterKey': 'ExistingVPC', 'ParameterValue': vpc_id},
                      {'ParameterKey': 'ExistingSubnet1', 'ParameterValue': subnet1},
                      {'ParameterKey': 'ExistingSubnet2', 'ParameterValue': subnet2}]
        
        github_base_dir = "https://raw.githubusercontent.com/mathworks-ref-arch"
        template_url_path = f"{github_base_dir}/{ref_arch_name}/{branch_name}/releases/{matlab_release}/templates/templateURL.txt"
        file = urllib.request.urlopen(template_url_path)
        template_url = file.read().decode("utf-8").rstrip()
        split_template_url = template_url.split("\n")
        existing_vpc_template_url = split_template_url[1]
        
        stack_name = f"mps-refarch-health-check-{matlab_release}{date.today().strftime('%m-%d-%Y')}{random.randint(1, 101)}"
        ct = datetime.datetime.now()
        print(f"Date time before deployment of stack: {ct}")
        
        stack = None
        try:
            print("Deploying the stack")
            stack = deploy.deploy_stack(existing_vpc_template_url, parameters, region, stack_name)
            print("Success deploying the stack")
            ct = datetime.datetime.now()
            print(f"Date time after deployment of stack: {ct}")
        except Exception as e:
            print(f"Error deploying stack: {e}")
            raise e
        finally:
            if stack is not None:
                print(f"Deleting the stack: {matlab_release}")
                deploy.delete_stack(stack)
                print("Success deleting the stack\n")
    
    print("Deleting the existing VPC stack")
    # Delete the existing VPC
    deploy.delete_stack(existingstack)
    print("Success deleting the existing VPC stack")
    ct = datetime.datetime.now()
    print(f"Date time after deletion of stacks: {ct}")


if __name__ == "__main__":
    if len(sys.argv) < 7:
        print("Error: Missing required arguments")
        print("Usage: python script.py <keypairname> <password> <SSLCertificateARN> <region> <platform> <git_token>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
