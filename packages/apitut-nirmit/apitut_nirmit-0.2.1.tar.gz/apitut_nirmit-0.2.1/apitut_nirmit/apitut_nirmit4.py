import ipaddress

def iprangefinder(ipcidr):
    """
    Prints the network address, subnet mask, and list of available hosts for an IPv4 or IPv6 CIDR notation string.

    Args:
        ipcidr (str): A string in CIDR notation that represents an IPv4 or IPv6 network.

    Returns:
        str: An error message if the input is not a valid CIDR notation string.

    """
    try:    
        # Attempt to create an IPv4 or IPv6 address object from a CIDR notation string
        # 'strict=False' allows for network addresses with host bits set (e.g. '192.168.1.1/24')
        ip_network_obj = ipaddress.ip_network(ipcidr, strict=False)

        # Print the network address and the subnet mask of the object
        print(f"Network address: {ip_network_obj.network_address}")
        print(f"Subnet mask: {ip_network_obj.netmask}")

        # Print a list of available hosts on the network
        print("Available hosts:")
        for host in ip_network_obj.hosts():
            print(host)
    except ValueError:
        # If the CIDR notation string is not valid, return an error message
        return "Invalid input...Please write a valid input"

