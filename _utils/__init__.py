import dbg
def LogTxt(prefix, msg):
	dbg.TraceError("<%s> -\t%s" % (prefix, msg))

# rectangle collision detection
def rect_collision(r1, r2):
	return (r1[0] < r2[0] + r2[2] and r1[0] + r1[2] > r2[0] and r1[1] < r2[1] + r2[3] and r1[1] + r1[3] > r2[1])

def case(d, key):
	return d.get(key, None)

import pythonscriptloader as pythonscriptloader
