################################################
########     ip_utilities.py       #############
################################################


""" 
class ipaddress:
    def __init__(self, ipstr):
        self.ipstr = ipstr
 
    # strictly less than operator 
    def __lt__(self, other):
        s = [ int(seg) for seg in self.ipstr.split('.')]
        o = [ int(seg) for seg in other.ipstr.split('.')]
        for i in [0, 1, 2, 3]:
            if s[i] < o[i]:
                return True
            if s[i] > o[i]:
                return False
        return False
    
    # less than (or equal) operator   
    def __le__(self, other):
        s = [ int(seg) for seg in self.ipstr.split('.')]
        o = [ int(seg) for seg in other.ipstr.split('.')]
        for i in [0, 1, 2, 3]:
            if s[i] < o[i]:
                return True
            if s[i] > o[i]:
                return False
        return True
    
    # strictly greater than operator 
    def __gt__(self, other):
        return not (self <= other)

    # greater than (or equal) operator 
    def __ge__(self, other):
        return not (self < other)
"""


def ipv4_cidrlen_to_mask(len):

    """convert mask length to ip mask 

    Args:
        len: mask length
        
    Returns:
        netmask in the form xxx.xxx.xxx.xxx
    """

    mask = ''
    if not isinstance(len, int) or len < 0 or len > 32:
        print("error")
        return None
    for t in range(4):
        if len > 7:
            mask += '255.'
        else:
            dec = 255 - (2**(8 - len) - 1)
            mask += str(dec) + '.'
        len -= 8
        if len < 0:
            len = 0
    return mask[:-1]


# strictly less than operator 
def ipv4_lt(self, other):

    """compare two ip addresses: strictly less than operator 

    Args:
        self: left operand ip address
        self: right operand ip address
        
    Returns:
        True if self < other, False otherwise
    """

    s = [ int(seg) for seg in self.split('.')]
    o = [ int(seg) for seg in other.split('.')]
    for i in [0, 1, 2, 3]:
        if s[i] < o[i]:
            return True
        if s[i] > o[i]:
            return False
    return False


# less than (or equal) operator
def ipv4_le(self, other):

    """compare two ip addresses: less or equal operator 

    Args:
        self: left operand ip address
        self: right operand ip address
        
    Returns:
        True if self <= other, False otherwise
    """

    s = [ int(seg) for seg in self.split('.')]
    o = [ int(seg) for seg in other.split('.')]
    for i in [0, 1, 2, 3]:
        if s[i] < o[i]:
            return True
        if s[i] > o[i]:
            return False
    return True


# strictly greater than operator
def ipv4_gt(self, other):

    """compare two ip addresses: strictly greater than operator 

    Args:
        self: left operand ip address
        self: right operand ip address
        
    Returns:
        True if self > other, False otherwise
    """

    return not (ipv4_le(self, other))


# greater than (or equal) operator 
def ipv4_ge(self, other):

    """compare two ip addresses: greater or equal operator 

    Args:
        self: left operand ip address
        self: right operand ip address
        
    Returns:
        True if self >= other, False otherwise
    """

    return not (ipv4_lt(self, other))


def ipv4_max(ip_list):

    """returns the highest ip address from an ip list 

    Args:
        ip_list: array of ip addresses: ["ip1", "ip2", ...]
    
    Returns:
        highest ip address
    """

    ipmax = ip_list[0]
    for ip in ip_list:
        if ipv4_gt(ip, ipmax):
            ipmax = ip
    return ipmax


def ipv4_min(ip_list):

    """returns the lowest ip address from an ip list 

    Args:
        ip_list: array of ip addresses: ["ip1", "ip2", ...]
    
    Returns:
        lowest ip address
    """

    ipmin = ip_list[0]
    for ip in ip_list:
        if ipv4_lt(ip, ipmin):
            ipmin = ip
    return ipmin
