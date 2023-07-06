![image](https://github.com/Gorlevichd/schoice/assets/59909335/cac35d8a-8fd4-4b65-846b-b71ff1c21408)# schoice

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

For use cases please refer to the [Documentation](https://github.com/Gorlevichd/schoice/blob/main/docs/Docs.md)

## Acknowledgements

This project was majorly inspired by HSE Master's Microeconomics course taught by prof. Tatiana Mayskaya
