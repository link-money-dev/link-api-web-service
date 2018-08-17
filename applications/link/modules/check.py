def check_validity_of_address(address):
    try:
        address=str(address)
        if len(address) != 56:
            return False
        elif address.upper() != address:
            return False
        elif address[0] != 'G':
            return False
        else:
            return True
    except:
        return False