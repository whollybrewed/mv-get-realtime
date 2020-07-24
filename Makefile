CC = gcc
LIBS = -lavcodec -lavformat -lavutil -lavdevice -lswresample -lswscale -lpython3.6m 
INCLUDES = -L/opt/dev-tools-sources/ffmpeg/build/lib -I/opt/dev-tools-sources/ffmpeg/build/include

# If fail, try "PY_CFLAGS := $(shell python3-config --cflags)"
PY_CFLAGS = -I/usr/include/python3.6m

TARGET = extract_mvs
all: $(TARGET)
$(TARGET): $(TARGET).c 
	$(CC) -o $(TARGET) $(TARGET).c $(LIBS) $(INCLUDES) $(PY_CFLAGS)  


