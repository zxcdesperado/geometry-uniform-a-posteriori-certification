from __future__ import annotations
import csv, hashlib, json, math, statistics, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
R=ROOT/'experiments'/'results'
def req(c,m):
 if not c: raise AssertionError(m)
def load(n): return json.loads((R/n).read_text(encoding='utf-8'))
def rows(n):
 with (R/n).open(newline='',encoding='utf-8') as f: return list(csv.DictReader(f))
def sha(p):
 h=hashlib.sha256();
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''): h.update(b)
 return h.hexdigest()
def close(a,b,rt=1e-10,at=1e-12): return math.isclose(float(a),float(b),rel_tol=rt,abs_tol=at)
# Main benchmark and reference study.
op=load('independent_forcing_operator_summary.json')
req(op['benchmark']['train_cases']==96 and op['benchmark']['test_cases']==90,'benchmark size')
req(op['benchmark']['solution_coefficients_exposed_to_model'] is False,'target leakage flag')
ref=load('independent_forcing_reference_convergence_summary.json')
req(ref['grouped']['overall']['cases']==90,'reference cases')
req(ref['grouped']['overall']['level32_to_level64']['max']<0.01,'reference convergence')
# Exact correction and complete RT2 audit.
corr=load('independent_forcing_correction_summary.json')
req(corr['cases']==27 and corr['maximum_relative_identity_defect']<1e-5,'Galerkin correction')
rt=load('independent_forcing_multicheckpoint_rt2_summary.json')
req(rt['cases']==270 and rt['all_covered'],'270 RT2 coverage')
req(rt['grouped']['all']['overall']['relative_linear_residual']['max']<1e-9,'RT linear residual')
gate=load('forcing_certificate_gate_summary.json')
req(gate['prediction_certificate_pairs']==270 and gate['all_accepted_verified'],'certificate gate')
# Official upstream GINO transfer.
g=load('official_upstream_gino_release_verification.json')
req(g['overall']['predictions']==450 and g['overall']['rt2_coverage']==1.0,'GINO transfer')
# Machine GINO rows: recompute key summary fields and checkpoint hashes.
gr=rows('official_gino_machine_rt2_rows.csv'); gs=load('official_gino_machine_rt2_summary.json')
req(len(gr)==9,'GINO machine row count')
req(all(x['majorant_upper_covers_error_upper']=='True' and x['exact_discrete_hdiv_membership']=='True' for x in gr),'GINO machine validity')
for seed in sorted({int(x['seed']) for x in gr}):
 p=R/'official_neuraloperator_gino_checkpoints'/f'official_gino_seed{seed}.pt'; req(p.is_file(),'GINO checkpoint')
 req(all(x['checkpoint_sha256']==sha(p) for x in gr if int(x['seed'])==seed),'GINO checkpoint hash')
req(close(gs['machine_coverage_rate'],1.0) and close(gs['hdiv_membership_rate'],1.0),'GINO machine summary')
# L-shaped nonmanufactured certificate.
l=load('nonmanufactured_lshape_reference_certificate.json')
req(l['two_certificate_consistency'] is True,'L-shape consistency')
req(l['continuous_prediction_error_bracket']['lower']<=l['continuous_prediction_error_bracket']['upper'],'L-shape bracket')
# Cost benchmark and exact endpoint suites.
c=load('optimized_end_to_end_cost_headline_confirmation_summary.json')
cp=R/'trained_operator_rt_checkpoints'/'existing_grid_fno_style_seed27182.pt'
cfg=ROOT/'experiments'/'configs'/'cost_benchmark_base_config.json'
req(c['model_checkpoint_sha256']==sha(cp) and c['base_config_sha256']==sha(cfg),'cost hashes')
req(c['aggregate']['true_best_retained_all'] is True,'screening correctness')
req(all(x['paired_samples']==40 for x in c['rows']),'cost pairs')
req(all(x['upper_95']<1.0 for x in c['rows'] if x['pool']=='cost_broad_125'),'cost intervals')
req(load('poisson_machine_strict_curved_summary.json')['all_machine_strict_covers'],'2D endpoint suite')
req(load('poisson_machine_strict_curved_3d_summary.json')['all_machine_strict_covers'],'3D endpoint suite')
req(load('elasticity_machine_strict_affine_suite_summary.json')['all_machine_checks_pass'],'elasticity endpoint suite')
req(load('delta_local_comparison_summary.json')['all_cases_pass'],'local audit')
print(json.dumps({'status':'PASS','rt2_cases':270,'reference_cases':90,'gino_outputs':450,'gino_machine_cases':9},indent=2))
