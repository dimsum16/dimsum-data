#!/usr/bin/env python2.7
#coding=utf-8
'''
Measures MWE and sueprsense labeling performance.
Adapted from AMALGrAM's mweval.py and ssteval.py
https://github.com/nschneid/pysupersensetagger/

@author: Nathan Schneider (nschneid@cs.cmu.edu)
@since: 2015-11-07
'''

from __future__ import print_function, division

import json, os, sys, fileinput, codecs, re
from collections import defaultdict, Counter, namedtuple

from tags2sst import readsents, render



class Ratio(object):
    '''
    Fraction that prints both the ratio and the float value.
    fractions.Fraction reduces e.g. 378/399 to 18/19. We want to avoid this.
    '''
    def __init__(self, numerator, denominator):
        self._n = numerator
        self._d = denominator
    def __float__(self):
        return self._n / self._d if self._d!=0 else float('nan')
    def __str__(self):
        return '{}/{}={:.4f}'.format(self.numeratorS, self.denominatorS, float(self))
    __repr__ = __str__
    def __add__(self, v):
        if v==0:
            return self
        if isinstance(v,Ratio) and self._d==v._d:
            return Ratio(self._n + v._n, self._d)
        return float(self)+float(v)
    def __mul__(self, v):
        return Ratio(self._n * float(v), self._d)
    def __truediv__(self, v):
        return Ratio(self._n / float(v) if float(v)!=0 else float('nan'), self._d)
    __rmul__ = __mul__
    @property
    def numerator(self):
        return self._n
    @property
    def numeratorS(self):
        return ('{:.2f}' if isinstance(self._n, float) else '{}').format(self._n)
    @property
    def denominator(self):
        return self._d
    @property
    def denominatorS(self):
        return ('{:.2f}' if isinstance(self._d, float) else '{}').format(self._d)

def is_tag(t):
    return t in {'B','b','O','o','I','i'}

def f1(prec, rec):
    return 2*prec*rec/(prec+rec) if prec+rec>0 else float('nan')


RE_TAGGING = re.compile(r'^(O|B(o|b[iīĩ]+|[IĪĨ])*[IĪĨ]+)+$'.decode('utf-8'))

def require_valid_mwe_tagging(tagging, kind='tagging'):
    """Verifies the chunking is valid."""
    
    # check regex
    assert RE_TAGGING.match(''.join(tagging).decode('utf-8')),kind+': '+''.join(tagging)


def form_groups(links):
    """
    >>> form_groups([(1, 2), (3, 4), (2, 5), (6, 8), (4, 7)])==[{1,2,5},{3,4,7},{6,8}]
    True
    """
    groups = []
    groupMap = {} # offset -> group containing that offset
    for a,b in links:
        assert a is not None and b is not None,links
        assert b not in groups,'Links not sorted left-to-right: '+repr((a,b))
        if a not in groupMap: # start a new group
            groups.append({a})
            groupMap[a] = groups[-1]
        assert b not in groupMap[a],'Redunant link?: '+repr((a,b))
        groupMap[a].add(b)
        groupMap[b] = groupMap[a]
    return groups


goldmwetypes, predmwetypes = Counter(), Counter()

