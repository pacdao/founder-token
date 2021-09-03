from brownie import *
import brownie.network 

def main():
    if network.show_active() == 'development':
        deployer = accounts[0]
        publish_source = False
    else:
        deployer = accounts.load('husky')
        publish_source = True
    
    beneficiary_address = deployer
    return PACFounder.deploy(Wei('.001 ether'), Wei('.001 ether'), beneficiary_address, {"from": deployer}, publish_source=publish_source)
