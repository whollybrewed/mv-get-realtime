/*
 * Copyright (c) 2012 Stefano Sabatini
 * Copyright (c) 2014 Clément Bœsch
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
 * THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */
#include <libavutil/motion_vector.h>
#include <libavformat/avformat.h>
#include "stdlib.h"

static AVFormatContext *fmt_ctx = NULL;
static AVCodecContext *video_dec_ctx = NULL;
static AVStream *video_stream = NULL;
static const char *src_filename = NULL;

static int video_stream_idx = -1;
static AVFrame *frame = NULL;
static int video_frame_count = 0;

static int maxfr, minfr, maxmv = 0, minmv = INT_MAX;

static int decode_packet(const AVPacket *pkt)
{   
    // int mv_arr [8];
    int ret = avcodec_send_packet(video_dec_ctx, pkt);
    if (ret < 0) {
        fprintf(stderr, "Error while sending a packet to the decoder: %s\n", av_err2str(ret));
        return ret;
    }

    while (ret >= 0)  {
        ret = avcodec_receive_frame(video_dec_ctx, frame);
        if (ret == AVERROR(EAGAIN) || ret == AVERROR_EOF) {
            break;
        } else if (ret < 0) {
            fprintf(stderr, "Error while receiving a frame from the decoder: %s\n", av_err2str(ret));
            return ret;
        }

        if (ret >= 0) {
            int i;
            AVFrameSideData *sd;
            video_frame_count++;
            // printf("\rProcessing frame: %d\r", video_frame_count);
            sd = av_frame_get_side_data(frame, AV_FRAME_DATA_MOTION_VECTORS);
            if (sd) {
                const AVMotionVector *mvs = (const AVMotionVector *)sd->data;
                int num_mvs = sd->size / sizeof(*mvs);
                int data_mv[4 * num_mvs + 1];
                data_mv[0] = video_frame_count;
                // if (num_mvs > maxmv) {
                //     maxmv = num_mvs;
                //     maxfr = video_frame_count;
                // }
                // else if(num_mvs < minmv) {
                //     minmv = num_mvs;
                //     minfr = video_frame_count;
                // }
                // fprintf(stdout,"%d, %d\n",video_frame_count, num_mvs);
                for (i = 0; i < num_mvs; i++) {
                    const AVMotionVector *mv = &mvs[i];
                    // mv_arr [1] = mv->source;
                    // mv_arr [2] = mv->w;
                    // mv_arr [3] = mv->h;
                    data_mv[i * 4 + 1] = mv->src_x;
                    data_mv[i * 4 + 2] = mv->src_y;
                    data_mv[i * 4 + 3] = mv->dst_x;
                    data_mv[i * 4 + 4] = mv->dst_y;
                    // for(int j = 0; j < 5; j++){
                    //     printf("%d ", mv_arr[j]);
                    // }
                    // printf("\n");
                }
                for(int j = 0; j <= num_mvs * 4; j++){
                    printf("%d ", data_mv[j]);
                    if (j % 4 == 0)
                        printf("\n");
                }
                // printf("%d ", *mv_arr[0]);
            }
            av_frame_unref(frame);
        }
    }
    return 0;
}

static int open_codec_context(AVFormatContext *fmt_ctx, enum AVMediaType type)
{
    int ret;
    AVStream *st;
    AVCodecContext *dec_ctx = NULL;
    AVCodec *dec = NULL;
    AVDictionary *opts = NULL;

    ret = av_find_best_stream(fmt_ctx, type, -1, -1, &dec, 0);
    if (ret < 0) {
        fprintf(stderr, "Could not find %s stream in input file '%s'\n",
                av_get_media_type_string(type), src_filename);
        return ret;
    } else {
        int stream_idx = ret;
        st = fmt_ctx->streams[stream_idx];

        dec_ctx = avcodec_alloc_context3(dec);
        if (!dec_ctx) {
            fprintf(stderr, "Failed to allocate codec\n");
            return AVERROR(EINVAL);
        }

        ret = avcodec_parameters_to_context(dec_ctx, st->codecpar);
        if (ret < 0) {
            fprintf(stderr, "Failed to copy codec parameters to codec context\n");
            return ret;
        }

        /* Init the video decoder */
        av_dict_set(&opts, "flags2", "+export_mvs", 0);
        if ((ret = avcodec_open2(dec_ctx, dec, &opts)) < 0) {
            fprintf(stderr, "Failed to open %s codec\n",
                    av_get_media_type_string(type));
            return ret;
        }

        video_stream_idx = stream_idx;
        video_stream = fmt_ctx->streams[video_stream_idx];
        video_dec_ctx = dec_ctx;
    }

    return 0;
}

AVPacket pkt = { 0 };
void setup()
{

    int ret = 0;
    // if (argc != 2) {
    //     fprintf(stderr, "Usage: %s <video>\n", argv[0]);
    //     exit(1);
    // }
    src_filename = "input.mp4";
    if (avformat_open_input(&fmt_ctx, src_filename, NULL, NULL) < 0) {
        fprintf(stderr, "Could not open source file %s\n", src_filename);
        exit(1);
    }

    if (avformat_find_stream_info(fmt_ctx, NULL) < 0) {
        fprintf(stderr, "Could not find stream information\n");
        exit(1);
    }

    open_codec_context(fmt_ctx, AVMEDIA_TYPE_VIDEO);

    av_dump_format(fmt_ctx, 0, src_filename, 0);

    if (!video_stream) {
        fprintf(stderr, "Could not find video stream in the input, aborting\n");
        ret = 1;
        //goto end;
    }

    frame = av_frame_alloc();

    if (!frame) {
        fprintf(stderr, "Could not allocate frame\n");
        ret = AVERROR(ENOMEM);
        //goto end;
    }


    /* read frames from the file */
    // while (av_read_frame(fmt_ctx, &pkt) >= 0) {
    //     if (pkt.stream_index == video_stream_idx)
    //         ret = decode_packet(&pkt);
    //     av_packet_unref(&pkt);
    //     if (ret < 0)
    //         break;
    // }

}

int call_readframe()
{
    return av_read_frame(fmt_ctx, &pkt);
}

int call_dec()
{
    int ret = decode_packet(&pkt);
    av_packet_unref(&pkt);
    return ret;
}

void release()
{
    /* flush cached frames */
    decode_packet(NULL);
    avcodec_free_context(&video_dec_ctx);
    avformat_close_input(&fmt_ctx);
    av_frame_free(&frame);
    //return ret < 0;
}

int main ()
{
    return 0;
}
