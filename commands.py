import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from lmfit.models import VoigtModel,PseudoVoigtModel, LinearModel
from scipy import stats

def LPM(theta,psi):
    radians     = np.radians(theta)
    radiansby2  = np.radians(theta/2)
    radianpsi   = np.radians(psi)

    cima  = 1  + np.cos(radians)**2
    baixo = np.sin(radiansby2)**2
    lado  = 1 - np.tan(radianpsi)/np.tan(radiansby2)

    LPM_value = (cima/baixo)*lado

    return LPM_value

def Lorentz_polarization_modified(psi,x,y):
    new_list =[]
    for key, value in enumerate(x):
        new = LPM(value,psi)
        new_list.append(y[key]/new)
    #import pdb;pdb.set_trace()
    return (new_list)

def plotar_intensity_position():
    plt.grid()
    plt.legend(loc=0)
    plt.xlabel('Position (2/Theta)')
    plt.ylabel('Intensity(u.a.)')
    plt.show()

#return K const, based in sample
def multi(E=210000,v=0.3,theta2=156):
    theta2/=2
    V=2.0*(1.0+v)
    theta = np.radians(theta2)
    theta = np.tan(theta)
    theta = 1.0/theta
    theta *= (np.pi/180.0)
    theta *=E
    theta /=-1.0*V
    ##    return theta/9.8#kg
    return theta#Mpa

##################################
#Cleand Data
#return novot
def removekalpha(y,x):
    novoy=[]
    lambida2=1.541220
    lambida1=1.537400
    deltaL = lambida2 - lambida1
    deltaL = deltaL/lambida1
    diferenca=x[1]-x[0]

    for i in range(len(y)):
        deltasoma = x[1]-x[0]
        ase= np.tan(np.radians(x[i]/2))*2*deltaL/(diferenca)
        n=1;

        while(ase>deltasoma):
            deltasoma=deltasoma+diferenca
            n+=1
        try:
            yy=y[i]-0.5*y[i-n]

            if yy<0:yy=(yy+y[i])/8

            novoy.append(yy)
        except:
            novoy.append(y[i])

    return novoy

#return y
def background(y):
    minimo=min(y)
    for i in range(len(y)):
        y[i]-=minimo
    return y

#return y
def normalizar(y):
    minimo=max(y)
    for i in range(len(y)):
        y[i]/=minimo
    return y

def removerzero(vetor):
    for key, value in enumerate(vetor):
        if value <0:
            vetor[key]=0

    for key,value in enumerate(vetor):
        try:
            if vetor[key+1]==0 and value >0:
                vetor[key]=0
        except:
            pass
    return vetor

def removerbackground(x,y,m=5):

    minimo= np.mean( np.sort(y)[:10])
    for i in range(len(y)):
        y[i]=y[i]-minimo
    slope, intercept, r_value, p_value, std_err = stats.linregress(np.append(x[:m],x[-m:]),np.append(y[:m],y[-m:]))
    abline_values = [slope * i + intercept for i in x]
    abline_values=np.asarray(abline_values)
    return removerzero(y-abline_values)
#Cleand Data


def processing_of_data(psi,x,y):
    #y = normalizar(y)

    y = background(y)

    y = removerbackground(x,y)


    #import pdb;pdb.set_trace()
    #plt.plot(y)
    y = Lorentz_polarization_modified(psi,x,y)
    #plt.plot(y);plt.show();import pdb;pdb.set_trace()
    #y = removekalpha(x,y)

    y = savgol_filter(y, 5, 2)

    y = normalizar(y)

    return y


def lenar_calc(x,y):
    mod = LinearModel()
    pars = mod.guess(y, x=x)
    out  = mod.fit(y, pars, x=x)
    calc= out.best_values['slope']
    stress=calc*multi()
    stress=round(stress,3)
    #plt.plot(x,out.bes_fit)
    return stress, x , out.best_fit,out
    #print(out.best_values)


def read_file(file_name):
    psi=0
    r = open(file_name,'r')
    printar = False
    vx = []
    vy = []
    for i in r:
        if printar:
            value = i.split(' ')
            x=value[3]
            x = float(x)
            vx.append(x)
            y=value[-1].split('\n')[0]
            y =float(y)
            vy.append(y)
        if not printar and '<2Theta>   <   I   >' in i:
            printar = True
        if not printar and 'psi angle' in i:
            value = i.split(' ')
            psi=float(value[-3])
            psi=np.sin(np.radians(psi))**2

    vx = np.asarray(vx)
    vy = np.asarray(vy)
    return psi, vx, vy


def calc_center_pseudoVoigt(vx,vy):
    mod     = PseudoVoigtModel()
    y       = vy
    pars    = mod.guess(y, x=vx)
    out     = mod.fit(y, pars, x=vx)
    center  = out.best_values['center']
    return center

def parabol(x):
    import pdb; pdb.set_trace()
#    for key, value in enumerate(x):


