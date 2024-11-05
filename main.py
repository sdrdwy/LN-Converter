import converter
import os
import mania
def get_arg_str(settings,randarg):
    arg='('
    if(settings['is_random']==0):
        arg+='Inv '
    else:
        arg+='Rel '
        if(randarg['max_gap']!=0):
            arg+='maxGap='+str(randarg['max_gap'])+" "
        else:
            arg+='minLen='+str(randarg['min_length'])+" "
            if(randarg['max_length']>0):
                arg+='maxLen='+str(randarg['min_length'])+" "
    arg+='shortest= '+str(settings['min_length'])+" "
    if(settings['is_tempo']!=0):
        arg+='T= '+str(int(1/settings['tempo']))+" "
    else:
        arg+="minGap= "+str(settings['min_gap'])
    arg+=')'
    return arg
def main():
    settings={
    'is_random':1,
    'min_length':40,
    'is_tempo':0,
    'min_gap':60,
    'tempo':1/8,
    'is_units':0,
    'min_units':0
    }   
    randarg={
    'is_rand':0,
    'max_gap':0,
    'min_length':200,
    'max_length':-1,
    }
    file=input("Input file path:").strip('"').strip("'")
    if(not os.path.exists(file)):
        print('file not exist')
    else:
        settings['is_random']=int(input("random release? (1=Y 0=N)"))
        if(settings['is_random']==1):
            randarg['is_rand']=1
            randarg['max_gap']=int(input("max gap between tail and next note (0 for not use this arg):"))
            randarg['min_length']=int(input("minimal ln length:"))
            randarg['max_length']=int(input("max ln length: (0 for not use this arg)"))
        settings['is_tempo']=int(input("is tempo? (1=Y 0=N)"))
        if(settings['is_tempo']==1):
            settings['tempo']=1/float(input("T=(eg:4,8)"))
        else:
            settings['min_gap']=int(input("minimum gap between tail and next note:"))
        settings['min_length']=int(input("lower bound of ln(lower than this->rc):"))
        m=mania.Mania(file)
        n=converter.convert(m,settings,randarg)
        n.osu.data['[Metadata]']['Version']+=get_arg_str(settings,randarg)
        index=file.find(".osu")
        sfile=file[:index]+get_arg_str(settings,randarg)+".osu"
        n.save_file(sfile)
if __name__ == "__main__":
    main()