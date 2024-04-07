# https://www.cs.colby.edu/maxwell/courses/tutorials/maketutor/
# https://stackoverflow.com/questions/73751174/makefile-build-o-files-in-another-directory
# https://stackoverflow.com/questions/2481269/how-to-make-a-simple-c-makefile

CC=gcc
CXX=g++

CXXFLAGS := $(CXXFLAGS) -g -Wall -Wextra -pedantic -Werror -std=c++23

SRCS = main.cpp negamax.cpp
BUILDDIR = build

all: main

main: $(SRCS:%.cpp=$(BUILDDIR)/%.o) 
	$(CXX) $(CXXFLAGS) $^ -o $@ 

$(BUILDDIR)/%.o : %.cpp | $(BUILDDIR)
	$(CXX) -o $@ -c $< 

$(BUILDDIR): ; @mkdir -p $@

.PHONY: clean

clean:
	rm -rf $(BUILDDIR)
	rm main
