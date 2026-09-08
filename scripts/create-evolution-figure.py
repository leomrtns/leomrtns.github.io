from pathlib import Path
p=Path(__file__).resolve().parents[1]/'assets/design/evolution.svg'
s=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 580 400" role="img" aria-labelledby="title desc"><title id="title">Shared ancestry and sequence variation</title><desc id="desc">An illustrative tree connects eight aligned DNA sequences. Colours identify the four nucleotide bases. Branch lengths are schematic.</desc>']
s.append('<g font-family="Segoe UI,Arial,sans-serif" font-size="14" fill="#526d79"><text x="22" y="25">ANCESTRY</text><text x="274" y="25">SEQUENCE ALIGNMENT</text></g>')
ys=[65+i*36 for i in range(8)]
def branch(x,y,xx,yy,c):
 s.append(f'<path d="M{x} {y}H{xx}V{yy}" fill="none" stroke="{c}" stroke-width="2.5" stroke-linejoin="round"/>')
def tree(ids,x,parent=None):
 y=sum(ys[i] for i in ids)/len(ids)
 c='#126c70' if max(ids)<4 else '#275ca0' if min(ids)>=4 else '#526d79'
 if parent: branch(parent[0],parent[1],x,y,c)
 if len(ids)==1:
  s.append(f'<path d="M{x} {y}H226" stroke="{c}" stroke-width="2.5"/><circle cx="226" cy="{y}" r="4" fill="{c}"/>')
 else:
  tree(ids[:len(ids)//2],x+52,(x,y));tree(ids[len(ids)//2:],x+52,(x,y))
tree(list(range(8)),28)
seqs=['ACGTACGTAC','ACGTACGTAT','ACGTATGTAC','ACGTATGTAT','ATGTACGCAC','ATGTACGCAT','ATGTATGCAC','ATGTATGCAT']
colors={'A':('#d5ebe5','#126c70'),'C':('#dbe8f6','#275ca0'),'G':('#f2e7cf','#7c5920'),'T':('#e6def0','#6a4892')}
for i,(seq,y) in enumerate(zip(seqs,ys)):
 s.append(f'<text x="241" y="{y+5}" font-family="monospace" font-size="14" fill="#526d79">{i+1}</text>')
 for j,b in enumerate(seq):
  bg,fg=colors[b];x=274+j*28
  s.append(f'<rect x="{x}" y="{y-13}" width="24" height="27" rx="3" fill="{bg}"/><text x="{x+12}" y="{y+5}" text-anchor="middle" font-family="monospace" font-size="16" font-weight="600" fill="{fg}">{b}</text>')
s.append('<path d="M28 355H226" stroke="#a9bdc7"/><text x="28" y="378" font-family="Segoe UI,Arial" font-size="13" fill="#526d79">Illustrative tree · no scale</text>')
for j,(b,(bg,fg)) in enumerate(colors.items()):
 x=286+j*67
 s.append(f'<circle cx="{x}" cy="361" r="5" fill="{fg}"/><text x="{x+12}" y="366" font-family="monospace" font-size="14" fill="#526d79">{b}</text>')
s.append('</svg>');p.write_text(''.join(s))
