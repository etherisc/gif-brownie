# GIF Brownie

This repository contains a GIF opinionated dockerized Solidity development environment based on [Brownie](https://eth-brownie.readthedocs.io)

## Prerequisites

This readme is based on the following assumption 
* You are familiar with bash shell commands
* You are familiar with Docker 
* You are familiar with git
* Your installation includes bash, Docker and git

PLEASE NOTE: The shell commands below are written for a bash shell.
If you are working on a Windows box you may use WSL2, Git Bash on Windows or similar. 

## Create the Docker Image

Start with cloning the `gif-brownie` repository.

```bash
git clone https://github.com/etherisc/gif-brownie.git
cd gif-brownie
```

Build the Brownie docker image.

```bash
docker build . -t brownie
```

## Example Usage

### Create a new Project

Start a new Brownie container.
```bash
docker run -it --rm -v $PWD:/projects brownie
```

In the container setup a new project.
```bash
brownie init <project-name>
```
The name `project-name` is used to create a new directory and create the brownie project structure inside.

### Compile and Test Smart Contracts

Start a new Brownie container.
```bash
docker run -it --rm -v $PWD:/projects brownie
```

In the container compile all contracts with all its dependencies.
```bash
brownie compile --all
```

To compile only the changed contracts/dependencies.
```bash
brownie compile
```

Run all test suites
```bash
brownie test
```

Run a specific test suite
```bash
brownie test tests/test_nft_simple.py
```

Run an individual test
```bash
brownie test tests/test_nft_advanced.py::test_transfer_not_owner
```

### Use Smart Contracts Interactively

Start a new Brownie container.
```bash
docker run -it --rm -v $PWD:/projects brownie
```

In the container start the Brownie console
```bash
brownie console
```

In the Brownie console deploy and use the DummyNFT token.
```bash
>>> 
owner = accounts[0]
user1 = accounts[1]
user2 = accounts[2]

# deploy nft
nft = DummyNFT.deploy({'from':owner})

# show transaction details
history[-1].info()

# mint token for user1
tx = nft.mint(user1, {'from': owner})
tokenId = tx.return_value

# show transaction details
tx.info()

# verify user1 is owner of the new token and check her balance
nft.ownerOf(tokenId) == user1
nft.balanceOf(user1)

exit()
```

### Start a Local Ganache Chain

As the brownie image contains an embedded [Ganache](https://trufflesuite.com/ganache/index.html) chain we can also use this image to create a Ganache container as shown below.

```bash
docker run -d -p 7545:7545 --name ganache brownie ganache-cli \
    --mnemonic "candy maple cake sugar pudding cream honey rich smooth crumble sweet treat" \
    --chainId 1234 \
    --port 7545 \
    -h "0.0.0.0"
```

The chosen setup deterministically creates addresses (and private keys) via a HD wallet with the mnemonic `"candy maple cake sugar pudding cream honey rich smooth crumble sweet treat"`.
Port `7545` is chosen to avoid conflicts with any productive local ethereum client that typically run on port 8545.

To connect with Metamaks using the mnemonic as secret recovery phrase.
As network parameter use `http://localhost:7545` as RPC URL and `1234` as Chain ID.

Use the commands below to stop and remove the ganace container.
```bash
docker stop ganache
docker rm ganache
```

### Use a Local Ganache Chain

TODO