# MATLAB Production Server on Amazon Web Services - R2023b

# Deployment Steps
Follow these steps to deploy the R2023b MATLAB Production Server reference architecture on AWS. To deploy reference architectures for other releases, see [Deploy Reference Architecture for Your Release](/README.md#deploy-reference-architecture-for-your-release). 
## Step 1. Launch Template
Before launching the template, make sure that you have selected one of these supported AWS regions from the top navigation:<ul><li>**US-East (N. Virginia)**</li><li>**US-West (Oregon)**</li><li>**Europe (Ireland)**</li><li>**Asia Pacific (Tokyo)**</li></ul>

Then, click the appropriate **Launch Stack** button to launch the stack configuration template for deploying resources onto your AWS account. You can deploy resources onto either a new or existing VPC.

| Release | New VPC | Existing VPC |
|---------|---------| ------------ |
| R2023b | <a href="https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/create/review?templateURL=https://matlab-production-server-templates.s3.amazonaws.com/r2023b_mps_refarch/mps-aws-refarch-new-vpc-cf.yml" target="_blank">     <img src="https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png"/> </a> | <a  href ="https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/create/review?templateURL=https://matlab-production-server-templates.s3.amazonaws.com/r2023b_mps_refarch/mps-aws-refarch-existing-vpc-cf.yml"  target ="_blank" >      <img  src ="https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png" /> </a> |

The AWS Management Console opens in your web browser.

## Step 2. Configure Stack
On the **Create Stack** page, specify these parameters:

| Parameter Name | Value |
|--------------- | ----- |
| **Stack name**                         | Choose a name for the stack. After the deployment finishes, this name is displayed in the AWS console. <p><em>*Example*</em>: Boston</p>  |
||**Server**|
| **Number of Server VMs**             | Choose the number of AWS instances to start for the server. <p><em>*Example*</em>: 6</p><p>For example, if you have a 24-worker MATLAB Production Server license and select `m6.xlarge` (4 cores) as the **Number of server VMs**, you need 6 worker nodes to fully use the workers in your license.</p><p>You can always underprovision the number instances, in which case you may end up using fewer workers than you are licensed for.</p>|
| **Server VM Type** | Choose the AWS instance type to use for the server instances. All AWS instance types are supported. For more information, see [Amazon EC2 Instance Types](https://aws.amazon.com/ec2/instance-types/). <p><em>*Example*</em>: m6.xlarge</p> |
| **Server VM Operating System** | Choose between Windows (Windows Server 2022) and Linux (Ubuntu 22) to use for the server instances.  |
| **Create Redis ElastiCache** | Choose whether you want to create a Redis ElastiCache service. Creating this service enables you to use the persistence functionality of the server. Persistence provides a mechanism to cache data between calls to MATLAB code running on a server instance. |
| **Deploy License Server** | Specify whether you want to deploy the Network License Manager for MATLAB. This parameter is available only if you use the deployment template for an existing VPC. <p>You can deploy a license server only if your solution uses public IP addresses. If your solution uses private IP addresses, you must separately deploy a license server in a public subnet.</p><p>If you are using an existing VPC, see the [Use Existing License Server in Existing VPC](#use-existing-license-server-in-existing-vpc) section.</p> |
||**Dashboard Login**|
| **Username for MATLAB Production Server Dashboard** | Specify the administrator username for logging in to the MATLAB Production Server Dashboard. |
| **Password for MATLAB Production Server and License Server** | Specify the password to use for logging in to MATLAB Production Server Dashboard and Network License Manager for MATLAB Dashboard. |
| **Confirm Password MATLAB Production Server and License Server** | Reenter the password to use for logging in to the MATLAB Production Server Dashboard and Network License Manager for MATLAB Dashboard. |    
| |**Network**|
| **Name of Existing Key Pair**          | Select the name of an existing EC2 Key Pair to allow access to all the VMs in the stack. For information about creating an Amazon EC2 key pair, see [Amazon EC2 Key Pairs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html#having-ec2-create-your-key-pair). <p><em>*Example*</em>: boston-keypair<p> |
| **Allow Connections from IP Address** | Specify the IP address range that is allowed to connect to the dashboard that manages the server. The format for this field is IP Address/Mask. <p><em>Example</em>: 10.0.0.1/32</p> <ul><li>This is the public IP address, which can be found by searching for "what is my ip address" on the web. The mask determines the number of IP addresses to include.</li><li>A mask of 32 is a single IP address.</li><li>If you need a range of IP addresses, use a [CIDR calculator](https://www.ipaddressguide.com/cidr).</li><li>To determine which address is appropriate, contact your IT administrator.</li></ul></p> |
| **Make Solution Available over Internet** | Choose 'Yes' if you want your solution to use public IP addresses. |
| **ARN of SSL Certificate**             | Provide the Amazon Resource Name (ARN) of an existing certificate in the AWS Certificate Manager. This certificate enables secure HTTPS communication to the HTTPS server endpoint. For information on creating and uploading a self-signed certificate, see [Create and sign an X509 certificate](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/configuring-https-ssl.html) and [Import SSL Certificate](https://www.mathworks.com/help/mps/server/manage-aws-resources-reference-architecture.html#mw_b0d98763-0e90-48fc-bcc3-ff2755ffe722).<p><em>*Example*</em>: arn:aws:acm:us-east-1:12345:certificate/123456789012</p>|

## Step 3. Configure Existing VPC

>**Note**: If you are deploying to a new VPC, skip this step.

To deploy MATLAB Production Server onto an existing VPC, specify these additional parameters.

| Parameter Name | Value |
|--------------- | ----- |
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

## Step 4. Create Stack
Review or edit your stack details. You must select the acknowledgements to create IAM resources. Otherwise, the deployment produces a `Requires capabilities : [CAPABILITY_IAM]` error and fails to create resources.

When you are satisfied with your stack configuration, click **Create stack**. AWS starts creating the resources for your server environment and opens you to the **Events** tab for the stack. 
    
>**Note**: Resource creation can take up to 20 minutes. After resource creation, it can take up to 15 minutes for the resources to be active.  

## Step 5. Upload License File
1. On the **Events** tab for your stack, wait for the status to reach **CREATE\_COMPLETE**.
1. On the **Outputs** tab, in the row for the `MatlabProductionServerLicenseServer` key, click the corresponding URL listed under **Value** to open the Network License Manager for MATLAB Dashboard login page.
1. Log in to the Network License Manager for MATLAB Dashboard.<ul><li>The username is **manager**.</li><li>For the password, enter the password that you entered in the **Dashboard Login** section while creating the stack.</li></ul>
1. Upload your MATLAB Production Server license by following the instructions in the dashboard.


## Step 6. Connect and Log In to MATLAB Production Server Dashboard
> **Note**: The Internet Explorer web browser is not supported for interacting with the dashboard.

1. On the **Outputs** tab for your stack, in the row for the `MatlabProductionServerDashboardURL` key, click the corresponding URL listed under **Value**. This URL is the HTTPS endpoint to the MATLAB Production Server Dashboard and brings you to the dashboard login page.
1. Log in using the administrator username and password that you specified in the **Dashboard Login** section while creating the stack. For more information on how to use the dashboard, see [Manage MATLAB Production Server Using the Dashboard](https://www.mathworks.com/help/mps/server/manage-matlab-production-server-using-the-dashboard.html).  

You are now ready to use MATLAB Production Server on AWS. 

To run applications on MATLAB Production Server, you need to create applications using MATLAB Compiler SDK. For more information, see [Create Deployable Archive for MATLAB Production Server](https://www.mathworks.com/help/compiler_sdk/mps_dev_test/create-a-deployable-archive-for-matlab-production-server.html). 

# Additional Information

## Use Existing License Server in Existing VPC
To manage MATLAB Production Server licenses, you can deploy an existing Network License Manager server for MATLAB instead of deploying a new one. To use an existing license server, on the *Deploy License Server* step of the deployment, select `No`.

The license manager must be in the same VPC and security group as MATLAB Production Server. You must also add the security group of the server VMs to the security group of the license server.
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

## Delete Your Stack

Once you finish using your stack, to avoid incurring further cost, it is recommended that you delete all resources. 

If you are using an existing license server, and have added the security group of the server VMs to the security group of the license server, you must delete the inbound rules before you delete the stack.
1. In the AWS management console, select the stack that you deployed. 
1. On the details page your stack, click the **Resources** tab.
1. In the **Logical ID** named `SecurityGroup`, click the corresponding URL listed under **Physical ID** to open the security group details.
1. On the **Inbound Rules** tab, click **Edit Inbound Rules**.
1. For each rule that has the **Source** tag set to `matlab-production-server-cloud-stack-elb-1-sg`, click **Delete Rule**. 
1. Click **Save Rules**.

To delete the stack, do the following:
1. Log in to the AWS Console.
3. Go to the AWS Cloud Formation page and select the stack that you created.
3. Click **Delete**.

If you do not want to delete the entire deployment but want to minimize the cost, you can bring the number of instances in the Auto Scaling Group down to 0 and then scale it back up when the need arises.

## Get License Server MAC Address
The Network License Manager for MATLAB reference architecture manages the MATLAB Production Server license file. The deployment templates for the MATLAB Production Server reference architecture provide an option to deploy the license manager. You can also use an existing license manager that is located in the same VPC and security group as the MATLAB Production Server instances. For more information about the Network License Manager for MATLAB reference architecture, see [Network License Manager for MATLAB](https://github.com/mathworks-ref-arch/license-manager-for-matlab-on-aws).

>**NOTE**: For a new license manager deployed with MATLAB Production Server, the license manager MAC address is available only after the deployment to the cloud is complete. For information on deploying the solution, see [Deployment Steps](/README.md#deployment-steps).

To get the MAC address of the license manager: 
1. Log in to the Network License Manager for MATLAB Dashboard. For a license manager deployed with the MATLAB Production Server deployment, use the following credentials:<br>
Username: **manager**<br>
Password: Enter the password that you specified during the deployment process.
1. Click **Administration** and then **License**.
1. Copy the license server MAC address displayed at the top.