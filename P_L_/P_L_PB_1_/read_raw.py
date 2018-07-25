#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Andrezio
#
# Created:     23/07/2017
# Copyright:   (c) Andrezio 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

file_name='P_L_PB_1_.raw'
datafile = file(file_name)

import fabio

image = fabio.open(file_name)