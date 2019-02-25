/*

iRRAM.h -- header file for iRRAM-controlled applications

Copyright (C) 2006 Norbert Mueller
 
This file is part of the iRRAM Library.
 
The iRRAM Library is free software; you can redistribute it and/or modify
it under the terms of the GNU Library General Public License as published by
the Free Software Foundation; either version 2 of the License, or (at your
option) any later version.
 
The iRRAM Library is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Library General Public
License for more details.
 
You should have received a copy of the GNU Library General Public License
along with the iRRAM Library; see the file COPYING.LIB.  If not, write to
the Free Software Foundation, Inc., 59 Temple Place - Suite 330, Boston,
MA 02111-1307, USA. 
*/


#ifndef iRRAM_H
#define iRRAM_H


#include <iRRAM/lib.h>

void compute(void); 

int iRRAM_compute(const int& arg){compute();return 0;}
 
int main (int argc,char **argv){
  iRRAM_initialize(argc,argv);
  return iRRAM::iRRAM_exec(iRRAM_compute,0);
}

#endif
/* ! iRRAM_H */



