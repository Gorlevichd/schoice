import numpy as np

class Social_Choice:
    def __init__(self, ranking, voters):
        self.ranking = ranking
        self.voters = voters
        self.candidates = np.unique(self.ranking)
    
    def is_prefered(self, candidate, other):
        rows, cols = np.where(self.ranking == candidate)
        position_candidate = rows[np.argsort(cols)]
            
        rows, cols = np.where(self.ranking == other)  
        position_other = rows[np.argsort(cols)]
        col_pref = np.sign(position_other - position_candidate)
        return col_pref
    
    
    def is_best(self, candidates_arr):
        candidate_positions = np.zeros((len(candidates_arr), self.ranking.shape[1]))
        for i, candidate in enumerate(candidates_arr):
            rows, cols = np.where(self.ranking == candidate)
            position_candidate = rows[np.argsort(cols)]
            candidate_positions[i] = position_candidate
        return candidates_arr[np.argmin(candidate_positions, axis = 0)]
            
        
    def condorcet_rule(self):
        result_matrix = np.zeros((len(self.candidates), len(self.candidates)))
        for i, candidate in enumerate(self.candidates):
            for j, other in enumerate(self.candidates):
                col_pref = self.is_prefered(candidate, other)
                
                votes = (col_pref * self.voters).sum()
                win_loss = np.sign(votes)

                result_matrix[i, j] = win_loss
                result_matrix[j, i] = -win_loss
        np.fill_diagonal(result_matrix, 1)
        winner = self.candidates[np.where((result_matrix == 1).all(axis = 1))[0]]
        return winner, result_matrix
    
    
    def copeland_rule(self):
        result_matrix = np.zeros((len(self.candidates), len(self.candidates)))
        for i, candidate in enumerate(self.candidates):
            for j, other in enumerate(self.candidates):
                col_pref = self.is_prefered(candidate, other)
                
                votes = (col_pref * self.voters).sum()
                win_loss = np.sign(votes)

                result_matrix[i, j] = win_loss
                result_matrix[j, i] = -win_loss
                
        return result_matrix.sum(axis = 1), result_matrix
    
    
    def simpson_rule(self):
        result_matrix = np.zeros((len(self.candidates), len(self.candidates)))
        for i, candidate in enumerate(self.candidates):
            for j, other in enumerate(self.candidates):
                col_pref = self.is_prefered(candidate, other)
                
                col_pref[col_pref < 0] = 0
                result_matrix[i, j] = (col_pref * self.voters).sum()
                result_matrix[j, i] = self.voters.sum() - result_matrix[i, j]
                
                np.fill_diagonal(result_matrix, np.Inf)
        return np.min(result_matrix, axis = 1), result_matrix
    
    
    def scoring_rule(self, weights = None):
        result_matrix = np.zeros((len(self.candidates), ))
        for i, candidate in enumerate(self.candidates):
            rows, cols = np.where(self.ranking == candidate)
            position_candidate = rows[np.argsort(cols)]
            
            if weights is None:
                # By default calculate Borda
                weights_per_voter = len(self.candidates) - position_candidate - 1
            else:
                # Calculate with user weights
                weights_per_voter = weights[position_candidate]
            
            score_aggr = weights_per_voter @ self.voters.T
            result_matrix[i] = score_aggr
        return result_matrix
    
    
    
    def plurality_rule(self, runoff = False):
        still_running = np.array([True] * len(self.candidates))
        for tour in range(2):
            resulting_matrix = np.zeros((len(self.candidates), ))
            first_choice = self.is_best(self.candidates[still_running])
            for candidate in np.unique(first_choice):
                i = np.where(self.candidates == candidate)
                resulting_matrix[i] = self.voters[np.where(first_choice == candidate)].sum()
            
            # If one round
            if not runoff:
                return resulting_matrix

            # More rounds
            # Check for majority
            if (resulting_matrix > (resulting_matrix.sum() / 2)).any():
                return resulting_matrix

            # All are equal
            elif (resulting_matrix[still_running] == resulting_matrix[still_running][0]).all():
                return resulting_matrix
                
            # Update running
            still_running[:] = False
            still_running[np.argsort(resulting_matrix)[-2:]] = True
                
                        
        else:
            resulting_matrix = np.zeros((len(self.candidates), ))
            first_choice = self.is_best(self.candidates)
            for candidate in np.unique(first_choice):
                i = np.where(self.candidates == candidate)
                resulting_matrix[i] = self.voters[np.where(first_choice == candidate)].sum()
            return resulting_matrix