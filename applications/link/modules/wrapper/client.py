# coding: utf-8
from address import Keypair, Address
from builder import Builder

class Client:

    def __init__(self, private_key=None, address=None, api_server=''):
        if private_key==None and address==None:
            raise Exception("private key and address can't both be none")
        elif private_key==None:
            self.api_server = api_server
            kp = Keypair.from_address(address)
            self.address = address
        elif address==None:
            self.private_key=private_key
            self.api_server=api_server
            self.address=Keypair.from_seed(private_key).address().decode()

        # return Keypair.from_seed(private_key)

    def set_api_server(self, api_server):
        self.api_server=api_server

    def fund(self, destination, amount):
        builder = Builder(secret=self.private_key, network=self.api_server)
        try:
            builder.append_create_account_op(destination=destination,starting_balance=amount)
            builder.sign()
            builder.submit()
        except:
            raise Exception('Unknon error')


    def pay_to(self, destination, amount, asset_code=None, asset_issuer=None):
        builder = Builder(secret=self.private_key, network=self.api_server)
        if asset_code:
            builder.append_payment_op(destination=destination, amount=amount, asset_type=asset_code, asset_issuer=asset_issuer)
        else:
            builder.append_payment_op(destination=destination, amount=amount)
        builder.sign()
        result = builder.submit()

    def get_info(self, address=''):
        if address=='':
            address = Address(address=self.address, network=self.api_server)
        else:
            address = Address(address=address, network=self.api_server)
        info=address.get()
        return info


    def get_balances(self, address=''):
        if address=='':
            address=Address(address=self.address,network=self.api_server)
        else:
            address = Address(address=address, network=self.api_server)
        address.get()
        self.balances=address.balances
        return address.balances

    def issue_asset(self, distributor_private_key, asset_code, amount):
        issuer_priv = self.private_key
        distributor_priv = distributor_private_key
        key_pairs = []

        issuer_address = Keypair.from_seed(issuer_priv).address().decode()
        distributor_address = Keypair.from_seed(distributor_priv).address().decode()

        builder = Builder(secret=distributor_priv, network=self.api_server)
        builder.append_trust_op(destination=issuer_address, code=asset_code, limit=amount)
        builder.sign()
        builder.submit()

        builder = Builder(secret=issuer_priv, network=self.api_server)
        builder.append_payment_op(destination=distributor_address, amount=amount, asset_type=asset_code,
                                  asset_issuer=issuer_address)
        builder.sign()
        result = builder.submit()
        return result

    def trust(self, issuer_address, asset_code, limit=None):
        builder = Builder(secret=self.private_key, network=self.api_server)
        builder.append_trust_op(destination=issuer_address, code=asset_code, limit=limit)
        builder.sign()
        builder.submit()