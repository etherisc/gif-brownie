import pytest

from brownie.network import accounts
from brownie.network.account import Account

from brownie import DummyNFT

ACCOUNTS_MNEMONIC = 'candy maple cake sugar pudding cream honey rich smooth crumble sweet treat'

# setup stakeholder accounts
@pytest.fixture(scope="module")
def owner(accounts) -> Account:
    return getAccount(accounts, 0, "1 ether")

@pytest.fixture(scope="module")
def user1(accounts) -> Account:
    return getAccount(accounts, 1, "1 ether")

@pytest.fixture(scope="module")
def user2(accounts) -> Account:
    return getAccount(accounts, 2, "1 ether")

# setup nft contract
@pytest.fixture(scope="module")
def nft(owner) -> DummyNFT:
    return DummyNFT.deploy({'from': owner})

# helper functions
def getAccount(accounts, account_no, funding) -> Account:
    owner = accounts.from_mnemonic(
        ACCOUNTS_MNEMONIC,
        count=1,
        offset=account_no)

    accounts[account_no].transfer(owner, funding)
    return owner
