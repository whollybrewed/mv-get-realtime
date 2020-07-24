# MV-get-realtime

## File Description

### extract_mvs.c
Extracts and passes the motion vectors (MV) data for each individual decoding of a frame as numpy array to the module `py_emb.py` in the format of `[frame number, source, width, height, x0, y0, x1, y1]`. It also passes the quantities of MV inside each frame to `stdout`, and computes the max and min value.

Compile: `Makefile`

Usage: `./extact_mvs [input video]`

### py_emb.py
Embedded module in `extract.c`. Receives numpy array about MV data (frame-by-frame) for further application.

### mpegutils.c
Dumps macroblock (MB) type data to `stderr`.

Compile: copy and replace the file to `ffmpeg/source/libavcodec`, then re-build ffmpeg.

Usage: `./ffmpeg -debug mb_type -i [input video] -thread_type none [output video]`

### plotframeinfo.py
Plots stacked bar chart of MV and MB for a given frame.

Usage: `python3 plotframeinfo.py [MV data] [MB data] [frame number]`

### mvs.txt
Contains MV data as `frame number, MV quantity`

### mbdata_clean.txt
Contains MB type data as `##FRAME## INTRA=quantity, SKIP=quantity, INTER=quantity`. Line number is equivalent to frame number.

## MB type index

| index | ffmpeg char | condition                    | remark                                              |
|-------|-------------|------------------------------|-----------------------------------------------------|
| 0     | P           | IS_PCM                       | Lossless (raw samples without prediction)           |
| 1     | A           | IS_INTRA && IS_ACPRED        | 16x16 Intra prediction                              |
| 2     | i           | IS_INTRA4x4                  | 4x4 Intra prediction                                |
| 3     | I           | IS_INTRA16x16                |                                                     |
| 4     | d           | IS_DIRECT && IS_SKIP         |                                                     |
| 5     | D           | IS_DIRECT                    | No motion vectors are sent (B slices)               |
| 6     | g           | IS_GMC && IS_SKIP            | 16x16 Skip macroblock (P or B slices)               |
| 7     | G           | IS_GMC                       | Global motion compensation (not relevant for H.264) |
| 8     | S           | IS_SKIP                      |                                                     |
| 9     | >           | !USES_LIST(1)                | Reference to past (List 0, P or B slices)           |
| 10    | <           | !USES_LIST(0)                | Reference to future (List 1, B slices)              |
| 11    | X           | USES_LIST(0) && USES_LIST(1) | Reference to past and future (List 1 & 2, B slices) |

## Troubleshoot
[ffmpeg: error while loading shared libraries:](https://stackoverflow.com/questions/12901706/ffmpeg-error-in-linux) 
