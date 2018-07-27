#import matplotlib.pyplot as plt
#from commands import multi, removerbackground,removekalpha, normalizar, removerzero, background,processing_of_data, lenar_calc, read_file,center_psi, red_file_rigaku,red_files_chimazu
from commands  import red_file_rigaku,red_files_chimazu
if __name__ == "__main__":


    print('Start')
    #red_files_chimazu('P_L_PB_3_')
    red_file_rigaku ('P_L_1/P_PB_L_{}.ASC'.format(7))
