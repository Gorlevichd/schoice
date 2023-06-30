from collections.abc import Iterable
from itertools import combinations
import numpy as np
from .matrix import RankingMatrix

def get_index_safe(rm_obj: RankingMatrix, candidate_list: Iterable):
    """
    Gets indexes for candidates, checking that they are present in mapping
    """
    candidate_idx = []
    for candidate in candidate_list:
        if candidate not in rm_obj.candidates_to_ix:
            raise ValueError(f"{candidate} not in candidate list \
                                {rm_obj.candidates}")
        candidate_idx.append(rm_obj.candidates_to_ix[candidate])
    return np.array(candidate_idx)


def candidate_list_filler(rm_obj: RankingMatrix, candidate_list: Iterable = None):
    """
    If candidate_list is None return all the candidates
    If candidate_list is not None return candidates and their indices from rm_obj
    """
    if candidate_list is not None:
        candidate_list = np.array(candidate_list)
        # Remove duplicates
        _, idx = np.unique(candidate_list, return_index = True)
        candidate_list = candidate_list[np.sort(idx)]
        indices = get_index_safe(rm_obj, candidate_list)
    else:
        # Take all
        candidate_list = rm_obj.candidates
        indices = np.arange(len(candidate_list))
    return candidate_list, indices


def is_prefered_num(rm_obj: RankingMatrix, candidate: str,
                    other: str):
    """
    Numeric calculation for is_prefered
    """
    indices = get_index_safe(rm_obj, [candidate, other])
    # Checks sign of difference between rank, other rank should be higher (!)
    preferences = np.sign(np.array([[-1, 1]]) @ rm_obj.ranking_matrix[indices, :])
    return preferences


def is_prefered(rm_obj: RankingMatrix, candidate: str,
                other: str):
    """
    Function returns voter preferences for candidate as candidate names
    """
    preferences = is_prefered_num(rm_obj, candidate, other)
    return np.where(preferences == 1, candidate, other)


def is_prefered_social_num(rm_obj: RankingMatrix, candidate: str,
                       other: str):
    """
    Function aggregates social preferences by multiplying individual preferences on number of voters
    with corresponding preferences

    Return +1 in columns where candidate wins, -1 where other
    """
    indiv_preferences_num = is_prefered_num(rm_obj, candidate, other)
    social_pref_num = int(np.sign(rm_obj.voters @ indiv_preferences_num.T).item())
    return social_pref_num


def is_prefered_social(rm_obj: RankingMatrix, candidate: str,
                       other: str):
    """
    Converts social_pref_num to candidate names
    """
    social_pref_num = is_prefered_social_num(rm_obj, candidate, other)
    if social_pref_num == 1:
        return candidate
    if social_pref_num == -1:
        return other
    if social_pref_num == 0:
        return "Tie"
    return None


def is_best_num(rm_obj: RankingMatrix, candidate_list: Iterable = None):
    """
    Function calculates indices of winners
    """
    candidate_list, indices = candidate_list_filler(rm_obj, candidate_list)
    winner_ids = np.argmin(rm_obj.ranking_matrix[indices, :], axis = 0)
    return candidate_list, winner_ids


def is_best(rm_obj: RankingMatrix, candidate_list: Iterable = None):
    """
    Function returns the most prefered candidate in candidate list for each voter group 
    """
    candidate_list, winner_ids = is_best_num(rm_obj, candidate_list)
    return candidate_list[winner_ids]


def pairwise_preferences(rm_obj: RankingMatrix, candidate_list: Iterable = None):
    """
    Constructs a matrix of pairwise preferences
    """
    # Run pairwise comparisons
    candidate_list, _ = candidate_list_filler(rm_obj, candidate_list)
    pairwise_size = len(candidate_list)
    pairwise_matrix = np.empty((pairwise_size, pairwise_size))
    np.fill_diagonal(pairwise_matrix, 1)
    for i, j in combinations(range(pairwise_size), r = 2):
        candidate, other = candidate_list[i], candidate_list[j]
        pairwise_ij = is_prefered_social_num(rm_obj, candidate, other)
        pairwise_matrix[i, j] = pairwise_ij
        pairwise_matrix[j, i] = -pairwise_ij
    return candidate_list, pairwise_matrix


def count_votes(rm_obj: RankingMatrix, candidate_list: Iterable = None):
    """
    Function returns the number of votes that candidates get, 
    only candidates in candidate_list run
    """
    # Maybe there is a better solution
    # At least, it preserves the order
    candidate_list, row_ind = is_best_num(rm_obj, candidate_list)
    col_ind = np.arange(len(row_ind))
    win_matrix = np.zeros((len(candidate_list), len(col_ind)))
    win_matrix[row_ind, col_ind] = 1
    return candidate_list, (win_matrix @ rm_obj.voters.T).astype(int)