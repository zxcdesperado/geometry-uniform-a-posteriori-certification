# Third-party notices

The original experiment and verification software is distributed under the
BSD 3-Clause License in `LICENSE`. Data, saved checkpoints, generated tables,
and original figures are distributed under CC BY 4.0 as stated in
`DATA_LICENSE.txt`.

The manuscript source package also contains Springer Nature LaTeX support
files (`svjour3.cls`, `svglov3.clo`, and `spmpsci.bst`). These files remain
subject to their original notices and terms and are not relicensed under the
BSD or CC BY licenses above.

Runtime dependencies are distributed by their respective copyright holders
under their own licenses. `requirements-core.txt` contains the pinned direct
dependencies needed for the default reproduction command.
`requirements-extended.txt` contains the broader fully pinned environment used
for the official upstream GINO machine-enclosure audit.  The compatibility file
`requirements-lock.txt` repeats the core direct pins; it is not represented as
a complete transitive lock.  This artifact does not redistribute third-party
packages.

Saved `.pt` checkpoint files are supplied as study data. Load only checkpoints
from this artifact after checking them against `MANIFEST_SHA256.json`, and use
PyTorch's `weights_only=True` mode. Do not load untrusted pickle-based model
files.
