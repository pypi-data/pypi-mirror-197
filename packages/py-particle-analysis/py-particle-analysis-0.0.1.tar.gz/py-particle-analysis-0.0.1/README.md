# pyPartAnalysis

Package for processing ImpactT and ImpactZ particle distributions as well as performing analysis on particle distributions in pandas dataframes.

## Compatibility

Compatible with Python 3.8.5.

Works with the default NERSC python module as of June 5th, 2022.

## Adding Directory to PYTHONPATH on NERSC

To make the `pyPartAnalysis` module available on the Python and Jupyter path, add the following lines to the `.bashrc` file in the home directory:

```bash
export PYTHONPATH='/global/homes/firstletterofusername/username/pyPartAnalysis'
export JUPYTER_PATH='/global/homes/firstletterofusername/username/pyPartAnalysis'
```

Note that we assume that the directory is in the home directory of 'username', where username is replaced with your name; though the path can be to wherever the module is eventually stored.

## Example Use Cases for ImpactT/Z

Example Jupyter notebooks using ImpactT and ImpactZ output files can by found [here](examples/). This package can be useful for creating interesting visualizations of from the particle distributions, such as the ones below:

<p align='center'><img src=".\examples\1-ImpactT_distribution\NormalizedPhaseSpaceVsSlice.png"></p>
<p align='center'><em>Series of z slices along the normalized x phase space.</em></p>

<p align='center'><img src=".\examples\4-Bunching Factor\bunching_area.gif"></p>
<p align='center'><em>Transversely binned bunching factor vs wavelength.</em></p>
