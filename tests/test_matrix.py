# pylint: skip-file

import pytest
import numpy as np
from src.schoice.matrix import RankingMatrix

@pytest.fixture()
def first_matrix_test():
    voters = (6, 3, 4, 4)
    ranking = [
        ["a", "b", "c"],
        ["b", "c", "a"],
        ["a", "c", "b"],
        ["b", "a", "c"]
        ]
    return ranking, voters


@pytest.fixture()
def second_matrix_test():
    # Should reduce dimensionality
    voters = (6, 3, 4, 4)
    ranking = [
        ["a", "b", "c"],
        ["b", "c", "a"],
        ["a", "b", "c"],
        ["b", "a", "c"]
    ]
    return ranking, voters


@pytest.fixture()
def error_cand_matrix():
    voters = (6, 3)
    ranking = [
        ["a", "b", "c"],
        ["z", "x", "y"]
    ]
    return ranking, voters


@pytest.fixture()
def error_dim_matrix():
    voters = (6, 3, 4)
    ranking = [
        ["a", "b"],
        ["b", "c"]
        ]
    return ranking, voters


@pytest.fixture
def unidim_matrix():
    voters = (6, 3, 4)
    ranking =  ["a", "b"]
    return voters, ranking


@pytest.fixture()
def add_matrix_1():
    add_candidates = ["c", "b", "a"]
    add_voters = [5]
    return add_candidates, add_voters


@pytest.fixture()
def add_matrix_1_expected():
    ranking = [
        ["a", "b", "c"],
        ["b", "c", "a"],
        ["a", "c", "b"],
        ["b", "a", "c"],
        ["c", "b", "a"],
    ]
    voters = [6, 3, 4, 4, 5]
    return RankingMatrix(ranking, voters)

@pytest.fixture()
def add_matrix_2():
    # Mutlidim
    add_candidates = [
        ["c", "b", "a"],
        ["c", "a", "b"]
        ]
    add_voters = [5, 4]
    return add_candidates, add_voters


@pytest.fixture()
def add_matrix_2_expected():
    ranking = [
        ["a", "b", "c"],
        ["b", "c", "a"],
        ["a", "c", "b"],
        ["b", "a", "c"],
        ["c", "b", "a"],
        ["c", "a", "b"]
        ]
    voters = (6, 3, 4, 4, 5, 4)
    return RankingMatrix(ranking, voters)


@pytest.fixture()
def add_matrix_3():
    # Non-unique
    add_candidates = ["b", "c", "a"]
    add_voters = [5]
    return add_candidates, add_voters


@pytest.fixture
def add_matrix_3_expected():
    voters = (6, 8, 4, 4)
    ranking = [
        ["a", "b", "c"],
        ["b", "c", "a"],
        ["a", "c", "b"],
        ["b", "a", "c"]
    ]
    return RankingMatrix(ranking, voters)

def test_matrix_1(first_matrix_test):
    ranking, voters = first_matrix_test
    matrix = RankingMatrix(ranking, voters)
    assert np.array_equal(matrix.voters, np.array([6, 3, 4, 4]))
    assert np.array_equal(matrix.ranking, np.array(ranking).T)
    assert np.array_equal(matrix.ranking_matrix, np.array([
        [0, 2, 0, 1],
        [1, 0, 2, 0],
        [2, 1, 1, 2]
    ]))
    assert np.array_equal(matrix.candidates, np.array(["a", "b", "c"]))


def test_matrix_2(second_matrix_test):
    ranking, voters = second_matrix_test
    matrix = RankingMatrix(ranking, voters)
    assert np.array_equal(matrix.voters, np.array([10, 3, 4]))
    assert np.array_equal(matrix.ranking, np.array([
        ["a", "b", "c"],
        ["b", "c", "a"],
        ["b", "a", "c"]
    ]).T)
    assert np.array_equal(matrix.ranking_matrix, np.array([
        [0, 2, 1],
        [1, 0, 0],
        [2, 1, 2]
    ]))
    assert np.array_equal(matrix.candidates, np.array(["a", "b", "c"]))


def test_candidate_error(error_cand_matrix):
    ranking, voters = error_cand_matrix
    with pytest.raises(ValueError) as verr:
        RankingMatrix(ranking, voters)
    assert "different candidates" in str(verr.value)


def test_dim_error(error_dim_matrix):
    ranking, voters = error_dim_matrix
    with pytest.raises(ValueError) as verr:
        RankingMatrix(ranking, voters)
    assert "dimensions to coincide" in str(verr.value)


def test_unidim_error(unidim_matrix):
    ranking, voters = unidim_matrix
    with pytest.raises(ValueError) as verr:
        RankingMatrix(ranking, voters)
    assert "2 dimensional" in str(verr.value)


def test_add_1(first_matrix_test, add_matrix_1, add_matrix_1_expected):
    ranking, voters = first_matrix_test
    ranking_add, voters_add = add_matrix_1
    matrix = RankingMatrix(ranking, voters)
    matrix.add(ranking_add, voters_add)
    for attr_ in ["ranking", "ranking_matrix", "voters", "candidates"]:
        assert np.array_equal(getattr(matrix, attr_), getattr(add_matrix_1_expected, attr_))


def test_add_2(first_matrix_test, add_matrix_2, add_matrix_2_expected):
    ranking, voters = first_matrix_test
    ranking_add, voters_add = add_matrix_2
    matrix = RankingMatrix(ranking, voters)
    matrix.add(ranking_add, voters_add)
    for attr_ in ["ranking", "ranking_matrix", "voters", "candidates"]:
        assert np.array_equal(getattr(matrix, attr_), getattr(add_matrix_2_expected, attr_))


def test_add_3(first_matrix_test, add_matrix_3, add_matrix_3_expected):
    ranking, voters = first_matrix_test
    ranking_add, voters_add = add_matrix_3
    matrix = RankingMatrix(ranking, voters)
    matrix.add(ranking_add, voters_add)
    for attr_ in ["ranking", "ranking_matrix", "voters", "candidates"]:
        assert np.array_equal(getattr(matrix, attr_), getattr(add_matrix_3_expected, attr_))
    