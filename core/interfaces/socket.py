def info():
	return "TESt"

def init(sio):
	sio.on_event('info', info)