def mweval_sent(sent, ggroups, pgroups, stats, indata=None):
    
    # verify the taggings are valid
    for k,kind in [(1,'gold'),(2,'pred')]:
        tags = zip(*sent)[k]
        require_valid_mwe_tagging(tags, kind=kind)
        
    if indata:
        gdata, pdata = indata
        stats['Gold_#Groups'] += len(gdata["_"])
        stats['Gold_#GappyGroups'] += sum(1 for grp in gdata["_"] if max(grp)-min(grp)+1!=len(grp))
        if "lemmas" in gdata:
            for grp in gdata["_"]: goldmwetypes['_'.join(gdata["lemmas"][i-1] for i in grp)] += 1
        stats['Pred_#Groups'] += len(pdata["_"])
        stats['Pred_#GappyGroups'] += sum(1 for grp in pdata["_"] if max(grp)-min(grp)+1!=len(grp))
        for grp in pdata["_"]: predmwetypes['_'.join(pdata["lemmas"][i-1] for i in grp)] += 1

    glinks, plinks = [], []
    g_last_BI, p_last_BI = None, None
    g_last_bi, p_last_bi = None, None
    for i,(tkn,goldTag,predTag) in enumerate(sent):
        
        if goldTag!=predTag:
            stats['incorrect'] += 1
        else:
            stats['correct'] += 1
        
        if goldTag=='I':
            glinks.append((g_last_BI, i))
            g_last_BI = i
        elif goldTag=='B':
            g_last_BI = i
        elif goldTag=='i':
            glinks.append((g_last_bi, i))
            g_last_bi = i
        elif goldTag=='b':
            g_last_bi = i
        
        if goldTag in {'O','o'}:
            stats['gold_Oo'] += 1
            if predTag in {'O', 'o'}:
                stats['gold_pred_Oo'] += 1
        else:
            stats['gold_non-Oo'] += 1
            if predTag not in {'O', 'o'}:
                stats['gold_pred_non-Oo'] += 1
                if (goldTag in {'b','i'})==(predTag in {'b','i'}):
                    stats['gold_pred_non-Oo_in-or-out-of-gap_match'] += 1
                if (goldTag in {'B','b'})==(predTag in {'B','b'}):
                    stats['gold_pred_non-Oo_Bb-v-Ii_match'] += 1
                if goldTag in {'I','i'} and predTag in {'I','i'}:
                    stats['gold_pred_Ii'] += 1
        
        
        if predTag=='I':
            plinks.append((p_last_BI, i))
            p_last_BI = i
        elif predTag=='B':
            p_last_BI = i
        elif predTag=='i':
            plinks.append((p_last_bi, i))
            p_last_bi = i
        elif predTag=='b':
            p_last_bi = i
    
    glinks1 = [(a,b) for a,b in glinks]
    plinks1 = [(a,b) for a,b in plinks]
    ggroups1 = [[k-1 for k in g] for g in ggroups]
    assert ggroups1==map(sorted, form_groups(glinks1)),('Possible mismatch between gold MWE tags and parent offsets',ggroups1,glinks1)
    pgroups1 = [[k-1 for k in g] for g in pgroups]
    assert pgroups1==map(sorted, form_groups(plinks1)),('Possible mismatch between predicted MWE tags and parent offsets',pgroups1,plinks1)
    
    # soft matching (in terms of links)
    stats['PNumer'] += sum(1 for a,b in plinks1 if any(a in grp and b in grp for grp in ggroups1))
    stats['PDenom'] += len(plinks1)
    stats['CrossGapPNumer'] += sum((1 if b-a>1 else 0) for a,b in plinks1 if any(a in grp and b in grp for grp in ggroups1))
    stats['CrossGapPDenom'] += sum((1 if b-a>1 else 0) for a,b in plinks1)
    stats['RNumer'] += sum(1 for a,b in glinks1 if any(a in grp and b in grp for grp in pgroups1))
    stats['RDenom'] += len(glinks1)
    stats['CrossGapRNumer'] += sum((1 if b-a>1 else 0) for a,b in glinks1 if any(a in grp and b in grp for grp in pgroups1))
    stats['CrossGapRDenom'] += sum((1 if b-a>1 else 0) for a,b in glinks1)
    
    # exact matching (in terms of full groups)
    stats['ENumer'] += sum(1 for grp in pgroups1 if grp in ggroups1)
    stats['EPDenom'] += len(pgroups1)
    stats['ERDenom'] += len(ggroups1)
    
    for grp in pgroups1:
        gappiness = 'ng' if max(grp)-min(grp)+1==len(grp) else 'g'
        stats['Pred_'+gappiness] += 1

sststats = defaultdict(Counter)
conf = Counter()    # confusion matrix

def ssteval_sent(sent, glbls, plbls):
    
    def lbl2pos(lbl): return lbl.split('.')[0].lower()  # should be "n" or "v"
    
    sstpositions = set(glbls.keys()+plbls.keys())

    sststats['Exact Tag']['nGold'] += len(sent)
    sststats['Exact Tag']['tp'] += len(sent) - len(sstpositions)
    
    for k in sstpositions:
        g = glbls.get(k)
        p = plbls.get(k)
        conf[g,p] += 1
        
        if g:
            sststats[None]['nGold'] += 1
            sststats[lbl2pos(g)]['nGold'] += 1
        if p:
            sststats[None]['nPred'] += 1
            sststats[lbl2pos(p)]['nPred'] += 1
            if g==p:
                sststats['Exact Tag']['tp'] += 1
                sststats[None]['tp'] += 1
                sststats[lbl2pos(g)]['tp'] += 1
    
    sststats['Exact Tag']['Acc'] = Ratio(sststats['Exact Tag']['tp'], sststats['Exact Tag']['nGold'])
    for x in sststats:
        if x!='Exact Tag':
            sststats[x]['P'] = Ratio(sststats[x]['tp'], sststats[x]['nPred'])
            sststats[x]['R'] = Ratio(sststats[x]['tp'], sststats[x]['nGold'])
            sststats[x]['F'] = f1(sststats[x]['P'], sststats[x]['R'])
    
