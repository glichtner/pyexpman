# Experiment Manager

## Description
Simple experiment manager to store parameters, outputs and datasets.

## Usage
```python
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import expmgr

output_base_path = './output'

expmgr.init(output_base_path)


# Creates experiment folder "<datetime_string>_<name>" in output_base_path
expmgr.create_experiment(name='my_experiment')

print(expmgr.get_experiment().output_path) # output: ./output/201026T132700_my_experiment/


# Store parameters
params = {
    'alpha': 0.001,
    'layers': 3,
    'output_layer': {
        'nodes': 10,
        'activation_function': 'softmax'
    },
    'optimizer': 'adam'
}
# Log parameter to .yaml file
fname = expmgr.log_params('model_params', params)
print(fname) # output: ./output/201026T132700_my_experiment/model_params.yaml

# Store image
f = plt.figure()
x = np.arange(1,20)
plt.plot(x, np.sin(x))
fname = expmgr.log_image('sine') # uses plt.gcf() to get current figure
print(fname) # output: ./output/201026T132700_my_experiment/sine.png

# Store dataframe
df = pd.DataFrame({'numbers': [1, 2, 3], 'colors': ['red', 'white', 'blue']})
fname = expmgr.log_dataframe('dataframe', df)
print(fname) # output: ./output/201026T132700_my_experiment/dataframe.xlsx

# Store dataset
fname = expmgr.log_artifact('dataset', df)
print(fname) # output: ./output/201026T132700_my_experiment/dataset.dump.gz


# Store artifact
fname = expmgr.log_artifact('artifact', df)
print(fname) # output: ./output/201026T132700_my_experiment/artifact.dump.gz
```
