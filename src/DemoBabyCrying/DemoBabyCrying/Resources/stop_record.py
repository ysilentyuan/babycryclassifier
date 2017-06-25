from win32event import SetEvent, ResetEvent, CreateEvent

if __name__ == '__main__':
	evt = CreateEvent(None, 0, 0, 'hackathon_recording_event')
	SetEvent(evt)
	ResetEvent(evt)