from __future__ import annotations
import argparse, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
PY=sys.executable
def call(*a): subprocess.run([PY,'-B',*a],cwd=ROOT,check=True)
def setup(): call('setup_artifact.py')
def verify(): setup(); call('verify_results.py')
def core():
 setup()
 call('experiments/independent_forcing_operator_pipeline.py','--epochs','120')
 call('experiments/independent_forcing_rt_reference_audit.py','--reference-cases-per-split','30','--rt-cases-per-split','3')
 call('experiments/independent_forcing_multicheckpoint_rt2_audit.py')
 call('experiments/multicheckpoint_certificate_gate_sweep.py')
 call('experiments/independent_forcing_paired_statistics.py')
 call('experiments/analyze_certificate_robustness.py')
 call('experiments/generate_rt_linear_stability_audit.py')
 call('experiments/optimized_end_to_end_cost_benchmark.py','--config','experiments/configs/optimized_end_to_end_cost_headline_confirmation_2026-08-01.json','--summary-out','experiments/results/optimized_end_to_end_cost_headline_confirmation_summary.json','--rows-out','experiments/results/optimized_end_to_end_cost_headline_confirmation_rows.csv','--pairs-out','experiments/results/cost_benchmark_paired_timings.csv')
 for s in ('poisson_machine_strict_curved_interval.py','poisson_machine_strict_curved_3d_interval.py','elasticity_machine_strict_affine_suite.py','delta_local_comparison_audit.py','nonmanufactured_lshape_reference_certificate.py'): call('experiments/'+s)
 verify()
def machine(): setup(); call('experiments/official_gino_machine_rt2_audit.py'); verify()
def main():
 ap=argparse.ArgumentParser(); g=ap.add_mutually_exclusive_group(); g.add_argument('--recompute-core',action='store_true'); g.add_argument('--recompute-machine',action='store_true'); a=ap.parse_args()
 if a.recompute_core: core()
 elif a.recompute_machine: machine()
 else: verify()
if __name__=='__main__': main()
