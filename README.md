<!-- BEGINNING: Intro -->
# WA HoneyTraps Program
This repository contains information on the WA Honey Traps Program onboarding process and a technical onboarding guide to assist with the technical integration of the Honey Trap platform.

## Table of Contents

1) [Platform Integration - Overview](#platform-integration---overview)

2) [Onboarding Checklist](#onboarding-checklist)

3) [Data Collection Rule and Logic App deployment guide](#data-collection-rule-and-logic-app-deployment-guide)

4) [Analytic Rules Deployment Guide](#analytic-rules-deployment-guide)

5) [Initiating an end-to-end test](#initiating-an-end-to-end-test)

6) [Feedback](#feedback-1)

---

<!-- ![Overview-HoneyTrapsIntegration](./images/overview-honey-traps-integration.png)) -->
## Platform Integration - Overview

<img src="images/overview-honey-traps-setup.png" width="900" height="700">

## Onboarding Checklist

- [ ] Refer to information and instructions provided in [WASOC Honey Trap (Pilot)](https://soc.cyber.wa.gov.au//onboarding/honey-traps/) get onboard to WA Honeytraps Program.
- [ ] Verify that a Canary group has been provisioned for agency by WA SOC.
- [ ] Complete the integrations for DCR and Logic Apps [Data Collection Rule and Logic App deployment guide](#data-collection-rule-and-logic-app-deployment-guide)
- [ ] Deploy analytic rules for Microsoft Sentinel [Analytic Rules Deployment Guide](#analytic-rules-deployment-guide)
- [ ] Ensure analytic rules and Logic Apps have been enabled
- [ ] [Initiate end-to-end test to generate alert](#initiating-an-end-to-end-test)

## Feedback
For questions or feedback, please contact cybersecurity@dpc.wa.gov.au


<!-- END: Intro -->

---

<!-- BEGINNING: Data Collection Rule and Custom Table creation ARM template deployment guide -->

# Data Collection Rule and Logic App deployment guide
The following steps will guide you on utilising Azure ARM templates to create a Data Collection Rule and Logic App to integrate Honey Traps canary platform with Microsoft Sentinel.



## Pre-requisites:
- Requires an Azure Log Analytics Workspace (to ingest the data from the Honey Traps canary platform).
- A Canary group that has been provisioned by WASOC.
- Requires Contributor permission to the Microsoft Subscription to deploy the required resources.
- Requires a minimum of 'User Access Administrator' for role assignment to the target subscription.

## Step by step guide

### Step 1. 
To start the integration of the Honey Traps platform with your Sentinel SIEM, click on the 'Deploy to Azure' button shown below. This will deploy the Data Collection Rule and Custom tables required for the integration.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw%2Egithubusercontent%2Ecom%2Fwagov%2Fwasoc%2Dhoneytraps%2Frefs%2Fheads%2Fmain%2Farm%2Dtemplates%2Fsiem%2Dintegration%2Dwith%2Ddcr%2FDCR%2DARM%2DTemplate%2Dv7%2E0%2Ejson)

### Step 2.
You will be redirected to the custom deployment screen in azure portal. Select/ fill-in the required information.

![Screenshot of the DCR ARM template](./images/deployment-guide-screenshots/dcr-custom-table-deployment-arm-template-marked.png.png)

Field description:
1. **Subscription**: The subscriptions where the Data Collection Rules will be deployed to.
2. **Resource Group**: The resource group where the Data Collection Rules will be deployed to.
3. **Data Collection Rule Name**: Name for the Data Collection Rule (Note: No special characters or numbers).
4. **Workspace Resource ID**: The Workspace Resource ID of the log analytics workspace. (Microsoft sentinel > Settings > Workspace Settings > Properties > Resource ID)
5. **Workspace Name**: The name of the Workspace you have selected above.


### Step 3.
Review and ensure all details provided in the deployment are correct and proceed with creating the resources. Otherwise, select the 'previous' button to go back and make any changes.


### Step 4.
Click on the Data Collection Rule resource that was just deployed and in the overview of the DCR, select JSON View on the top right hand corner. 

![Data Collection Rule overview](./images/deployment-guide-screenshots/dcr-overview.png)

Leave this open on this tab and proceed to the next step.

### Step 5. 
Now select the 'Deploy to Azure' below and open it in a new tab to deploy the Logic Apps for sending the Canary data over to the Log Analytic workspace/datalake and fill in the following information.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw%2Egithubusercontent%2Ecom%2Fwagov%2Fwasoc%2Dhoneytraps%2Frefs%2Fheads%2Fmain%2Farm%2Dtemplates%2Fsiem%2Dintegration%2Dwith%2Ddcr%2FCanary%2DLogicApp%2DARM%2DTemplate%2DV2%2E0%2Ejson)

![Screenshot of the Logic App ARM Template Deployment](./images/deployment-guide-screenshots/logic-app-deployment-arm-template.png)

Field description:
1. **Subscription**: The subscriptions where the Logic apps will be deployed to.
2. **Resource Group**: The resource group where the Logic apps will be deployed to.
3. **Logic App Name**: The name of the Logic App. (Please update the 'AGENCYNAME' to reflect your agency's name)
4. **DCR Immutable ID**: DCR Immutable ID from the previously deployed DCR (from the JSON view).
5. **DCR Log Ingestion**: DCR Log Ingestion URI from the previously deployed DCR (from the JSON view).

{: .important }
If the DCR resource group and Logic App resource groups are different, you may need to manually assign the Monitoring Metrics Publisher role to the Managed Identity of the Logic App, scoped to the resource group that contains the Data Collection Rule (DCR).

### Step 6.

Once the information has been filled in and the resources are successfully deployed, select the deployed logic app resource (You should see a screen like the one shown below).

![Screenshot of the successful deployment of the Logic App](./images/deployment-guide-screenshots/logic-app-successful-resource-deployment.png)


### Step 7.

Select the 'Logic app designer' under the 'Development Tools' and select the trigger action as shown below.

![Screenshot of the Logic app designer - trigger action](./images/deployment-guide-screenshots/logic-app-designer-view-trigger.png)

### Step 8.

From the trigger action parameters, copy the HTTP URL for the webhook.

![Screenshot of the HTTP URL - trigger action](./images/deployment-guide-screenshots/logic-app-designer-trigger-http-url.png)

### Step 9.

In a new tab; navigate to the Honey Traps Canary platform and select the settings cogwheel at the top.

![Screenshot of the Canary settings](./images/deployment-guide-screenshots/canary-platform-settings-cogwheel.png)

### Step 10. 

Go to 'Notifications' and select the '+' sign under 'Webhooks' to setup a new webhook for the logic apps. And then select 'Add Generic' option to add a generic webhook.

![Screenshot of add webhook - Canary platform](./images/deployment-guide-screenshots/canary-platform-notifications-webhook-add.png)

![Screenshot of the Webhook options - Canary platform](./images/deployment-guide-screenshots/canary-platform-notifications-webhook-options.png)

### Step 11.

1. Paste the HTTP URL that was copied from the Logic App in the step 8 under the 'Webhook URL' text field.
2. Turn on the 'Add custom request headers' option.
3. Enter ***'key'*** for the header name.
4. Copy-paste the key value from the 'Condition' action of Logic App. (Note: you have to go back to the ***Logic App*** and copy the ***guid*** value)

![Screenshot of the Generic Webhook values](./images/deployment-guide-screenshots/canary-platform-notifications-webhook-values.png)

Finally, click on 'Save' button at the bottom to add the webhook to the Canary.

---

This completes the integration for the Honey Traps project. You can now create canary tokens and perform testing to ensure the integration is working correctly.


---

<!-- BEGINNING: Analytic Rules Deployment Guide -->
# Analytic Rules Deployment Guide

The following steps will guide you on deploying analytic-rules to generate alerts and incident in your Microsoft Sentinel workspace.

## Prerequisites

- You must have completed the [Honey Traps Canary Integration](#data-collection-rule-and-logic-app-deployment-guide) prior to deploying the analytic rules.
- You must have atleast one Canary token incident generated on the Canary platform.
- The analytic rule uses the following default table name in your Log Analytics Workspace: **Canary_CL**.

## Step by step guide

### Step 1.

To start the deployment of the Azure Analytic Rules for each type of canary, click on the 'Deploy to Azure' buttons shown below.

| Rule | Deploy |
|-|-|
| **Canary - Analytic Rules** | [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw%2Egithubusercontent%2Ecom%2Fwagov%2Fwasoc%2Dhoneytraps%2Frefs%2Fheads%2Fmain%2Farm%2Dtemplates%2Fanalytic%2Drules%2Fcombined%2Dcanary%2Drules%2Ddcr%2Ejson) | 
| **Threat Intelligence - Honey Traps - Suspicious Sign-in** | [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw%2Egithubusercontent%2Ecom%2FDinindu%2DWick%2Fwasoc%2Dhoneytraps%2Frefs%2Fheads%2Fmain%2Farm%2Dtemplates%2Ftip%2Danalytic%2Drules%2FWASOC%2DIntelligence%2Da%2Dsuspicious%2Dsign%2Dins%2Dattempts%2Ddetected%2Dfrom%2Dknown%2Dthreat%2Dactor%2Dinfrastructure%2DWASOC%2DHoneyToken%2Ejson) | 

### Step 2.

You will be redirected to the custom deployment screen in azure portal. Select/ fill-in the required information

![Screenshot of Deployment page](./images/deployment-guide-screenshots/analytic-rule-combined-deployment.png)

Field description:
1. **Subscription**: The subscriptions where the Sentinel workspace is located.
2. **Resource Group**: The resource group where the Sentinel workspace is located.
3. **Region**: The region where the Sentinel workspace is located.
4. **Workspace Name**: The _workspaceName_ of Sentinel log analytics workspace, where the analytic rule will be deployed to.
5. **Rule Id's**: Function value to obtain new Rule Id's for Canary and Canary Tokens.
6. **Domain**: The domain of the canary platform. e.g. '83ndg2ob.canary.tools'

{: .warning }
Do not replace or change the value in the 'Rule Id' fields. This is to generate unique Ids for your analytic rules.

### Step 3.
Review and ensure all details provided in the deployment are correct and proceed with creating the resources. Otherwise, select the 'previous' button to go back and make any changes.

### Step 4.
Navigate to _Analytics_ blade inside the Microsoft Sentinel, and verify that the analytics rules has been created and enabled.

### Step 5.
Initiate test to generate incident from the canary platform, and verify that incidents were generated in Microsoft Sentinel.
<!-- END: Analytic Rules Guide -->


## Initiating an end-to-end test
To initiate an end-to-end test the integration of the Honey Traps canary platform and the SIEM, you could do the following:

### Pre-requisites
- You must have a canary group provisioned by WA SOC.
- You must have completed the [DCR and Logic App deployment](#data-collection-rule-and-logic-app-deployment-guide) and have the [Analytic Rules Deployed](#analytic-rules-deployment-guide).

### Step 1. 
Create a new canary token within your canary group.

### Step 2. 
Trigger the canary token by interacting with it.

### Step 3. 
Navigate to your Log Analytics Workspace to check if any alerts have been ingested.

{: .note }
It may take up to 5 minutes for the alerts to be ingested for the first time.

If you have alerts being ingested into your Log Analytics Workspace, you have successfully completed your canary platform and SIEM integration. 


## Feedback
For questions or feedback, please contact cybersecurity@dpc.wa.gov.au


