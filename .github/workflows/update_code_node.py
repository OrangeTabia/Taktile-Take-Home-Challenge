# requests library which is similar to JS fetch
import requests
# To work with the environment variables
import os
# To work with the files
import sys

TAKTILE_API_KEY = os.getenv("TAKTILE_API_KEY")
TAKTILE_URL = "https://eu-central-1.taktile-org.decide.taktile.com"

CODE_NODE_MAP = {
  # File Name -> [flow_id, node_id]
  "Multiply.py": ["flow_id_1", "code_node_id_1"], 
  "Summarize.py": ["flow_id_2", "code_node_id_2"], 
}

# Fetch the file name passed as argument
file_path = sys.argv[1]

# Fetch the file content
def get_code_content(file_path):
    with open(file_path, 'r') as f:
        return f.read()


def update_taketile_code_node(flow_id, node_id, code_content): 
  """
  Updates the node code contents.
  NOTE: Does not do any validation to see if there are meaningful differences in the contents
  """
  url = f"{TAKTILE_URL}/run/api/v1/flows/patch-decision-graph/sandbox/decide"
  headers = {
    # This should come from the environment variables, this should NOT be in plain text. 
    # THIS IS VERY VERY VERY VERY SENSITIVE
    "X-Api-Key": TAKTILE_API_KEY,
    "accept": "application/json",
    "Content-Type": "application/json"
  }
  data = {
    "flow_id": flow_id, 
    "node_id": node_id, 
    "src_code": code_content 
  }
  response = requests.post(url, headers=headers, json=data)
  if response.status_code == 200:
    print(f"Succesfully updated Code Node {node_id}")
  else: 
    print(f"Failed to update Code Node {node_id}. Error: {response.text}")


if file_path in CODE_NODE_MAP:
    code_content = get_code_content(file_path)
    flow_id, node_id = CODE_NODE_MAP[file_path]
    update_taketile_code_node(flow_id, node_id, code_content)
else:
    print(f"File {file_path} does not map to a known Code Node")

