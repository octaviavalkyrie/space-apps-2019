from paramiko import SSHClient

from fabric import Connection

c = Connection(host='10.1.78.165', user='pi', port=22,
               connect_kwargs={'password': 'raspberry'})

while True:
    if(input() is 'a'):
        result = c.run('./rover')
        print(result.stdout)
