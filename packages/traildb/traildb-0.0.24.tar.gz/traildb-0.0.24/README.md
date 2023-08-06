# Trail

Trail brings more transparency in your ml experimentation.
Start by using mlflow to track experiments and follow the steps below.

# Installation

Install Trail from Pypi via ```python pip install traildb```

# Get started
```python from traildb import trail_init```

# log experiment

Call the log_experiment() method after the mlflow run (not within the run) <br />

<br />

```python
with mlflow.start_run() as run: <br />
    with trail_init(email, password, project_id, parent):
      ...your training code... <br />
```
