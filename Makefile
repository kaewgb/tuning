CC			= g++
NVCC		= nvcc

COMMON_OBJS	= util.o util_cpu.o
HEADERS		= header.h util.h util.cuh

CFLAGS		=
NVCCFLAGS	= -arch=sm_20 --fmad=false --ptxas-options=-v --disable-warnings

two:			twopasses.o hypterm2.o $(COMMON_OBJS)
				$(NVCC) -o $@ $^
one:			onepass.o hypterm3.o $(COMMON_OBJS)
				$(NVCC) -o $@ $^

test:			test.o simple.o $(COMMON_OBJS)
				$(NVCC) -o $@ $^

%.o:		%.cpp $(HEADERS)
			$(CC) $(CFLAGS) -c $< -o $@
%.o:		%.cu $(HEADERS)
			$(NVCC) -c $< -o $@ $(NVCCFLAGS)
clean:
			rm -f *.o one two test
