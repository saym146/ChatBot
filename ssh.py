from paramiko import client
import getpass

class ssh:
    client = None
 
    def __init__(self, address, username, password):
        print("Connecting to server.")
        self.client = client.SSHClient()
        self.client.set_missing_host_key_policy(client.AutoAddPolicy())
        self.client.connect(address, username=username, password=password, look_for_keys=False)
 
    def sendCommand(self, command):
        if(self.client):
            stdin, stdout, stderr = self.client.exec_command(command)
            while not stdout.channel.exit_status_ready():
                # Print data when available
                if stdout.channel.recv_ready():
                    alldata = stdout.channel.recv(1024)
                    prevdata = b"1"
                    while prevdata:
                        prevdata = stdout.channel.recv(1024)
                        alldata += prevdata
 
                    print(str(alldata, "utf8"))
        else:
            print("Connection not opened.")

if __name__ == "__main__":
    try:
        ip,username = input("Host name or IP address: "),input("Login as: ")
        password=getpass.getpass(prompt="%s@%s's password: " % (username,ip), stream=None)
        sshclient = ssh(ip,username,password)
        while True:
            inp = input("Command: ")
            if inp == "quit":
                break
            sshclient.sendCommand(inp)
    except Exception as ex:
        print(ex.args)
