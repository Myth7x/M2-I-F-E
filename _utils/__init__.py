import dbg
def LogTxt(prefix, msg):
	"""Log text to the console"""
	dbg.TraceError("<%s> -\t%s" % (prefix, msg))

def rect_collision(r1, r2):
	"""Find if two rectangles collide"""
	return (r1[0] < r2[0] + r2[2] and r1[0] + r1[2] > r2[0] and r1[1] < r2[1] + r2[3] and r1[1] + r1[3] > r2[1])

def rect_intersect_area_factor(r1, r2):
	"""Find the intersect area factor of two rectangles"""
	r = [
		max(r1[0], r2[0]),
		max(r1[1], r2[1]),
		min(r1[0] + r1[2], r2[0] + r2[2]) - max(r1[0], r2[0]),
		min(r1[1] + r1[3], r2[1] + r2[3]) - max(r1[1], r2[1]),
	]
	return r[2] * r[3]


import pythonscriptloader as pythonscriptloader

import ui_class_gathering as ui_class_gathering
