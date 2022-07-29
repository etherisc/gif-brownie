import brownie
import pytest

# test that don't impact each other
def test_deploy(nft, owner, user1, user2):

    assert nft.symbol() == "DNT"
    assert nft.tokens() == 0
    assert nft.balanceOf(owner) == 0

    assert user1 != user2
    assert nft.balanceOf(user1) == 0
    assert nft.balanceOf(user2) == 0

# enforce function isolation for tests below
@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass

def test_mint(nft, owner, user1):

    # mint nft for user 1
    tx = nft.mint(user1, {'from': owner})
    print(tx.info())

    # check user1 has this token
    tokenId = tx.return_value
    assert nft.tokens() == 1
    assert nft.balanceOf(owner) == 0
    assert nft.balanceOf(user1) == 1
    assert nft.ownerOf(tokenId) == user1


def test_transfer(nft, owner, user1, user2):

    # mint nft for user 1
    tx1 = nft.mint(user1, {'from': owner})
    print(tx1.info())

    tokenId = tx1.return_value
    assert nft.balanceOf(user1) == 1
    assert nft.balanceOf(user2) == 0
    assert nft.ownerOf(tokenId) == user1

    # user1 transfers token to user2
    tx2 = nft.safeTransferFrom(
        user1,
        user2,
        tokenId,
        {'from': user1}
    )
    print(tx2.info())
    
    # check user2 new has this token
    assert nft.tokens() == 1
    assert nft.balanceOf(user1) == 0
    assert nft.balanceOf(user2) == 1
    assert nft.ownerOf(tokenId) == user2