def center_psi(file_name):
    #print(file_name)
    psi, vx, vy = read_file(file_name)
    vy = processing_of_data(psi,vx,vy)
    legenda = file_name.split('/')[-1]
    #plt.grid()
    #plt.legend(loc=0)
    import pdb; pdb.set_trace()
    plt.plot(vx,vy,label=legenda)
    mod = PseudoVoigtModel()
    y=vy
    pars = mod.guess(y, x=vx)
    out  = mod.fit(y, pars, x=vx)
    center =out.best_values['center']
    print('center: {} <--> psi: {}'.format(center,psi))
    return psi, center



#Medidas Rigaku
def get_value(i):
    return float(i.split(' ')[-1].split('\n')[0])


#list_keys = list(dicio.keys())


def red_file_rigaku(folder_name):
    dicio={
        '*START':0.0,
        '*STOP' :0.0,
        '*STEP' :0.0,
        '*ST_PSI_ANGLE':0.0
    }

    dados={}

    file ='P_L_1/P_PB_L_1.ASC'
    file = folder_name
    r = open(file,'r')
    find_intensity=False
    x=[]
    y=[]
    for i in r:
        #print(i)
        if '*END' in i:
            find_intensity=False
            vx = np.asarray(x)
            vy = np.asarray(y)
            vy = processing_of_data(dicio['*ST_PSI_ANGLE'],vx,vy)
            #import pdb; pdb.set_trace()
            plt.plot(vx,vy,label=dicio['*ST_PSI_ANGLE'])

            #plt.plot(vy)
            dados[dicio['*ST_PSI_ANGLE']]={}
            dados[dicio['*ST_PSI_ANGLE']]['x']=vx
            dados[dicio['*ST_PSI_ANGLE']]['y']=vy
            x=[]
            y=[]
        elif find_intensity:
            value = i.split(',')
            for i in value:
                if len(x)==0:
                    x.append(dicio['*START'])
                    y.append(float(i))
                    dicio['*NEW_DICIO']=(dicio['*START']+dicio['*STEP'])
                else:
                    x.append(dicio['*NEW_DICIO'])
                    dicio['*NEW_DICIO']=(dicio['*NEW_DICIO']+dicio['*STEP'])
                    y.append(float(i))
        elif '*START' in i:
            dicio['*START']=get_value(i)
        elif '*STOP' in i:
            dicio['*STOP']=get_value(i)
        elif '*STEP' in i:
            dicio['*STEP']=get_value(i)
        elif '*ST_PSI_ANGLE' in i:
            dicio['*ST_PSI_ANGLE']=get_value(i)
        elif '*COUNT' in i and not '*COUNTER' in i:
            find_intensity=True

    plotar_intensity_position()

    center_list =[]
    psi_list =[]
    for key, value in dados.items():
        psi_list.append(np.sin(np.radians(key))**2)
        center = calc_center_pseudoVoigt(value['x'],value['y'])
        center_list.append(center)
        print('center: {} <--> psi: {}'.format(center,np.sin(np.radians(key))**2))

    legenda ,x,bestY, out= lenar_calc(psi_list,center_list)

    plt.plot(psi_list,center_list,'o',label='Values')
    plt.plot(x,bestY,label='Best')
    miny=int(min(center_list))-2
    maxy=int(max(center_list))+2
    maxx=round(max(psi_list),3)+round(max(psi_list),3)/2
    plt.axis([0,maxx,miny,maxy])

    plt.grid()
    #plt.title(dados)
    plt.legend()
    plt.xlabel('$\sin ^{2}\omega (Mpa)$')
    plt.ylabel('$2\Theta (Degre)$')
    #import pdb;pdb.set_trace()
    plt.title('{}'.format(legenda))
    plt.show()

#Chimazu
def red_files_chimazu(folder_name):
        #dados='P_L_PB_3_'
        center_list =[]
        psi_list =[]

        dados = folder_name
        first_file='P_L_/{}/{}.txt'.format(dados,dados)
        file_names=[]
        file_names.append(first_file)

        for i in range(1,11):
            file_name='P_L_/{}{}/{}{}.txt'.format(dados,str(i),dados,str(i))
            file_names.append(file_name)



        for file_name in file_names:
            psi, center = center_psi(file_name)
            psi_list.append(psi)
            center_list.append(center)
        plotar_intensity_position()
        #print(psi_list)
        #print(center_list)


        miny=int(min(center_list))-2
        maxy=int(max(center_list))+2
        maxx=round(max(psi_list),3)+round(max(psi_list),3)/2
        plt.axis([0,maxx,miny,maxy])

        plt.grid()
        plt.title(dados)
        plt.xlabel('$\sin ^{2}\omega (Mpa)$')
        plt.ylabel('$2\Theta (Degre)$')
        legenda ,x,bestY,out= lenar_calc(psi_list,center_list)
        #plt.legend(legenda)
        plt.plot(psi_list,center_list,'o',label=('{}'.format(legenda)))
        plt.plot(x,bestY)
        plt.legend(loc=0)
        plt.show()
