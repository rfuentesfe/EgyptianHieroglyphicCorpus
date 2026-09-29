"""Reproduce public data without modifying the external source."""
import argparse
import hashlib
import io
import json
import platform
from pathlib import Path
import numpy as np
import pandas as pd

SOURCE_SHA256 = "da9079e3c2e2dcd09392c982875f3f071171908705391652c031817017fa6cdb"
COLUMNS = ["Gardiner Code", "Translation English"]
EXPECTED = dict(source_records=123658, incomplete=34, valid=123624,
    duplicate_groups=312, rows_in_duplicate_groups=632, removable_copies=320,
    unique_pairs=123304, train=98643, validation=12330, test=12331)

def normalize_text(x):
    if pd.isna(x):
        return ""
    return " ".join(str(x).strip().split())

def require(ok, message):
    if not ok:
        raise ValueError(message)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def build(source):
    require(pd.__version__ == "1.4.0" and np.__version__ == "1.23.5", "Install requirements.txt versions")
    raw = source.read_bytes()
    require(digest(raw) == SOURCE_SHA256, "Source SHA-256 mismatch; no output written")
    df = pd.read_csv(io.BytesIO(raw))
    normalized = df[COLUMNS].applymap(normalize_text)
    valid = normalized[(normalized != "").all(axis=1)].reset_index(drop=True)
    sizes = valid.groupby(COLUMNS, sort=False).size()
    duplicates = sizes[sizes > 1]
    unique = valid.drop_duplicates(subset=COLUMNS, keep="first").reset_index(drop=True)
    shuffled = unique.sample(frac=1.0, random_state=42).reset_index(drop=True)
    a, b = int(len(unique)*0.8), int(len(unique)*0.1)
    splits = dict(train=shuffled.iloc[:a], validation=shuffled.iloc[a:a+b], test=shuffled.iloc[a+b:])
    counts = dict(source_records=len(df), incomplete=len(df)-len(valid), valid=len(valid),
        duplicate_groups=len(duplicates), rows_in_duplicate_groups=int(duplicates.sum()),
        removable_copies=len(valid)-len(unique), unique_pairs=len(unique),
        **{k:len(v) for k,v in splits.items()})
    require(counts == EXPECTED, "Unexpected counts: " + json.dumps(counts))
    sets = {k:set(v.itertuples(index=False, name=None)) for k,v in splits.items()}
    overlaps = {a+"_"+b:len(sets[a]&sets[b]) for a,b in [("train","validation"),("train","test"),("validation","test")]}
    require(not any(overlaps.values()), "Exact pair overlap")
    require(set.union(*sets.values()) == set(unique.itertuples(index=False,name=None)), "Partition mismatch")
    frames = {"data/gardiner_english_corpus.csv":valid,
              "data/gardiner_english_corpus_deduplicated.csv":unique,
              **{"splits/"+k+".csv":v for k,v in splits.items()}}
    outputs = {}
    for name,frame in frames.items():
        content = frame.to_csv(index=False,line_terminator="\n").encode("utf-8")
        restored = pd.read_csv(io.BytesIO(content),keep_default_na=False)
        require(restored.equals(frame.reset_index(drop=True)), "CSV round-trip mismatch: "+name)
        outputs[name] = content
    audit = dict(source=dict(filename=source.name,sha256=digest(raw),bytes=len(raw)),
        columns=COLUMNS, counts=counts, seed=42,
        normalization='if pd.isna(x): return ""; otherwise return " ".join(str(x).strip().split())',
        read_method="pandas.read_csv defaults; select the two named columns",
        deduplication="drop_duplicates(subset=columns, keep='first'); preserve source order",
        split_method="unique.sample(frac=1.0, random_state=42).reset_index(drop=True); int(n*0.8), int(n*0.1), remainder",
        exact_pair_overlaps=overlaps, split_union_equals_unique_corpus=True,
        serialization="UTF-8 without BOM, LF, header, no index",
        runtime=dict(python=platform.python_version(),pandas=pd.__version__,numpy=np.__version__),
        files={k:dict(bytes=len(v),sha256=digest(v)) for k,v in sorted(outputs.items())})
    outputs["results/corpus_audit.json"] = (json.dumps(audit,ensure_ascii=False,indent=2)+"\n").encode("utf-8")
    # Hash all CSVs and the audit; exclude this manifest itself to avoid self-reference.
    outputs["results/SHA256SUMS.txt"] = "".join(digest(v)+"  "+k+"\n" for k,v in sorted(outputs.items())).encode("utf-8")
    return outputs,audit

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source",type=Path,required=True)
    p.add_argument("--output-dir",type=Path,default=Path(__file__).resolve().parents[1])
    p.add_argument("--check",action="store_true",help="Rebuild in memory and verify existing files without writing")
    args=p.parse_args()
    outputs,audit=build(args.source)
    for name in outputs:
        require((args.output_dir/name).resolve()!=args.source.resolve(),"Input/output collision")
    for name,content in outputs.items():
        target=args.output_dir/name
        if not args.check:
            target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes(content)
        require(target.is_file() and target.read_bytes()==content,"Artifact mismatch: "+name)
    print(json.dumps(dict(counts=audit["counts"],exact_pair_overlaps=audit["exact_pair_overlaps"],
        source_sha256=audit["source"]["sha256"],mode="verified" if args.check else "generated and verified"),indent=2))

if __name__ == "__main__":
    main()
