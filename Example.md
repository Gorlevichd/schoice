```python
import numpy as np
from schoice import Social_Choice
```


```python
voters = np.array([6, 3, 4, 4])
ranking =  np.array([
    ["a", "c", "b", "b"],
    ["b", "a", "a", "c"],
    ["c", "b", "c", "a"]
])
```


```python
sc1 = Social_Choice(ranking, voters)
```


```python
sc1.condorcet_rule()
```




    (array(['a'], dtype='<U1'),
     array([[ 1.,  1.,  1.],
            [-1.,  1.,  1.],
            [-1., -1.,  1.]]))




```python
voters = np.array([1, 4, 1, 3])
ranking = np.array([
    ["a", "c", "e", "e"],
    ["b", "d", "a", "a"],
    ["c", "b", "d", "b"],
    ["d", "e", "b", "d"],
    ["e", "a", "c", "c"]
])
```


```python
sc2 = Social_Choice(ranking, voters)
sc2.copeland_rule()
```




    (array([ 2.,  0.,  0.,  0., -2.]),
     array([[ 0.,  1.,  1.,  1., -1.],
            [-1.,  0.,  1., -1.,  1.],
            [-1., -1.,  0.,  1.,  1.],
            [-1.,  1., -1.,  0.,  1.],
            [ 1., -1., -1., -1.,  0.]]))




```python
sc2.simpson_rule()
```




    (array([1., 4., 4., 4., 4.]),
     array([[inf,  5.,  5.,  5.,  1.],
            [ 4., inf,  5.,  4.,  5.],
            [ 4.,  4., inf,  5.,  5.],
            [ 4.,  5.,  4., inf,  5.],
            [ 8.,  4.,  4.,  4., inf]]))




```python
sc2.scoring_rule(weights = np.array([10, 9, 8, 7, 6]))
```




    array([70., 72., 72., 72., 74.])




```python
sc2.condorcet_rule()
```




    (array([], dtype='<U1'),
     array([[ 1.,  1.,  1.,  1., -1.],
            [-1.,  1.,  1., -1.,  1.],
            [-1., -1.,  1.,  1.,  1.],
            [-1.,  1., -1.,  1.,  1.],
            [ 1., -1., -1., -1.,  1.]]))




```python
ranking = np.array([
    ["a", "a", "b", "c"],
    ["d", "d", "c", "d"],
    ["c", "b", "d", "b"],
    ["b", "c", "a", "a"]
])
voters = np.array([5, 3, 5, 4])
sc3 = Social_Choice(ranking, voters)
```


```python
sc3.plurality_rule()
```




    array([8., 5., 4., 0.])




```python
sc3.plurality_rule(runoff = True)
```




    array([8., 9., 0., 0.])




```python
sc3.scoring_rule()
```




    array([24., 22., 27., 29.])




```python
sc3.condorcet_rule()
```




    (array(['c'], dtype='<U1'),
     array([[ 1., -1., -1., -1.],
            [ 1.,  1., -1., -1.],
            [ 1.,  1.,  1.,  1.],
            [ 1.,  1., -1.,  1.]]))




```python
ranking = np.array([
    ["d", "d", "b", "c"],
    ["c", "b", "c", "d"],
    ["b", "c", "d", "b"],
])
voters = np.array([5, 3, 5, 4])
sc4 = Social_Choice(ranking, voters)
```


```python
sc4.plurality_rule(runoff = True)
```




    array([ 5.,  0., 12.])


