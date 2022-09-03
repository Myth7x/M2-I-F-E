from dbg import TraceError

def LogTxt(prefix, msg):
	TraceError("<{}> {}".format(prefix, msg))
