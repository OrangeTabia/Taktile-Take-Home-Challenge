# requests library which is similar to JS fetch
import requests
# To work with the environment variables
import os
# To work with the files
import sys

# For local dev
from dotenv import load_dotenv 
# loading variables from .env file
load_dotenv() 

# API key comes from environment variables added in GitHub Actions
TAKTILE_API_KEY = os.getenv("TAKTILE_API_KEY")
TAKTILE_URL = "https://eu-central-1.taktile-org.decide.taktile.com"
ORGANIZATION_NAME = "NB36"
REQ_HEADERS = {
  "X-Api-Key": TAKTILE_API_KEY,
  "accept": "application/json",
  "Content-Type": "application/json"
}


# Fetch the file name passed as argument
# TODO: add the org_name as an arg
file_path = sys.argv[1]

print("Processing file path: ", file_path)

# Only use the name of the file (remove the file extension and the location of the file)
file_name = file_path.split('/')[-1].split('.py')[0]

print("File name", file_name)

# Fetch the file content
def get_code_content(file_path):
  with open(file_path, 'r') as f:
    return f.read()


# method to get the flow_id by specific org name
def get_flow_ids(org_name = ORGANIZATION_NAME):
  """
  Return a list of the flow ids for a given organization
  """
  print(f"Accessing flows for the organization {org_name}")
  url = f"{TAKTILE_URL}/run/api/v1/flows/list-decision-graphs/sandbox/decide"
  data = {
    "organization_name": org_name
  }
  body = {
    "data": data, 
    "metadata": {
      "version": "v1.0",
      "entity_id": "string"
    },
    "control": {
      "execution_mode": "sync"
    }
  }
  response = requests.post(url, headers=REQ_HEADERS, json=body)
  if response.status_code == 200:
    response_json = response.json()
    print(f"{response_json['data']['message']}")
    # Only return the flow ids
    return [flow["flow_id"] for flow in response_json["data"]["flows"]]
  else: 
    print(f"Failed to retrieve flow_id. Error: {response.text}")


# method to get the graph by accessing all nodes from decision graph 
# associated with the flow id
def get_graph(flow_id): 
  """
  Return the graph (a list of nodes) for a given flow
  """
  print(f"Accessing graph for {flow_id}")
  url = f"{TAKTILE_URL}/run/api/v1/flows/get-decision-graph/sandbox/decide"
  data = {
    "flow_id": flow_id
  }
  body = {
    "data": data,
      "metadata": {
      "version": "v1.0",
      "entity_id": "string"
    },
    "control": {
      "execution_mode": "sync"
    }
  }
  response = requests.post(url, headers=REQ_HEADERS, json=body)
  if response.status_code== 200:
    response_json = response.json()
    print(f"{response_json['data']['message']}")
    return response_json["data"]["graph"]
  else: 
    print(f"Failed to retrieve the graph from {flow_id}. Error: {response.text}")


# method to patch code changes in a specific node
def update_code_node(flow_id, node_id, code_content): 

  """
  Updates the node code contents.
  NOTE: Does not do any validation to see if there are meaningful differences in the contents. 
  This is because we assume that there's a diffed file that's passed in
  """

  print(f"Updating the node: {node_id} with new source code")
  url = f"{TAKTILE_URL}/run/api/v1/flows/patch-decision-graph/sandbox/decide"
  headers = REQ_HEADERS
  data = {
    "flow_id": flow_id, 
    "node_id": node_id, 
    "src_code": code_content 
  }
  body = {
     "data": data,
     "metadata": {
        "version": "v1.0",
        "entity_id": "string"
      },
      "control": {
        "execution_mode": "sync"
      }
  }
  response = requests.post(url, headers=headers, json=body)
  if response.status_code == 200:
    print(f"Success! \n {response.json()['data']['message']} {node_id}")
  else: 
    print(f"Failed to update Code Node {node_id}. Error: {response.text}")




if __name__ == "__main__":
    
    # This represents the flow-node pairs that need to have a node updated by the new code change
    matching_node_pairs = []
    
    # First, get all of the flow ids
    flow_ids = get_flow_ids()

    # Then get all of the code nodes (by type) that match the name of the current file
    for flow_id in flow_ids: 
      nodes = get_graph(flow_id)

      for node in nodes: 
        if node['node_type'] == 'code_node' and node['node_name'] == file_name: 
          print("Found a match!")
          matching_node_pairs.append((flow_id, node['node_id']))

    # Then update all of the flow, node pairs that have the file name matching
    file_content = get_code_content(file_path)
    for flow_id, node_id in matching_node_pairs: 
      update_code_node(flow_id, node_id, file_content)

