from collections.abc import Iterable
import numpy as np

class RankingMatrix:
    """
    Class that contains ranking tables and conducts operations on them

    Attributes
    ----------
    ranking: np.array
        Two dimensional np.array that represents the ranking table as a matrix
    voters: np.array
        One dimensional np.array that contains quantity of voters with given preferences
    candidates: np.array
        One dimensional np.array that contains unique values of ranking table
    """
    def __init__(self, ranking: Iterable, voters: Iterable):
        """
        Initalizes SocialChoice class, converts iterables to numpy

        Parameters
        ----------
        ranking: Iterable
            Two dimensional Iterable with ranked alternatives corresponding 
            to quantities of voters
            Rows correspond to voters
        voters: Iterable
            One dimensional Iterable with quantities of voters with corresponding ranking
        """
        ## Convert to numpy
        try:
            ranking_raw = np.array(ranking)
            self.voters = np.array(voters)
        except Exception as np_read_err:
            raise RuntimeError("Could not convert parameters to np.array:",
                               np_read_err) from np_read_err
        # Transpose ranking for further use (Backward compatibility)
        self.ranking = ranking_raw.T

        ## Run diagnostics
        # check that dimensions follow the logic
        self._dimension_checker(self.ranking, self.voters)
        # Check that all preferences are defined over the same candidates
        self.candidates = self._candidates_safe(self.ranking)
        # Remove duplicates
        self.ranking, self.voters = self._shrink_duplicates(self.ranking, self.voters)

        ## Save shapes for further use
        # Shapes should be updated in add
        self.n_candidates = self.candidates.shape[0]
        self.n_voters = self.voters.shape[0]
        self.candidates_to_ix = {candidate: id for id, candidate in enumerate(self.candidates)}

        # Build ranking matrix for further calculations
        self.ranking_matrix = self._build_ranking_matrix(self.ranking, self.candidates_to_ix)


    def _dimension_checker(self, ranking, voters):
        """
        Internal function, checks that parameters are behaving as expected
        """

        # Check that ranking_np is two dimensional
        if ranking.ndim != 2:
            raise ValueError(f"Expected ranking to be 2 dimensional, \
                             received ranking of shape {ranking.shape}")

        # Check that dimension 1 of ranking_np correspond to dimension 1 of voters_np
        if ranking.shape[1] != voters.shape[0]:
            raise ValueError(f"Expected voters and rankings dimensions to coincide, but received: \
                             ranking: {ranking.shape[1]}, \n \
                             voters: {voters.shape[0]})")


    def _candidates_safe(self, ranking):
        """
        Constructs candidate list safely (Checks for missings, duplicates and unexpected 
        values)
        """
        # Columns should not differ in values and include duplicates, check for that
        # At the same time allows to construct list of candidates more safely than np.unique
        candidates_0 = np.unique(ranking[:, 0])
        for i in range(1, ranking.shape[1]):
            candidates_i = np.unique(ranking[:, i])
            if np.setxor1d(candidates_0, candidates_i).size != 0:
                raise ValueError(f"Preferences for voter {i} rank different candidates: \n \
                                 Missing candidates: {np.setdiff1d(candidates_0, candidates_i)} \n \
                                 Unique candidates: {np.setdiff1d(candidates_i, candidates_0)}"
                                )
        return candidates_0


    def _shrink_duplicates(self, ranking, voters):
        """
        Function converts duplicates into sums to make further processing faster
        """
        unique_rankings, index_unique, inverse_pos = np.unique(ranking, axis = 1,
                                                       return_inverse = True,
                                                       return_index = True
                                                      )
        index_argsort = np.argsort(index_unique)
        voters_reduced = np.empty_like(index_unique)
        for i, index in enumerate(index_argsort):
            voters_reduced[i] = voters[inverse_pos == index].sum()
        return unique_rankings[:, index_argsort], voters_reduced


    def add(self, new_ranking, new_voters):
        """
        Adds new columns to the ranking table

        Parameters
        ----------
        ranking_new: Iterable
            Contains new columns, can be 2 dimensional, rows correspond to voters
        voters_new: Iterable
            Contains quantites of voters corresponding to new rankings
        """
        try:
            new_ranking = np.array(new_ranking)
            new_voters = np.array(new_voters)
        except Exception as np_read_err:
            raise RuntimeError("Could not convert argument to np.array:",
                               np_read_err) from np_read_err
        # Fast shape check
        # NB: Class stores self.ranking transposed
        if new_ranking.ndim == 1:
            new_ranking = np.expand_dims(new_ranking, axis = 0)
        # Transpose for further compatibility
        new_ranking = new_ranking.T
        if new_ranking.shape[0] != self.ranking.shape[0]:
            raise ValueError(f"New ranking does not have the same number of candidates: \n \
                             base ranking: {self.ranking.shape[0]} \n \
                             new ranking: {new_ranking.shape[0]}")
        # Run further adequacy checks
        self._dimension_checker(new_ranking, new_voters)
        # Should not include new candidates
        new_candidates = self._candidates_safe(new_ranking)
        if np.setxor1d(new_candidates, self.candidates).size != 0:
            raise ValueError(f"Candidates in new data differ from previous candidates: \n \
                             Missing candidates: {np.setdiff1d(self.candidates, new_candidates)} \n \
                             Unique candidates: {np.setdiff1d(new_candidates, self.candidates)}")
        # All checks complete, now finally add
        self.voters = np.append(self.voters, new_voters)
        self.ranking = np.hstack((self.ranking, new_ranking))
        # Remove duplicates
        self.ranking, self.voters = self._shrink_duplicates(self.ranking, self.voters)
        self.n_voters = self.voters.shape[0]
        self.ranking_matrix = self._build_ranking_matrix(self.ranking, self.candidates_to_ix)


    def _build_ranking_matrix(self, ranking, candidates_to_ix):
        """
        Function build a matrix with rankings, where [i, j] corresponds to a position
        of candidate i in preferences of voter j
        """
        ranking_matrix = np.empty((self.n_candidates, self.n_voters))
        for candidate, i in candidates_to_ix.items():
            rows, cols = np.where(ranking == candidate)
            ranking_matrix[i, :] = rows[np.argsort(cols)]
        return ranking_matrix
