import xmlrpc.client

def execute_remote_function(url, function_name, *args):
    """
    Executes a remote function using XML-RPC.
    :param url: The URL of the remote XML-RPC server.
    :param function_name: The name of the remote function to execute.
    :param args: The arguments to pass to the remote function.
    :return: The result of the remote function.
    """
    proxy = xmlrpc.client.ServerProxy(url)
    return getattr(proxy, function_name)(*args)
