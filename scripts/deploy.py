from brownie import *
import brownie.network 
from brownie.network import priority_fee

def main():
    publish_source = False

    beneficiary_address = '0xf27AC88ac7e80487f21e5c2C847290b2AE5d7B8e'
    if network.show_active() == 'development':
        deployer = accounts[0]
        publish_source = False
        beneficiary_address = deployer
    elif network.show_active() in ['mainnet', 'mainnet-fork'] :
        if network.show_active() == 'mainnet':
            priority_fee("2 gwei")
            publish_source = True

        z = accounts.load('zcroo')
        deployer = accounts.load('minnow')

        z.transfer(deployer, .25 * 10 ** 18)
           
    else:
        deployer = accounts.load('husky')
        publish_source = True
    
    return PACFounder.deploy(beneficiary_address, {"from": deployer}, publish_source=publish_source)
