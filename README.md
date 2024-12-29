
# Toy Blockchain Demo

A minimal toy example of block mining and chain verification in Python.

## Features

-   **Block**: Holds data, timestamp, previous hash, nonce, and a computed hash.
-   **Blockchain**: Creates a genesis block, adds and mines new blocks, and validates the entire chain.

## Quick Start

1.  **Clone**:
    `git clone https://github.com/your-username/toy-blockchain-demo.git` 
    
2.  **Run**:
    `python demo_mining.py` 
    
3.  **Observe**: Watch blocks get mined and see the chain validated.

## Adjust Difficulty

Inside `main()` of **demo_mining.py**:
`def main():
    difficulty = 5  # Increase or decrease as desired
    ...`
