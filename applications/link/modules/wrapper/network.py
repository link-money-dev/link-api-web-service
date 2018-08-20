# coding: utf-8
from .utils import xdr_hash

NETWORKS = {'PUBLIC': 'Fotono Main Net; 2018-8-10',
            'TESTNET': 'Fotono Test Network; 2017-1-1',
            'LOCAL': 'Fotono Network Main Net; 2018-3-15',
            'STELLAR': 'Public Global Stellar Network ; September 2015'
            }


class Network(object):
    def __init__(self, passphrase=None):
        if passphrase is None:
            self.passphrase = NETWORKS['TESTNET']
        else:
            self.passphrase = passphrase

    def network_id(self):
        return xdr_hash(self.passphrase.encode())


def test_network():
    return Network(NETWORKS['TESTNET'])


def live_network():
    return Network(NETWORKS['PUBLIC'])

def local_network():
    return Network(NETWORKS['LOCALNET'])

def stellar_network():
    return Network(NETWORKS['STELLAR'])