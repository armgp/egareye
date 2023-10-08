import paramiko

host = "20.77.2.3"
port = 22  
username = "armgp"
password = "egareye123@pass"  

try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port=port, username=username, password=password, timeout=60)
    command = "python3 monitor.py skanda 5 hyderabad +917012496675"  

    stdin, stdout, stderr = ssh.exec_command(command, timeout=60)

    print("Output of 'monitor.py' script:")
    print(stdout.read().decode())

except Exception as e:
    print("An error occurred:", str(e))

finally:
    if ssh is not None:
        ssh.close()
