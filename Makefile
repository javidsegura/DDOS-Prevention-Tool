CC = gcc

# Defined the path for -o (executable)
TARGET = src/defend/protecter/packetSniffer/bin/packet_sniffer

SRC = src/defend/protecter/packetSniffer/main.c

LIBS = -lpcap

#  What dis doing?
all: $(TARGET) 

$(TARGET): $(SRC)
	$(CC) $(SRC) -o $(TARGET) $(LIBS)

clean || clear:
	rm -f $(TARGET)
