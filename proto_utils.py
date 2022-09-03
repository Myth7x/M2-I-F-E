import dbg
def LogTxt(prefix, msg):
	dbg.TraceError("<%s> %s" % (prefix, msg))
