# Airdrop-helper

A tool to measure participation in the Olas ecosystem

> :warning: **Warning** <br />
> The code within this repository is provided without any warranties. It is important to note that the code has not been audited for potential security vulnerabilities.
> Valory AG is not responsible for any airdrops resulting from use of this resource.
> Exercise caution and use this code at your own risk. Please refer to the [LICENSE](./LICENSE) file for details about the terms and conditions.

## Preparation

1. Clone this repo

2. Install [Python 3.10](https://www.python.org/downloads/) and [Poetry](https://python-poetry.org/docs/)

3. Prepare the virtual environment and install dependencies
    ```bash
    poetry shell
    poetry install
    ```

4. Set environment variables:
    ```bash
    cp sample.env .env
    ```
    And populate the environment variables as required.

## Run an existing airdrop example

1. Explore the airdrop example in the script [airdrop_example.py](https://github.com/valory-xyz/airdrop-helper/blob/main/airdrop_example.py).

2. Adjust the airdrop parameters and run the script like:
    > **Note** <br />
    > Some of the tools require API keys or RPCs to be set in a .env file. Read the example scripts for more information.
    ```bash
    python airdrop_example.py
    ```

## Create your own airdrop logic

1. Explore the examples in the script [basic_example.py](https://github.com/valory-xyz/airdrop-helper/blob/main/basic_example.py), for example:

    > **Note** <br />
    > Some of the tools require API keys or RPCs to be set in a .env file. Read the example scripts for more information.

    ```python
    # Instantiate the Olas airdrop helper
    olas = Olas()

    # Get all Contribute users that have at least 50k points
    contributors = olas.contributors.get(min_points=50000)

    # Get veOLAS holders at a given block with a minimum voting power of 100
    veolas_holders = olas.veolas_holders.get(block=19263301, min_power=100)
    ``````

2. Modify the script to your needs and run it like:
    ```bash
    python basic_example.py
    ```
