import sys,json,tempfile,subprocess
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[3]/'tooling/vibe-publisher'))
from test_publisher import Fixture,Evidence,CODE_SHA
import publisher as P
f=Fixture(); f.setUp()
try:
    # Remove binding from canonical history rather than deleting a worktree file.
    f.git('checkout','--orphan','unbound'); f.git('rm','--cached','-r','.')
    (f.source/'binding.json').unlink()
    for p in f.packages:
        root=f.source/p['root']; (root/'LICENSE').unlink()
        m=root/'vibe.toml'; m.write_text(m.read_text().replace('license = "MIT"\n',''))
    old=f.commit()
    for i,p in enumerate(f.packages):
        root=f.source/p['root']; (root/'LICENSE').write_text('MIT\nSynthetic notice\n')
        m=root/'vibe.toml'; m.write_text(m.read_text().replace('1.0.0','1.0.1')+'license = "MIT"\n')
    frozen=f.commit()
    for p in f.packages:
        p['baseline']=frozen; p['baseline_disposition']='https://github.com/fixture/private-source/issues/1#issuecomment-1'
    f.save_binding(); onboard=f.commit(); f.api=Evidence(f.binding,[frozen,onboard])
    for label,rev in [('historical-source',frozen),('binding-integration',onboard)]:
        rows=P.plan(f.source,rev,'unbound',f.binding,f.api,CODE_SHA,'binding.json')['packages']
        print(label,json.dumps([{'status':r['status'],'reason_code':r.get('reason_code')} for r in rows]))
    (f.source/'research.txt').write_text('Unrelated evidence'); unrelated=f.commit()
    print('later-evidence',json.dumps([r['status'] for r in P.plan(f.source,unrelated,'unbound',f.binding,f.api,CODE_SHA,'binding.json')['packages']]))
finally: f.doCleanups()
