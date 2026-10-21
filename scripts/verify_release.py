"""Offline consistency and integrity checks for this limited public package."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
ALLOWED = frozenset({
    '.gitignore','.gitattributes','README.md','METHODS.md','DATA_SOURCES.md','OMITTED_FILES.md',
    'LICENSE','LICENSE-DATA.md','LICENSE_SCOPE.md','CITATION.cff','PROVENANCE.json','MANIFEST.json',
    'data/draft_summary.json','data/draft_picks.json','data/team_scores.json','data/source_receipts.json',
    'scripts/verify_release.py','tests/test_verify_release.py',
})
PROVIDERS = frozenset({'anthropic','deepseek','gemini','meta','mistral','moonshot','openai','qwen','xai','zai'})

def require(condition, message):
    if not condition:
        raise ValueError(message)

def read(root, relative):
    return json.loads((root/relative).read_text(encoding='utf-8'))

def public_files(root):
    paths = []
    for path in root.rglob('*'):
        relative = path.relative_to(root)
        if '.git' in relative.parts or '__pycache__' in relative.parts:
            continue
        require(not path.is_symlink(), 'Symlinks are not allowed')
        if path.is_file():
            paths.append(relative.as_posix())
    return set(paths)

def validate_records(summary, picks, scores, receipts, provenance):
    require(summary['settled_picks']==150 and summary['ai_picks']==96 and summary['organizer_picks']==54, 'Draft totals')
    require(summary['opening_lineup_author']=='ORGANIZER' and summary['in_season_ai_management_operated'] is False, 'Management disclosure')
    require(summary['fallback_policy']=='ASCENDING_PLAYER_ID_LEGAL_COMPLETION', 'Fallback disclosure')
    require(len(summary['providers'])==10 and {r['provider'] for r in summary['providers']}==PROVIDERS, 'Provider population')
    require(len(picks['picks'])==150 and {p['pick'] for p in picks['picks']}==set(range(1,151)), 'Unique picks')
    require(all(set(p)=={'pick','provider','origin','mechanism','player_id','player_name'} for p in picks['picks']), 'Pick field allowlist')
    require(all(isinstance(p['player_id'],str) and p['player_id'].strip() for p in picks['picks']) and len({p['player_id'] for p in picks['picks']})==150, 'Unique player IDs')
    require(all(isinstance(p['player_name'],str) and p['player_name'].strip() and not any(ord(c)<32 for c in p['player_name']) for p in picks['picks']), 'Player names')
    require(all(p['provider'] in PROVIDERS and p['origin'] in {'AI','ORGANIZER','FALLBACK'} for p in picks['picks']), 'Pick identity')
    count=Counter((p['provider'],p['origin']) for p in picks['picks'])
    require(sum(p['origin']=='AI' for p in picks['picks'])==96, 'AI total')
    for row in summary['providers']:
        provider=row['provider']
        require(row['ai_picks']==count[provider,'AI'] and row['organizer_picks']==count[provider,'ORGANIZER']+count[provider,'FALLBACK'], 'Attribution mismatch')
        require(row['ai_picks']+row['organizer_picks']==15, 'Roster pick count')
    require(scores['included_weeks']==[1,2,3,4,5], 'Common week basis')
    require(scores['week_states']=={'1':'FINAL','2':'PROVISIONAL','3':'PROVISIONAL','4':'PROVISIONAL','5':'PROVISIONAL'}, 'Finality disclosure')
    require(scores['treatment']=='UNCHANGED_ORGANIZER_LINEUPS_AI_MANAGEMENT_INACTIVE', 'Scoring treatment')
    require(len(scores['teams'])==10 and {r['provider'] for r in scores['teams']}==PROVIDERS, 'Scoring population')
    for row in scores['teams']:
        require(set(row['weeks_milli'])=={'1','2','3','4','5'}, 'Missing week')
        require(all(type(v) is int and v%20==0 for v in row['weeks_milli'].values()), 'Missing or invalid score')
        require(type(row['cumulative_milli']) is int and row['cumulative_milli']==sum(row['weeks_milli'].values()), 'Cumulative total')
    order=[r['provider'] for r in sorted(scores['teams'],key=lambda r:(-r['cumulative_milli'],r['provider']))]
    require(scores['provisional_cumulative_order']==order, 'Cumulative order')
    require(len(receipts['receipts'])==25, 'Receipt population')
    require(len({r['source_receipt_path'] for r in receipts['receipts']})==25, 'Duplicate receipt')
    receipt_fields={'source_receipt_path','original_receipt_sha256','download_url','http_status','raw_artifact_sha256','bytes','retrieved_at','third_party_bytes_included'}
    for row in receipts['receipts']:
        require(set(row)==receipt_fields and row['third_party_bytes_included'] is False, 'Receipt field allowlist')
        url=urlsplit(row['download_url'])
        require(url.scheme=='https' and not url.query and not url.fragment and not url.username and not url.password, 'Unsafe receipt URL')
        require(row['http_status']==200 and type(row['bytes']) is int and row['bytes']>0, 'Receipt retrieval')
        require(all(re.fullmatch('[0-9a-f]{64}',row[k]) for k in ('raw_artifact_sha256','original_receipt_sha256')), 'Receipt fingerprint')
    for key in ('original_git_history_imported','original_code_snapshots_included','databases_included','raw_source_data_included','full_reproduction_supported'):
        require(provenance[key] is False, 'Release scope changed')
    require(len(provenance['historical_commits'])==5 and all(re.fullmatch('[0-9a-f]{40}',v) for v in provenance['historical_commits'].values()), 'Historical anchors')

def verify(root=ROOT):
    root=Path(root)
    require(public_files(root)==ALLOWED, 'Unexpected or missing public file')
    manifest=read(root,'MANIFEST.json')
    require(set(manifest['files'])==ALLOWED-{'MANIFEST.json'}, 'Manifest allowlist')
    for relative,entry in manifest['files'].items():
        raw=(root/relative).read_bytes()
        require(entry=={'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)}, 'File integrity mismatch: '+relative)
    validate_records(read(root,'data/draft_summary.json'),read(root,'data/draft_picks.json'),
                     read(root,'data/team_scores.json'),read(root,'data/source_receipts.json'),read(root,'PROVENANCE.json'))
    return {'state':'MINIMAL_PACKAGE_CHECKS_PASS','files':len(ALLOWED),'picks':150,'ai_picks':96,
            'organizer_picks':54,'scored_weeks':[1,2,3,4,5],'full_reproduction_supported':False,
            'independent_review':'REQUIRED','network_calls':0}

if __name__=='__main__':
    print(json.dumps(verify(),indent=2))
