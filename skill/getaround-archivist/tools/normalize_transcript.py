"""Normalize a Teams meeting transcript to lines of `SPEAKER (Character): text`.
Usage: python3 normalize_transcript.py <transcript> [<transcript> ...] [-o OUTDIR]
Without -o, prints to stdout. Add new joke display-names to ALIAS / HAIRY below.
Accepts: VTT, Teams markdown export (plain text with .docx extension), and
real Word .docx (requires python-docx).
"""
import re,sys,os
ALIAS={
 'Phil':'PHIL (Tordrug)','Phil Smith':'PHIL (Tordrug)',
 'Jacob Featherstone':'JAKE (Fic)',
 'Steve Shaddick':'STEVE (PQNine)','Steve Shaddick (LCL)':'STEVE (PQNine)',
 'Jeff Burke':'JEFF (Baron)','El Jeff eh':'JEFF (Baron)','Halfhammer':'JEFF (Baron)','D Bro':'JEFF (Baron)',
}
HAIRY={'WHITRED, Peter','Peedub','Peedubyuh','pw','whitmo','yeahimlate...sowhat?!?','imdaboss','Thesameone','thesameaslasttime','Sameaslasttime','sameaslasttime'}
FILLER=re.compile(r"^(yeah|yep|yes|no|ok|okay|oh|um|uh|mhm|right|alright|all right|sure|so|hmm|nice|wow|what|huh|cool|haha|ha|lol|oh yeah|oh no|oh okay|oh ok|and|but|i|the)[.!?,]*$",re.I)
def canon(n):
    n=n.strip()
    if n in ALIAS: return ALIAS[n]
    if n in HAIRY: return 'SAMEASLASTTIME (Hairy)'
    return 'DM'
def extract(path):
    with open(path,'rb') as f: head=f.read(2)
    if head==b'PK':
        import docx
        return '\n'.join(p.text for p in docx.Document(path).paragraphs)
    return open(path,encoding='utf-8',errors='ignore').read()
def parse(path):
    t=extract(path); turns=[]
    if '-->' in t[:500]:
        for blk in re.split(r'\n\s*\n',t):
            ls=[l for l in blk.strip().split('\n') if l.strip()]
            if len(ls)>=3 and '-->' in ls[0]: turns.append((ls[1],' '.join(ls[2:])))
    elif re.search(r'^\*\*.+?\*\*\s*\d+:\d+',t,re.M):
        cur=None;buf=[]
        for l in t.split('\n'):
            m=re.match(r'^\*\*(.+?)\s*\*\*\s*\d+:\d+',l)
            if m:
                if cur: turns.append((cur,' '.join(buf)))
                cur=m.group(1);buf=[]
            elif cur and l.strip(): buf.append(l.strip())
        if cur: turns.append((cur,' '.join(buf)))
    else:
        cur=None;buf=[]; HDR=re.compile(r"^(.+?)\s{2,}\d+:\d+(:\d+)?\s*$")
        for l in t.split('\n'):
            s=l.strip()
            if not s: continue
            m=HDR.match(l) or HDR.match(s)
            if m:
                if cur: turns.append((cur,' '.join(buf)))
                cur=m.group(1).strip();buf=[]
            elif cur: buf.append(s)
        if cur: turns.append((cur,' '.join(buf)))
    out=[]
    for sp,tx in turns:
        sp=canon(sp); tx=tx.strip()
        if not tx or FILLER.match(tx): continue
        if out and out[-1][0]==sp: out[-1][1]+=' '+tx
        else: out.append([sp,tx])
    return out
if __name__=="__main__":
    args=sys.argv[1:]; out=None
    if '-o' in args: k=args.index('-o'); out=args[k+1]; del args[k:k+2]
    for f in args:
        text='\n'.join(f"{s}: {t}" for s,t in parse(f))
        if out:
            os.makedirs(out,exist_ok=True)
            open(os.path.join(out,os.path.basename(f).rsplit('.',1)[0]+'.txt'),'w').write(text)
        else: print(text)
