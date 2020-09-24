CC = gcc
LIBS = -lavcodec -lavformat -lavutil -lavdevice -lswresample -lswscale -lpython3.6m 
INCLUDES = -L/home/user/ffmpeg_build/lib -I/home/user/ffmpeg_build/include

# If fail, try "PY_CFLAGS := $(shell python3-config --cflags)"
PY_CFLAGS = -I/usr/include/python3.6m

TARGET = extract_mvs
all: $(TARGET)
$(TARGET): $(TARGET).c 
	$(CC) -fPIC -shared -o lextractmvs.so $(TARGET).c $(LIBS) $(INCLUDES) $(PY_CFLAGS)  


