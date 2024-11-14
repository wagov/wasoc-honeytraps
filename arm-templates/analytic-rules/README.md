# About

This folder contains analytic-rules to generate alerts and incident in agency's Microsoft Sentinel workspace.

## Prerequisites

- You must have set up [send-canary-alert-webhook](./send-canary-alert-webhook/README.md) logic-apps prior to deploying the analytic rules
- The analytic rule uses the following default table name: **CanaryLogs_CL**

## Step by step guide

### Step 1.

To start the deployment of the Azure Analytic Rules, click on the 'Deploy to Azure' button shown below.

![Deploy to Azure](https://aka.ms/deploytoazurebutton)

### Step 2.

> Note: Please deploy each analytic rule template one at a time.

You will be redirected to the custom deployment screen in azure portal. Select/ fill-in the required information

![Screenshot of Deployment page](./images/DeploymentPage.png)

Field description:
1. **Subscription**: The subscriptions where the Sentinel workspace is located
2. **Resource Group**: The resource group where the Sentinel workspace is located
3. **Region**: The region where the Sentinel workspace is located
4. **Workspace Name**: The _workspaceId_ of Sentinel log analytics workspace, where the analytic rule will be deployed to
5. **Rule Id**: Value to obtain a new Rule Id using the newGuid function in Azure
6. **Domain**: The domain name for the canary platform, to be provided by WASOC.

> Note: Do not replace or change the value in the 'Rule Id' field, this is to generate unique Id for your analytic rules.

### Step 3.
Review and ensure all details provided in the deployment are correct and proceed with creating the resources. Otherwise, select the 'previous' button to go back and make any changes.

![image](https://github.com/user-attachments/assets/d0426b4d-d76a-4668-8a5e-d20fc0a58a52)

### Step 4.
Navigate to _Analytics_ blade inside the Microsoft Sentinel, and verify that the analytics rules has been created and enabled.

![image](https://github.com/user-attachments/assets/642fef4b-409d-473b-b074-fa80c02afa3a)

### Step 5.
Initiate test to generate incident from the canary platform, and verify that incidents were generated in Microsoft Sentinel.

## Feedback
For questions or feedback, please contact cybersecurity@dpc.wa.gov.au
