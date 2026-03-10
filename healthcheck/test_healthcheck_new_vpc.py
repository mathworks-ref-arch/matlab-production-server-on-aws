# Health check Test for MATLAB Production Server Reference Architecture AWS on Linux where new VPC is created.
# Copyright 2022-2026 The MathWorks, Inc.
import refarch_testtools.deploy as deploy
import refarch_testtools.git_utils as git_utils
import sys
import requests
import datetime
import urllib.request
import random
from datetime import date


def main(keypairname, password, SSLCertificateARN, region, platform, git_token):
    # Reference architectures in production.
    ref_arch_name = 'matlab-production-server-on-aws'
    branch_name = git_utils.get_current_branch()
    
    ipAddress = requests.get("https://api.ipify.org").text + "/32"
    parameters = [{'ParameterKey': 'KeyPairName', 'ParameterValue': keypairname},
                  {'ParameterKey': 'SSLCertificateARN', 'ParameterValue': SSLCertificateARN},
                  {'ParameterKey': 'ClientIPAddress', 'ParameterValue': ipAddress},
                  {'ParameterKey': 'WorkerSystem', 'ParameterValue': platform},
                  {'ParameterKey': 'Username', 'ParameterValue': 'admin'},
                  {'ParameterKey': 'Password', 'ParameterValue': password},
                  {'ParameterKey': 'ConfirmPassword', 'ParameterValue': password}]
    
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
        github_base_dir = "https://raw.githubusercontent.com/mathworks-ref-arch"
        template_url_path = f"{github_base_dir}/{ref_arch_name}/{branch_name}/releases/{matlab_release}/templates/templateURL.txt"
        file = urllib.request.urlopen(template_url_path)
        template_url = file.readline().decode("utf-8").rstrip()
        stack_name = f"mps-refarch-health-check-{matlab_release}{date.today().strftime('%m-%d-%Y')}{random.randint(1, 101)}"
        ct = datetime.datetime.now()
        print(f"Date time before deployment of stack: {ct}")
        
        stack = None
        try:
            print("Deploying the stack")
            stack = deploy.deploy_stack(template_url, parameters, region, stack_name)
            print("Success deploying the stack")
        except Exception as e:
            print(f"Error deploying stack: {e}")
            raise e
        finally:
            if stack is not None:
                print("Deleting the stack")
                deploy.delete_stack(stack)
                print("Success deleting the stack\n")
                ct = datetime.datetime.now()
                print(f"Date time after deployment and deletion of stack: {ct}")


if __name__ == '__main__':
    if len(sys.argv) < 7:
        print("Error: Missing required arguments")
        print("Usage: python script.py <keypairname> <password> <SSLCertificateARN> <region> <platform> <git_token>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
