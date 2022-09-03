
def LogTxt(prefix, msg):
	from dbg import TraceError
	TraceError("<{}> {}".format(prefix, msg))
