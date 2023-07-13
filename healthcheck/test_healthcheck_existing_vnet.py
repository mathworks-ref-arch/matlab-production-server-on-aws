# Health check Test for MATLAB Production Server Reference Architecture AWS on Linux where existing VPC is used for stack creation.
# Copyright 2022 The MathWorks, Inc.

import refarch_testtools.deploy as deploy
import sys
import re
import requests
import datetime
import urllib
import random
from datetime import date
import time

def main(keypairname, password, ipAddress, SSLCertificateARN, region, platform):

        # Reference architectures in production.
        ref_arch_name = 'matlab-production-server-on-aws'

        vpc_parameters  = [{"ParameterKey": "AllowPublicIP",
                            "ParameterValue": "Yes"}]

        # Deploy a stack for creating VPC with 2 subnets
        existing_template_url = "https://matlab-production-server-templates.s3.amazonaws.com/mw-aws-payg-vpc-stack-cf.yml"
        existingstack = deploy.deploy_stack(existing_template_url, vpc_parameters, region, "existingvpc")
        time.sleep(90)
        vpc_id = deploy.get_stack_output_value(existingstack, 'VPCID')
        vpc_cidr = deploy.get_stack_output_value(existingstack, 'VPCCIDR')
        subnet1 = deploy.get_stack_output_value(existingstack, 'Subnet1')
        subnet2 = deploy.get_stack_output_value(existingstack, 'Subnet2')
        vpc_parameters = {'ExistingVPC' : vpc_id, 'ExistingVPCAddress' : vpc_cidr,
        'ExistingSubnet1': subnet1, 'ExistingSubnet2': subnet2}

        parameters = [{'ParameterKey': 'KeyPairName', 'ParameterValue': keypairname},
                  {'ParameterKey': 'SSLCertificateARN', 'ParameterValue': SSLCertificateARN},
                  {'ParameterKey': 'ClientIPAddress', 'ParameterValue': ipAddress},
                  {'ParameterKey': 'WorkerSystem', 'ParameterValue': platform},
                  {'ParameterKey': 'Username', 'ParameterValue': 'admin'},
                  {'ParameterKey': 'Password', 'ParameterValue': password},
                  {'ParameterKey': 'ConfirmPassword', 'ParameterValue': password},
                  {"ParameterKey": "ExistingVPC","ParameterValue": vpc_id},
                  {"ParameterKey": "ExistingVPCAddress","ParameterValue": vpc_cidr},
                  {"ParameterKey": "ExistingSubnet1","ParameterValue": subnet1},
                  {"ParameterKey": "ExistingSubnet2","ParameterValue": subnet2}]

        # Find latest MATLAB release from Github page and get template url text
        res = requests.get(f"https://github.com/mathworks-ref-arch/{ref_arch_name}/blob/master/releases/")

        latest_releases = [re.findall("releases/(R\d{4}[ab]\\b)", res.text)[-1], re.findall("releases/(R\d{4}[ab]\\b)", res.text)[-2]]

        for i in range(2):
            matlab_release = latest_releases[i]
            print("Testing Health Check Release: " + matlab_release + "\n")
            github_base_dir = "https://raw.githubusercontent.com/mathworks-ref-arch"
            template_url_path = f"{github_base_dir}/{ref_arch_name}/master/releases/{matlab_release}/templates/templateURL.txt"
            file = urllib.request.urlopen(template_url_path)
            template_url = file.read().decode("utf-8").rstrip()
            split_template_url = template_url.split("\n")
            existing_vpc_template_url = split_template_url[1]

            stack_name = "mps-refarch-health-check-" + matlab_release + date.today().strftime('%m-%d-%Y') + str(random.randint(1,101))
            ct = datetime.datetime.now()
            print("Date time before deployment of stack: ", ct)
            try:
                stack = deploy.deploy_stack(existing_vpc_template_url, parameters, region, stack_name)
                ct = datetime.datetime.now()
                print("Date time after deployment of stack: ", ct)
            except Exception as e:
                raise (e)
            finally:
                # delete the stack
                print("deleting the stack : ", matlab_release)
                deploy.delete_stack(stack)
                print("success deleting the stack"+ "\n")
                ct = datetime.datetime.now()

        print("deleting the existing VPC stack")
        # delete the existing VPC
        deploy.delete_stack(existingstack)
        print("success deleting the existing VPC stack")
        ct = datetime.datetime.now()
        print("Date time after deletion of stacks:-", ct)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
