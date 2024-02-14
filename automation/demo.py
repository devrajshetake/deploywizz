import requests
import json

def get_csrf_crumb(url, username, password):
    # Jenkins API endpoint for obtaining CSRF crumb
    api_url = f"{url}/crumbIssuer/api/json"

    # Perform GET request to obtain the CSRF crumb
    response = requests.get(api_url, auth=(username, password))
    # print(response.text)

    # Check response status
    if response.status_code == 200:
        crumb = response.json()
        return crumb['crumb']
    else:
        print(f"Failed to obtain CSRF crumb. Status code: {response.status_code}")
        return None

def create_jenkins_agent(url, username, password, agent_name, remote_root, ssh_host, ssh_port, ssh_credentials_id):
    # Obtain CSRF crumb
    crumb = get_csrf_crumb(url, username, password)

    if not crumb:
        return

    # Jenkins API endpoint for creating a new agent
    api_url = f"{url}/computer/doCreateItem?name={agent_name}"

    # JSON configuration for the agent with SSH launcher
    agent_config_json = {
        "name": agent_name,
        "description": "",
        "remoteFS": remote_root,
        "numExecutors": 1,
        "mode": "NORMAL",
        "retentionStrategy": {"class": "hudson.slaves.RetentionStrategy$Always"},
        "launcher": {
            "class": "hudson.plugins.sshslaves.SSHLauncher",
            "plugin": "ssh-slaves@1.31.0",
            "host": ssh_host,
            "port": ssh_port,
            "credentialsId": ssh_credentials_id,
            "maxNumRetries": 0,
            "retryWaitTime": 0,
            "sshHostKeyVerificationStrategy": {
                "class": "hudson.plugins.sshslaves.verifiers.NonVerifyingKeyVerificationStrategy"
            }
        },
        "label": "",
        "nodeProperties": {},
        "userId": username,
        'Jenkins-Crumb': crumb
    }

    # Headers for authentication and CSRF crumb
    headers = {'Content-Type': 'application/json', 'Jenkins-Crumb': crumb}

    # Perform POST request to create the agent
    response = requests.post(api_url, auth=(username, password), headers=headers, json=agent_config_json)

    # Check response status
    if response.status_code == 200:
        print(f"Jenkins agent '{agent_name}' created successfully.")
    else:
        print(f"Failed to create Jenkins agent. Status code: {response.status_code}")
        print(response.text)

# Example usage
jenkins_url = 'http://98.70.112.27:8080/'
jenkins_username = 'devraj'
jenkins_password = '11393f9f7775d49d3ed559b131e51fc2a4'
agent_name = 'test2'
remote_root = 'home/jenkins'
ssh_host = '20.244.84.147'
ssh_port = '22'
ssh_credentials_id = 'test1_vm'

create_jenkins_agent(jenkins_url, jenkins_username, jenkins_password, agent_name, remote_root, ssh_host, ssh_port, ssh_credentials_id)