class Colors(object):
    RED = '\033[91m'
    GREEN = '\033[92m'
    ORANGE = '\033[93m'
    YELLOW = '\033[33m'
    BLUE = '\033[94m'
    PINK = '\033[95m'
    ENDC = '\033[0m'    # end color

def color_render(*args, **kwargs):
    # terminal colors
    WORDS = Colors.YELLOW
    VERBS = Colors.RED
    NOUNS = Colors.BLUE
    MWE = Colors.ENDC
    
    s = render(*args, **kwargs)
    c = WORDS+s.replace('_',MWE+'_'+WORDS)+Colors.ENDC
    c = re.sub(r'(\|v.\w+)', VERBS+r'\1'+WORDS, c)   # verb supersenses
    c = re.sub(r'(\|n.\w+)', NOUNS+r'\1'+WORDS, c)   # noun supersenses
    
    return c
    
if __name__=='__main__':
    args = sys.argv[1:]
    printSents = False
    while args and args[0].startswith('-'):
        if args[0]=='-p':   # print sentences to stderr
            printSents = True
        elif args[0]=='-C': # turn off colors
            for c in dir(Colors):
                if not c.startswith('_'):
                    setattr(Colors, c, '')
        else:
            assert False,'Unexpected option: '+args[0]
        args = args[1:]
    stats = Counter()
    
    nToks = nFullTagCorrect = 0
    
    sent = []
    goldFP, predFP = args
    predF = readsents(fileinput.input(predFP))
    for gdata in readsents(fileinput.input(goldFP)):
        gtags_mwe = [t.encode('utf-8') for t in gdata["tags"]]
        assert all(len(t)<=1 for t in gtags_mwe)
        glbls = {k-1: v[1].encode('utf-8') for k,v in gdata["labels"].items()}
        pdata = next(predF)
        ptags_mwe = [t.encode('utf-8') for t in pdata["tags"]]
        plbls = {k-1: v[1].encode('utf-8') for k,v in pdata["labels"].items()}
        assert all(len(t)<=1 for t in ptags_mwe)
        words, poses = zip(*gdata["words"])
        assert len(words)==len(gtags_mwe)==len(ptags_mwe)
        nToks += len(words)
        nFullTagCorrect += sum(1 for k in range(len(words)) if gtags_mwe[k]==ptags_mwe[k] and glbls.get(k)==plbls.get(k))
        if printSents:
            print(color_render(words, gdata["_"], [], {k+1: v for k,v in glbls.items()}), file=sys.stderr)
            print(color_render(words, pdata["_"], [], {k+1: v for k,v in plbls.items()}), file=sys.stderr)
        try:
            mweval_sent(zip(words,gtags_mwe,ptags_mwe), gdata["_"], pdata["_"], stats, indata=(gdata,pdata))
            
            ssteval_sent(words, glbls, plbls)
        except AssertionError as ex:
            print(render(words, gdata["_"], []))
            print(render(words, pdata["_"], []))
            raise ex
    
    fullAcc = Ratio(nFullTagCorrect, nToks)
    
    nTags = stats['correct']+stats['incorrect']
    stats['Acc'] = Ratio(stats['correct'], nTags)
    stats['Tag_R_Oo'] = Ratio(stats['gold_pred_Oo'], stats['gold_Oo'])
    stats['Tag_R_non-Oo'] = Ratio(stats['gold_pred_non-Oo'], stats['gold_non-Oo'])
    stats['Tag_Acc_non-Oo_in-gap'] = Ratio(stats['gold_pred_non-Oo_in-or-out-of-gap_match'], stats['gold_pred_non-Oo'])
    stats['Tag_Acc_non-Oo_B-v-I'] = Ratio(stats['gold_pred_non-Oo_Bb-v-Ii_match'], stats['gold_pred_non-Oo'])
    stats['Tag_Acc_I_strength'] = Ratio(stats['gold_pred_Ii_strength_match'], stats['gold_pred_Ii'])
    
    
    stats['P'] = Ratio(stats['PNumer'], stats['PDenom'])
    stats['R'] = Ratio(stats['RNumer'], stats['RDenom'])
    stats['F'] = f1(stats['P'], stats['R'])
    stats['CrossGapP'] = stats['CrossGapPNumer']/stats['CrossGapPDenom'] if stats['CrossGapPDenom']>0 else float('nan')
    stats['CrossGapR'] = stats['CrossGapRNumer']/stats['CrossGapRDenom'] if stats['CrossGapRDenom']>0 else float('nan')
    stats['EP'] = Ratio(stats['ENumer'], stats['EPDenom'])
    stats['ER'] = Ratio(stats['ENumer'], stats['ERDenom'])
    stats['EF'] = f1(stats['EP'], stats['ER'])
    
    if goldmwetypes:
        assert stats['Gold_#Groups']==sum(goldmwetypes.values())
        stats['Gold_#Types'] = len(goldmwetypes)
    assert stats['Pred_#Groups']==sum(predmwetypes.values())
    stats['Pred_#Types'] = len(predmwetypes)
    
    print('mwestats = ', dict(stats), ';', sep='')
    print()
    print('sststats = ', dict(sststats), ';', sep='')
    print()
    print('conf = ', dict(conf), ';', sep='')
    print()
    print('   P   |   R   |   F   |   EP  |   ER  |   EF  |  Acc  |   O   | non-O | ingap | B vs I')
    parts = [(' {:.2%}'.format(float(stats[x])), 
              '{:>7}'.format('' if x.endswith('F') or isinstance(stats[x],(float,int)) else stats[x].numeratorS), 
              '{:>7}'.format('' if x.endswith('F') or isinstance(stats[x],(float,int)) else stats[x].denominatorS)) for x in ('P', 'R', 'F', 'EP', 'ER', 'EF', 'Acc', 
              'Tag_R_Oo', 'Tag_R_non-Oo', 
              'Tag_Acc_non-Oo_in-gap', 'Tag_Acc_non-Oo_B-v-I')]
    for pp in zip(*parts):
        print(' '.join(pp))
        
    #print(predmwetypes)
    
    # supersenses
    print('  Acc  |   P   |   R   |   F   || R: NSST | VSST ')
    parts = [(' {:.2%}'.format(float(sststats['Exact Tag']['Acc'])),
              '{:>7}'.format(sststats['Exact Tag']['Acc'].numeratorS),
              '{:>7}'.format(sststats['Exact Tag']['Acc'].denominatorS))]
    parts += [(' {:.2%}'.format(float(sststats[None][x])),
               '{:>7}'.format(sststats[None][x].numeratorS),
               '{:>7}'.format(sststats[None][x].denominatorS)) for x in ('P', 'R')]
    parts += [(' {:.2%}  '.format(float(sststats[None]['F'])),
               '         ',
               '         ')]
    parts += [(' {:.2%}'.format(float(sststats[y]['R'])),
               '{:>7}'.format(sststats[y]['R'].numeratorS),
               '{:>7}'.format(sststats[y]['R'].denominatorS)) for y in ('n', 'v')]
    for pp in zip(*parts):
        print(' '.join(pp))
    
    # combined acc, P, R, F
    cstats = Counter()
    cstats['Acc'] = fullAcc
    cstats['P'] = Ratio(stats['P'].numerator + sststats[None]['P'].numerator, 
                        stats['P'].denominator + sststats[None]['P'].denominator)
    cstats['R'] = Ratio(stats['R'].numerator + sststats[None]['R'].numerator, 
                        stats['R'].denominator + sststats[None]['R'].denominator)
    cstats['F'] = f1(cstats['P'], cstats['R'])
    
    print()
    print('SUMMARY SCORES')
    print('==============')
    print(re.sub(r'=([^=]+)$', '='+Colors.YELLOW+r'\1'+Colors.ENDC, 'MWEs: P={stats[P]} R={stats[R]} F={f:.2%}'.format(stats=stats, f=float(stats['F']))))
    print(re.sub(r'=([^=]+)$', '='+Colors.PINK+r'\1'+Colors.ENDC, 'Supersenses: P={stats[P]} R={stats[R]} F={f:.2%}'.format(stats=sststats[None], f=float(sststats[None]['F']))))
    print(re.sub(r'=([^=]+)$', '='+Colors.GREEN+r'\1'+Colors.ENDC, 'Combined: Acc={stats[Acc]} P={stats[P]} R={stats[R]} F={f:.2%}'.format(stats=cstats, f=float(cstats['F']))))
