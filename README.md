# MATLAB Production Server on Amazon Web Services

# Requirements

Before starting, you need the following:

-   A MATLAB® Production Server™ license that meets the following conditions:
    - Linked to a MathWorks Account.
    - Concurrent license type. To check your license type, see [MathWorks License Center](https://www.mathworks.com/licensecenter/).
    - Configured to use a network license manager on the virtual network. By default, the deployment of MATLAB Production Server includes a network license manager, but you can also use an existing license manager. In either case, activate or move the license after deployment. For details, see [Configure MATLAB Production Server License for Use on the Cloud](https://www.mathworks.com/help/mps/server/configure-matlab-production-server-license-for-use-on-the-cloud.html).
-   An Amazon Web Services™ (AWS) account. If you do not have an account, create one at https://aws.amazon.com by following the on-screen instructions.

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
1. In the top navigation of your AWS account, select the region where you want to deploy MATLAB Production Server. You must select one of these supported regions:<ul><li>**US-East (N. Virginia)**</li><li>**US-West (Oregon)** &mdash; R2022b or later only</li><li>**Europe (Ireland)**</li><li>**Asia Pacific (Tokyo)**</li></ul>
1. Create a [key pair](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html) in that region.  The key pair is necessary because it is the only way to connect to the instance as an administrator.
1. If necessary, [request a service limit increase](https://console.aws.amazon.com/support/home#/case/create?issueType=service-limit-increase) for the Amazon EC2 instance type or VPCs.  You might need to do this if you already have existing deployments that use that instance type or you think you might exceed the [default limit](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-resource-limits.html) with this deployment.

# Deploy Reference Architecture for Your Release
To deploy the reference architecture, select your MATLAB Production Server release from the table and follow the instructions to deploy the server using the provided template. A deployment of MATLAB Production Server supports MATLAB Runtime versions up to six releases back.
| Release | Supported MATLAB Runtime Versions |
| ------- | --------------------------------- |
| [R2023a](releases/R2023a/README.md) | R2023a, R2022b, R2022a, R2021b, R2021a, R2020b |
| [R2022b](releases/R2022b/README.md) | R2022b, R2022a, R2021b, R2021a, R2020b, R2020a |
| [R2022a](releases/R2022a/README.md) | R2022a, R2021b, R2021a, R2020b, R2020a, R2019b |
| [R2021b](releases/R2021b/README.md) | R2021b, R2021a, R2020b, R2020a, R2019b, R2019a |
| [R2021a](releases/R2021a/README.md) | R2021a, R2020b, R2020a, R2019b, R2019a, R2018b |
| [R2020b](releases/R2020b/README.md) | R2020b, R2020a, R2019b, R2019a, R2018b, R2018a |
> **Note**: MathWorks provides templates for only the six most recent releases of MATLAB Production Server. Earlier templates are removed and are no longer supported.
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

## Why do requests to the server fail with errors such as “untrusted certificate” or “security exception”?  
These errors occur either when CORS is not enabled on the server or when the server endpoint uses a self-signed certificate. 

If you are making an AJAX request to the server, make sure that CORS is enabled in the server configuration. You can enable CORS by editing the property `CORS Allowed Origins` property in the **Settings** tab of the dashboard.

Also, some HTTP libraries and JavaScript AJAX calls will reject a request originating from a server that uses a self-signed certificate. You may need to manually override the default security behavior of the client application. Alternatively, you can add a new HTTPS endpoint to the application gateway. For more information, see [Change SSL Certificate](https://www.mathworks.com/help/mps/server/manage-aws-resources-reference-architecture.html#mw_51d64616-777c-4e15-af40-ab3d8dcc418f). 


## How do I allow multiple IP address ranges access to the dashboard?
The deployment template allows you to enter only one range of IP addresses that can access the dashboard. After the deployment is complete, you can allow additional IP ranges access to the dashboard. For details, see 
[Update security group rules](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/working-with-security-groups.html#updating-security-group-rules) in the AWS documentation.

The name of the security group to update is ``` matlab-production-server-cloud-stack-elb-1-sg```. Edit inbound rules to add additional IP address ranges in CIDR format for the ```HTTPS``` type.

## How do I upgrade an existing deployment to a newer MATLAB version?
Use the instructions at the following link to upgrade an existing deployment to a newer MATLAB version: [Upgrading an Existing Deployment](UPGRADES.md)

# Enhancement Request
Provide suggestions for additional features or capabilities using the following link: https://www.mathworks.com/solutions/cloud.html

# Technical Support
If you require assistance or have a request for additional features or capabilities, please contact [MathWorks Technical Support](https://www.mathworks.com/support/contact_us.html).

