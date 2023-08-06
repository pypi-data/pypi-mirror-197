# influence

The `influence` library implements the generalized, observable structure _influence model_ proposed in Asavathiratham's 2000 Ph.D. thesis.

## Installation

```
pip install git+ssh://git@github.com/keelerh/influence.git
```

## Usage

As a basic example, we define two sites (nodes) in the network: a leader and a follower. The follower meticulously
follows the behavior of the leader. Both sites have two possible statuses, `0` or `1`, represented by indicator
vectors. We also define a network matrix $D$ and a state-transition matrix $A$ to instantiate the influence model.

```python
>> import numpy as np
>>
>> from influence.influence_model import InfluenceModel
>> from influence.site import Site
>>
>> leader = Site('leader', np.array([[1], [0]]))
>> follower = Site('follower', np.array([[0], [1]]))
>> D = np.array([
>>     [1, 0],
>>     [1, 0],
>> ])
>> A = np.array([
>>     [.5, .5, 1., 0.],
>>     [.5, .5, 0., 1.],
>>     [.5, .5, .5, .5],
>>     [.5, .5, .5, .5],
>> ])
>> model = InfluenceModel([leader, follower], D, A)
>> initial_state = model.get_state_vector()
>> print(initial_state)
```

The initial state of the network is simply a vector stack of the initial statuses of the two sites.

```python
[[1]
 [0]
 [0]
 [1]]
```

Now, we apply the evolution equations of the influence model to progress to the next state of the network.

```python
>> next(model)
>> next_state = model.get_state_vector()
>> print(next_state)
```

We see that the follower has adapted the previous status of the leader.

```python
[[0]
 [1]
 [1]
 [0]]
```

This following behavior continues through subsequent iterations.

```python
>> next(model)
>> next_state = model.get_state_vector()
>> print(next_state)
```

```python
[[1]
 [0]
 [0]
 [1]]
```

## Acknowledgements

Please cite the accompanying paper in your publications if this library helps your research. Here is an example BibTeX entry:

```
@inproceedings{erhardt2022detection,
  title={Detection of Coordination Between State-Linked Actors},
  author={Erhardt, Keeley and Pentland, Alex},
  booktitle={International Conference on Social Computing, Behavioral-Cultural Modeling and Prediction and Behavior Representation in Modeling and Simulation},
  pages={144--154},
  year={2022},
  organization={Springer}
}
```

And let me know!
