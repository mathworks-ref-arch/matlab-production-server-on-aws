# Upgrading an Existing Deployment

# Overview

This page walks through the steps to upgrade a MATLAB Production Server (MPS) deployment hosted on AWS using the reference architectures. 

You may choose to deploy a new virtual public cloud (VPC) and/or a new network license manager (NLM) depending on your cloud resource configuration. The table below summarizes the standard workflows.  
| --- | Existing NLM | New NLM |
| --- | ------------ | ------- |
| **Existing VPC** | Deploy the “How do I use an existing VPC to deploy MATLAB Production Server?” template, select **No** for DeployLicenseServer | Deploy the “How do I use an existing VPC to deploy MATLAB Production Server?” template, select **Yes** for DeployLicenseServer |
| **New VPC** | Not recommended | Deploy the standard template |


# Prerequisites 

1. An existing deployment of MATLAB Production Server, as deployed by the reference architecture. 
2. Back up all applications uploaded to your current MPS deployment. You can do this by copying the contents of the S3 bucket containing your application CTF files to a secure location. 
3. *If using an existing VPC*: <ul><li> Refer to “How do I use an existing VPC to deploy MATLAB Production Server?” under the FAQ section of the reference architecture documentation on GitHub. This section describes the subnets and ports required to deploy MPS to this VPC. If you already have an existing MPS deployment in this VPC, these requirements should already be met. </li></ul>


# Considerations

## URL Compatibility
If your client applications access MPS applications using the default MATLAB Execution Endpoint URL ```MATLABProductionServerFunctionExecutionURL``` provided in the **Outputs** tab of the root stack, note that this URL will be different for your new deployment.  

You can avoid this issue in future upgrades by setting a custom DNS name for the MATLAB Execution Endpoint load balancer ```MATLABProductionServerLoadBalancer```. Refer to the following AWS documentation for instructions: 

https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/using-domain-names-with-elb.html 

Set a custom DNS name for the MATLAB Production Server dashboard load balancer ```MATLABProductionServerDashboardLoadBalancer``` to preserve this URL as well. 

## Deployed Applications 
MATLAB Production Server supports MATLAB Runtime versions from the six most recent releases. Applications that were compiled using a supported MATLAB Runtime version may be migrated to the new MPS deployment by following the instructions for Step 2 above. All other applications must be recompiled using a supported version of MATLAB Runtime. Refer to the following link for information on how to create deployable archives for MPS: 

https://www.mathworks.com/help/compiler_sdk/mps_dev_test/create-a-deployable-archive-for-matlab-production-server.html

Refer to the README for a complete list of supported MATLAB Runtime versions for your release. 

## Server Downtime
The following measures may help to reduce the time your MATLAB Production Server and deployed applications are inaccessible during this transition: 

- **Use a new NLM for your new deployment.** This will allow you to keep both deployments functional while deployed applications and client applications are migrated. Please note that running two instances of MATLAB Production Server simultaneously does require two separate license instances. 
- **Set a custom URL for your MATLAB Execution Endpoint.** This will allow you to upgrade your MPS deployment without needing to update your client applications. Refer to the “URL Compatibility” section above for instructions on setting a custom DNS name for this endpoint. 
- **Compile deployed applications using the newest supported MATLAB Runtime version**. MATLAB Production Server supports the most recent six version of MATLAB Runtime, so applications compiled for existing deployments of recent releases may be immediately migrated to a new deployment without needing to be recompiled. Deployed applications can be updated and redeployed after the upgrade process is complete. 


# Upgrade Steps 

