from brownie import FundMe, MockV3Aggregator, network, config
from scripts.helpful_scripts import (
    get_account,
    deploy_mocks,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)


def deploy_fund_me():
    account = get_account()
    # There is a Price Feed Contract on the Persistan Chains ... goerli, rinkby, mainnet ect.
    # There is not a Price Feed Contract on the Local BlockChains so we need to deploy a MOCK !!
    #   Development blockchain start with Nothing on the BlockChain
    #   Deploy Mock:
    #           1) Create a [test] folder under the Contracts folder for the [mock] Contract
    #           2) All [contracts] under the [contracts folder] will get compiled
    #           3) Create a [Mock] Solidity Contract by copying the code from [Chainlink-Mix] repository
    #                   1) Check out the Constructor in the Mock contract
    #           4) Compile
    #           5) Import [MockV3Aggregator] into Deploy script
    #           6) mock_contract_address = MockV3Aggregator.deploy(<constructors>, {"from": account}) and deploy to the Local Network
    #           7) price_feed_address = mock_contract_address.address

    if (
        network.show_active()
        not in LOCAL_BLOCKCHAIN_ENVIRONMENTS  # [I.E. A live BlockChain ]
    ):  # [I.E. ["development", "ganache-local"]
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[
            -1
        ].address  # Get current MockV3Aggregator contract address

    # We need to Pass the [Price Feed Contract Address when deploying our FundMe Contract]
    # As shown above if we are using a LOCAL_BLOCKCHAIN_ENVIRONMENTS environment [I.E. ["development", "ganache-local"]]
    # then we need to deploy a Mock of the Price Feed Contract onto the Local BlockChain
    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"Contract deployed to {fund_me.address}")
    return fund_me


def main():
    deploy_fund_me()
