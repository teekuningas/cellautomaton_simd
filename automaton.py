import numpy as np
from enum import Enum


class Rule2DBlock:
    """Base class for 2D block rules."""

    def apply_block(self, block):
        """Apply rule to a single quad."""
        raise Exception("Not implemented.")

    def apply(self, state, idx):
        """Apply rule to data."""

        data = state.data
        n_rows = data.shape[0]
        n_columns = data.shape[1]

        if idx % 2 == 0:
            blocks = np.empty((int(n_rows/2), int(n_columns/2)), dtype=np.ndarray)
        else:
            blocks = np.empty((int(n_rows/2) - 1, int(n_columns/2) - 1), dtype=np.ndarray)

        for row_idx in range(n_rows):
            for column_idx in range(n_columns):
                if idx % 2 == 0:
                    if row_idx % 2 == 0 and column_idx % 2 == 0:
                        blocks[int(row_idx/2), int(column_idx/2)] = data[row_idx:row_idx+2, column_idx:column_idx+2]
                else:
                    if row_idx % 2 == 1 and row_idx < n_rows - 1 and column_idx % 2 == 1 and column_idx < n_columns - 1:
                        blocks[int((row_idx-1)/2), int((column_idx-1)/2)] = data[row_idx:row_idx+2, column_idx:column_idx+2]

        new_data = np.copy(data)
        for block_row_idx in range(blocks.shape[0]):
            for block_column_idx in range(blocks.shape[1]):
                if idx % 2 == 0:
                    new_data[2*block_row_idx:(2*block_row_idx+2), 2*block_column_idx:(2*block_column_idx+2)] = (
                        self.apply_block(blocks[block_row_idx, block_column_idx])
                    )
                else:
                    new_data[(2*block_row_idx+1):(2*block_row_idx+3), (2*block_column_idx+1):(2*block_column_idx+3)] = (
                        self.apply_block(blocks[block_row_idx, block_column_idx])
                    )

        return State2D(new_data)


class State2D:
    """Stores a state."""

    def __init__(self, data):
        if data.shape[0] % 2 != 0:
            raise Exception('Shape[0] should be divisible by 2')

        if data.shape[1] % 2 != 0:
            raise Exception('Shape[1] should be divisible by 2')

        self.data = data


class RuleSimulation(Rule2DBlock):
    """Implementation of Gas simulation."""

    RULES = [
        ### collision rules
        (np.array([
            ['x', 'o'], 
            ['o', 'o']
        ]),
        np.array([
            ['o', 'o'], 
            ['o', 'x']
        ])),
        ###
        (np.array([
            ['o', 'o'], 
            ['x', 'o']
        ]),
        np.array([
            ['o', 'x'], 
            ['o', 'o']
        ])),
        ###
        (np.array([
            ['o', 'o'], 
            ['x', 'x']
        ]),
        np.array([
            ['x', 'x'], 
            ['o', 'o']
        ])),
        ###
        (np.array([
            ['o', 'x'], 
            ['o', 'x']
        ]),
        np.array([
            ['x', 'o'], 
            ['x', 'o']
        ])),
        ###
        (np.array([
            ['o', 'x'], 
            ['x', 'o']
        ]),
        np.array([
            ['x', 'o'], 
            ['o', 'x']
        ])),
        ###
        (np.array([
            ['o', 'x'], 
            ['x', 'x']
        ]),
        np.array([
            ['x', 'x'], 
            ['x', 'o']
        ])),
        ###
        (np.array([
            ['x', 'x'], 
            ['o', 'x']
        ]),
        np.array([
            ['x', 'o'], 
            ['x', 'x']
        ])),
        ### wall rules
        (np.array([
            ['o', 'x'], 
            ['w', 'w']
        ]),
        np.array([
            ['x', 'o'], 
            ['w', 'w']
        ])),
        ###
        (np.array([
            ['w', 'x'], 
            ['w', 'o']
        ]),
        np.array([
            ['w', 'o'], 
            ['w', 'x']
        ])),
        ###
        (np.array([
            ['w', 'w'], 
            ['x', 'o']
        ]),
        np.array([
            ['w', 'w'], 
            ['o', 'x']
        ])),
        ###
        (np.array([
            ['o', 'w'], 
            ['x', 'w']
        ]),
        np.array([
            ['x', 'w'], 
            ['o', 'w']
        ])),
    ]

    def apply_block(self, block):
        """Apply rule to a single block."""
        for rule in self.RULES:
            if np.array_equal(block, rule[0]):
                return rule[1]
            if np.array_equal(block, rule[1]):
                return rule[0]
        return block


def apply_rule(state, idx):
    """Given state, compute next one."""
    s = State2D(state)
    rule = RuleSimulation()
    return rule.apply(s, idx).data
    
