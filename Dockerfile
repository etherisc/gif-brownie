# source for this dockerfile: https://github.com/eth-brownie/brownie
FROM python:3.10

EXPOSE 8000

# Set up code directory
RUN mkdir -p /usr/src/app/brownie-setup
WORKDIR /usr/src/app

# Install linux dependencies
RUN apt-get update && apt-get install -y libssl-dev npm

# Install Ganache chain
RUN npm install --global ganache-cli

# Install Brownie
RUN echo force-brownie-upgrade-0
RUN wget https://raw.githubusercontent.com/eth-brownie/brownie/master/requirements.txt

RUN pip install -r requirements.txt \
    && pip install eth-brownie \
    && pip install fastapi \
    && pip install uvicorn

# Add some aliases
RUN echo "alias rm='rm -i'" >> /root/.bashrc \
    && echo "alias l='ls -CF'" >> /root/.bashrc \
    && echo "alias la='ls -A'" >> /root/.bashrc \
    && echo "alias ll='ls -alF'" >> /root/.bashrc

# force installation of solc in docker image
# solc version is defined in brownie-config.yaml
WORKDIR /usr/src/app/brownie-setup
RUN echo force-dependency-upgrade-0

# download required solidity compiler
COPY .devcontainer/scripts/get_solidity.py .
RUN python get_solidity.py

# Initialize dummy project, copy brownie-config for dependencies and compile to download all dependencies
COPY brownie-config.yaml /usr/src/app/brownie-setup
RUN brownie init dummy \
    && cd dummy \
    && cp ../brownie-config.yaml . \
    && brownie compile --all \
    && cd ../../

WORKDIR /projects

# Install starship.rs prompt
RUN curl -fsSL https://starship.rs/install.sh | sh -s -- --yes 
RUN echo "eval \"\$(starship init bash)\"" >> ~/.bashrc && echo "eval \"\$(starship init zsh)\"" >> ~/.zshrc

CMD [ "bash" ]