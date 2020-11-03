import refarch_testtools.deploy as deploy
import sys

def main(keypairname, password, ipAddress):
    parameters = [{'ParameterKey': 'KeyPairName', 'ParameterValue': keypairname},
                  {'ParameterKey': 'ClientIPAddress', 'ParameterValue': ipAddress},
                  {'ParameterKey': 'WorkerSystem', 'ParameterValue': 'Ubuntu'}, 
                  {'ParameterKey': 'Password', 'ParameterValue': password},
                  {'ParameterKey': 'ConfirmPassword', 'ParameterValue': password}]

    template_url = "https://matlab-production-server-templates.s3.amazonaws.com/MatlabProductionServer_R2020a_New.yml"
    
    try:
        print("deploying the stack")
        stack = deploy.deploy_stack(template_url, parameters, "us-east-1", "mpsRefArchAuto")
        print("success deploying the stack")
    except Exception as e:
        raise (e)
   
    # delete the deployment
    print("deleting the stack")
    deploy.delete_stack(stack)
    print("success deleting the stack")

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])