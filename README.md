# Airdrop-helper

A tool to measure participation in the Olas ecosystem


## How to use

1. Clone this repo

2. Install [Python 3.10](https://www.python.org/downloads/) and [Poetry](https://python-poetry.org/docs/)

3. Prepare the virtual environment and install dependencies
    ```bash
    cd packages
    poetry shell
    poetry install
    ```

4. Explore the examples in the script at [packages/example.py](https://github.com/valory-xyz/airdrop-helper/blob/main/packages/example.py), for example:

    > [NOTE]
    > Some of the following tools require API keys or RPCs to be set in a .env file. Read the example script for more information.

    ```python
    # Instantiate the Olas airdrop helper
    olas = Olas()

    # Get all Contribute users that have at least 50k points
    contributors = olas.contributors.get(min_points=50000)

    # Get veOLAS holders at a given block
    veolas_holders = olas.veolas_holders.get(block=19263301)
    ``````

5. Modify the script to your needs and run it like:
    ```bash
    python packages/example.py
    ```