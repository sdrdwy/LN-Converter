from mania import Mania
from utils import *
from copy import deepcopy
import random
'''
HitObjects:
    0 x: where notes begin floor(x*keycount/512) = keypos; keypos between 0 and keycount-1
    1 y: dosen't matter 
    2 begin: start time
    3 type: 1/5->note;128->ln
    4 voice: dosen't matter
    5 endtime: note ends, useful for mania
    6 v_group: dosen't matter
    type=1 or 5->note //00000101
    type=128->LN    //01111111
TimingPoints:
    0 begintime: timing begin
    1 beatlength: bpm=1000*60/beatlength; when beatlength<0: this is green line, might not important for conversion
    2 meter: egL4/4
    3 sampleset: dosen't matter
    4 sampleIndex: dosen't matter
    5 volume: dosen't matter
    6 uninherited: dosen't matter
    7 effects: dosen't matter

'''
def getbpmlist(timingpoints:list):
    bpm=[]
    for i in timingpoints:
        t={}
        if(len(i)==1):
            continue
        
        t['begin']=int(float(i[0]))
        t['bpm']=1/float(i[1])*1000*60
        t['ms']=float(i[1])
        if(t['bpm']>0):
            bpm.append(t)
    return bpm
def getnotebpm(begin,bpms:list):
    begin=int(begin)
    cur=bpms[0]
    for i in range(0,len(bpms)):
        if(bpms[i]['begin']<=begin):
            cur=bpms[i]
        else:
            return cur
    return cur
randarg={
    'is_rand':1,
    'max_gap':0,
    'min_length':200,
    'max_length':-1,
    'min_percent':0,
    'max_percent':1,
}
def convert_core(note1,note2,ms,minlength=0,randarg=None):
    begin=int(note1[2])
    end=int(note2[2])-ms
    type_='128'
    if(randarg['is_rand']==1):
        length=end-begin
        if(end-begin>=randarg['min_length']):
            if(randarg['max_length']<=0):
                length=random.randint(randarg['min_length'],end-begin)
            else:
                length=random.randint(randarg['min_length'],randarg['max_length'])
            end=begin+length
        if randarg['max_gap']>ms:
            end=int(note2[2])-random.randint(ms,randarg['max_gap'])
        if(end>int(note2[2])-ms):
            end=int(note2[2])-ms
    if(end-begin<=minlength):
        type_='1'
        end=0
    
    if note1[3]=='1' or note1[3]=='5':
        v_group=':0:0:0:0:'
    else:
        v_group=note1[6]
    return gen_key(note1[0],note1[1],begin,type_,note1[4],end,v_group)

def convert(chart:Mania,settings,randarg) -> Mania:
    bpms=getbpmlist(chart.osu.data["[TimingPoints]"])
    for i in range(chart.cs):
        for j in range(0,len(chart.key_index[i])-1):
            note1=chart.keys[chart.key_index[i][j]]
            note2=chart.keys[chart.key_index[i][j+1]]
            minlength=settings["min_length"]
            if settings["is_random"] == 0:
                if(settings["is_tempo"]==1):
                    ms=bpm2ms(getnotebpm(note2[2],bpms)['bpm'],tempo=settings['tempo'])
                else:
                    ms=settings["min_gap"]
            else:
                ms=settings["min_gap"]
                if(settings["is_units"]==1):
                    ms=normalize(settings["min_units"],ms)
            k=convert_core(note1,note2,ms,minlength,randarg)
            chart.keys[chart.key_index[i][j]]=k
    return chart
settings={
    'is_random':1,
    'is_rlength':0,
    'min_length':40,
    'is_tempo':0,
    'min_gap':60,
    'tempo':1/8,
    'is_units':0,
    'min_units':0
}
if __name__ == "__main__":
    m=Mania("E:\\osumap\\osu!\\Songs\\2049944 Bambinton - Zaya\\Bambinton - Zaya (YuEast 2018) [Northern Story.].osu") 
    n=convert(m,settings,randarg)
    n.osu.data['[Metadata]']['Version']+=' test'
    n.osu.data['[Metadata]']['BeatmapID']='-1'
    n.save_file("E:\\osumap\\osu!\\Songs\\2049944 Bambinton - Zaya\\Bambinton - Zaya (YuEast 2018) [Northern Story. test].osu")