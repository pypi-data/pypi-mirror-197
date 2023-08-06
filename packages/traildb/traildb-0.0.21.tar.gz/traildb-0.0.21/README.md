# Trail

Trail brings more transparency in your ml experimentation.
Start by using mlflow to track experiments and follow the steps below.

# Installation

Install Trail from Pypi via ```python pip install traildb```

# Get started
```python from traildb import trail_init```

# Initialize a trail object

add this line of code in the beginning of the trainingscript.

```python trail = trail_init(username, password)```

The input paramter "username" and "password" will be provided by the trail-team.


# log experiment

Call the log_experiment() method after the mlflow run (not within the run) <br />

<br />

```python
with mlflow.start_run() as run: <br />
    with trail_init(email, password, project_id, parent):
      ...your training code... <br />
```

The input paramters parent_id [String] and data_meta [dict] must be provided in the according type.
If they are non existing please provide empty String ("") or dict ({})