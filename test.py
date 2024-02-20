from jenkinsapi.jenkins import Jenkins

# Jenkins server URL and credentials
jenkins_url = 'http://98.70.112.27:8080/'
username = 'devraj'
password = 'bvsj5208'

# Connect to Jenkins server
jenkins = Jenkins(jenkins_url, username, password)

# Node configuration
node_name = 'ssh-node'
remote_fs = '/home/jenkins'
num_executors = 1
labels = 'linux ssh'
host = '20.244.84.147'
credentials_id = 'test_2vm'

# SSH launcher configuration
launcher_dict = {
    'stapler-class': 'hudson.plugins.sshslaves.SSHLauncher',
    'host': host,
    'credentialsId': credentials_id,
    'port': 444,
    'javaPath': '/usr/bin/java',  # Example javaPath
    'prefixStartSlaveCmd': '',
    'suffixStartSlaveCmd': '',
    'launchTimeoutSeconds': '120',
    'maxNumRetries': '10',
    'retryWaitTime': '15'
}

# Additional SSH node properties
additional_props = {
    'stapler-class': 'hudson.plugins.sshslaves.SSHLauncher\$SSHDescriptor',
    'strategies': [
        {'stapler-class': 'hudson.slaves.RetentionStrategy\$Always'},
        {'stapler-class': 'jenkins.slaves.JNLPLauncher\$JNLP'},
        {'stapler-class': 'hudson.plugins.sshslaves.verifiers.NonVerifyingKeyVerificationStrategy'}
    ],
    'launcher': launcher_dict
}

# Create SSH node
jenkins.create_node(node_name, num_executors, remote_fs, labels, launcher='hudson.plugins.sshslaves.SSHLauncher',
                    launcher_params=launcher_dict, node_properties=additional_props)
