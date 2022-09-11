import dbg
def LogTxt(prefix, msg):
	dbg.TraceError("<%s> -\t%s" % (prefix, msg))
