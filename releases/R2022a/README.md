# MATLAB Production Server on Amazon Web Services

# Requirements

Before starting, you need the following:

-   A MATLAB® Production Server™ license that meets the following conditions:
    - Current on Software Maintenance Service (SMS).
    - Linked to a MathWorks Account.
    - Concurrent license type. To check your license type, view your MathWorks Account.
    - Configured to use a network license manager on the virtual network. By default, the deployment of MATLAB Production Server includes a network license manager, but you can also use an existing license manager. In either case, activate or move the license after deployment. For details, see [Configure MATLAB Production Server Licensing on the Cloud](https://www.mathworks.com/help/licensingoncloud/matlab-production-server-on-the-cloud.html).
-   An Amazon Web Services™ (AWS) account.
-   A Key Pair for your AWS account in the US East (N. Virginia), EU (Ireland) or Asia Pacific (Tokyo) region. For more information, see [Amazon EC2 Key Pairs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html).

# Costs
You are responsible for the cost of the AWS services used when you create cloud resources using this guide. Resource settings, such as instance type, will affect the cost of deployment. For cost estimates, see the pricing pages for each AWS service you will be using. Prices are subject to change.


# Introduction
The following guide will help you automate the process of running MATLAB
Production Server on the Amazon Web Services (AWS) Cloud. The automation is
accomplished using an AWS CloudFormation template. The template is a JSON
file that defines the resources required to deploy and manage MATLAB Production
Server on AWS. Once deployed, you can manage the server using the
MATLAB Production Server dashboard&mdash;a web-based interface to
configure and manage server instances on the cloud. For more information, see [Manage MATLAB Production Server Using the Dashboard](https://www.mathworks.com/help/mps/server/manage-matlab-production-server-using-the-dashboard.html).
For information about the architecture of this solution, see [Architecture and Resources](#architecture-and-resources). For information about AWS templates, see [AWS CloudFormation Templates](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-guide.html). <br>

The default MATLAB Production Server deployment template uses the Network License Manager for MATLAB reference architecture to manage MATLAB Production Server licenses. The template for using an exisitng VPC for the deployment provides an option to either deploy the Network License Manager or use your own license server. For more information about the Network License Manager for MATLAB reference architecture, see [Network License Manager for MATLAB](https://github.com/mathworks-ref-arch/license-manager-for-matlab-on-aws).

# Prepare Your AWS Account
1. If you do not have an AWS account, create one at https://aws.amazon.com by following the on-screen instructions.
2. Use the regions selector in the navigation bar to choose **US-EAST (N. Virginia)**, **EU (Ireland)** or **Asia Pacific (Tokyo)**, as the region where you want to deploy MATLAB Production Server.
3. Create a [key pair](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html) in that region.  The key pair is necessary as it is the only way to connect to the instance as an administrator.
4. If necessary, [request a service limit increase](https://console.aws.amazon.com/support/home#/case/create?issueType=service-limit-increase&limitType=service-code-) for the Amazon EC2 instance type or VPCs.  You might need to do this if you already have existing deployments that use that instance type or you think you might exceed the [default limit](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-resource-limits.html) with this deployment.

# Deployment Steps

## Step 1. Launch Template
Click the **Launch Stack** button to deploy resources on AWS. This will open the AWS Management Console in your web browser.

| Release | Windows Server 2019 or Ubuntu 18.04 VM |
|---------------|------------------------|
| MATLAB R2022a | <a href="https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/create/review?templateURL=https://matlab-production-server-templates.s3.amazonaws.com/r2022a_mps_refarch/mps-aws-refarch-new-vpc-cf.yml" target="_blank">     <img src="https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png"/> </a> |
| MATLAB R2021b | <a href="https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/create/review?templateURL=https://matlab-production-server-templates.s3.amazonaws.com/r2021b_mps_refarch/mps-aws-refarch-new-vpc-cf.yml" target="_blank">     <img src="https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png"/> </a> |

For other releases, see [How do I launch a template that uses a previous MATLAB release?](#how-do-i-launch-a-template-that-uses-a-previous-matlab-release)
<p><strong>Note:</strong> Creating a stack on AWS can take at least 20 minutes.</p>

## Step 2. Configure Stack
1. Provide values for parameters in the **Create Stack** page:

    | Parameter Name                         | Value                                                                                                                                                                                                                                                                                                                                                 |
    |----------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **Stack name**                         | Choose a name for the stack. After the deployment finishes, this name is displayed in the AWS console. <p><em>*Example*</em>: Boston</p>  |
    ||**Server**|
    | **Number of Server VMs**             | Choose the number of AWS instances to start for the server. <p><em>*Example*</em>: 6</p><p>If you have a standard 24 worker MATLAB Production Server license and select `m5.xlarge` (4 cores) as the **Number of server VMs**, you need 6 worker nodes to fully utilize the workers in your license.</p><p>You can always under provision the number instances, in which case you may end up using fewer workers than you are licensed for.</p>|
    | **Server VM Type** | Choose the AWS instance type to use for the server instances. All AWS instance types are supported. For more information, see [Amazon EC2 Instance Types](https://aws.amazon.com/ec2/instance-types/). <p><em>*Example*</em>: m5.xlarge</p> |
    | **Server VM Operating System** | Choose between Windows (Windows Server) and Linux(Ubuntu) to use for the server instances.  |
    | **Create Redis ElastiCache** | Choose whether you want to create a Redis ElastiCache service. Creating this service will allow you to use the persistence functionality of the server. Persistence provides a mechanism to cache data between calls to MATLAB code running on a server instance. |
    | **Deploy License Server** | Specify whether you want to deploy the Network License Manager for MATLAB. This parameter is available only if you use the deployment template for an existing VPC. <p>You can deploy a license server only if your solution uses public IP adresses. If your solution uses private IP addresses, you must separately deploy a license server in a public subnet.</p> |
    ||**Dashboard Login**|
    | **Username for MATLAB Production Server Dashboard** | Specify the administrator user name to log in to the MATLAB Production Server dashboard. |
    | **Password for MATLAB Production Server and License Server** | Enter the password to use for logging in to MATLAB Production Server dashboard and the Network License Manager for MATLAB dashboard. |
    | **Confirm Password MATLAB Production Server and License Server** | Reenter the password to log in to the MATLAB Production Server dashboard and the Network License Manager for MATLAB dashboard. |    
    | |**Network**|
    | **Name of Existing Key Pair**          | Choose the name of an existing EC2 Key Pair to allow access to all the VMs in the stack. For information about creating an Amazon EC2 key pair, see [Amazon EC2 Key Pairs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html#having-ec2-create-your-key-pair). <p><em>*Example*</em>: boston-keypair<p> |
    | **Allow Connections from IP Address** | Specify the IP address range that is allowed to connect to the dashboard that manages the server. The format for this field is IP Address/Mask. <p><em>Example</em>: </p>10.0.0.1/32 <ul><li>This is the public IP address which can be found by searching for "what is my ip address" on the web. The mask determines the number of IP addresses to include.</li><li>A mask of 32 is a single IP address.</li><li>Use a [CIDR calculator](https://www.ipaddressguide.com/cidr) if you need a range of more than one IP addresses.</li><li>You may need to contact your IT administrator to determine which address is appropriate.</li></ul></p> |
    | **Make Solution Available over Internet** | Choose 'Yes' if you want your solution to use public IP addresses. |
    | **ARN of SSL Certificate**             | Provide the Amazon Resource Name (ARN) of an existing certificate in the AWS Certificate Manager to enable secure HTTPS communication to the HTTPS server endpoint. For information on creating and uploading a self-signed certificate, see [Create and Sign an X509 Certificate](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/configuring-https-ssl.html) and [Import SSL Certificate]().<p><em>*Example*</em>: arn:aws:acm:us-east-1:12345:certificate/123456789012</p>|


    >**Note**: Make sure you select US East (N.Virginia), EU (Ireland) or Asia Pacific (Tokyo) as your region from the navigation panel on top. Currently, US East, EU (Ireland), and Asia Pacific (Tokyo) are the only supported regions.

2. Click **Next** to continue configuring stack options. Configuring stack options is optional. You can leave all fields blank or enter values based on your requirement. Click **Next** to review your stack details and stack options.

4. Review or edit your stack details and any stack options that you set. You must select the acknowledgement to create IAM resources. Otherwise, the deployment produces a `Requires capabilities : [CAPABILITY_IAM]` error and fails to create resources.

    When you are satisfied with your stack configuration, click **Create stack** to start the creation of AWS resources for your server environment. Resource creation can take up to 20 minutes. After resource creation, it can take up to 15 minutes for the resources to be active.  

## Step 3. Upload License File
1. Clicking **Create stack** takes you to the *Stack Detail* page for your stack. Wait for the status to reach **CREATE\_COMPLETE**.
1. In the Stack Detail for your stack, click **Outputs**.
1. Look for the key named `MatlabProductionServerLicenseServer` and click the corresponding URL listed under value. Doing so takes you to Network License Manager for MATLAB dashboard log in page.
1. The user name for the Network License Manager for MATLAB dashboard is **manager**. For the password, enter the password that you entered in the **Network License Manager for MATLAB** section while creating the stack in [Step 2](#step-2-configure-the-stack).
1. Follow the instructions to upload your MATLAB Production Server license.


## Step 4. Connect and Log In to MATLAB Production Server Dashboard
> **Note**: The Internet Explorer web browser is not supported for interacting with the dashboard.

1. In the Stack Detail for your stack, expand the **Outputs** section. 
1. Look for the key named `MatlabProductionServerDashboardURL` and click the corresponding URL listed under value. This is the HTTPS endpoint to the MATLAB Production Server dashboard.
1. Use the administrator user name and password that you specified in the dashboard login step of the deployment process to log in. For more information on how to use the dashboard, see [Manage MATLAB Production Server using Dashboard](https://www.mathworks.com/help/mps/server/manage-matlab-production-server-using-the-dashboard.html).  

You are now ready to use MATLAB Production Server on AWS. 

To run applications on MATLAB Production Server, you need to create applications using MATLAB Compiler SDK. For more information, see [Deployable Archive Creation](https://www.mathworks.com/help/mps/deployable-archive-creation.html) in the MATLAB Production Server product documentation.

# Additional Information

## Delete Your Stack

Once you have finished using your stack, it is recommended that you delete all resources to avoid incurring further cost. 

If you are using an existing license server, and have added the security group of the server VMs to the security group of the license server, you must delete the inbound rules before you delete the stack.
1. In the AWS management console, select the stack that you deployed. 
1. In the stack detail for your stack, click **Resources**.
1. Look for the **Logical ID** named `SecurityGroup` and click the corresponding URL listed under **Physical ID**. This will take you to the security group details.
1. Click the **Inbound Rules** tab, then click **Edit Inbound Rules**.
1. Click **Delete Rule** for the rules that have the tag `matlab-production-server-cloud-stack-elb-1-sg` as their **Source**. 
1. Click **Save Rules**.

To delete the stack, do the following:
1. Log in to the AWS Console.
3. Go to the AWS Cloud Formation page and select the stack that you created.
3. Click the **Actions** button and click **Delete Stack** from the menu that appears.

If you do not want to delete the entire deployment but want to minimize the cost, you can bring the number of instances in the Auto Scaling Group down to 0 and then scale it back up when the need arises.

## Get License Server MAC Address
The Network License Manager for MATLAB reference architecture manages the MATLAB Production Server license file. The deployment templates for the MATLAB Production Server reference architecture provide an option to deploy the license manager. You can also use an existing license manager that is located in the same VPC and the security group of the MATLAB Production Server instances. For more information about the Network License Manager for MATLAB reference architecture, see [Network License Manager for MATLAB](https://github.com/mathworks-ref-arch/license-manager-for-matlab-on-aws).

>**NOTE**: For a new license manager deployed with MATLAB Production Server, the license manager MAC address is available only after the deployment to the cloud is complete. For information on deploying the solution, see [Deployment Steps](/README.md#deployment-steps).

To get the MAC address of the license manager: 
1. Log in to the Network License Manager for MATLAB dashboard. For a license manager deployed with the MATLAB Production Server deployment, use the following credentials:<br>
Username: **manager**<br>
Password: Enter the password that you entered during the deployment process.
1. Click **Administration** > **License**.
1. Copy the license server MAC address displayed at the top.
# Architecture and Resources
Deploying this reference architecture will create several resources in your
resource group.


![Architecture](/releases/R2022a/images/mps_ref_arch_aws_diagram.png?raw=true)

*Architecture on AWS*

### Resources

| Resource Type                                                              | Number of Resources | Description                                                                                                                                                                                                                                                                                                                        |
|----------------------------------------------------------------------------|---------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| AWS EC2 Instance                                                           | 2                   | <ol><li>Virtual machine (VM) that hosts the MATLAB Production Server dashboard. Use the dashboard to: <ul><li>Get HTTPS endpoint to make requests</li><li> Upload applications (CTF files) to the server</li><li> Manage server configurations</li><li> Manage the HTTPS certificate</li></ul><p>For more information, see [MATLAB Production Server Using the Dashboard](https://www.mathworks.com/help/mps/server/manage-matlab-production-server-using-the-dashboard.html).</li><li>VM that hosts the Network License Manager for MATLAB. For more information, see [Network License Manager for MATLAB](https://github.com/mathworks-ref-arch/license-manager-for-matlab-on-aws).</li></ol>   |
| Auto Scaling Group                                                         | 1                   | Manages the number of identical VMs to be deployed. Each VM runs an instance of MATLAB Production Server which in turn runs multiple MATLAB workers.                                                                                                                                                                               |
| Load Balancer                                                              | 2                   | Provides routing and load balancing service to MATLAB Production Server instances. The MATLAB Production Server dashboard retrieves the HTTPS endpoint for making requests to the server from the load balancer resource.<p></p>                                                                                           |
| S3 Bucket                                                                  | 1                  | S3 storage bucket created during the creation of the stack where applications deployed to the reference architecture are stored.                                                                                                                                                                                                  |
| Virtual Private Cluster (VPC)                                              | 1                   | Enables resources to communicate with each other.                                           |
| Redis ElastiCache | 1 | Enables caching of data between calls to MATLAB code running on a server instance. |
| CloudWatch | 1 | Enables viewing of logs. |

# FAQ
## How do I use an existing VPC to deploy MATLAB Production Server?

Use the following templates to launch the reference architecture within an existing VPC and subnet. The templates provide an option to deploy the Network License Manager for MATLAB to manage MATLAB Production Server licenses. The license manager must be in the same VPC and security group as MATLAB Production Server.

| Release | Windows Server 2019 or Ubuntu 18.04 VM |
|---------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| R2022a | <a  href ="https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/create/review?templateURL=https://matlab-production-server-templates.s3.amazonaws.com/r2022a_mps_refarch/mps-aws-refarch-existing-vpc-cf.yml"  target ="_blank" >      <img  src ="https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png" />  </a> |
| R2021b | <a  href ="https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/create/review?templateURL=https://matlab-production-server-templates.s3.amazonaws.com/r2021b_mps_refarch/mps-aws-refarch-existing-vpc-cf.yml"  target ="_blank" >      <img  src ="https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png" />  </a> |

In addition to the parameters specified in the section [Configure the Stack](#step-2-configure-the-stack), you will need to specify the following parameters in the template to use your existing VPC.

| Parameter  | Value |
|----------------------------------|--------------------------------------------------------------------------------|
| Existing VPC ID | ID of your existing VPC. |
| IP address range of existing VPC | IP address range from the existing VPC. To find the IP address range: <ol><li>Log in to the AWS Console.</li><li>Navigate to the VPC dashboard and select your VPC.</li><li>Click the **CIDR blocks** tab.</li><li>The **IPv4 CIDR Blocks** gives the IP address range.</li></ol> |
| Subnet 1 ID | ID of an existing subnet that will host the dashboard and other resources. |
| Subnet 2 ID | ID of an existing subnet that will host the application load balancer. |

- If Subnet 1 and Subnet 2 are public, then you must connect the EC2 VPC endpoint and the AutoScaling VPC endpoint to the VPC.
- If Subnet 1 and Subnet 2 are private, then you must either deploy a NAT gateway in the VPC, or connect all of the following endpoints to the VPC:
    - EC2 VPC endpoint
    - AutoScaling VPC endpoint
    - S3 VPC endpoint
    - CloudFormation endpoint 

For more information about creating endpoints, see [AWS documentation](https://docs.aws.amazon.com/vpc/latest/userguide/vpce-interface.html#create-interface-endpoint).

You will also need to open the following ports in your VPC:

| Port | Description |
|------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `443` | Required for communicating with the dashboard and the MATLAB execution endpoint. |
| `8000`, `8002`, `9910` | Required for communication between the dashboard and workers within the VPC.  These ports do not need to be open to the internet. |
| `27000`, `50115` | Required for communication between the network license manager and the workers. |
| `22`, `3389` | Required for Remote Desktop functionality. This can be used for troubleshooting and debugging. |

### How to use an existing license server in an existing VPC?
If you want to use an exisiting license server, select `No` for the *Deploy License Server* step of the deployment.

To use an existing license server, you must add the security group of the server VMs to the security group of the license server.
1. In the AWS management console, select the stack that you deployed. 
1. In the stack detail for your stack, click **Resources**.
1. Look for the **Logical ID** named ```SecurityGroup``` and click the corresponding URL listed under **Physical ID**. This will take you to the security group details.
1. Click the **Inbound Rules** tab, then click **Edit Inbound Rules**.
1. Click **Add Rule**.
1. In the **Type** dropdown, select ```All TCP```.
1. In the **Source**, search and add the ```MatlabProductionServerCloudStackElb1Sg``` security group. 
1. Click **Save Rules**.

You must also add the private IP address of the license server to the `License Server` property in the **Settings** tab of the dashboard. 
Find the IP address of the license server from the AWS management console.
1. In the AWS management console, navigate to the EC2 dashboard. 
1. Select the license server instance.
1. In the instance details, copy the value of **Private IPs**. For example, 172.30.1.126
1. Add the private IP to the `License Server` property. For example, ` 27000@172.30.1.126`. 

## How do I launch a template that uses a previous MATLAB release?
| Release | Windows Server VM | Ubuntu VM |
|---------------|------------------------|-----------------|
| MATLAB R2020a | <a href="https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/create/review?templateURL=https://matlab-production-server-templates.s3.amazonaws.com/MatlabProductionServer_R2020a_New.yml" target="_blank">     <img src="https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png"/> </a> | <a href="https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/create/review?templateURL=https://matlab-production-server-templates.s3.amazonaws.com/MatlabProductionServer_R2020a_New.yml" target="_blank">     <img src="https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png"/> </a>|
| MATLAB R2020b | <a href="https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/create/review?templateURL=https://matlab-production-server-templates.s3.amazonaws.com/r2020b_mps_refarch/MatlabProductionServer_New.yml" target="_blank">     <img src="https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png"/> </a> | <a href="https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/create/review?templateURL=https://matlab-production-server-templates.s3.amazonaws.com/r2020b_mps_refarch/MatlabProductionServer_New.yml" target="_blank">     <img src="https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png"/> </a>|
| MATLAB R2021a | <a href="https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/create/review?templateURL=https://matlab-production-server-templates.s3.amazonaws.com/r2021a_mps_refarch/mps-aws-refarch-existing-vpc-cf.yml" target="_blank">     <img src="https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png"/> </a> | <a href="https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/create/review?templateURL=https://matlab-production-server-templates.s3.amazonaws.com/r2021a_mps_refarch/mps-aws-refarch-existing-vpc-cf.yml" target="_blank">     <img src="https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png"/> </a>|
| MATLAB R2021b | <a href="https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/create/review?templateURL=https://matlab-production-server-templates.s3.amazonaws.com/r2021b_mps_refarch/mps-aws-refarch-existing-vpc-cf.yml" target="_blank">     <img src="https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png"/> </a> | <a href="https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/create/review?templateURL=https://matlab-production-server-templates.s3.amazonaws.com/r2021b_mps_refarch/mps-aws-refarch-existing-vpc-cf.yml" target="_blank">     <img src="https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png"/> </a>|

For more information, see [previous releases](/releases).

## What versions of MATLAB Runtime are supported?

| Release | MATLAB Runtime | MATLAB Runtime | MATLAB Runtime | MATLAB Runtime | MATLAB Runtime | MATLAB Runtime | MATLAB Runtime | MATLAB Runtime | MATLAB Runtime | MATLAB Runtime | MATLAB Runtime |
|---------------|----------------|----------------|----------------|----------------|----------------|----------------|----------------|----------------|----------------|---------------|---------------|
| MATLAB R2019b |  R2017a | R2017b | R2018a | R2018b | R2019a |  R2019b |
| MATLAB R2020a |  |  R2017b | R2018a | R2018b | R2019a |  R2019b | R2020a |
| MATLAB R2020b |  |  |  R2018a | R2018b | R2019a |  R2019b | R2020a | R2020b |
| MATLAB R2021a |  |  |  |  R2018b | R2019a |  R2019b | R2020a | R2020b | R2021a |
| MATLAB R2021b |  |  |  |  | R2019a |  R2019b | R2020a | R2020b | R2021a | R2021b |
| MATLAB R2022a |  |  |  |  |  |  R2019b | R2020a | R2020b | R2021a | R2021b | R2022a |


## Why do requests to the server fail with errors such as “untrusted certificate” or “security exception”?  

These errors result from either CORS not being enabled on the server or due to the fact that the server endpoint uses a self-signed 
certificate. 

If you are making an AJAX request to the server, make sure that CORS is enabled in the server configuration. You can enable CORS by editing the property `CORS Allowed Origins` property in the **Settings** tab of the dashboard.

Also, some HTTP libraries and Javascript AJAX calls will reject a request originating from a server that uses a self-signed certificate. You may need to manually override the default security behavior of the client application. Or you can add a new 
HTTPS endpoint to the application gateway. For more information, see [Change SSL Certificate](https://www.mathworks.com/help/mps/server/manage-aws-resources-reference-architecture.html#mw_51d64616-777c-4e15-af40-ab3d8dcc418f). 

## How do I allow multiple IP address ranges access to the dashboard?
The deployment template allows you to enter only one range of IP addresses that can access the dashboard. After the deployment is complete, you can allow additional IP ranges access to the dashboard. For details, see 
[Update security group rules](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/working-with-security-groups.html#updating-security-group-rules) in the AWS documentation.

The name of the security group to update is ``` matlab-production-server-cloud-stack-elb-1-sg```. Edit inbound rules to add additional IP address ranges in CIDR format for the ```HTTPS``` type.


# Enhancement Request
Provide suggestions for additional features or capabilities using the following link: https://www.mathworks.com/cloud/enhancement-request.html

# Technical Support
If you require assistance or have a request for additional features or capabilities, please contact [MathWorks Technical Support](https://www.mathworks.com/support/contact_us.html).

