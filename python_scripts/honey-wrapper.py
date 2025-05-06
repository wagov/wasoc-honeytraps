import os # Import os module for secret management
import requests # For http requests
import json # Import Json module


####                   <<<<< Secrets >>>                          ####
secret = os.getenv("HONEY_TRAPS_SECRETS", default=None) # Grab the HoneyTraps API token from env secrets
domain = os.getenv("HONEY_TRAPS_DOMAIN", default=None) # Get the HoneyTraps domain from the env secrets
la_url = os.getenv("HONEY_TRAPS_LA_URL", default=None) # Get the HoneyTraps LogicApp URL from the env secrets
tenant_id = "<yourTenantId_Here>" # Enter the flock ID of the flock you need to query for information
#### ------------------------------------------------------------ ####


# Difference between this func and 'all_tenant_summary' is that this will provide the number of triggered tokens
def single_tenant_summary(tenant_id:str) -> dict:

  #Definitions of variables
  url = f'https://{domain}/api/v1/flock/summary'

  payload = {
    'auth_token': f'{secret}',
    'flock_id': f'{tenant_id}'
  }

  response = requests.get(url, params=payload)

  tenant_summary_dict = response.json()

  # Calculate and add the number of active tokens into the tenant summary dictionary
  if (tenant_summary_dict["total_tokens"] > 0):
    active_tokens = tenant_summary_dict['total_tokens'] - tenant_summary_dict["disabled_tokens"]
    tenant_summary_dict["active_tokens"] = f"{active_tokens}"

  return tenant_summary_dict


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

  # Go through the tenants summary dictionary and assign the values to their relevant variables
  for tenant, tenant_details in tenants_summary_dict["flocks_summary"].items():
    tenant_name = tenant_details["name"]
    disabled_tokens = tenant_details["disabled_tokens"]
    enabled_tokens = tenant_details["enabled_tokens"]
    total_tokens = tenant_details["total_tokens"]

    tenant_token_info[tenant] = {'Tenant-Name': tenant_name, 'Enabled-Tokens': enabled_tokens, 'Disabled-Tokens':disabled_tokens, 'Total-Tokens':total_tokens} # Store in dictionary for export
    tokens_arr.append({'Flock-ID': tenant, 'Tenant-Name': tenant_name, 'Enabled-Tokens': enabled_tokens, 'Disabled-Tokens':disabled_tokens, 'Total-Tokens':total_tokens}) # Store in array for export
  
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

  # Go through the tenants summary dictionary and assign the values to their relevant variables
  for tenant, tenant_details in tenants_summary_dict["flocks_summary"].items():
    tenant_name = tenant_details["name"]
    disabled_tokens = tenant_details["disabled_tokens"]
    enabled_tokens = tenant_details["enabled_tokens"]
    total_tokens = tenant_details["total_tokens"]
    devices_offline = tenant_details["offline_devices"]
    devices_online = tenant_details["online_devices"]
    total_devices = devices_online + devices_offline

    # Store info in a dictionary for export
    tenant_token_device_info[tenant] = {'Tenant-Name': tenant_name, 'Enabled-Tokens': enabled_tokens, 'Disabled-Tokens':disabled_tokens, 'Total-Tokens':total_tokens, 'Devices-Online': devices_online, 'Devices-Offline': devices_offline, 'Total-Devices': total_devices} 
    # Store info in an array for export
    tenant_token_device_info_arr.append({'Flock-ID': tenant, 'Tenant-Name': tenant_name, 'Enabled-Tokens': enabled_tokens, 'Disabled-Tokens':disabled_tokens, 'Total-Tokens':total_tokens, 'Devices-Online': devices_online, 'Devices-Offline': devices_offline, 'Total-Devices': total_devices}) 
  
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
  


# print(json.dumps(all_tenants_summary(), indent=4)) # Gives all the information in json format
# print(json.dumps(all_tenant_tokens_info(all_tenants_summary()), indent=4))
# print(json.dumps(all_tenant_devices_info(all_tenants_summary()), indent=4))
# print(all_tenant_token_device_info(all_tenants_summary(),"array"))
