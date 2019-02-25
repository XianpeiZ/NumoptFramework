TOP=`pwd`
echo ${TOP}

cd ${TOP}/Source/libs/iRRAM/


tar xvf gmp-5.1.3.tar.bz2
cd  gmp-5.1.3
make clean 2> /dev/null
./configure --prefix=${TOP}/Binary/iRRAM 
make
make check
    if ( ! make install) 
    then
      echo "Errors during configuration/compilation/installion of gmp-5.1.3..."
      echo "Giving up...."
      exit
    fi
cd ..
rm -r gmp-5.1.3
 

tar xvf mpfr-3.1.2.tar.bz2
cd mpfr-3.1.2
make clean 2> /dev/null
./configure --with-gmp-include=${TOP}/Binary/iRRAM/include  --with-gmp-lib=${TOP}/Binary/iRRAM/lib --prefix=${TOP}/Binary/iRRAM
    make
    if ( ! make install) 
     then
      echo "Errors during configuration/compilation/installion of MPFR-3.1.2..."
      echo "Giving up...."
      exit
    fi
 cd ..
 rm -r mpfr-3.1.2


make distclean 2> /dev/null
autoreconf -s -i
echo ./configure --with-gmp-include=${TOP}/Binary/iRRAM/include --with-gmp-lib=${TOP}/Binary/iRRAM/lib --with-mpfr-lib=${TOP}/Binary/iRRAM/lib --prefix=${TOP}/Binary/iRRAM 
./configure --with-gmp-include=${TOP}/Binary/iRRAM/include --with-gmp-lib=${TOP}/Binary/iRRAM/lib --with-mpfr-lib=${TOP}/Binary/iRRAM/lib --prefix=${TOP}/Binary/iRRAM 
sed -i 's,LIBS *= *-lmpfr,LIBS = -L'"${TOP}"'\/Binary\/iRRAM\/lib -lmpfr,' ./build/Makefile
sed -i 's,LIBS_INST *= *-lmpfr,LIBS = -L'"${TOP}"'\/Binary\/iRRAM\/lib -lmpfr,' ./build/Makefile
make
    if ( ! make install) 
     then
      echo "Errors in iRRAM ..."
      echo "Giving up...."
      exit
    fi

cd ${TOP}
