# MATLAB Production Server on Amazon Web Services

# Requirements

Before starting, you need the following:

-   A MATLAB® Production Server™ license. For more information, see [Configure MATLAB Production Server Licensing on the Cloud](https://www.mathworks.com/help/licensingoncloud/matlab-production-server-on-the-cloud.html). In order to configure the license in the cloud, you need the MAC address of the license server on the cloud. For more information, see [Get License Server MAC Address](#get-license-server-mac-address).
-   An Amazon Web Services™ (AWS) account.
-   A Key Pair for your AWS account in the US East (N. Virginia), EU (Ireland) or Asia Pacific (Tokyo) region. For more information, see [Amazon EC2 Key Pairs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html).

# Costs
You are responsible for the cost of the AWS services used when you create cloud resources using this guide. Resource settings, such as instance type, will affect the cost of deployment. For cost estimates, see the pricing pages for each AWS service you will be using. Prices are subject to change.


# Introduction
The following guide will help you automate the process of running MATLAB
Production Server on the Amazon Web Services (AWS) Cloud. The automation is
accomplished using an AWS CloudFormation template. The template is a JSON
file that defines the resources needed to deploy and manage MATLAB Production
Server on AWS. Once deployed, you can manage the server using the
MATLAB Production Server cloud console&mdash;a web-based interface to
configure and manage server instances on the cloud. For more information, see [MATLAB Production Server Cloud Console User's Guide](/releases/R2020b/doc/cloudConsoleDoc.md#matlab-production-server-cloud-console-users-guide).
For information about the architecture of this solution, see [Architecture and Resources](#architecture-and-resources). For information about AWS templates, see [AWS CloudFormation Templates](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-guide.html). <br>

The default MATLAB Production Server deployment template uses the Network License Manager for MATLAB reference architecture to manage MATLAB Production Server licenses. The template for using an exisitng VPC for the deployment provides an option to either deploy the Network License Manager or use your own license server. For more information about the Network License Manager for MATLAB reference architecture, see [Network License Manager for MATLAB](https://github.com/mathworks-ref-arch/license-manager-for-matlab-on-azure).

# Prepare Your AWS Account
1. If you do not have an AWS account, create one at https://aws.amazon.com by following the on-screen instructions.
2. Use the regions selector in the navigation bar to choose **US-EAST (N. Virginia)**, **EU (Ireland)** or **Asia Pacific (Tokyo)**, as the region where you want to deploy MATLAB Production Server.
3. Create a [key pair](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html) in that region.  The key pair is necessary as it is the only way to connect to the instance as an administrator.
4. If necessary, [request a service limit increase](https://console.aws.amazon.com/support/home#/case/create?issueType=service-limit-increase&limitType=service-code-) for the Amazon EC2 instance type or VPCs.  You might need to do this if you already have existing deployments that use that instance type or you think you might exceed the [default limit](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-resource-limits.html) with this deployment.

# Deployment Steps

## Step 1. Launch the Template
Click the **Launch Stack** button to deploy resources on AWS. This will open the AWS Management Console in your web browser.

| Release | Windows Server 2019 or Ubuntu 18.04 VM |
|---------------|------------------------|
| MATLAB R2020b | <a href="https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/create/review?templateURL=https://matlab-production-server-templates.s3.amazonaws.com/MatlabProductionServer_R2020a_New.yml" target="_blank">     <img src="https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png"/> </a> |

For other releases, see [How do I launch a template that uses a previous MATLAB release?](#how-do-i-launch-a-template-that-uses-a-previous-matlab-release)
<p><strong>Note:</strong> Creating a stack on AWS can take at least 20 minutes.</p>

## Step 2. Configure the Stack
1. Provide values for parameters in the **Create Stack** page:

    | Parameter Name                         | Value                                                                                                                                                                                                                                                                                                                                                 |
    |----------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **Stack name**                         | Choose a name for the stack. This will be shown in the AWS console. <p><em>*Example*</em>: Boston</p>                                                                                                                                                                                                                                                                       |
    | |**Remote access**|
    | **Name of Existing Key Pair**          | Choose the name of an existing EC2 Key Pair to allow access to all the VMs in the stack. For information about creating an Amazon EC2 key pair, see [Amazon EC2 Key Pairs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html#having-ec2-create-your-key-pair). <p><em>*Example*</em>: boston-keypair</p>                                                                                   |
    | **Allow connections from IP Address** | This is the IP address range that will be allowed to connect to the cloud console that manages the server. The format for this field is IP Address/Mask. <p><em>Example</em>: </p>10.0.0.1/32 <ul><li>This is the public IP address which can be found by searching for "what is my ip address" on the web. The mask determines the number of IP addresses to include.</li><li>A mask of 32 is a single IP address.</li><li>Use a [CIDR calculator](https://www.ipaddressguide.com/cidr) if you need a range of more than one IP addresses.</li><li>You may need to contact your IT administrator to determine which address is appropriate.</li></ul></p> |
    | **Make Solution Available over Internet** | Choose 'Yes' if you want your solution to use public IP addresses. |
    ||**Server**|
    | **Number of Server VMs**             | Choose the number of AWS instances to start for the server. <p><em>*Example*</em>: 6</p><p>If you have a standard 24 worker MATLAB Production Server license and select `m5.xlarge` (4 cores) as the **Number of server VMs**, you need 6 worker nodes to fully utilize the workers in your license.</p><p>You can always under provision the number instances, in which case you may end up using fewer workers than you are licensed for.</p>|
    | **Server VM Type** | Choose the AWS instance type to use for the server instances. All AWS instance types are supported. For more information, see [Amazon EC2 Instance Types](https://aws.amazon.com/ec2/instance-types/). <p><em>*Example*</em>: m5.xlarge</p> |
    | **Server VM Operating System** | Choose between Windows (Windows Server) and Linux(Ubuntu) to use for the server instances.  |
    | **ARN of SSL Certificate**             | Provide the Amazon Resource Name (ARN) of an existing certificate in the AWS Certificate Manager to enable secure HTTPS communication to the HTTPS server endpoint. This field is optional and may be left blank to use HTTP communication instead. For more information, see [Create Self-signed Certificate](/README.md#create-self-signed-certificate) and [Upload Self-signed Certificate to AWS Certificate Manager](/README.md#upload-self-signed-certificate-to-aws-certificate-manager).<p><em>*Example*</em>: 123456789012</p>                                                                                        |
    | **Create Redis ElastiCache** | Choose whether you want to create a Redis ElastiCache service. Creating this service will allow you to use the persistence functionality of the server. Persistence provides a mechanism to cache data between calls to MATLAB code running on a server instance. |    
    ||**Network License Manager for MATLAB**|
    | **Password** | Enter the password to use for logging in to the Network License Manager for MATLAB dashboard. |
    | **Confirm Password** | Reenter the password to log in to the Network License Manager for MATLAB dashboard. |

    >**Note**: Make sure you select US East (N.Virginia), EU (Ireland) or Asia Pacific (Tokyo) as your region from the navigation panel on top. Currently, US East, EU (Ireland), and Asia Pacific (Tokyo) are the only supported regions.

2. Tick the box to accept that the template uses IAM roles. For more information about IAM, see [IAM FAQ](https://aws.amazon.com/iam/faqs). 
  
3. Click the **Create** button. The CloudFormation service will start creating the resources for the stack.

## Step 3. Upload the License File
1. Clicking **Create** takes you to the *Stack Detail* page for your stack. Wait for the Status to reach **CREATE\_COMPLETE**. This can take up to 20 minutes.
1. In the Stack Detail for your stack, click **Outputs**.
1. Look for the key named `MatlabProductionServerLicenseServer` and click the corresponding URL listed under value. This will take you to Network License Manager for MATLAB dashboard log in page.
1. The user name for the Network License Manager for MATLAB dashboard is **manager**. For the password, enter the password that you entered in the **Network License Manager for MATLAB** section while creating the stack in [Step 2](#step-2-configure-the-stack).
1. Follow the instructions to upload your MATLAB Production Server license.

## Step 4. Get the Password to the Cloud Console
1. In the AWS management console, select the stack that you deployed. 
1. In the Stack Detail for your stack, expand the **Outputs** section.
1. Look for the key named `MatlabProductionServerInstance` and click the corresponding URL listed under value. This will take you to the server instance (`matlab-production-server-vm`) page. 
1. Click the **Connect** button at the top.
1. In the *Connect To Your Instance* dialog box, choose **Get Password**.
1. Click **Choose File** to navigate and select the private key file (`.pem` file) for the key pair that you used while creating the stack in [Step 2](#step-2-configure-the-stack).
1. Click **Decrypt Password**. The console displays the password for the instance in the *Connect To Your Instance* dialog box, replacing the link to *Get Password* shown previously with the actual password.
1. Copy the password to the clipboard.



## Step 5. Connect to the Cloud Console
> **Note**: The Internet Explorer web browser is not supported for interacting with the cloud console.

1. In the Stack Detail for your stack, expand the **Outputs** section. 
1. Look for the key named `MatlabProductionServerVM` and click the corresponding URL listed under value. This is the HTTPS endpoint to the MATLAB Production Server Cloud Console. 



## Step 6. Log in to the Cloud Console
The username to the cloud console is **Administrator**. For the password, paste the password you copied to the clipboard by completing [Step 4](#step-4-get-password-to-the-cloud-console). The cloud console provides a web-based interface to configure and manage server instances on the cloud. For more information on how to use the cloud console, see [MATLAB Production Server Cloud Console User  Guide](/releases/R2020b/doc/cloudConsoleDoc.md#matlab-production-server-cloud-console-users-guide).  

![MATLAB Production Server Cloud Console](/releases/R2020a/images/cloudConsoleLogin.png?raw=true)

You are now ready to use MATLAB Production Server on AWS. 

>**Accept Terms and Conditions**: Access to and use of the MATLAB Production Server cloud console is governed by license terms in the file `C:\MathWorks\Cloud Console License.txt` (Linux: `/MathWorks/Cloud Console License.txt`) available on the `servermachine` in the resource group for this solution. 


>**Note**: The cloud console uses a self-signed certificate which you can change. For information on changing the self-signed certificates, see [Change Self-signed Certificates](/releases/R2020b/doc/cloudConsoleDoc.md#change-self-signed-certificates).

To run applications on MATLAB Production Server, you need to create applications using MATLAB Compiler SDK. For more information, see [Deployable Archive Creation](https://www.mathworks.com/help/mps/deployable-archive-creation.html) in the MATLAB Production Server product documentation.

# Additional Information

## Delete Your Stack

Once you have finished using your stack, it is recommended that you delete all resources to avoid incurring further cost. 

If you are using an existing license server, and have added the security group of the server VMs to the security group of the license server, you must delete the inbound rules before you delete the stack.
1. In the AWS management console, select the stack that you deployed. 
1. In the stack detail for your stack, click **Resources**.
1. Look for the **Logical ID** named `SecurityGroup` and click the corresponding URL listed under **Physical ID**. This will take you to the security group details.
1. Click the **Inbound Rules** tab, then click **Edit Inbound Rules**.
1. Click **Delete Rule** for the rules that have the tag `matlab-production-server-cloud-stack-elb-1-sg` and `
matlab-production-server-cloud-stack-elb-2-sg` as their **Source**. 
1. Click **Save Rules**.

To delete the stack, do the following:
1. Log in to the AWS Console.
3. Go to the AWS Cloud Formation page and select the stack that you created.
3. Click the **Actions** button and click **Delete Stack** from the menu that appears.

If you do not want to delete the entire deployment but want to minimize the cost, you can bring the number of instances in the Auto Scaling Group down to 0 and then scale it back up when the need arises.

## Security
When you run MATLAB Production Server on the cloud you get two HTTP/HTTPS endpoints. 

1. An HTTP/HTTPS endpoint to the application gateway/load balancer that connects the server instances. This endpoint is displayed in the home page of the cloud console and is used to make requests to the server. Whether the endpoint is HTTP or HTTPS depends on whether you provided a certificate during the creation of the stack.

1. An HTTPS endpoint to the cloud console. This endpoint is used to connect to the cloud console. The cloud console comes with a self-signed certificate.  

For information on changing the self-signed certificates, see [Change Self-signed Certificates](/releases/R2020b/doc/cloudConsoleDoc.md#change-self-signed-certificates). 

### Create Self-signed Certificate
For information on creating a self-signed certificate, see [Create and Sign an X509 Certificate](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/configuring-https-ssl.html).

### Upload Self-signed Certificate to AWS Certificate Manager

1. Open the AWS Certificate Manager.
2. Click the button at the top of the page to **Import a certificate**.
3. Copy the contents of the `.crt` file containing the certificate into the field labeled **Certificate body**.
4. Copy the contents of the `.pem` file containing the private key into the field labeled **Certificate private key**.
5. Leave the field labeled **Certificate chain** blank.
6. Click the button labeled **Review and import**.
7. Review the settings and click the **Import** button.
8. Copy the value of the Amazon Resource Name (ARN) field from the **Details** section of the certificate.

The ARN value that you copied should be pasted into the **ARN of SSL Certificate** parameter of the template in [Step 2](#step-2-configure-the-stack).

## View Logs
Logs are available in Amazon CloudWatch. 
1. In the AWS management console, select the stack that you deployed. 
1. In the Stack Detail for your stack, expand the **Outputs** section.
1. To view logs related to the cloud console and the MATLAB Production Server workers, look for the key named `MatlabProductionCloudConsoleWorkerLogGroup`, and click the corresponding URL listed under value. These logs contain information about user logins, deployed archives (CTF files), certificate changes, and user interface actions.
1. To view logs related to the server instance, look for the key named `MatlabProductionServerLogGroup`, and click the corresponding URL listed under value.

## Upload Multiple Applications
You can upload multiple deployed archives (CTF files) using the Amazon S3 management console. 
1. In the AWS management console, select the stack that you deployed. 
1. In the Stack Detail for your stack, expand the **Outputs** section.
1. Look for the key named `MATLABProductionServerApplicationsBucket`, and click the corresponding URL listed under value. Doing so takes you to the S3 console.
1. In the S3 console, click **CTF**.
1. Click **Upload** > **Add Files** to select and upload applications.

## Get License Server MAC Address
The Network License Manager for MATLAB reference architecture manages the MATLAB Production Server license file. The deployment templates for the MATLAB Production Server reference architecture provide an option to deploy the license manager. You can also use an existing license manager that is located in the same VPC and the security group of the MATLAB Production Server instances. For more information about the Network License Manager for MATLAB reference architecture, see [Network License Manager for MATLAB](https://github.com/mathworks-ref-arch/license-manager-for-matlab-on-azure).

>**NOTE**: For a new license manager deployed with MATLAB Production Server, the license manager MAC address is available only after the deployment to the Cloud is complete. For information on deploying the solution, see [Deployment Steps](/README.md#deployment-steps).

To get the MAC address of the license manager: 
1. Log in to the Network License Manager for MATLAB dashboard. For a license manager deployed with the MATLAB Production Server deployment, use the following credentials:<br>
Username: **manager**<br>
Password: Enter the password that you entered during the deployment process.
1. Click **Administration** > **License**.
1. Copy the license server MAC address displayed at the top.
# Architecture and Resources
Deploying this reference architecture will create several resources in your
resource group.


![Architecture](/releases/R2020a/images/Architecture.png?raw=true)

*Architecture on AWS*

### Resources

| Resource Type                                                              | Number of Resources | Description                                                                                                                                                                                                                                                                                                                        |
|----------------------------------------------------------------------------|---------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| AWS EC2 Instance                                                           | 2                   | <ol><li>Virtual machine (VM) that hosts the MATLAB Production Server Cloud Console. Use the cloud console to: <ul><li>Get HTTP/HTTPS endpoint to make requests</li><li> Upload applications (CTF files) to the server</li><li> Manage server configurations</li><li> Manage the HTTPS certificate</li></ul><p>For more information, see [MATLAB Production Server Cloud Console User's Guide](/releases/R2020b/doc/cloudConsoleDoc.md#matlab-production-server-cloud-console-users-guide).</li><li>VM that hosts the Network License Manager for MATLAB. For more information, see [Network License Manager for MATLAB](https://github.com/mathworks-ref-arch/license-manager-for-matlab-on-aws).</li></ol>   |
| Auto Scaling Group                                                         | 1                   | Manages the number of identical VMs to be deployed. Each VM runs an instance of MATLAB Production Server which in turn runs multiple MATLAB workers.                                                                                                                                                                               |
| Load Balancer                                                              | 1                   | Provides routing and load balancing service to MATLAB Production Server instances. The MATLAB Production Server cloud console retrieves the HTTP/HTTPS endpoint for making requests to the server from the load balancer resource.<p>**NOTE**: Provides HTTPS endpoint to the server for making requests.</p>                                                                                           |
| S3 Bucket                                                                  | 1                  | S3 storage bucket created during the creation of the stack where applications deployed to the reference architecture are stored.                                                                                                                                                                                                  |
| Virtual Private Cluster (VPC)                                              | 1                   | Enables resources to communicate with each other.                                           |
| Redis ElastiCache | 1 | Enables caching of data between calls to MATLAB code running on a server instance. |
| CloudWatch | 1 | Enables viewing of logs. |

# FAQ
## How do I use an existing VPC to deploy MATLAB Production Server?

Use the following templates to launch the reference architecture within an existing VPC and subnet. The templates provide an option to deploy the Network License Manager for MATLAB to manage MATLAB Production Server licenses. The license manager must be in the same VPC and security group as MATLAB Production Server.

| Release | Windows Server 2019 or Ubuntu 18.04 VM |
|---------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| R2020b | <a  href ="https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/create/review?templateURL=https://matlab-production-server-templates.s3.amazonaws.com/MatlabProductionServer_R2020a_Existing.yml"  target ="_blank" >      <img  src ="https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png" />  </a> |

In addition to the parameters specified in the section [Configure the Stack](#step-2-configure-the-stack), you will need to specify the following parameters in the template to use your existing VPC.

| Parameter  | Value |
|----------------------------------|--------------------------------------------------------------------------------|
| Existing VPC ID | ID of your existing VPC. |
| IP address range of existing VPC | IP address range from the existing VPC. To find the IP address range: <ol><li>Log in to the AWS Console.</li><li>Navigate to the VPC dashboard and select your VPC.</li><li>Click the **CIDR blocks** tab.</li><li>The **IPv4 CIDR Blocks** gives the IP address range.</li></ol> |
| Subnet 1 ID | ID of an existing subnet that will host the cloud console and other resources. |
| Subnet 2 ID | ID of an existing subnet that will host the application gateway. |

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
| `443` | Required for communicating with the cloud console. |
| `8000`, `8002`, `9910` | Required for communication between the cloud console and workers within the VPC.  These ports do not need to be open to the internet. |
| `27000`, `50115` | Required for communication between the network license manager and the workers. |
| `3389` | Required for Remote Desktop functionality. This can be used for troubleshooting and debugging. |

### How to use an existing license server in an existing VPC?
If you want to use an exisiting license server, select `No` for the *Deploy License Server* step of the deployment.

To use an existing license server, you must add the security group of the server VMs to the security group of the license server.
1. In the AWS management console, select the stack that you deployed. 
1. In the stack detail for your stack, click **Resources**.
1. Look for the **Logical ID** named ```SecurityGroup``` and click the corresponding URL listed under **Physical ID**. This will take you to the security group details.
1. Click the **Inbound Rules** tab, then click **Edit Inbound Rules**.
1. Click **Add Rule**.
1. In the **Type** dropdown, select ```All TCP```.
1. In the **Source**, search and add the ```matlab-production-server-cloud-stack-elb-1-sg``` and ```matlab-production-server-cloud-stack-elb-2-sg``` security groups. 
1. Click **Save Rules**.

You must also add the private IP address of the license server to the `--license` property in the server configuration file. 
Find the IP address of the license server from the AWS management console.
1. In the AWS management console, navigate to the EC2 dashboard. 
1. Select the license server instance.
1. In the instance details, copy the value of **Private IPs**. For example, 172.30.1.126
1. Add the private IP to the `--license` property. For example, `--license 27000@172.30.1.126`. For more information about editing the server configuration, see [Edit the Server Configuration](/releases/R2020b/doc/cloudConsoleDoc.md#edit-the-server-configuration). 

## How do I launch a template that uses a previous MATLAB release?
| Release | Windows Server 2016 VM | Ubuntu 16.04 VM |
|---------------|------------------------|-----------------|
| MATLAB R2019a | <a href="https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/create/review?templateURL=https://s3.amazonaws.com/matlab-production-server-templates/MatlabProductionServer_Windows_R2019a.template" target="_blank">     <img src="https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png"/> </a> | <a href="https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/create/review?templateURL=https://s3.amazonaws.com/matlab-production-server-templates/MatlabProductionServer_Linux_R2019a.template" target="_blank">     <img src="https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png"/> </a>|
| MATLAB R2019b | <a href="https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/create/review?templateURL=https://s3.amazonaws.com/matlab-production-server-templates/MatlabProductionServer_Windows_R2019a.template" target="_blank">     <img src="https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png"/> </a> | <a href="https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/create/review?templateURL=https://s3.amazonaws.com/matlab-production-server-templates/MatlabProductionServer_Linux_R2019a.template" target="_blank">     <img src="https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png"/> </a>|
| MATLAB R2020a | <a href="https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/create/review?templateURL=https://s3.amazonaws.com/matlab-production-server-templates/MatlabProductionServer_Windows_R2018b.template" target="_blank">     <img src="https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png"/> </a> | <a href="https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/create/review?templateURL=https://s3.amazonaws.com/matlab-production-server-templates/MatlabProductionServer_Linux_R2018b.template" target="_blank">     <img src="https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png"/> </a>|

For more information, see [previous releases](/releases).

## What versions of MATLAB Runtime are supported?

| Release | MATLAB Runtime | MATLAB Runtime | MATLAB Runtime | MATLAB Runtime | MATLAB Runtime | MATLAB Runtime | MATLAB Runtime | MATLAB Runtime | MATLAB Runtime |
|---------------|----------------|----------------|----------------|----------------|----------------|----------------|----------------|----------------|----------------|
| MATLAB R2019a |  R2016b | R2017a | R2017b | R2018a | R2018b | R2019a |  |
| MATLAB R2019b |  |  R2017a | R2017b | R2018a | R2018b | R2019a |  R2019b |
| MATLAB R2020a |  |  |  R2017b | R2018a | R2018b | R2019a |  R2019b | R2020a |
| MATLAB R2020b |  |  |  | R2018a | R2018b | R2019a |  R2019b | R2020a | R2020b |


## Why do requests to the server fail with errors such as “untrusted certificate” or “security exception”?  

These errors result from either CORS not being enabled on the server or due to the fact that the server endpoint uses a self-signed 
certificate. 

If you are making an AJAX request to the server, make sure that CORS is enabled in the server configuration. You can enable CORS by editing the property `--cors-allowed-origins` in the config file. For more information, see [Edit the Server Configuration](/releases/R2020b/doc/cloudConsoleDoc.md#edit-the-server-configuration).

Also, some HTTP libraries and Javascript AJAX calls will reject a request originating from a server that uses a self-signed certificate. You may need to manually override the default security behavior of the client application. Or you can add a new 
HTTP/HTTPS endpoint to the application gateway. For more information, see [Create a Listener](/releases/R2020b/doc/cloudConsoleDoc.md#create-a-listener). 

# Enhancement Request
Provide suggestions for additional features or capabilities using the following link: https://www.mathworks.com/cloud/enhancement-request.html

# Technical Support
If you require assistance or have a request for additional features or capabilities, please contact [MathWorks Technical Support](https://www.mathworks.com/support/contact_us.html).

