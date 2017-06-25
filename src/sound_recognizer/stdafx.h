// stdafx.h : include file for standard system include files,
// or project specific include files that are used frequently, but
// are changed infrequently
//

#pragma once

#include "targetver.h"
#include <stdlib.h>
#include <stdio.h>
#include <windows.h>
#include <conio.h>
#include <errno.h>
#include <process.h>
#include <mmsystem.h>
#include <cmath>
#include <fstream>
#include <iostream>
#include "msp_cmn.h"
#include "msp_errors.h"
#include "winrec.h"

#ifdef _WIN64
#pragma comment(lib,"../../libs/msc_x64.lib") //x64
#else
#pragma comment(lib,"../../libs/msc.lib") //x86
#endif

#define DBG_ON 0

#if DBG_ON
#define dbg  printf
#else
#define dbg
#endif





// TODO: reference additional headers your program requires here
