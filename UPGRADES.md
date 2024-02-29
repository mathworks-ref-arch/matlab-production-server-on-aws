# Upgrading an Existing Deployment

## Overview

This page shows you how to upgrade the release of a MATLAB® Production Server™ deployment that is hosted on Amazon Web Services (AWS) and deployed using the reference architecture. 


## Prerequisites 

- An existing deployment of MATLAB Production Server, as deployed by the reference architecture. 
- A backup of all applications uploaded to your current MATLAB Production Server deployment. You can create this by copying the contents of the S3 bucket containing your application code archives (CTF files) to a secure location. 
- (Optional) An existing virtual private cloud (VPC) with the required subnets and ports to deploy MATLAB Production Server to it. For more information on these requirements, navigate to the [reference architecture documentation](https://github.com/mathworks-ref-arch/matlab-production-server-on-aws) for the MATLAB release of your existing deployment. Required subnets and ports are described in "Step 3. Configure Existing VPC" for R2023a and later, or "How do I use an existing VPC to deploy MATLAB Production Server" in the FAQ section for earlier releases. If you already have an existing deployment in this VPC, these requirements should already be met.


## Considerations

### URL Compatibility
Your client applications might access MATLAB Production Server applications using the default MATLAB Execution Endpoint URL ```MATLABProductionServerFunctionExecutionURL``` provided in the **Outputs** tab of the root stack. If they do, note that this URL is different for your new deployment.  

You can avoid this issue in future upgrades by setting a custom DNS name for the MATLAB Execution Endpoint load balancer ```MATLABProductionServerLoadBalancer```. See [Configure a custom domain name for your Classic Load Balancer](https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/using-domain-names-with-elb.html) for instructions.

Set a custom DNS name for the MATLAB Production Server dashboard load balancer ```MATLABProductionServerDashboardLoadBalancer``` to preserve this URL as well. 

### Deployed Applications 
MATLAB Production Server supports MATLAB Runtime versions from the six most recent releases. You can migrate applications that were compiled using a supported MATLAB Runtime version to the new MATLAB Production Server deployment:
- If your application is compiled using a supported MATLAB Runtime version, follow [Step 3](UPGRADES.md#step-3-migrate-applications-to-the-new-deployment) of this procedure to migrate it.
- For all other applications, recompile your application using a supported version of MATLAB Runtime. See the [MATLAB Compiler SDK documentation](https://www.mathworks.com/help/compiler_sdk/mps_dev_test/create-a-deployable-archive-for-matlab-production-server.html) for information on how to create deployable archives for MATLAB Production Server.

See the [MATLAB Production Server on AWS README](https://github.com/mathworks-ref-arch/matlab-production-server-on-aws#deploy-reference-architecture-for-your-release) for a complete list of supported MATLAB Runtime versions for your release. 

### Server Downtime
Take these measures to help reduce the time MATLAB Production Server and your deployed applications are inaccessible during the upgrade process: 

- **Use a new network license manager for your new deployment.** Doing so allows you to keep both deployments functional while deployed applications and client applications are migrated. Note that to run two instances of MATLAB Production Server simultaneously, you must have two separate license instances. 
- **Set a custom URL for your MATLAB execution endpoint.** Doing so allows you to upgrade your MATLAB Production Server deployment without needing to update your client applications. Refer to the [URL Compatibility](#url-compatibility) section above for instructions on setting a custom DNS name for this endpoint. 
- **Compile deployed applications using the newest supported MATLAB Runtime version**. MATLAB Production Server supports the six most recent versions of MATLAB Runtime, so applications compiled for existing deployments of recent releases can be immediately migrated to a new deployment without needing to be recompiled. Deployed applications can be updated and redeployed after the upgrade process is complete. 


## Upgrade Steps 

### Step 1. Deploy Newest MATLAB Production Server Release from GitHub CloudFormation Template
When you upgrade the deployment, you can also deploy a new VPC and a new network license manager. This table summarizes the standard workflows.  
|  | Existing Network License Manager | New Network License Manager |
| --- | ------------ | ------- |
| **Existing VPC** | Deploy the “Existing VPC” template, selecting **No** for **DeployLicenseServer**. | Deploy the “Existing VPC” template, selecting **Yes** for **DeployLicenseServer**. |
| **New VPC** | Not recommended | Deploy the "New VPC" template. |


*If using a new VPC*: 
1. In the GitHub repository for [MATLAB Production Server on AWS](https://github.com/mathworks-ref-arch/matlab-production-server-on-aws), go to the [MATLAB release](https://github.com/mathworks-ref-arch/matlab-production-server-on-aws#deploy-reference-architecture-for-your-release) you are deploying. Under “Step 1. Launch Template,” click **Launch Stack**. (For R2023a and later, click the button under **New VPC**.)
2. Fill out the template fields, then click **Create Stack**. You can monitor the resource creation from the **Stacks** section of the CloudFormation service in the AWS Portal. 
3. Wait for the resource creation process to complete for your deployed stack. 

*If using an existing VPC*: 
1. In the GitHub repository for [MATLAB Production Server on AWS](https://github.com/mathworks-ref-arch/matlab-production-server-on-aws), go to the [MATLAB release](https://github.com/mathworks-ref-arch/matlab-production-server-on-aws#deploy-reference-architecture-for-your-release) you are deploying. Go to the FAQ section and select **Launch Stack** under “How do I use an existing VPC to deploy MATLAB Production Server?” (For R2023a and later, click the button in Step 1 under **Existing VPC**.)
2. Fill out the template fields as specified in the GitHub documentation for the release you are deploying, then click **Create Stack**. You can monitor the resource creation from the **Stacks** section of the CloudFormation service in the AWS Portal. 
3. Wait for the resource creation process to complete for your deployed stack. 

### Step 2. Upload License File
1. Log in to the Network License Manager Dashboard.
	- *If using a new network license manager*:<ol style="list-style-type:lower-roman"><li>In the **Outputs** tab for your new stack, locate the ```MatlabProductionServerLicenseServer``` key and click the corresponding URL. This takes you to the Network License Manager for MATLAB Dashboard login page.</li><li>Log in with the username ```manager``` and the password you specified while creating the stack. </li></ol>
	- *If using an existing network license manager*:<ol style="list-style-type:lower-roman"><li>In the AWS Console, navigate to the EC2 instance for your network license manager. Locate the public IPv4 DNS for this instance and click the corresponding URL. This takes you to the Network License Manager for MATLAB Dashboard login page.</li><li>Log in with the username and password configured when initially deploying this License Manager.</li><li>Go to the [reference architecture documentation](https://github.com/mathworks-ref-arch/matlab-production-server-on-aws#deploy-reference-architecture-for-your-release) for the MATLAB release of your new deployment. Follow the additional configuration steps in the “How to use an existing license server in an existing VPC?” subsection, under “How do I use an existing VPC to deploy MATLAB Production Server?” in the FAQ section. (For R2023a and later, follow the steps under "Use Existing License Server in Existing VPC," under "Additional Information.")</li></ol>
2. Follow the instructions in the dashboard to retrieve and upload the license file. Make sure to choose the release and operating system that match your new deployment. 
3. (Optional) Deactivate the previous license in the MathWorks License Center. 

### Step 3. Migrate Applications to New Deployment
**Note**: These instructions are for deployed applications compiled using one of the six most recent versions of MATLAB Runtime. For all other applications, refer to [Deployed Applications](UPGRADES.md#deployed-applications).

1. Go to the S3 bucket containing the applications for your existing deployment. This can be found in the **Outputs** tab for your existing deployment's stack, with the key ```MATLABProductionServerApplicationsBucket```. 
2. Select all code archives (CTF files) in the **auto_deploy** folder, then select **Actions > Move**. 
3. Set the destination as the **auto_deploy** folder in the S3 bucket for your new deployment. This can be found in **Outputs** tab for your new stack, with the key ```MATLABProductionServerApplicationsBucket```. 
4. Select **Move**.  

### Step 4. Verify Access to MATLAB Production Server Dashboard and Applications for New Deployment
1. In the **Outputs** tab for your new stack, locate the ```MatlabProductionServerDashboardURL``` key and click the corresponding URL. This takes you to the dashboard login page.  
2. Log in using the administrator username and password that you specified in the **Dashboard Login** section while creating the stack. 
3. Confirm that the displayed server information matches the version and operating system specified during deployment, and that all deployed applications appear in the **Applications** tab. 

### Step 5. Delete Unused Resources from Previous Deployment
Deploying MATLAB Production Server from the reference architecture creates a CloudFormation stack in AWS. This root stack deploys up to four nested stacks, which can be viewed from the **Resources** tab for the root stack. Refer to this table for the nested stacks that you can safely delete from your previous deployment. If you want to delete all nested stacks deployed as part of your previous deployment, delete the root stack. 
|  | Existing Network License Manager | New Network License Manager |
| --- | ------------ | ------- |
| **Existing VPC** | <ol><li> ```MatlabProductionServerResourcesStack```</li><li> ```MatlabProductionServerCustomParamLambdaFunctionStack```</li></ol> | <ol><li> ```MatlabProductionServerResourcesStack```</li><li>```MatlabProductionServerLicenseServerStack```</li><li> ```MatlabProductionServerCustomParamLambdaFunctionStack```</li></ol> |
| **New VPC** | Not recommended | <ol><li> ```MatlabProductionServerResourcesStack```</li><li>```MatlabProductionServerLicenseServerStack```</li><li>```MatlabProductionServerVPCStack```</li><li> ```MatlabProductionServerCustomParamLambdaFunctionStack```</li></ol>  |

Note that when deleting nested stacks, you are prompted to confirm if you want to delete the root stack instead. Do not delete the root stack unless you intend to delete all resources included in your previous deployment. 

A summary of each stack and its contents follows. For more detailed information on the stack resources, refer to the GitHub documentation for your deployment.
- ```MatlabProductionServerResourcesStack``` &mdash; Contains all resources specific to MATLAB Production Server. This stack is always deployed, and you can delete it regardless of the configuration used by your new deployment. This stack also has its own nested stack ```MatlabProductionServerLambdaFunctionsStack```, which is deleted when you delete the main stack. 
- ```MatlabProductionServerLicenseServerStack``` &mdash; Contains the network license manager and related resources. This stack is deployed when you deploy to a new VPC or when you deploy to an existing VPC with the **DeployLicenseServer** field set to **Yes**. You can delete this stack if you are using a new network license manager or a license manager not deployed by this stack. 
- ```MatlabProductionServerVPCStack``` &mdash; Contains the VPC and related resources. This stack is deployed when you use the standard template. You can delete this stack if you are using a VPC that was not deployed by this stack. 
- ```MatlabProductionServerCustomParamLambdaFunctionStack``` (R2023b and later) &mdash; Contains a Lambda function used to retrieve the CIDR range of an existing VPC. This stack is deployed when you use the "Existing VPC" template. You can delete this stack regardless of the configuration used by your new deployment.

See [Working with stacks](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacks.html) for more information on risks and best practices when deleting AWS CloudFormation stacks.