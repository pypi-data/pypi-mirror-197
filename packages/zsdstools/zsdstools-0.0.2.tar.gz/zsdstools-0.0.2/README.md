# dstools

Create functions that help analyze models

## Instructions

1. Install:

```
pip install zsdstools
```

2. Create Entropy plot for Probability outputs:

```python
from zsdstools import dstools

dstools.entropy_plot(entropy_report, type_report = 'facetgrid', type_plot = 'violinplopt')
dstools.entropy_plot(entropy_report, type_report = 'facetgrid', type_plot = 'boxplot')
dstools.entropy_plot(entropy_report, type_report = 'facetgrid', type_plot = 'histogram')

dstools.entropy_plot(entropy_report, type_report = 'summary', type_plot = 'violinplopt')
dstools.entropy_plot(entropy_report, type_report = 'summary', type_plot = 'boxplot')
dstools.entropy_plot(entropy_report, type_report = 'summary', type_plot = 'histogram')

dstools.max_print_out()
```
