# Installation

## Pre-Requisites

- Debian 11
- python3.10
- pip3.10
- cargo-update

## Install python3.10

1. Ensure that your system is updated and the required packages installed.

`sudo apt update && sudo apt upgrade -y`

1. Install the required dependencies:

`sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev`

1. get python3.10 tar.gz

`wget https://www.python.org/ftp/python/3.10.0/Python-3.10.0.tgz`

`tar -xf Python-3.10.*.tgz`

`cd Python-3.10.*/`

`./configure --enable-optimizations`

`make -j4`

`sudo make altinstall`

## **Install Cargo and Solc prerequisites**

1. `sudo apt install lsb-release wget software-properties-common gnupg pkg-config libssl-dev build-essential cmake git libboost-all-dev libjsoncpp-dev jq`

## Install rust

1. `wget -O rustup.sh https://sh.rustup.rs`
2. `bash rustup.sh -y`
3. `source "$HOME/.cargo/env"`

## Install cargo-update

`cargo install cargo-update`

## Install ziion cli

`sudo pip3.10 install ziion`

## Upgrade ziion cli

`sudo pip3.10 install ziion -U`

# How to use it

## ARM/AMD
`ziion --help`: Show help message and exit.
`ziion --version`: Show version message and exit.
`ziion list-metapackages`: List metapackages that can be updated with the cli and exit.
`ziion self-update`: Update ziion cli to latest version and exit.

## ARM
`ziion update [cargo|solc] [--dryrun]`: 
    - If cargo|solc packages are installed: Update cargo|solc packages to the latest version if needed.
    - If cargo|solc packages are not installed: Install latest version of cargo|solc packages. 
`ziion solc-select [version] [--install]`:
    - Changes solc's current version to be used.
    - if --install is provided the installation of the specified version is forced.
`ziion solc-select versions`: Shows installed version and the one which is currently in use.

## AMD
`ziion update [cargo] [--dryrun]`:
    - If cargo packages are installed: Update cargo packages to the latest version if needed.
    - If cargo packages are not installed: Install latest version of cargo packages. 
