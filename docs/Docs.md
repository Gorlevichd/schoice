```python
from schoice import *
```

# matrix

Start with initializing the `RankingMatrix(ranking, voters)` object. We start with the following ranking matrix:

| 6 | 3 | 4 |
|:-:|:-:|:-:|
| a | c | b |
| b | a | a |
| c | b | c |


```python
voters = [6, 3, 4]
ranking = [
    ["a", "b", "c"],
    ["c", "a", "b"],
    ["b", "a", "c"],
]
```


```python
matrix = RankingMatrix(ranking, voters)
```

RankingMatrix object holds information about the ranking task at hand. It has the following attributes:
* `ranking`: Stores the ranking with names of candidates, the passed ranking is transposed for further use
* `voters`: Stores the amount of voters corresponding to the preferences in each column of ranking matrix 
* `ranking_matrix`: Stores the candidate rankings, where row corresponds to candidate and column corresponds to the voter group
* `candidates`: Stores candidate order 


```python
matrix.voters
```




    array([6, 3, 4], dtype=int64)




```python
matrix.ranking
```




    array([['a', 'c', 'b'],
           ['b', 'a', 'a'],
           ['c', 'b', 'c']], dtype='<U1')




```python
matrix.ranking_matrix
```




    array([[0., 1., 1.],
           [1., 2., 0.],
           [2., 0., 2.]])



RankingMatrix has `add(ranking, voters)` method, which allows to add new columns to the ranking matrix. You should specify new ranking and the corresponding amount of voters


```python
matrix.add(["b", "c", "a"], [4])
```


```python
matrix.ranking
```




    array([['a', 'c', 'b', 'b'],
           ['b', 'a', 'a', 'c'],
           ['c', 'b', 'c', 'a']], dtype='<U1')




```python
matrix.voters
```




    array([6, 3, 4, 4], dtype=int64)




```python
matrix.candidates
```




    array(['a', 'b', 'c'], dtype='<U1')




```python
matrix.ranking_matrix
```




    array([[0., 1., 1., 2.],
           [1., 2., 0., 0.],
           [2., 0., 2., 1.]])



# preferences

Further functionality allows to run preference operations on RankingMatrix:
* `is_prefered(RankingMatrix, candidate, other)`: returns which of the two candidates is prefered in every column of ranking_matrix
* `is_prefered_social(RankingMatrix, candidate, other)`: returns which of the two candidates is socially preferred - accounts for number of votes
* `is_best(RankingMatrix, candidate_list)`: returns which of the candidates in `candidate_list` is the best one in each column of ranking matrix
* `count_votes(RankingMatrix, candidate_list)`: Returns the amount of votes that candidates in candidate_list get when only they are running. Voters vote for their best alternative
* `pairwise_preferences(RankingMatrix, candidate_list)`: Returns the matrix with pairwise social preferences between candidates. 1 corresponds to candidate being the best alternative, -1 - the worst, 0 - draw  


```python
is_prefered(matrix, "b", "c")
```




    array([['b', 'c', 'b', 'b']], dtype='<U1')




```python
is_best(matrix)
```




    array(['a', 'c', 'b', 'b'], dtype='<U1')




```python
is_prefered_social(matrix, "a", "b")
```




    'a'




```python
is_best(matrix, ["c", "b"])
```




    array(['b', 'c', 'b', 'b'], dtype='<U1')




```python
count_votes(matrix, ["c", "b"])
```




    (array(['c', 'b'], dtype='<U1'), array([ 3, 14]))




```python
pairwise_preferences(matrix)
```




    (array(['a', 'b', 'c'], dtype='<U1'),
     array([[ 1.,  1.,  1.],
            [-1.,  1.,  1.],
            [-1., -1.,  1.]]))



# aggr_rules

`aggr_rules` module implements main social choice rules:
* `condorcet_rule(matrix, candidate_list)`: Winner should be the best alternative in every pairwise comparison. Returns: winner(s), candidates, pairwise preference matrix
* `copeland_rule(matrix, candidate_list)`: If candidate $x$ is prefered to candidate $a$, $S(x, a) = 1$, if $a$ is prefered to $x$: $S(x, a) = -1$. Copeland score for $x$ is calculated by $Copeland(x) = \sum_{\forall a \neq x}S(x, a)$. Candidate with the highest Copeland score wins. Returns: winner(s), candidates, Copeland scores
* `simpson_rule(matrix, candidate_list)`: For each candidate $x$ calculate the amount of voters that prefer them to $a$: $N(x, a)$. Simpson score for candidate $x$ is defined as $Simpson(x) = \min_{\forall a \neq x} N(x, a)$ Returns: winner(s), candidates, Simpson scores
* `scoring_rule(matrix, candidate_list, weights)`: Each voter gives $s_{i - 1}$ points to the candidate in $i$ position. Candidate with the most points wins. `weights` parameter corresponds to the sequence of points: $s_0 \leq s_1 \leq \ldots s_{n - 1}$, where $n$ is the amount of candidates. If `weights` are not specified, calculates Borda score: $s_k = k$. Returns: winner(s), candidates, scores
* `plurality_rule(matrix, candidate_list, runoff)`: Voters vote for their most prefered alternative, candidates with the most votes win. If `runoff = True`, two tour algorithm is used. If none of candidates get the majority of the votes, candidates with the two highest vote counts run in the second round. Returns: tour, winner(s), candidates, vote counts


```python
condorcet_rule(matrix)
```




    (array(['a'], dtype='<U1'),
     array(['a', 'b', 'c'], dtype='<U1'),
     array([[ 1.,  1.,  1.],
            [-1.,  1.,  1.],
            [-1., -1.,  1.]]))




```python
copeland_rule(matrix)
```




    (array(['a'], dtype='<U1'),
     array(['a', 'b', 'c'], dtype='<U1'),
     array([ 2.,  0., -2.]))




```python
simpson_rule(matrix)
```




    (array(['a'], dtype='<U1'),
     array(['a', 'b', 'c'], dtype='<U1'),
     array([9., 8., 3.]))




```python
scoring_rule(matrix)
```




    (array(['b'], dtype='<U1'),
     array(['a', 'b', 'c'], dtype='<U1'),
     array([19, 22, 10], dtype=int64))




```python
plurality_rule(matrix)
```




    (1,
     array(['b'], dtype='<U1'),
     array(['a', 'b', 'c'], dtype='<U1'),
     array([6, 8, 3]))




```python
plurality_rule(matrix, runoff = True)
```




    (2, array(['a'], dtype='<U1'), array(['a', 'b'], dtype='<U1'), array([9, 8]))


