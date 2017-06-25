// sound_recognizer.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"

HANDLE event_recording;
char* output_path;


#define DEFAULT_INPUT_DEVID     (-1)
#define E_SR_NOACTIVEDEVICE		(-1)
#define E_SR_NOMEM				(-2)
#define E_SR_INVAL				(-3)
#define E_SR_RECORDFAIL			(-4)
#define E_SR_ALREADY			(-5)
#define TIMEOUT_MS              500
#define	BUFFER_SIZE	            4096
#define SAMPLE_RATE             16000
#define SAMPLE_BIT_SIZE         16
#define FRAME_CNT               10
#define BUF_COUNT               4

static char *g_result = NULL;
static unsigned int g_buffersize = BUFFER_SIZE;

#define DEFAULT_FORMAT		\
{\
	WAVE_FORMAT_PCM,	\
	1,					\
	16000,				\
	32000,				\
	2,					\
	16,					\
	sizeof(WAVEFORMATEX)	\
}

struct speech_rec_notifier {
    void(*on_result)(const char *result, char is_last);
    void(*on_speech_begin)();
    void(*on_speech_end)(int reason);	/* 0 if VAD.  others, error : see E_SR_xxx and msp_errors.h  */
};

#define END_REASON_VAD_DETECT	0	/* detected speech done  */

struct speech_rec {
    enum sr_audsrc aud_src;  /* from mic or manual  stream write */
    struct speech_rec_notifier notif;
    const char * session_id;
    int ep_stat;
    int rec_stat;
    int audio_status;
    struct recorder *recorder;
    volatile int state;
    char * session_begin_params;
};

void start_speech_recorder(struct speech_rec& sr)
{
    WAVEFORMATEX wavfmt = DEFAULT_FORMAT;
    if (waveInGetNumDevs() != 0)
    {
        memset(&sr, 0, sizeof(struct speech_rec));
        sr.session_id = NULL;
        sr.ep_stat = MSP_EP_LOOKING_FOR_SPEECH;
        sr.rec_stat = MSP_REC_STATUS_SUCCESS;
        sr.audio_status = MSP_AUDIO_SAMPLE_FIRST;
        create_recorder(&sr.recorder, [](char* data,unsigned long len, void* para)-> void{
            auto pf = fopen(output_path, "ab+");
            fwrite(data, 1, len, pf);
            fclose(pf);
        }, &sr);
        open_recorder(sr.recorder, -1, &wavfmt);
        auto ret = start_record(sr.recorder);
        if (ret != 0) {
            dbg("start record failed: %d\n", ret);
            sr.session_id = NULL;
            exit(E_SR_RECORDFAIL);
        }

        if (sr.notif.on_speech_begin)
        {
            sr.notif.on_speech_begin();
        }
    }
    else
    {
        printf("No device available please check it first!");
        getch();
        exit(E_SR_RECORDFAIL);
    }
}

template <typename T>
void write(std::ofstream& stream, const T& t) {
    stream.write((const char*)&t, sizeof(T));
}

template <typename SampleType>
void writeWAVData(const char* outFile, SampleType* buf, size_t bufSize,
    int sampleRate, short channels)
{
    std::ofstream stream(outFile, std::ios::binary);
    stream.write("RIFF", 4);
    write<int>(stream, 36 + bufSize);
    stream.write("WAVE", 4);
    stream.write("fmt ", 4);
    write<int>(stream, 16);
    write<short>(stream, 1);                                        // Format (1 = PCM)
    write<short>(stream, channels);                                 // Channels //mono/sterio
    write<int>(stream, sampleRate);

    write<int>(stream, sampleRate * channels * sizeof(SampleType)); // Byterate
    write<short>(stream, channels * sizeof(SampleType));            // Frame size
    write<short>(stream, 8 * sizeof(SampleType));                   // Bits per sample
    stream.write("data", 4);
    uint32_t sz = bufSize;
    stream.write((const char*)&sz, 4);
    stream.write((const char*)buf, bufSize);
}

void prepare_output()
{
    //truncate output
    fclose(fopen(output_path, "w+"));
}

static unsigned int __stdcall recording_procedure(void *param)
{
    bool is_quit = false;
    struct speech_rec sr;
    int timeout = TIMEOUT_MS;
    size_t file_length;
    FILE* pf;
    size_t length = 0;
    short* buff = NULL;

    printf("Start recording\n");
    prepare_output();
    start_speech_recorder(sr);

    while (1) 
    {
        auto result = WaitForSingleObject(event_recording, INFINITE);
        switch (result) 
        {
        case WAIT_OBJECT_0:
            printf("Write to file path %s\n", output_path);
            if (stop_record(sr.recorder) != 0)
            {
                dbg("Stop failed! \n");
                exit(E_SR_RECORDFAIL);
            }
            while (!is_record_stopped(sr.recorder)) {
                Sleep(1);
                timeout--;
                if (0 == timeout)
                {
                    break;
                }
            }
            destroy_recorder(sr.recorder);
            pf = fopen(output_path, "rb");
            fseek(pf, 0, SEEK_END);
            length = ftell(pf);
            rewind(pf);
            buff = (short*)malloc(length * sizeof(short));
            fread(buff, 1, length, pf);
            fclose(pf);
            writeWAVData(output_path, buff, length, SAMPLE_RATE, 1);
            free(buff);
            is_quit = true;
            break;
        default:
            break;
        }
        if (is_quit) {
            break;
        }
    }
    return 0;
}

/*
    @argv[1] output wav file path
*/
static HANDLE start_recording_thread(void* params = nullptr)
{
    HANDLE hdl;

    hdl = (HANDLE)_beginthreadex(NULL, 0, recording_procedure, params, 0, NULL);

    return hdl;
}

int main(int argc, char** argv)
{   
    
    if (argc != 2) {
        printf("Wrong arguments! Expect the output file path\n");
        exit(1);
    }
    output_path = argv[1];
    event_recording = CreateEventEx(NULL, L"hackathon_recording_event", CREATE_EVENT_MANUAL_RESET, EVENT_ALL_ACCESS);
    auto recording_thread = start_recording_thread();

    if (recording_thread != NULL) {
        WaitForSingleObject(recording_thread, INFINITE);
        CloseHandle(recording_thread);
    }

    if (event_recording != NULL) {
        CloseHandle(event_recording);
    }

    getch();
    return 0;
}

