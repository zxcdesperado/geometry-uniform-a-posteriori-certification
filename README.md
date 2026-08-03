# Online Resource 2 — minimal reproducibility package

**Article:** Exact Galerkin Correction and Geometry-Uniform A Posteriori Certification of Neural-Operator Predictions for Symmetric Elliptic Problems  
**Journal:** Journal of Scientific Computing  
**Author:** Xiaochuan Zhang  
**Affiliation:** School of Science and Engineering, The Chinese University of Hong Kong, Shenzhen  
**Corresponding email:** 122090764@link.cuhk.edu.cn

This is the reviewer-facing minimal package. It intentionally excludes manuscript source files, generated PDF/table copies, development tests, caches, internal audit reports, and exploratory experiments. Only code, fixed configurations, released numerical evidence, and model files needed for the manuscript claims are retained.

## Quick verification

```bash
python run.py
```

The command automatically extracts `experiments.zip`, `released_results.zip`, and `models.zip`, then checks the main benchmark, 90-case reference study, 270 RT2 certificates, certificate gate, 450-output official GINO transfer, nine machine-enclosed GINO cases, L-shaped nonmanufactured certificate, paired cost benchmark, machine-enclosed endpoint suites, and local audit.

## Recompute

Core experiments (long CPU run):

```bash
python -m pip install -r requirements-core.txt
python run.py --recompute-core
```

Official GINO machine-enclosure audit (extended environment):

```bash
python -m pip install -r requirements-extended.txt
python run.py --recompute-machine
```

## Contents

- `experiments.zip`: scientific implementations and fixed configurations; extracted automatically by `run.py`;
- `released_results.zip`: raw rows and summaries used by the paper;
- `models.zip`: only checkpoints required for fixed-model verification;
- `verify_results.py`: compact standard-library verification;
- `run.py`: single entry point;
- `LICENSE`, `DATA_LICENSE.txt`, and dependency notices.
