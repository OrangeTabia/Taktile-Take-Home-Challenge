# requests library which is similar to JS fetch
import requests

def update_taketile_code_node(flow_id, node_id, code_content): 
  url = f"https://eu-central-1.taktile-org.decide.taktile.com/run/api/v1/flows/patch-decision-graph/sandbox/decide"
  headers = {
    # This should come from the environment variables, this should NOT be in plain text. 
    # THIS IS VERY VERY VERY VERY SENSITIVE
    "X-Api-Key": "c179117d-a4ce-4635-a268-b37d13668515",
    "accept": "application/json",
    "Content-Type": "application/json"
  }
  data = {
    "flow_id": flow_id, 
    "node_id": node_id, 
    "src_code": code_content 
  }
  response = requests.put(url, headers=headers, json=data)
  if response.status_code == 200:
    print(f"Succesfully updated Code Node {node_id}")
  else: 
    print(f"Failed to update Code Node {node_id}. Error: {response.text}")

code_node_map = {
  "Multiply.py": "code_node_id_1", 
  "Summarize.py": "code_node_id_2"
}



