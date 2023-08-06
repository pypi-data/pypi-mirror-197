import xmlrpc.client

# create a client instance and call the remote function
proxy = xmlrpc.client.ServerProxy('http://localhost:8000')
result = proxy.add(10, 3)

print(result)  # prints 5
