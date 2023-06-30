from collections.abc import Iterable
from itertools import combinations
import warnings
import numpy as np
from .preferences import pairwise_preferences, candidate_list_filler, count_votes
from .matrix import RankingMatrix


def condorcet_rule(rm_obj: RankingMatrix, candidate_list: Iterable = None):
    """
    Winner should win all pairwise comparisons
    """
    candidates, preferences = pairwise_preferences(rm_obj, candidate_list)
    condorcet_winner_index = np.where((preferences == 1).all(axis = 1))[0]
    return candidates[condorcet_winner_index], candidates, preferences


def copeland_rule(rm_obj: RankingMatrix, candidate_list: Iterable = None):
    """
    Calculates the following score for pairwise comparisons with candidate:
    - Candidate won: 1
    - Candidate lost: -1
    - Indifference: 0
    """
    candidates, preferences = pairwise_preferences(rm_obj, candidate_list)
    # Fill diagonal with zeros to get the right score
    # As we sum for x neq a
    np.fill_diagonal(preferences, 0)
    copeland_score = preferences.sum(axis = 1)
    return candidates[copeland_score == copeland_score.max()], candidates, copeland_score


def simpson_rule(rm_obj: RankingMatrix, candidate_list: Iterable = None):
    """
    Minimum amount of voters that vote for candidate 
    """
    candidate_list, _ = candidate_list_filler(rm_obj, candidate_list)
    pairwise_size = len(candidate_list)
    vote_matrix = np.zeros((pairwise_size, pairwise_size))
    np.fill_diagonal(vote_matrix, rm_obj.voters.sum())
    for i, j in combinations(range(pairwise_size), r = 2):
        candidate, other = candidate_list[i], candidate_list[j]
        # Check how much voters vote for candidate and other in pairwise vote
        _, votes = count_votes(rm_obj, [candidate, other])
        vote_matrix[i, j] = votes[0]
        vote_matrix[j, i] = votes[1]
    simpson_score = vote_matrix.min(axis = 1)
    return candidate_list[simpson_score == simpson_score.max()], candidate_list, simpson_score


def scoring_rule(rm_obj: RankingMatrix, candidate_list: Iterable = None, weights: Iterable = None):
    """
    Assign descending score to each place in ranking, calculate sums
    """
    candidate_list, _ = candidate_list_filler(rm_obj, candidate_list)
  
    if weights is None:
        # Running Borda
        weights = np.arange(0, len(candidate_list))[::-1]
    else:
        weights = np.array(weights)
        # Run some checks
        if weights.shape[0] != len(candidate_list):
            raise ValueError(f"Shape of weights does not correspond to the shape \
                                of candidate_list: {weights.shape[0]}, {len(candidate_list)}")
        if np.any(np.diff(weights) > 0):
            raise ValueError("Weights array is not descending")
    weight_matrix = weights[rm_obj.ranking_matrix.astype(int)]
    scores = weight_matrix @ rm_obj.voters
    return candidate_list[scores == scores.max()], candidate_list, scores


def plurality_rule(rm_obj: RankingMatrix, candidate_list: Iterable = None, runoff: bool = False):
    """
    Calculates winners in plurality rule with runoff
    """
    still_running = candidate_list
    for tour in range(2):
        still_running, votes = count_votes(rm_obj, still_running)

        # If one-round election
        if not runoff:
            return (tour,
                    still_running[votes == votes.max()],
                    still_running,
                    votes)
        
        # Two round election
        # Strict majority
        # Votes is int anyway
        if (votes > votes.sum() / 2).any():
            # If anyone gets more than half
            return (tour,
                    still_running[votes == votes.max()],
                    still_running,
                    votes)
        
        if (votes == votes[0]).all():
            # If all equal
            return (tour,
                    still_running,
                    still_running,
                    votes)
        
        # If not returned, take first two candidates
        max_votes = votes[np.argsort(np.unique(votes))[-2:]]
        # Select candidates with votes corresponding to top 2
        # This should solve the problem with repeated max
        still_running_1 = still_running[votes == max_votes[0]]
        if still_running_1.shape[0] >= 2:
            # We already filled our 2 places with top 1 candidates
            still_running = still_running_1
            continue
        # If still_running_1 is less than 2 voters long
        # add voters with second max
        still_running_2 = still_running[votes == max_votes[1]]
        still_running = np.concat(still_running_1, still_running_2)
    warnings.warn("Failed to find a winner in two steps")
    return (tour, still_running, still_running, votes)


# Would be interesting to implement with graphx or ??
def _plot_condorcet_graph(self):
    raise NotImplementedError("This functionality is not implemented yet")
