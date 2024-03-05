CXX = g++
CXXFLAGS = -std=c++23 -Wall -Wextra -g -O3
BINDIR = bin

# Declare phony targets
.PHONY: all run clean

# List of source files
SRCS = main.cpp partition.cpp

# Derive object files from source files
OBJS = $(patsubst %.cpp,$(BINDIR)/%.o,$(SRCS))

# Name of the executable
TARGET = $(BINDIR)/myprogram

# Main target
all: $(TARGET)

# Linking the object files to generate the executable
$(TARGET): $(OBJS) | $(BINDIR)
	$(CXX) $(CXXFLAGS) -o $@ $^

# Compilation rule for each .cpp file
$(BINDIR)/%.o: %.cpp | $(BINDIR)
	$(CXX) $(CXXFLAGS) -c -o $@ $<

# Create the bin directory if it doesn't exist
$(BINDIR):
	mkdir -p $(BINDIR)

# Run the program
run: $(TARGET)
	./$(TARGET)

# Clean rule
clean:
	rm -f $(OBJS) $(TARGET)
	rmdir $(BINDIR) 2>/dev/null || true