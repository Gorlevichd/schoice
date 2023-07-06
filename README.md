# schoice

Small Python project for Social Choice calculations

Consists of one big class:

For now, the package works only with tasks that are formulated as follows:

| 5 | 3 | 5 | 4 |
|:-:|:-:|:-:|:-:|
| a | b | c | d |
| b | c | d | a |

Social choice class takes 2 dimensional list of rankings as in table and corresponding numbers of voters (first row of the table)

For use cases see docs/Docs.md

## Installation 

To install package run:

`pip install git+https://github.com/Gorlevichd/schoice.git`

Package requires `numpy`.