# Makefile for user_programs

iRRAM_HOME = ../Binary/iRRAM
VPATH = ../Source/backend

CC = clang -std=c11
CFLAGS = -g -O2
CPP = clang -E
CPPFLAGS =  -I$(iRRAM_HOME)/include
CXX = clang++ -std=c++11
CXXCPP = clang++ -E -std=c++11
CXXFLAGS = -g -O2
LDFLAGS = -Xlinker -rpath -Xlinker $(iRRAM_HOME)/lib
LDLIBS =  -L$(iRRAM_HOME)/lib -liRRAM -lmpfr -lgmp -lm -lpthread

all: float real bits_error analysis analysis_irram

$(VPATH)/float: points.o self_math.o

$(VPATH)/float_origin: points.o self_math.o

$(VPATH)/real: points.o self_math.o

$(VPATH)/bits_error: points.o self_math.o

$(VPATH)/analysis: points.o self_math.o

$(VPATH)/analysis_irram: points.o self_math.o

$(VPATH)/points.o: points.cc points.h

$(VPATH)/self_math.o: self_math.cc self_math.h

clean:
	rm -rf $(EXAMPLES_BIN) float.cpp real.cpp input output float real float_output points.o bits_error analysis

install:
