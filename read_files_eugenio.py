import matplotlib.pyplot as plt
from commands import multi, removerbackground, removekalpha, normalizar, removerzero, background, processing_of_data, lenar_calc, read_file, center_psi


if __name__ == "__main__":

    center_list =[]
    psi_list =[]

    print('Start')


    dados='P_L_PB_1_'
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
    plt.show()
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
