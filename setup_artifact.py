from __future__ import annotations
import argparse, hashlib, shutil, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
BUNDLES=('experiments.zip','released_results.zip','models.zip')
def sha256(p):
 h=hashlib.sha256();
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''): h.update(b)
 return h.hexdigest()
def safe_extract(zp):
 with zipfile.ZipFile(zp) as z:
  for n in z.namelist():
   q=(ROOT/n).resolve()
   if ROOT.resolve() not in q.parents and q!=ROOT.resolve(): raise RuntimeError(f'unsafe archive member: {n}')
  z.extractall(ROOT)
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--clean',action='store_true'); a=ap.parse_args()
 if a.clean:
  shutil.rmtree(ROOT/'experiments',ignore_errors=True)
  shutil.rmtree(ROOT/'environment',ignore_errors=True)
 for b in BUNDLES: safe_extract(ROOT/b)
 print('Artifact data prepared.')
if __name__=='__main__': main()
