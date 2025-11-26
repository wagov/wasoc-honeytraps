import os # Importing for secret management
import requests # For http requests
import json


####                   <<<<< Secrets >>>                          ####
secret = os.getenv("HONEY_TRAPS_SECRETS_RO", default=None) # Grab the HoneyTraps API token from env secrets
domain = os.getenv("HONEY_TRAPS_DOMAIN", default=None) # Get the HoneyTraps domain from the env secrets
la_url = os.getenv("HONEY_TRAPS_LA_URL", default=None) # Get the HoneyTraps LogicApp URL from the env secrets
#### ------------------------------------------------------------ ####


# Retrieve canary device info for each tenancy
def all_tenant_devices_info(tenants_summary_dict:dict, return_values:str="default") -> dict: # Input maybe tenant_summary func
  #Init Vars
  tenant_device_info = {}
  devices_arr = []
  tenant_name = ""
  devices_offline = 0
  devices_online = 0
  total_devices = 0
  
  # Go through the tenants summary dictionary and filter out specific values and assign them to vars
  for tenant, tenant_details in tenants_summary_dict["flocks_summary"].items():
    tenant_name = tenant_details["name"]
    devices_offline = tenant_details["offline_devices"]
    devices_online = tenant_details["online_devices"]
    total_devices = devices_online + devices_offline

    # Store values for each tenant in a dictionary
    tenant_device_info[tenant] = {"Tenant-Name": tenant_name, "Devices-Online": devices_online, "Devices-Offline": devices_offline, "Total-Devices": total_devices}

    # Store values of each tenant in an array (stored in array to meet LA data format requirements)
    devices_arr.append({'Flock-ID': tenant, 'Tenant-Name': tenant_name, 'Devices-Online': devices_online, 'Devices-Offline': devices_offline, 'Total-Devices': total_devices})

  if return_values == "array":
    return devices_arr
  else:
    return tenant_device_info
  

# Token info of each tenancy
def all_tenant_tokens_info(tenants_summary_dict:dict, return_values:str = "default") -> dict:
  #Init vars
  tenant_token_info = {}
  tokens_arr = []
  tenant_name = ""
  disabled_tokens = 0
  enabled_tokens = 0
  total_tokens = 0
  webhooks = []

  # Go through the tenants summary dictionary and assign the values to their relevant variables
  for tenant, tenant_details in tenants_summary_dict["flocks_summary"].items():
    tenant_name = tenant_details["name"]
    disabled_tokens = tenant_details["disabled_tokens"]
    enabled_tokens = tenant_details["enabled_tokens"]
    total_tokens = tenant_details["total_tokens"]
    webhooks = tenant_details["settings"]["webhooks"]["generic_webhooks"]

    tenant_token_info[tenant] = {'Tenant-Name': tenant_name, 'Enabled-Tokens': enabled_tokens, 'Disabled-Tokens':disabled_tokens, 'Total-Tokens':total_tokens, 'Webhooks': webhooks} # Store in dictionary for export
    tokens_arr.append({'Flock-ID': tenant, 'Tenant-Name': tenant_name, 'Enabled-Tokens': enabled_tokens, 'Disabled-Tokens':disabled_tokens, 'Total-Tokens':total_tokens, 'Webhooks': webhooks}) # Store in array for export
  
  if return_values == "array":
    # Return token info as an array
    return tokens_arr
  else:
    # Return the token info as a dictionary
    return tenant_token_info

# Token and Device info for each tenancy
def all_tenant_token_device_info(tenants_summary_dict:dict, return_values:str = "default") -> dict:
  #Init vars
  tenant_token_device_info = {}
  tenant_token_device_info_arr = []
  tenant_name = ""
  disabled_tokens = 0
  enabled_tokens = 0
  total_tokens = 0
  devices_offline = 0
  devices_online = 0
  total_devices = 0
  webhooks = []

  # Go through the tenants summary dictionary and assign the values to their relevant variables
  for tenant, tenant_details in tenants_summary_dict["flocks_summary"].items():
    tenant_name = tenant_details["name"]
    disabled_tokens = tenant_details["disabled_tokens"]
    enabled_tokens = tenant_details["enabled_tokens"]
    total_tokens = tenant_details["total_tokens"]
    devices_offline = tenant_details["offline_devices"]
    devices_online = tenant_details["online_devices"]
    webhooks = tenant_details["settings"]["webhooks"]["generic_webhooks"]

    total_devices = devices_online + devices_offline

    # Store info in a dictionary for export
    tenant_token_device_info[tenant] = {'Tenant-Name': tenant_name, 'Enabled-Tokens': enabled_tokens, 'Disabled-Tokens':disabled_tokens, 'Total-Tokens':total_tokens, 'Devices-Online': devices_online, 'Devices-Offline': devices_offline, 'Total-Devices': total_devices, "Webhooks": webhooks} 
    # Store info in an array for export
    tenant_token_device_info_arr.append({'Flock-ID': tenant, 'Tenant-Name': tenant_name, 'Enabled-Tokens': enabled_tokens, 'Disabled-Tokens':disabled_tokens, 'Total-Tokens':total_tokens, 'Devices-Online': devices_online, 'Devices-Offline': devices_offline, 'Total-Devices': total_devices, "Webhooks": webhooks}) 
  
  if return_values == "array":
    # Return token info as an array
    return tenant_token_device_info_arr
  else:
    # Return the token info as a dictionary
    return tenant_token_device_info


# Get info of all tenants
def all_tenants_summary(return_value:str="default") -> dict:
  
  url=f"https://{domain}/api/v1/flocks/summary"

  payload = {
    'auth_token':f'{secret}'
  }

  response = requests.get(url, params=payload)
  
  tenants_summary_dict = response.json()
  tenant_id_list = [] # Init list for a list of tenant IDs

  # Make a list of tenants (tenant id and name)
  for tenant in tenants_summary_dict["flocks_summary"]: 
    tenant_id_list.append(f"{tenant} : {tenants_summary_dict["flocks_summary"][tenant]["name"]}")

  if return_value == 'tenant_id_list':
    return tenant_id_list # Return only the tenant ID information
  else: 
    return tenants_summary_dict # Return tenants summary info
  
# Send data over to Logic Apps
def send_data_la(data:dict) -> None:

  payload = json.dumps(data)

  header = {
    "Content-Type": "application/json",
  }

  response = requests.post(f"{la_url}", data=payload, headers=header)
  
  if response.status_code == 202:
    print (f"Data sent to target successfully!")
  else:
    print(f"Failed to send data. Status Code {response.status_code}, Response {response.reason}")


if __name__ == '__main__':
  send_data_la(all_tenant_token_device_info(all_tenants_summary(),"array"))
