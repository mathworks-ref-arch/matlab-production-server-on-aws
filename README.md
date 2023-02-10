# MATLAB Production Server on Amazon Web Services

# Requirements

Before starting, you need the following:

-   A MATLAB® Production Server™ license that meets the following conditions:
    - Linked to a MathWorks Account.
    - Concurrent license type. To check your license type, see [MathWorks License Center](https://www.mathworks.com/licensecenter/).
    - Configured to use a network license manager on the virtual network. By default, the deployment of MATLAB Production Server includes a network license manager, but you can also use an existing license manager. In either case, activate or move the license after deployment. For details, see [Configure MATLAB Production Server License for Use on the Cloud](https://www.mathworks.com/help/mps/server/configure-matlab-production-server-license-for-use-on-the-cloud.html).
-   An Amazon Web Services™ (AWS) account.
-   A Key Pair for your AWS account in the US East (N. Virginia), US West (Oregon), EU (Ireland) or Asia Pacific (Tokyo) region. For more information, see [Amazon EC2 Key Pairs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html).

# Costs
You are responsible for the cost of the AWS services used when you create cloud resources using this guide. Resource settings, such as instance type, affect the cost of deployment. For cost estimates, see the pricing pages for each AWS service you will be using. Prices are subject to change.


# Introduction
Use this guide to automate running MATLAB Production Server
on the Amazon Web Services (AWS) Cloud using an AWS CloudFormation template.
The template is a JSON file that defines the resources required to deploy and manage MATLAB Production
Server on AWS. Once deployed, you can manage the server using the
MATLAB Production Server dashboard&mdash;a web-based interface to
configure and manage server instances on the cloud. For more information, see [Manage MATLAB Production Server Using the Dashboard](https://www.mathworks.com/help/mps/server/manage-matlab-production-server-using-the-dashboard.html).
For information about the architecture of this solution, see [Architecture and Resources](#architecture-and-resources). For information about AWS templates, see [Working with AWS CloudFormation Templates](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-guide.html). <br>

The default MATLAB Production Server deployment template uses the Network License Manager for MATLAB reference architecture to manage MATLAB Production Server licenses. The template for using an exisitng VPC for the deployment provides an option to either deploy the Network License Manager or use your own license server. For more information about the Network License Manager for MATLAB reference architecture, see [Network License Manager for MATLAB on Amazon Web Services](https://github.com/mathworks-ref-arch/license-manager-for-matlab-on-aws).

# Prepare Your AWS Account
1. If you do not have an AWS account, create one at https://aws.amazon.com by following the on-screen instructions.
2. In the top navigation, select the region where you want to deploy MATLAB Production Server. You must select one of these supported regions:  <ul><li>**US-East (N. Virginia)**</li><li>**US-West (Oregon)**</li><li>**Europe (Ireland)**</li><li>**Asia Pacific (Tokyo)**</li></ul>
3. Create a [key pair](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html) in that region.  The key pair is necessary because it is the only way to connect to the instance as an administrator.
4. If necessary, [request a service limit increase](https://console.aws.amazon.com/support/home#/case/create?issueType=service-limit-increase) for the Amazon EC2 instance type or VPCs.  You might need to do this if you already have existing deployments that use that instance type or you think you might exceed the [default limit](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-resource-limits.html) with this deployment.

# Deploy Reference Architecture for Your Release
To deploy the reference architecture, select your MATLAB Production Server release from the table and follow the instructions. Verify that you are using one of the supported MATLAB Runtime versions.
| Instructions | Supported MATLAB Runtime Versions
| ------------ | ---------------------------------
| [R2023a](releases/R2023a/README.md) | R2020b, R2021a, R2021b, R2022a, R2022b, R2023a
| [R2022b](releases/R2022b/README.md) | R2020a, R2020b, R2021a, R2021b, R2022a, R2022b
| [R2022a](releases/R2022a/README.md) | R2019b, R2020a, R2020b, R2021a, R2021b, R2022a
| [R2021b](releases/R2021b/README.md) | R2019a, R2019b, R2020a, R2020b, R2021a, R2021b
| [R2021a](releases/R2021a/README.md) | R2018b, R2019a, R2019b, R2020a, R2020b, R2021a
| [R2020b](releases/R2020b/README.md) | R2018a, R2018b, R2019a, R2019b, R2020a, R2020b


# Architecture and Resources
Deploying this reference architecture creates several resources in your
resource group.


![Architecture](/releases/R2023a/images/mps_ref_arch_aws_diagram.png?raw=true)

*Architecture on AWS*

### Resources

| Resource Type                                                              | Number of Resources | Description                                                                                                                                                                                                                                                                                                                        |
|----------------------------------------------------------------------------|---------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| AWS EC2 Instance                                                           | 2                   | This resource consists of two virtual machines (VMs):<ul><li>A VM that hosts the MATLAB Production Server Dashboard. Use the dashboard to: <ul><li>Get the HTTPS endpoint to make requests</li><li> Upload applications (CTF files) to the server</li><li> Manage server configurations</li><li> Manage the HTTPS certificate</li></ul><p>For more information, see [Manage MATLAB Production Server Using the Dashboard](https://www.mathworks.com/help/mps/server/manage-matlab-production-server-using-the-dashboard.html).</li><li>A VM that hosts the Network License Manager for MATLAB. For more information, see [Network License Manager for MATLAB](https://github.com/mathworks-ref-arch/license-manager-for-matlab-on-aws).</li></ul>   |
| Auto Scaling Group                                                         | 1                   | Manages the number of identical VMs to be deployed. Each VM runs an instance of MATLAB Production Server which in turn runs multiple MATLAB workers.                                                                                                                                                                               |
| Load Balancer                                                              | 2                   | Provides routing and load balancing services to MATLAB Production Server instances. The MATLAB Production Server Dashboard retrieves the HTTPS endpoint for making requests to the server from the load balancer resource.<p></p>                                                                                           |
| S3 Bucket                                                                  | 1                  | S3 storage bucket created during the creation of the stack. This resource stores the applications deployed to the reference architecture.                                                                                                                                                                                                  |
| Virtual Private Cluster (VPC)                                              | 1                   | Enables resources to communicate with each other.                                           |
| Redis ElastiCache | 1 | Enables caching of data between calls to MATLAB code running on a server instance. |
| CloudWatch | 1 | Enables viewing of logs. |

# FAQ
## How do I use an existing VPC to deploy MATLAB Production Server?

Use the template for your release to launch the reference architecture within an existing VPC and subnet. This templates support both Windows and Linux operating systems. They provide an option to deploy the Network License Manager for MATLAB to manage MATLAB Production Server licenses. The license manager must be in the same VPC and security group as MATLAB Production Server.

| Release | Template | Supported Windows OS | Supported Linux OS 
|---------|----------| ------- | -----
| [R2023a](/releases/R2023a) | <a  href ="https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/create/review?templateURL=https://matlab-production-server-templates.s3.amazonaws.com/r2023a_mps_refarch/mps-aws-refarch-existing-vpc-cf.yml"  target ="_blank" >      <img  src ="https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png" />  </a> | Windows Server 2019 | Ubuntu 22.04 VM
| [R2022b](/releases/R2022b) | <a href="https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/create/review?templateURL=https://matlab-production-server-templates.s3.amazonaws.com/r2022b_mps_refarch/mps-aws-refarch-new-vpc-cf.yml" target="_blank">     <img src="https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png"/> </a> |Windows Server 2019 | Ubuntu 22.04 VM
| [R2022a](/releases/R2022a) | <a href="https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/create/review?templateURL=https://matlab-production-server-templates.s3.amazonaws.com/r2022a_mps_refarch/mps-aws-refarch-new-vpc-cf.yml" target="_blank">     <img src="https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png"/> </a> |Windows Server 2019 | Ubuntu 18.04 VM
| [R2021b](/releases/R2021b) | <a href="https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/create/review?templateURL=https://matlab-production-server-templates.s3.amazonaws.com/r2021b_mps_refarch/mps-aws-refarch-new-vpc-cf.yml" target="_blank">     <img src="https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png"/> </a> |Windows Server 2019 | Ubuntu 18.04 VM
| [R2021a](/releases/R2021a) | <a href="https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/create/review?templateURL=https://matlab-production-server-templates.s3.amazonaws.com/r2021a_mps_refarch/MatlabProductionServer_R2021a_New.yml" target="_blank">     <img src="https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png"/> </a> |Windows Server 2019 | Ubuntu 18.04 VM
| [R2020b](/releases/R2020b) | <a href="https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/create/review?templateURL=https://matlab-production-server-templates.s3.amazonaws.com/r2020b_mps_refarch/MatlabProductionServer_New.yml" target="_blank">     <img src="https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png"/> </a> |Windows Server 2019 | Ubuntu 18.04 VM


In addition to the parameters specified in the **Configure Stack** section of your release-specific deployment instructions, to use your existing VPC, specify these template parameters:

| Parameter | Value |
|---------- | ----- |
| Existing VPC ID | ID of your existing VPC. |
| IP address range of existing VPC | IP address range from the existing VPC. To find the IP address range: <ol><li>Log in to the AWS Console.</li><li>Navigate to the VPC dashboard and select your VPC.</li><li>Click the **CIDR blocks** tab.</li><li>Get the IP address range listed under **IPv4 CIDR Blocks**.</li></ol> |
| Subnet 1 ID | ID of an existing subnet that will host the dashboard and other resources. |
| Subnet 2 ID | ID of an existing subnet that will host the application load balancer. |

- If Subnet 1 and Subnet 2 are public, then you must connect the EC2 VPC endpoint and the AutoScaling VPC endpoint to the VPC.
- If Subnet 1 and Subnet 2 are private, then you must either deploy a NAT gateway in the VPC, or connect all of these endpoints to the VPC:
    - EC2 VPC endpoint
    - AutoScaling VPC endpoint
    - S3 VPC endpoint
    - CloudFormation endpoint 

For more information about creating endpoints, see the [AWS documentation](https://docs.aws.amazon.com/vpc/latest/userguide/vpce-interface.html#create-interface-endpoint).

You also need to open these ports in your VPC:

| Port | Description |
|------|------------ |
| `443` | Required for communicating with the dashboard and the MATLAB execution endpoint. |
| `8000`, `8002`, `9910` | Required for communication between the dashboard and workers within the VPC.  These ports do not need to be open to the Internet. |
| `27000`, `50115` | Required for communication between the Network License Manager and the workers. |
| `22`, `3389` | Required for Remote Desktop functionality. This can be used for troubleshooting and debugging. |

### How to use an existing license server in an existing VPC?
To use an existing license server, select `No` for the *Deploy License Server* step of the deployment. You must also add the security group of the server VMs to the security group of the license server.
1. In the AWS management console, select the stack that you deployed. 
1. In the stack details page, click **Resources**.
1. In the **Logical ID** named ```SecurityGroup```, click the corresponding URL listed under **Physical ID** to open the security group details.
1. Click the **Inbound Rules** tab, and then click **Edit Inbound Rules**.
1. Click **Add Rule**.
1. In the **Type** dropdown, select ```All TCP```.
1. Under **Source**, search and add the ```MatlabProductionServerCloudStackElb1Sg``` security group. 
1. Click **Save Rules**.

You must also add the private IP address of the license server to the `License Server` property in the **Settings** tab of the dashboard. 
You can find the IP address of the license server from the AWS management console.
1. In the AWS management console, navigate to the EC2 dashboard. 
1. Select the license server instance.
1. In the instance details, copy the value of **Private IPs**. For example: 172.30.1.126
1. Add the private IP to the `License Server` property. For example: ` 27000@172.30.1.126` 


## Why do requests to the server fail with errors such as “untrusted certificate” or “security exception”?  
These errors occur either when CORS is not enabled on the server or when the server endpoint uses a self-signed certificate. 

If you are making an AJAX request to the server, make sure that CORS is enabled in the server configuration. You can enable CORS by editing the property `CORS Allowed Origins` property in the **Settings** tab of the dashboard.

Also, some HTTP libraries and JavaScript AJAX calls will reject a request originating from a server that uses a self-signed certificate. You may need to manually override the default security behavior of the client application. Alternatively, you can add a new HTTPS endpoint to the application gateway. For more information, see [Change SSL Certificate](https://www.mathworks.com/help/mps/server/manage-aws-resources-reference-architecture.html#mw_51d64616-777c-4e15-af40-ab3d8dcc418f). 


## How do I allow multiple IP address ranges access to the dashboard?
The deployment template allows you to enter only one range of IP addresses that can access the dashboard. After the deployment is complete, you can allow additional IP ranges access to the dashboard. For details, see 
[Update security group rules](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/working-with-security-groups.html#updating-security-group-rules) in the AWS documentation.

The name of the security group to update is ``` matlab-production-server-cloud-stack-elb-1-sg```. Edit inbound rules to add additional IP address ranges in CIDR format for the ```HTTPS``` type.

# Enhancement Request
Provide suggestions for additional features or capabilities using the following link: https://www.mathworks.com/solutions/cloud.html

# Technical Support
If you require assistance or have a request for additional features or capabilities, please contact [MathWorks Technical Support](https://www.mathworks.com/support/contact_us.html).

