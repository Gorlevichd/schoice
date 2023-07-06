#pylint: skip-file
import pytest
import numpy as np
from src.schoice import *


@pytest.fixture()
def matrix1():
    voters = [6, 3, 4, 4]
    ranking = [
        ["a", "b", "c"],
        ["c", "a", "b"],
        ["b", "a", "c"],
        ["b", "c", "a"]
    ]
    return RankingMatrix(ranking, voters)


@pytest.fixture()
def matrix2():
    voters = [1, 4, 1, 3]
    ranking = [
        ["a", "b", "c", "d", "e"],
        ["c", "d", "b", "e", "a"],
        ["e", "a", "d", "b", "c"],
        ["e", "a", "b", "d", "c"]
    ]
    return RankingMatrix(ranking, voters)


@pytest.fixture()
def matrix3():
    voters = [5, 3, 5, 4]
    ranking = [
        ["a", "d", "c", "b"],
        ["a", "d", "b", "c"],
        ["b", "c", "d", "a"],
        ["c", "d", "b", "a"]
    ]
    return RankingMatrix(ranking, voters)


def test1(matrix1):
    
    ## Condorcet
    condorcet_result = condorcet_rule(matrix1)
    assert condorcet_result[0].item() == "a"
    assert np.array_equal(condorcet_result[1], np.array(["a", "b", "c"]))
    assert np.array_equal(
        condorcet_result[2], 
        np.array([
            [1, 1, 1],
            [-1, 1, 1],
            [-1, -1, 1]
    ])
    )

    ## Copeland
    copeland_result = copeland_rule(matrix1)
    assert copeland_result[0].item() == "a"
    assert np.array_equal(copeland_result[1], np.array(["a", "b", "c"]))
    assert np.array_equal(copeland_result[2], np.array([2, 0, -2]))

    ## Simpson
    simpson_result = simpson_rule(matrix1)
    assert simpson_result[0].item() == "a"
    assert np.array_equal(simpson_result[1], np.array(["a", "b", "c"]))
    assert np.array_equal(simpson_result[2], np.array([9, 8, 3]))

    ## Borda
    borda_result = scoring_rule(matrix1)
    assert borda_result[0].item() == "b"
    assert np.array_equal(borda_result[1], np.array(["a", "b", "c"]))
    assert np.array_equal(borda_result[2], np.array([19, 22, 10]))

    ## Plurality
    plurality_result = plurality_rule(matrix1)
    assert plurality_result[0] == 1
    assert plurality_result[1].item() == "b"
    assert np.array_equal(plurality_result[2], np.array(["a", "b", "c"]))
    assert np.array_equal(plurality_result[3], np.array([6, 8, 3]))

    ## Runoff
    runoff_result = plurality_rule(matrix1, runoff = True)
    assert runoff_result[0] == 2
    assert runoff_result[1].item() == "a"
    assert np.array_equal(runoff_result[2], np.array(["a", "b"]))
    assert np.array_equal(runoff_result[3], np.array([9, 8]))


def test2(matrix2):

    ## Condorcet
    condorcet_result = condorcet_rule(matrix2)
    assert np.size(condorcet_result[0]) == 0
    assert np.array_equal(condorcet_result[1], np.array(["a", "b", "c", "d", "e"]))
    assert np.array_equal(condorcet_result[2], np.array([
        [1, 1, 1, 1, -1],
        [-1, 1, 1, -1, 1],
        [-1, -1, 1, 1, 1],
        [-1, 1, -1, 1, 1],
        [1, -1, - 1, -1, 1]
    ]))

    ## Copeland
    copeland_result = copeland_rule(matrix2)
    assert copeland_result[0].item() == "a"
    assert np.array_equal(copeland_result[1], np.array(["a", "b", "c", "d", "e"]))
    assert np.array_equal(copeland_result[2], np.array([2, 0, 0, 0, -2]))

    ## Simpson
    simpson_result = simpson_rule(matrix2)
    assert np.array_equal(simpson_result[0], ["b", "c", "d", "e"])
    assert np.array_equal(simpson_result[1], np.array(["a", "b", "c", "d", "e"]))
    assert np.array_equal(simpson_result[2], np.array([1, 4, 4, 4, 4]))

    ## Borda
    borda_result = scoring_rule(matrix2)
    assert borda_result[0].item() == "e"
    assert np.array_equal(borda_result[1], np.array(["a", "b", "c", "d", "e"]))
    assert np.array_equal(borda_result[2], np.array([16, 18, 18, 18, 20]))

    ## Scoring, custom weights
    scoring_result = scoring_rule(matrix2, weights = [6, 7, 8, 9, 10])
    assert scoring_result[0].item() == "e"
    assert np.array_equal(scoring_result[1], np.array(["a", "b", "c", "d", "e"]))
    assert np.array_equal(scoring_result[2], np.array([70, 72, 72, 72, 74]))

    ## Plurality
    plurality_result = plurality_rule(matrix2)
    assert plurality_result[0] == 1
    assert np.array_equal(plurality_result[1], np.array(["c", "e"]))
    assert np.array_equal(plurality_result[2], np.array(["a", "b", "c", "d", "e"]))
    assert np.array_equal(plurality_result[3], np.array([1, 0, 4, 0, 4]))

    # Runoff
    runoff_result = plurality_rule(matrix2, runoff = True)
    assert runoff_result[0] == 2
    assert runoff_result[1].item() == "c"
    assert np.array_equal(runoff_result[2], np.array(["c", "e"]))
    assert np.array_equal(runoff_result[3], np.array([5, 4]))


def test3(matrix3):

    ## Condorcet
    condorcet_result = condorcet_rule(matrix3)
    assert condorcet_result[0].item() == "c"
    assert np.array_equal(condorcet_result[1], np.array(["a", "b", "c", "d"]))
    assert np.array_equal(condorcet_result[2], np.array([
        [1, -1, -1, -1],
        [1, 1, -1, -1],
        [1, 1, 1, 1],
        [1, 1, -1, 1]
    ]))

    ## Copeland
    copeland_result = copeland_rule(matrix3)
    assert copeland_result[0].item() == "c"
    assert np.array_equal(copeland_result[1], np.array(["a", "b", "c", "d"]))
    assert np.array_equal(copeland_result[2], np.array([-3, -1, 3, 1]))

    ## Simpson
    simpson_result = simpson_rule(matrix3)
    assert simpson_result[0].item() == "c"
    assert np.array_equal(simpson_result[1], np.array(["a", "b", "c", "d"]))
    assert np.array_equal(simpson_result[2], np.array([8, 5, 9, 8]))

    ## Borda
    borda_result = scoring_rule(matrix3)
    assert borda_result[0].item() == "d"
    assert np.array_equal(borda_result[1], np.array(["a", "b", "c", "d"]))
    assert np.array_equal(borda_result[2], np.array([24, 22, 27, 29]))

    ## Plurality
    plurality_result = plurality_rule(matrix3)
    assert plurality_result[0] == 1
    assert plurality_result[1].item() == "a"
    assert np.array_equal(plurality_result[2], np.array(["a", "b", "c", "d"]))
    assert np.array_equal(plurality_result[3], np.array([8, 5, 4, 0]))

    ## Runoff 
    runoff_result = plurality_rule(matrix3, runoff = True)
    assert runoff_result[0] == 2
    assert runoff_result[1].item() == "b"
    assert np.array_equal(runoff_result[2], np.array(["a", "b"]))
    assert np.array_equal(runoff_result[3], np.array([8, 9]))