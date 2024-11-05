import math
def bpm2ms(bpm,tempo):
    return math.floor((60*1000)/(bpm/tempo))
def ms2bpm(ms):
    return 60*1000/ms
def normalize(bpms,ms):
    ret=ms%bpms
    ms=ms-ret
    if(ret>bpms/2):
        ms+=bpms
    return ms
def gen_key(keys='64',y='192',begin='0',type='1',voice='0',end='0',v_group=':0:0:0:0:'):
        k=[str(keys),str(y),str(begin),str(type),str(voice),str(end),str(v_group)]
        return k
if __name__ == "__main__":
    print(bpm2ms(204,1/4))
    print(ms2bpm(294.1176470588))
    print(normalize(204,30,1/4))
    print(gen_key())