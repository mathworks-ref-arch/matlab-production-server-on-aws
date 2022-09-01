# Health check Test for MATLAB Production Server Reference Architecture AWS on Linux where new VPC is created.
# Copyright 2022 The MathWorks, Inc.

import refarch_testtools.deploy as deploy
import sys
import re
import requests
import datetime
import urllib
import random
from datetime import date

def main(keypairname, password, ipAddress, SSLCertificateARN, region, platform):
    # Reference architectures in production.
    ref_arch_name = 'matlab-production-server-on-aws'
    parameters = [{'ParameterKey': 'KeyPairName', 'ParameterValue': keypairname},
                  {'ParameterKey': 'SSLCertificateARN', 'ParameterValue': SSLCertificateARN},
                  {'ParameterKey': 'ClientIPAddress', 'ParameterValue': ipAddress},
                  {'ParameterKey': 'WorkerSystem', 'ParameterValue': platform},
                  {'ParameterKey': 'Username', 'ParameterValue': 'admin'},
                  {'ParameterKey': 'Password', 'ParameterValue': password},
                  {'ParameterKey': 'ConfirmPassword', 'ParameterValue': password}]
    parameters1 = [{'ParameterKey': 'KeyPairName', 'ParameterValue': keypairname},
                  {'ParameterKey': 'SSLCertificateARN', 'ParameterValue': SSLCertificateARN},
                  {'ParameterKey': 'ClientIPAddress', 'ParameterValue': ipAddress},
                  {'ParameterKey': 'WorkerSystem', 'ParameterValue': platform},
                  {'ParameterKey': 'Password', 'ParameterValue': password},
                  {'ParameterKey': 'ConfirmPassword', 'ParameterValue': password}]

    # Find latest MATLAB release from Github page and get template url text
    res = requests.get(f"https://github.com/mathworks-ref-arch/{ref_arch_name}/blob/master/releases/")

    latest_releases = [re.findall("master/releases/(R\d{4}[ab]\\b)", res.text)[-1], re.findall("master/releases/(R\d{4}[ab]\\b)", res.text)[-2]]
    for i in range(2):
        matlab_release = latest_releases[i]
        print("Testing Health Check Release: " + matlab_release + "\n")
        github_base_dir = "https://raw.githubusercontent.com/mathworks-ref-arch"
        template_url_path = f"{github_base_dir}/{ref_arch_name}/master/releases/{matlab_release}/templates/templateURL.txt"
        file = urllib.request.urlopen(template_url_path)
        template_url = file.readline().decode("utf-8").rstrip()

        stack_name = "mps-refarch-health-check-" + matlab_release + date.today().strftime('%m-%d-%Y') + str(random.randint(1,101))
        ct = datetime.datetime.now()
        print("Date time before deployment of stack:-", ct)

        try:
            print("deploying the stack")

            if matlab_release == "R2021a" :
                stack = deploy.deploy_stack(template_url, parameters1, region, stack_name)
            else :
                stack = deploy.deploy_stack(template_url, parameters, region, stack_name)

            print("success deploying the stack")
        except Exception as e:
            raise (e)
        finally:
            # delete the stack
            print("deleting the stack")
            deploy.delete_stack(stack)
            print("success deleting the stack" + "\n")
            ct = datetime.datetime.now()
            print("Date time after deployment and deletion of stack:-", ct)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
