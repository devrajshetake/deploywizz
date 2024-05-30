from .models import VirtualMachine
import paramiko

PRIVATE_KEY_PATH = "C:\\Users\\dshetake\\OneDrive - Avaya\\Desktop\\cicd\\deploy\\test1_vm.pem"
class VMUtils():
    def __init__(self, vm : VirtualMachine) -> None:
        self.vm = vm
        try: 
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.file_path = PRIVATE_KEY_PATH
            self.pkey = paramiko.RSAKey.from_private_key_file(self.file_path)


            # self.client.connect(hostname=self.vm.public_ip, username="azureuser", key_filename=self.file_path)


            # # Execute the ls command
            # # Execute commands to gather system information
            # stdin, stdout, stderr = self.client.exec_command('nproc')
            # cpu_cores = stdout.read().decode().strip()

            # stdin, stdout, stderr = self.client.exec_command('df -h --total | grep "total" | awk \'{print $2}\'')
            # disk_size = stdout.read().decode().strip()

            # stdin, stdout, stderr = self.client.exec_command('free -h | awk \'/^Mem/ {print $2}\'')
            # ram = stdout.read().decode().strip()

            # stdin, stdout, stderr = self.client.exec_command('uname -m')
            # architecture = stdout.read().decode().strip()

            # # Close client connection
            # self.client.close()

            # print( {
            #     "CPU Cores": cpu_cores,
            #     "Total Disk Size": disk_size,
            #     "RAM": round(float(ram[:-2])),
            #     "Architecture": architecture
            # })
    


        except Exception as e:
            raise Exception("Error connecting the VM: " + str(e))

    
    def get_system_info(self):
        try:
            # self.client.connect(hostname=self.vm.public_ip, username="root", key_filename=self.file_path)
            self.client.connect(hostname=self.vm.public_ip, username="root", pkey=self.pkey, look_for_keys=False)

            

            stdin, stdout, stderr = self.client.exec_command('nproc')
            cpu_cores = stdout.read().decode().strip()

            stdin, stdout, stderr = self.client.exec_command('df -h --total | grep "total" | awk \'{print $2}\'')
            disk_size = stdout.read().decode().strip()

            stdin, stdout, stderr = self.client.exec_command('free -h | awk \'/^Mem/ {print $2}\'')
            ram = stdout.read().decode().strip()

            stdin, stdout, stderr = self.client.exec_command('uname -m')
            architecture = stdout.read().decode().strip()

            # Close client connection
            self.client.close()

            return {
                "cpus": cpu_cores,
                "memory": disk_size,
                "ram": ram,
                "architecture": architecture
            }
        except Exception as e:
            raise Exception("Error connecting the VM: " + str(e) + "While getting system info")
        
    def setup(self):
        try:
            self.client.connect(hostname=self.vm.public_ip, username="azureuser", key_filename=self.file_path)

            stdin, stdout, stderr = self.client.exec_command('add setup command here') # Change
        except Exception as e:
            raise Exception("Error connecting the VM: " + str(e))


# C:\Users\dshetake\OneDrive - Avaya\Desktop\cicd\deploy\test1_vm.pem



