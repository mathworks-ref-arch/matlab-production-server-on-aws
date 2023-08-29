# Upgrading an Existing Deployment

## Overview

This page shows you how to upgrade the MATLAB<sup>:registered:</sup> version of a MATLAB Production Server:tm: deployment hosted on AWS using the reference architectures. 


## Prerequisites 

- An existing deployment of MATLAB Production Server, as deployed by the reference architecture. 
- A backup of all applications uploaded to your current MATLAB Production Server deployment. You can create this by copying the contents of the S3 bucket containing your application code archives (.ctf files) to a secure location. 
- (Optional) An existing VPC with the required subnets and ports to deploy MATLAB Production Server to it. See "How do I use an existing VPC to deploy MATLAB Production Server" under the FAQ section of the reference architecture [documentation](https://github.com/mathworks-ref-arch/matlab-production-server-on-aws#deploy-reference-architecture-for-your-release) for the MATLAB release of your new deployment. If you already have an existing deployment in this VPC, these requirements should already be met.


## Considerations

### URL Compatibility
If your client applications access MATLAB Production Server applications using the default MATLAB Execution Endpoint URL ```MATLABProductionServerFunctionExecutionURL``` provided in the **Outputs** tab of the root stack, note that this URL is different for your new deployment.  

You can avoid this issue in future upgrades by setting a custom DNS name for the MATLAB Execution Endpoint load balancer ```MATLABProductionServerLoadBalancer```. Refer to the following AWS documentation for instructions: 

https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/using-domain-names-with-elb.html 

Set a custom DNS name for the MATLAB Production Server dashboard load balancer ```MATLABProductionServerDashboardLoadBalancer``` to preserve this URL as well. 

### Deployed Applications 
MATLAB Production Server supports MATLAB Runtime versions from the six most recent releases. You can migrate applications that were compiled using a supported MATLAB Runtime version to the new MATLAB Production Server deployment:
- If your application is compiled using a supported MATLAB Runtime version, follow Step 3 to migrate it.
- For all other applications, recompile using a supported version of MATLAB Runtime. See the following link for information on how to create deployable archives for MATLAB Production Server: https://www.mathworks.com/help/compiler_sdk/mps_dev_test/create-a-deployable-archive-for-matlab-production-server.html

See the README for a complete list of supported MATLAB Runtime versions for your release. 

### Server Downtime
The following measures can help reduce the time your MATLAB Production Server and deployed applications are inaccessible during this transition: 

- **Use a new network license manager for your new deployment.** This allows you to keep both deployments functional while deployed applications and client applications are migrated. Please note that running two instances of MATLAB Production Server simultaneously does require two separate license instances. 
- **Set a custom URL for your MATLAB Execution Endpoint.** This allows you to upgrade your MATLAB Production Server deployment without needing to update your client applications. Refer to the “URL Compatibility” section above for instructions on setting a custom DNS name for this endpoint. 
- **Compile deployed applications using the newest supported MATLAB Runtime version**. MATLAB Production Server supports the most recent six versions of MATLAB Runtime, so applications compiled for existing deployments of recent releases can be immediately migrated to a new deployment without needing to be recompiled. Deployed applications can be updated and redeployed after the upgrade process is complete. 


## Upgrade Steps 

### Step 1. Deploy the newest release of MATLAB Production Server from the CloudFormation template on GitHub
When you upgrade the deployment, you can deploy a new virtual public cloud (VPC), a new network license manager, or both, depending on your cloud resource configuration. The table below summarizes the standard workflows.  
|  | Existing Network License Manager | New Network License Manager |
| --- | ------------ | ------- |
| **Existing VPC** | Deploy the “How do I use an existing VPC to deploy MATLAB Production Server?” template, selecting **No** for **DeployLicenseServer**. | Deploy the “How do I use an existing VPC to deploy MATLAB Production Server?” template, selecting **Yes** for **DeployLicenseServer**. |
| **New VPC** | Not recommended | Deploy the standard template. |

*If using a new VPC*: 
1. In the GitHub for [MATLAB Production Server on AWS](https://github.com/mathworks-ref-arch/matlab-production-server-on-aws), navigate to the [MATLAB release](https://github.com/mathworks-ref-arch/matlab-production-server-on-aws#deploy-reference-architecture-for-your-release) you are deploying. Under “Step 1. Launch Template,” click **Launch Stack**. (For R2023a and later, click the button under New VPC.)
2. Fill out the template fields, then select **Create Stack**. You can monitor the resource creation from the **Stacks** section of the CloudFormation service in the AWS Portal. 
3. Wait for the resource creation process to complete for your deployed stack. 

*If using an existing VPC*: 
1. From the GitHub for [MATLAB Production Server on AWS](https://github.com/mathworks-ref-arch/matlab-production-server-on-aws), navigate to the [MATLAB release](https://github.com/mathworks-ref-arch/matlab-production-server-on-aws#deploy-reference-architecture-for-your-release) you are deploying. Go to the FAQ section and select **Launch Stack** under “How do I use an existing VPC to deploy MATLAB Production Server?”. (For R2023a and later, click the button in Step 1 under Existing VPC.)
2. Fill out the template fields according to the GitHub documentation for this FAQ, then select **Create Stack**. You can monitor the resource creation from the **Stacks** section of the CloudFormation service in the AWS Portal. 
3. Wait for the resource creation process to complete for your deployed stack. 

### Step 2. Upload the license file
1. Log in to the Network License Manager Dashboard.
	- *If using a new network license manager*:<ol style="list-style-type:lower-roman"><li>In the **Outputs** tab for your new stack, locate the ```MatlabProductionServerLicenseServer``` key and click the corresponding URL. This takes you to the Network License Manager for MATLAB Dashboard login page.</li><li>Log in with the username manager and the password you specified while creating the stack. </li></ol>
	- *If using an existing network license manager*:<ol style="list-style-type:lower-roman"><li>From the EC2 instance for your network license manager, locate the public IPv4 DNS and click the corresponding URL. This takes you to the Network License Manager for MATLAB Dashboard login page.</li><li>Log in with the previously configured username and password.</li><li>Navigate to the reference architecture [documentation](https://github.com/mathworks-ref-arch/matlab-production-server-on-aws#deploy-reference-architecture-for-your-release) for the MATLAB release of your new deployment. Follow the additional configuration steps in the “How to use an existing license server in an existing VPC?” subsection, under “How do I use an existing VPC to deploy MATLAB Production Server?” in the FAQ section. (For R2023a and later, follow the steps under "Use Existing License Server in Existing VPC," under "Additional Information.")</li></ol>
2. Follow the instructions in the dashboard to retrieve and upload the license file. Make sure to choose the release and operating system that match your new deployment. 
3. (Optional) Deactivate the previous license in the License Center. 

### Step 3. Migrate applications to the new deployment
**Note**: The following instructions are for deployed applications compiled using one of the six most recent versions of MATLAB Runtime. For all other applications, refer to [Deployed Applications](UPGRADES.md#deployed-applications).

1. Navigate to the S3 bucket containing the applications for your existing deployment. This can be found in the **Outputs** tab for your existing deployment's stack, with the key ```MATLABProductionServerApplicationsBucket```. 
2. Select all code archives (.ctf files) in the **auto_deploy** folder, then select **Actions > Move**. 
3. Set the destination as the **auto_deploy** folder in the S3 bucket for your new deployment. This can be found in Outputs tab for your new stack, with the key ```MATLABProductionServerApplicationsBucket```. 
4. Select **Move**.  

### Step 4. Verify that you can access the MATLAB Production Server dashboard and applications for your new deployment
1. In the **Outputs** tab for your new stack, locate the ```MatlabProductionServerDashboardURL``` key and click the corresponding URL. This takes you to the dashboard login page.  
2. Log in using the administrator username and password that you specified in the **Dashboard Login** section while creating the stack. 
3. Confirm that the displayed server information matches the version and operating system specified during deployment, and that all deployed applications appear in the **Applications** tab. 

### Step 5. Delete unused resources from your previous deployment
Deploying MATLAB Production Server from the reference architecture creates a CloudFormation stack in AWS. This root stack deploys up to 3 nested stacks, which can be viewed from the **Resources** tab for the root stack. Refer to the following table for the nested stacks that can be safely deleted from your previous deployment. If you want to delete all nested stacks deployed as part of your previous deployment, delete the root stack. 
|  | Existing Network License Manager | New Network License Manager |
| --- | ------------ | ------- |
| **Existing VPC** | <ol><li> ```MatlabProductionServerResourcesStack```</li></ol> | <ol><li> ```MatlabProductionServerResourcesStack```</li><li>```MatlabProductionServerLicenseServerStack```</li></ol> |
| **New VPC** | Not recommended | <ol><li> ```MatlabProductionServerResourcesStack```</li><li>```MatlabProductionServerLicenseServerStack```</li><li>```MatlabProductionServerVPCStack```</li></ol>  |

Note that when deleting nested stacks, you are prompted to confirm if you would like to delete the root stack instead. Do not delete the root stack unless you intend to delete all resources included in your previous deployment. 

These are summaries of each stack and its contents. For more detailed information on the stack resources, refer to the GitHub documentation for your deployment.
- ```MatlabProductionServerResourcesStack```: Contains all MATLAB Production Server-specific resources. This is always deployed and can be deleted regardless of the configuration used by your new deployment. This also has its own nested stack ```MatlabProductionServerLambdaFunctionsStack```, which is deleted when deleting the main stack. 
- ```MatlabProductionServerLicenseServerStack```: Contains the network license manager and related resources. This is deployed when deploying to a new VPC or when deploying to an existing VPC with the **DeployLicenseServer** field set to **Yes**. This can be deleted if you are using a new network license manager or a license manager not deployed by this stack. 
- ```MatlabProductionServerVPCStack```: Contains the VPC and related resources. This is deployed when using the standard template. This can be deleted if you are using a VPC that was not deployed by this stack. 

See [Working with stacks](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacks.html) for more information on risks and best practices when deleting AWS CloudFormation stacks.