# Step 1. Deploy the newest release of MATLAB Production Server from the CloudFormation template on GitHub.
*If using a new VPC*: 
1. From the GitHub for [MATLAB Production Server on AWS](https://github.com/mathworks-ref-arch/matlab-production-server-on-aws), under “Step 1. Launch Template,” select **Launch Stack**.  
2. Fill out the template fields, then select **Create Stack**. You can monitor the resource creation from the “Stacks” section of the CloudFormation service in the AWS Portal. 
3. Wait for the resource creation process to complete for your deployed stack. 

*If using an existing VPC*: 
1. From the GitHub for [MATLAB Production Server on AWS](https://github.com/mathworks-ref-arch/matlab-production-server-on-aws), navigate to the FAQ section and select **Launch Stack** under “How do I use an existing VPC to deploy MATLAB Production Server?” 
2. Fill out the template fields according to the GitHub documentation for this FAQ, then select **Create Stack**. You can monitor the resource creation from the “Stacks” section of the CloudFormation service in the AWS Portal. 
3. Wait for the resource creation process to complete for your deployed stack. 

# Step 2. Upload the license file.
1. Log in to the NLM Dashboard.
	- *If using a new NLM*:<ol style="list-style-type:lower-roman"><li>In the Outputs tab for your new stack, locate the MatlabProductionServerLicenseServer key and click the corresponding URL. This will take you to the Network License Manager for MATLAB Dashboard login page.</li><li>Log in with the username manager and the password you specified while creating the stack. </li></ol>
	- *If using an existing NLM*:<ol style="list-style-type:lower-roman"><li>From the EC2 instance for your NLM, locate the public IPv4 DNS and click the corresponding URL. This will take you to the Network License Manager for MATLAB Dashboard login page.</li><li>Log in with the previously configured username and password.</li><li>Refer to the “How to use an existing license server in an existing VPC?” subsection, under “How do I use an existing VPC to deploy MATLAB Production Server?” in the FAQ section of the reference architecture documentation on GitHub for additional configuration steps required for your MPS deployment to use this NLM.</li></ol>
2. Follow the instructions in the dashboard to retrieve and upload the license file. Make sure to choose the release and operating system that match your new deployment. 
3. (Optional) Deactivate the previous license in the License Center. 

# Step 3. Migrate applications to the new deployment.
**Note**: The following instructions are for deployed applications compiled using one of the six most recent versions of MATLAB Runtime. For all other applications, refer to "Deployed Applications" in the Additional Considerations section above.

1. Navigate to the S3 bucket containing the applications for your existing deployment. This can be found in **Outputs** tab for your existing deployment's stack, with the key ```MATLABProductionServerApplicationsBucket```. 
2. Select all CTF files in the **auto_deploy** folder, then select **Actions > Move**. 
3. Set the destination as the **auto_deploy** folder in the S3 bucket for your new deployment. This can be found in Outputs tab for your new stack, with the key ```MATLABProductionServerApplicationsBucket```. 
4. Select **Move**.  

# Step 4. Verify that you can access the MPS dashboard and applications for your new deployment. 
1. In the **Outputs** tab for your new stack, locate the ```MatlabProductionServerDashboardURL``` key and click the corresponding URL. This will take you to the dashboard login page.  
2. Log in using the administrator username and password that you specified in the Dashboard Login section while creating the stack. 
3. Confirm that all configurations and applications appear as expected. 

# Step 5. Delete unused resources from your previous deployment. 
Deploying MATLAB Production Server from the reference architecture creates a CloudFormation stack in AWS. This root stack deploys up to 3 nested stacks, which can be viewed from the **Resources** tab for the root stack. Refer to the following table for which nested stacks can be safely deleted from your previous deployment. If you would like to delete all nested stacks deployed as part of your previous deployment, delete the root stack. 
| --- | Existing NLM | New NLM |
| --- | ------------ | ------- |
| **Existing VPC** | <ol><li> ```MatlabProductionServerResourcesStack```</li></ol> | <ol><li> ```MatlabProductionServerResourcesStack```</li><li>```MatlabProductionServerLicenseServerStack```</li></ol> |
| **New VPC** | Not recommended | <ol><li> ```MatlabProductionServerResourcesStack```</li><li>```MatlabProductionServerLicenseServerStack```</li><li>```MatlabProductionServerVPCStack```</li></ol>  |
Note that when deleting nested stacks, you will be prompted to confirm if you would like to delete the root stack instead. Do not delete the root stack unless you intend to delete all resources included in your previous deployment. 

A summary of each stack and its contents can be found below. For more detailed information on the stack resources, refer to the GitHub documentation for your deployment.
- ```MatlabProductionServerResourcesStack```: Contains all MPS-specific resources. This is always deployed, and can be deleted regardless of the configuration used by your new deployment. This also has its own nested stack ```MatlabProductionServerLambdaFunctionsStack```, which is deleted when deleting the main stack. 
- ```MatlabProductionServerLicenseServerStack```: Contains the NLM and related resources. This is deployed when deploying to a new VPC, or when deploying to an existing VPC with the **DeployLicenseServer** field set to **Yes**. This can be deleted if you are using a new NLM or a NLM not deployed by this stack. 
- ```MatlabProductionServerVPCStack```: Contains the VPC and related resources. This is deployed when using the standard template. This can be deleted if you are using a VPC that was not deployed by this stack. 
