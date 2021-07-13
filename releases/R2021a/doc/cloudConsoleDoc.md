# MATLAB Production Server Cloud Console User Guide

1. [Get Information About Server Instances](#get-information-about-server-instances)
1. [Get HTTPS End Point](#get-https-end-point)
1. [Upload a MATLAB Application Created with MATLAB Compiler SDK](#upload-a-matlab-application-created-with-matlab-compiler-sdk)
1. [Edit the Server Configuration](#edit-the-server-configuration)
1. [Edit the Redis ElastiCache Configuration](#edit-the-redis-elasticache-configuration)
1. [Upload an HTTPS Certificate](#upload-an-https-certificate)
1. [Setup Authentication Using Azure Active Directory](#setup-authentication-using-azure-active-directory)
1. [Change the Number of Virtual Machines](#change-the-number-of-virtual-machines)
1. [Change Self-signed Certificates](#change-self-signed-certificates)

## Get Information About Server Instances
To get information about server instances:
- On the cloud console navigation menu, click **Home**.

![Cloud Console Home](/releases/R2021a/images/cloudConsoleHome02.png)

[Back to Top](/releases/R2021a/doc/cloudConsoleDoc.md#matlab-production-server-cloud-console-users-guide) | [Back to Main](/README.md#matlab-production-server-on-amazon-web-services)

## Get HTTPS End Point
To get the HTTPS end point:
1. On the cloud console navigation menu, click **Home**. 
1. Copy the parameter value listed next to **HTTPS Server Endpoint**.

[Back to Top](/releases/R2021a/doc/cloudConsoleDoc.md#matlab-production-server-cloud-console-users-guide) | [Back to Main](/README.md#matlab-production-server-on-amazon-web-services)

## Upload a MATLAB Application Created with MATLAB Compiler SDK
To upload an application:
1. On the cloud console navigation menu, click **Applications**. 
1. Click **+Upload Application**.
1. Click **Browse CTF File**, select the file, and click **Upload**.

For information on how to create an application, see [Package Deployable Archives
with Production Server Compiler App](https://www.mathworks.com/help/mps/ml_code/create-a-deployable-ctf-archive-with-the-library-compiler-app.html) in the MATLAB® Compiler SDK™ documentation.
  
[Back to Top](/releases/R2021a/doc/cloudConsoleDoc.md#matlab-production-server-cloud-console-users-guide) | [Back to Main](/README.md#matlab-production-server-on-amazon-web-services)

## Edit the Server Configuration
To edit the server configuration:
1. On the cloud console navigation menu, select **Administration** > **Server Configuration**. 
1. Find the server property you want to change and enter the appropriate value. For
a list of server properties and values, see [Server Properties](https://www.mathworks.com/help/mps/referencelist.html?type=property).

>**NOTE**: To assign a value to a property that has been commented out, remove the #
symbol and assign a value.

*Example*: Enabling CORS:

`--cors-allowed-origins http://www.w3.org, https://www.apache.org`

>**NOTE**: When setting the `num-workers` property in the server configuration you need to carefully consider your cluster setup. Each virtual machine in the cluster runs an instance of MATLAB Production Server and each instance runs multiple MATLAB workers. MathWorks recommends 1 core per MATLAB worker. For example, a `Standard_D4s_v3` **Server VM Instance Size** has 4 cores and therefore we recommend that you set `num-workers` be no more than 4 per instance.<p>`--num-workers 4`</p> 

[Back to Top](/releases/R2021a/doc/cloudConsoleDoc.md#matlab-production-server-cloud-console-users-guide) | [Back to Main](/README.md#matlab-production-server-on-amazon-web-services)

## Edit the Redis ElastiCache Configuration
To edit the Azure Cache for Redis configuration:
- On the cloud console navigation menu, select **Administration** > **Persistence Configuration**.

The cache configuration is specified in JSON format as follows: 
```
{
  "Connections": {
    "<connection_name>": {
      "Provider": "Redis",
      "Host": "<hostname>",
      "Port": <port_number>,      
    }
  }
}
```
If you create a Redis ElastiCache while launching the stack, the cache configuration is automatically populated. The default connection name is `Connection_Name` and can be changed. 

If you plan on using a different Redis ElastiCache, specify the `<connection_name>`, `<hostname>`, and `<port_number>` values in the configuration. The Redis ElastiCache must be within the same VPC as the deployment. 

For more information, see [Use a Data Cache to Persist Data](https://www.mathworks.com/help/mps/ml_code/use-a-data-cache-to-persist-data.html).

[Back to Top](/releases/R2021a/doc/cloudConsoleDoc.md#matlab-production-server-cloud-console-users-guide) | [Back to Main](/README.md#matlab-production-server-on-amazon-web-services)


## Upload an HTTPS Certificate
> **NOTE**: When you upload a new certificate, you will lose all pending requests.

To upload an HTTPS certificate:
1. On the cloud console navigation menu, select **Administration** > **HTTPS Certificate**.
1. Click **Browse Certificate...** and select a certificate file. Only `.pfx` files are supported.
1. Enter the certificate password in the **Certificate Password** field.
1. Click **Upload**.

The server will automatically restart after uploading a certificate. You will
need to log out and log back in.

[Back to Top](/releases/R2020a/doc/cloudConsoleDoc.md#matlab-production-server-cloud-console-users-guide) | [Back to Main](/README.md#matlab-production-server-on-amazon-web-services)

## Setup Authentication Using Azure Active Directory
You can use Azure Active Directory (Azure AD) to provide an identity to each user. To use Azure AD you will need to specify an:
* Access Control Configuration File
* Access Control Policy File

<table>
  <tr>
    <th>Sample Access Control Configuration File</th>
  </tr>
  <tr>
    <td><pre>{<br>  "tenantId": "54ss4lk1-8428-7256-5fvh-d5785gfhkjh6",<br>  "serverAppId": "j21n12bg-3758-3r78-v25j-35yj4c47vhmt",<br>  "jwksUri": "https://login.microsoftonline.com/common/discovery/keys",<br>  "issuerBaseUri": "https://sts.windows.net/",<br>  "jwksTimeOut": 120<br>}</pre></td>
  </tr>
</table>

<table>
  <tr>
    <th>Sample Access Control Policy File</th>
  </tr>
  <tr>
    <td><pre>{<br>  "version": "1.0.0",<br>  "policy" : [<br>    {<br>      "id": "policy1",<br>      "description": "MPS Access Control policy for XYZ Corp.",<br>      "rule": [<br>        {<br>          "id": "rule1",<br>          "description": "group A can execute ctf magic",<br>          "subject": { "groups": ["aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"] },<br>          "resource": { "ctf": ["magic"] },<br>          "action": ["execute"]<br>        },<br>        {<br>          "id": "rule2",<br>          "description": "group A and group B can execute ctf monteCarlo and fastFourier",<br>          "subject": { "groups": ["aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa", "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"]  },<br>          "resource": { "ctf": ["monteCarlo", "fastFourier"] },<br>          "action": ["execute"]<br>        },<br>        {<br>          "id": "rule3",<br>          "description": "QE group C can execute any ctf starts with test",<br>          "subject": { "groups": ["cccccccc-cccc-cccc-cccc-cccccccccccc"] },<br>          "resource": { "ctf": ["test*"] },<br>          "action": ["execute"] <br>        }<br>      ]<br>    }<br>  ]<br>}<br></pre></td>
  </tr>
</table>

For more information, see [Access Control](https://www.mathworks.com/help/mps/server/access_control.html).&nbsp;

After you enter the details of each file and click **Save and Apply Configuration**, you will need to edit the [Server Configuration](#edit-the-server-configuration) and enable the option `access-control-provider`.

[Back to Top](/releases/R2021a/doc/cloudConsoleDoc.md#matlab-production-server-cloud-console-users-guide) | [Back to Main](/README.md#matlab-production-server-on-amazon-web-services)


## Change the Number of Virtual Machines
You cannot change the number of virtual machines (VMs) from the cloud console.
To change the number of VMs:

1. Log in to the AWS Console.
2. Expand **Services** and select **CloudFormation** under Management Tools. 
3. Select the stack you created for this solution.
4. Expand **Outputs**.
5. Look for the key named `MatlabProductionServerAutoScalingGroup` and click the corresponding URL listed under value. This will take you to the auto scaling group associated with your stack.
6. In the **Details** tab, click **Edit** and change the value for the **Desired** field to the number of VMs you want. 

If you have a standard 24 worker MATLAB Production Server license and select `t2.xlarge` as the **Instance type for the worker nodes** during setup, you will need 6 worker nodes to fully utilize the workers in your license.

[Back to Top](/releases/R2021a/doc/cloudConsoleDoc.md#matlab-production-server-cloud-console-users-guide) | [Back to Main](/README.md#matlab-production-server-on-amazon-web-services)

## Change Self-signed Certificates
You can change the self-signed certificate to:
- The HTTPS endpoint to the load balancer. This endpoint is used to make requests to the server. 
- The HTTPS endpoint to the cloud console. This endpoint is used to connect to the cloud console. 

To change the self-signed certificate used to connect to the cloud console, see [Upload an HTTPS Certificate](#upload-an-https-certificate).

To change the self-signed certificate to the load balancer you need to create a new listener for the load balancer. 

> NOTE: The load balancer HTTPS endpoint is used to make requests to the server. 

### Create a Listener
1. Select the stack you created for this solution.
2. Expand **Resources**.
3. Look for the Logical ID with type `AWS::ElasticLoadBalancing::LoadBalancer`.  
4. Click the corresponding URL listed under value for the load balancer Logical ID. This will take you to the load balancer associated with your stack.
5. Select the **Listeners** tab and click the **Edit** button. 
6. Click **Add** and fill in the details:

    | Parameter Name             | Value                              |
    |----------------------------|------------------------------------|
    | **Load Balancer Protocol** | HTTPS (Secure HTTP) or HTTP        |
    | **Load Balancer Port**     | 443 (HTTPS) and  80 (HTTP)         |
    | **Instance Protocol**      | HTTP                               |
    | **Instance Port**          | 9910                               |
    | **Cipher**                 | Select a cipher as applicable.     |
    | **SSL Certificate**        | Select an appropriate certificate. |

7. Click **Save**.

[Back to Top](/releases/R2021a/doc/cloudConsoleDoc.md#matlab-production-server-cloud-console-users-guide) | [Back to Main](/README.md#matlab-production-server-on-amazon-web-services)
