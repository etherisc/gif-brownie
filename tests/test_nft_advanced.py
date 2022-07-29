import brownie
import pytest

ZERO_ADDRESS = '0x0000000000000000000000000000000000000000'

# enforce function isolation for tests below
@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


def test_mint_event(nft, owner, user1):
    tx = nft.mint(user1, {'from': owner})
    tokenId = tx.return_value

    print(tx.info())

    # check event from minting
    assert 'Transfer' in tx.events
    assert len(tx.events['Transfer']) == 1

    # check event attributes
    transferEvent = tx.events['Transfer'][0]
    assert transferEvent['from'] == ZERO_ADDRESS
    assert transferEvent['to'] == user1
    assert transferEvent['tokenId'] == tokenId


def test_mint_not_owner(nft, owner, user1):
    # verify that user1 may not mint its own token
    with brownie.reverts('Ownable: caller is not the owner'):
        nft.mint(user1, {'from': user1})


def test_transfer_not_owner(nft, owner, user1, user2):
    tx = nft.mint(user1, {'from': owner})
    tokenId = tx.return_value

    assert nft.balanceOf(user1) == 1
    assert nft.ownerOf(tokenId) == user1

    # verify that user2 cannot take away token from user1
    with brownie.reverts('ERC721: caller is not token owner nor approved'):
        nft.safeTransferFrom(
            user1,
            user2,
            tokenId,
            {'from': user2}
        )
