# `ndx-odor-metadata`

[![pipeline status](https://img.shields.io/gitlab/pipeline-status/fleischmann-lab/ndx/ndx-odor-metadata?branch=main&label=pipeline&style=flat-square)](https://gitlab.com/fleischmann-lab/ndx/ndx-odor-metadata/-/commits/main)
[![license](https://img.shields.io/gitlab/license/fleischmann-lab/ndx/ndx-odor-metadata?color=yellow&label=license&style=flat-square)](LICENSE.txt)


![python version](https://img.shields.io/pypi/pyversions/ndx-odor-metadata?style=flat-square)
[![release](https://img.shields.io/gitlab/v/release/fleischmann-lab/ndx/ndx-odor-metadata?label=release&sort=date&style=flat-square)](https://gitlab.com/fleischmann-lab/ndx/ndx-odor-metadata/-/releases)
[![pypi package](https://img.shields.io/pypi/v/ndx-odor-metadata?label=pypi%20package&style=flat-square&color=blue)](https://pypi.org/pypi/ndx-odor-metadata)
[![conda package](https://img.shields.io/conda/v/fleischmannlab/ndx-odor-metadata?color=green&style=flat-square)](https://anaconda.org/FleischmannLab/ndx-odor-metadata)

NWB extension to store odor stimulus metadata with `DynamicTable` format. Entries that have a PubChem and `stim_types` indicate odor/chemical will also be queried with `pubchempy` for more information.

This is in alpha development stages **WITHOUT** any appropriate tests yet. Please use with discretion.

## Requirement

The requirements and additional development requirements can be seen in [`pyproject.toml`](pyproject.toml) file.

Here are the minimum requirements:

- `python >=3.8`
- `pynwb>=1.5.0,<3`
- `hdmf>=3.4.7,<4`
- `pubchempy>=1.0.4`
- `pyyaml>=5.0`

## Installation

You can install via `pip`:

```bash
pip install ndx-odor-metadata
```

Or `conda`:

```bash
conda install -c fleischmannlab ndx-odor-metadata
```

Or directly from the `git` repository:

```bash
pip install git+https://gitlab.com/fleischmann-lab/ndx/ndx-odor-metadata
```

## Usage

### Main usage

```python
from ndx_odor_metadata import OdorMetaData

odor_table = OdorMetaData(name='odor_table', description='an odor table')

odor_table.add_stimulus(
    pubchem_id = 7662.0,
    stim_name = "3-Phenylpropyl isobutyrate",
    raw_id = 3,
    stim_id = 1,
    stim_types = "od
    chemical_dilution_type='vaporized',
    chemical_concentration = 0.01,
    chemical_concentration_unit='%',
    chemical_solvent = "Mineral Oil",
    chemical_provider = "Sigma",
    stim_description = "Legit odor stimulus #1",
)

nwbfile.add_acquisition(odor_table)
```

### Demonstration

For more detailed demonstration, please visit the [`demo`](demo/demo.ipynb) folder.

## TODOs

- [ ] Create test
- [ ] Publish on `conda`
- [ ] Publish on `pypi`
- [x] Fetch pubchem data using `pubchempy`
- [x] Use `pyproject.toml` instead of `setup.py`

---
This extension was created using [ndx-template](https://github.com/nwb-extensions/ndx-template).
