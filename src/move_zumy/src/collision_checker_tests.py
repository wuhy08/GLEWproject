import math
import collision_checker as cc
import matplotlib.pyplot as plt
import time
import sys
import copy

def point_check(x1, y1, x2, y2):
	p1 = cc.Point2D(x1,y1)
	p2 = cc.Point2D(x2,y2)
	print("p1 = (%f, %f), p2 = (%f, %f)." % (p1.x, p1.y, p2.x, p2.y))
	print ("Euclidean dist wrt p1 is %f: " % p1.e_dist(p2))
	print ("Euclidean dist wrt p2 is %f: " % p2.e_dist(p1))
	if(p1.isEqualPt(p2)):
		print "p1 == p2 is TRUE"
	else:
		print "p1 == p2 is FALSE"
	print ""

def plot_vector(v1):
	# Plot the vector and start and end points.
	# Set properties for vector and endpoints.  mec = marker edge color, mfc = "" face "", ms = marker size
	# Colors = b,g,r,m,c,y, k(black),w or RGB tuple (r,g,b)
	plt.plot([v1.point1.x, v1.point2.x], [v1.point1.y, v1.point2.y], color='b', linewidth=2.0)
	plt.plot([v1.point1.x], [v1.point1.y], 'o', mec = 'r', mfc = 'r', ms = 5)
	plt.plot([v1.point2.x], [v1.point2.y], 'o',  mec = 'g', mfc = 'g', ms = 5)
	plt.axis('equal')
	plt.show()

def plot_vectors(v_tuple):
	for v in v_tuple:
		plt.plot([v.point1.x, v.point2.x], [v.point1.y, v.point2.y], color='b', linewidth=2.0)
		plt.plot([v.point1.x], [v.point1.y], 'o', mec = 'r', mfc = 'r', ms = 5)
		plt.plot([v.point2.x], [v.point2.y], 'o',  mec = 'g', mfc = 'g', ms = 5)
	plt.axis('equal')
	plt.show()

def plot_perp_vectors(v1, v2, v3):
	# Vector 1 - Blue
	# Set properties for vector and endpoints.  mec = marker edge color, mfc = "" face "", ms = marker size
	# Colors = b,g,r,m,c,y, k(black),w or RGB tuple (r,g,b)
	plt.plot([v1.point1.x, v1.point2.x], [v1.point1.y, v1.point2.y], color='b', linewidth=2.0)
	plt.plot([v1.point1.x], [v1.point1.y], 'o', mec = 'r', mfc = 'r', ms = 5)
	plt.plot([v1.point2.x], [v1.point2.y], 'o', mec = 'g', mfc = 'g', ms = 5)
	
	# Vector 2 - Cyan
	plt.plot([v2.point1.x, v2.point2.x], [v2.point1.y, v2.point2.y], color='c', linewidth=2.0)
	plt.plot([v2.point1.x], [v2.point1.y], 'o', mec = 'r', mfc = 'r', ms = 5)
	plt.plot([v2.point2.x], [v2.point2.y], 'o',  mec = 'g', mfc = 'g', ms = 5)
	
	# Vector 3 - Magenta
	plt.plot([v3.point1.x, v3.point2.x], [v3.point1.y, v3.point2.y], color='m', linewidth=2.0)
	plt.plot([v3.point1.x], [v3.point1.y], 'o', mec = 'r', mfc = 'r', ms = 5)
	plt.plot([v3.point2.x], [v3.point2.y], 'o', mec = 'g', mfc = 'g', ms = 5)
	
	plt.axis('equal')
	plt.show()	

def plot_bounding_box(rect, path_vector, radius):
	circle_st=plt.Circle((path_vector.point1.x, path_vector.point1.y),radius,color='r',fill=False)
	circle_end=plt.Circle((path_vector.point2.x, path_vector.point2.y),radius, color='g', fill=False)

	for v in (rect.side1, rect.side2, rect.side3, rect.side4):
		plt.plot([v.point1.x, v.point2.x], [v.point1.y, v.point2.y], color='k', linewidth=2.0)
		plt.plot([v.point1.x], [v.point1.y], 'o', mec = 'k', mfc = 'k', ms = 5)
		plt.plot([v.point2.x], [v.point2.y], 'o',  mec = 'k', mfc = 'k', ms = 5)
	plt.plot([path_vector.point1.x, path_vector.point2.x], [path_vector.point1.y, path_vector.point2.y], color='b', linewidth=2.0)
	plt.plot([path_vector.point1.x], [path_vector.point1.y], 'o', mec = 'r', mfc = 'r', ms = 5)
	plt.plot([path_vector.point2.x], [path_vector.point2.y], 'o',  mec = 'g', mfc = 'g', ms = 5)

	fig = plt.gcf()
	fig.gca().add_artist(circle_st)
	fig.gca().add_artist(circle_end)	
	plt.axis('equal')
	plt.show()	

def plot_bounding_boxes(rects, v1, v2, v3, v4, radius):
	for rect in rects:
		for v in (rect.side1, rect.side2, rect.side3, rect.side4):
			plt.plot([v.point1.x, v.point2.x], [v.point1.y, v.point2.y], color='k', linewidth=2.0)
			plt.plot([v.point1.x], [v.point1.y], 'o', mec = 'k', mfc = 'k', ms = 5)
			plt.plot([v.point2.x], [v.point2.y], 'o',  mec = 'k', mfc = 'k', ms = 5)

	fig = plt.gcf()

	for v in (v1,v2,v3,v4):
		plt.plot([v.point1.x, v.point2.x], [v.point1.y, v.point2.y], color='b', linewidth=2.0)
		plt.plot([v.point1.x], [v.point1.y], 'o', mec = 'r', mfc = 'r', ms = 5)
		plt.plot([v.point2.x], [v.point2.y], 'o',  mec = 'g', mfc = 'g', ms = 5)
		circle_st=plt.Circle((v.point1.x, v.point1.y),radius,color='r',fill=False)
		circle_end=plt.Circle((v.point2.x, v.point2.y),radius, color='g', fill=False)
		fig.gca().add_artist(circle_st)
		fig.gca().add_artist(circle_end)	

	plt.axis('equal')
	plt.show()	

def vector_basic_check(x1,y1,x2,y2, run_plot):
	v1 = cc.Vector2D(cc.Point2D(x1,y1), cc.Point2D(x2,y2))

	# Compute the vectors perpendicular to v1 with norm 0.25.  Plot all three vectors.
	perp1, perp2 = v1.getPerpVectors(0.25)
	v2x = v1.point1.x + perp1.point2.x
	v2y = v1.point1.y + perp1.point2.y
	v3x = v1.point1.x + perp2.point2.x
	v3y = v1.point1.y + perp2.point2.y

	v2 = cc.Vector2D(v1.point1, cc.Point2D(v2x, v2y)) # cyan perp vector in figure
	v3 = cc.Vector2D(v1.point1, cc.Point2D(v3x, v3y)) # magenta perp vector in figure

	# Some checks on dot products and orthogonality.
	print ("Dot Prod with Perp1: %f, Dot Prod with Perp2: %f" % (v1.dotProduct(v2), v1.dotProduct(v3)))
	if(v1.isPerp(v2)):
		print "Vector is perpendicular to Perp1"
		if(v1.isRightAngle(v2)):
			print "Vector forms a right angle with Perp1"
	if(v1.isPerp(v3)):
		print "Vector is perpendicular to Perp2"
		if(v1.isRightAngle(v3)):
			print "Vector forms a right angle with Perp2"
	print ("Induced norm: %f, euclid_norm: %f" % (math.sqrt(v1.dotProduct(v1)), v1.point1.e_dist(v1.point2)))
	print ("Perp1 Induced norm: %f, Perp1 euclid_norm: %f" % (math.sqrt(v2.dotProduct(v2)), v2.point1.e_dist(v2.point2)))
	print ("Perp1 Induced norm: %f, Perp1 euclid_norm: %f" % (math.sqrt(v3.dotProduct(v3)), v3.point1.e_dist(v3.point2)))
	print ""
	if(run_plot > 0):
		plot_perp_vectors(v1,v2,v3)

def vector_intersect_check(vect1_tuple, vect2_tuple, run_plot):
	# each input should be of type (x1,y1), (x2,y2)
	v1 = cc.Vector2D(cc.Point2D(vect1_tuple[0][0],vect1_tuple[0][1]), cc.Point2D(vect1_tuple[1][0],vect1_tuple[1][1]))
	v2 = cc.Vector2D(cc.Point2D(vect2_tuple[0][0],vect2_tuple[0][1]), cc.Point2D(vect2_tuple[1][0],vect2_tuple[1][1]))
	if v1.check_intersection(v2):
		print ("(%f,%f)->(%f,%f) intersects (%f,%f)->(%f,%f)" % (v1.point1.x, v1.point1.y, v1.point2.x, v1.point2.y, \
		v2.point1.x, v2.point1.y, v2.point2.x, v2.point2.y))
	else:
		print ("(%f,%f)->(%f,%f) does not intersect (%f,%f)->(%f,%f)" % (v1.point1.x, v1.point1.y, v1.point2.x, v1.point2.y, \
		v2.point1.x, v2.point1.y, v2.point2.x, v2.point2.y))
	print ""
	if(run_plot > 0):
		plot_vectors((v1,v2))
	

def rect_check(v1, v2, v3, v4, run_plot):
	r1 = cc.Rectangle2D(v1,v2,v3,v4) # this will check that the four vectors are actually a rectangle
	print ("(%f,%f)->(%f,%f), (%f,%f)->(%f,%f), (%f,%f)->(%f,%f), (%f,%f)->(%f,%f) form a rectangle" % \
		  (v1.point1.x, v1.point1.y, v1.point2.x, v1.point2.y, \
		  v2.point1.x, v2.point1.y, v2.point2.x, v2.point2.y, \
		  v3.point1.x, v3.point1.y, v3.point2.x, v3.point2.y, \
		  v4.point1.x, v4.point1.y, v4.point2.x, v4.point2.y) )
	print ""
	if(run_plot > 0):
		plot_vectors((v1,v2,v3,v4))
	return r1

def rect_intersection_check(ra, rb):
	if not (isinstance(ra, cc.Rectangle2D) and isinstance(rb, cc.Rectangle2D)):
		print "Args should be of type Rectangle2D!"
		raise TypeError
	if(ra.isRectIntersection(rb)):
		print "Rectangles intersect!"
	else:
		print "Rectangles do not intersect."
	print ""
	if(run_plot > 0):
		plot_vectors((ra.side1, ra.side2, ra.side3, ra.side4, rb.side1, rb.side2, rb.side3, rb.side4))
	
def bounding_box_check(start_x, start_y, end_x, end_y, robot_radius, isMoving, run_plot):
	path_vector = cc.Vector2D(cc.Point2D(start_x, start_y), cc.Point2D(end_x, end_y))
	rect = cc.getBoundingBox(path_vector, robot_radius, isMoving)
	if(run_plot > 0):
		plot_bounding_box(rect, path_vector, robot_radius)
	return rect



# Main function for testing functionality above. #
#************************************************#
if __name__=='__main__':
	run_plot = int(sys.argv[1])

	# Point2D Checks
	point_check(0.5,0.5,1.5,1.5)
	point_check(1,1,1,1)
	point_check(0.25, 0.34, 0.25, 0.34)
	point_check(-3,2,2,5.5)
	
	# Vector 2D Checks
	vector_basic_check(0.5, 0.5, -0.5, 0.8, run_plot)
	vector_basic_check(0.0, 0.0, 1.0, 1.0, run_plot)

	# V2D Intersection Check 1: line segments crisscross
	vector_intersect_check(((0.1,0.2),(0.5,1.0)), ((0.2, 0.8),(0.5,0.2)), run_plot)

	# V2D Intersection Check 2: parallel line segments apart by 1 unit
	vector_intersect_check(((1,2),(3,4)), ((1,3),(3,5)), run_plot)

	# V2D Intersection Check 3: parallel line segments that overlap
	vector_intersect_check(((1,2),(3,4)), ((1.5,2.5),(2,3)), run_plot)
	
	# V2D Intersection Check 4: One vertical line segment, other intersects
	vector_intersect_check(((2.5,2),(2.5,4.4)), ((1.5,2.5),(3,2.5)), run_plot)

	# V2D Intersection Check 5: Two vertical line segments, intersects
	vector_intersect_check(((5,1),(5,2)), ((5,-1.5),(5,1)), run_plot)

	# V2D Intersection Check 6: Two vertical line segments, no intersections
	vector_intersect_check(((1,1),(1,2)), ((2,2),(2,1)), run_plot)

	# Rectangle Check
	va1 = cc.Vector2D(cc.Point2D(0,0), cc.Point2D(0,1))
	va2 = cc.Vector2D(cc.Point2D(0,1), cc.Point2D(1,1))
	va3 = cc.Vector2D(cc.Point2D(1,1), cc.Point2D(1,0))
	va4 = cc.Vector2D(cc.Point2D(1,0), cc.Point2D(0,0))
	ra = rect_check(va1,va2,va3,va4, run_plot) # RA = square

	vb1 = cc.Vector2D(cc.Point2D(-1,0.25), cc.Point2D(3,0.25))
	vb2 = cc.Vector2D(cc.Point2D(3,0.25), cc.Point2D(3,0.75))
	vb3 = cc.Vector2D(cc.Point2D(3,0.75), cc.Point2D(-1,0.75))
	vb4 = cc.Vector2D(cc.Point2D(-1,0.75), cc.Point2D(-1,0.25))
	rb = rect_check(vb1, vb2, vb3, vb4, run_plot) # RB = thin horizontal rectangle

	vc1 = cc.Vector2D(cc.Point2D(0.3,-0.3), cc.Point2D(1.3,0.7))
	vc2 = cc.Vector2D(cc.Point2D(1.3,0.7), cc.Point2D(1.05,0.95))
	vc3 = cc.Vector2D(cc.Point2D(1.05,0.95), cc.Point2D(0.05,-0.05))
	vc4 = cc.Vector2D(cc.Point2D(0.05,-0.05), cc.Point2D(0.3,-0.3))
	rc = rect_check(vc1, vc2, vc3, vc4, run_plot) # RC = slanted rectangle

	vd1 = copy.deepcopy(va1)
	vd2 = copy.deepcopy(va2)
	vd3 = copy.deepcopy(va3)
	vd4 = copy.deepcopy(va4)
	for v in (vd1, vd2, vd3, vd4):
		v.point1.x = v.point1.x + 1.3
		v.point1.y = v.point1.y + 0.7
		v.point2.x = v.point2.x + 1.3
		v.point2.y = v.point2.y + 0.7
	rd = rect_check(vd1, vd2, vd3, vd4, run_plot) # RD = square at corner of RC

	#R2D Intersection Check: Look at every pair of rectangles that are not the same and look for intersection.
	for r1 in (ra, rb, rc, rd):
		for r2 in (ra, rb, rc, rd):
			if not (r1 == r2):
				rect_intersection_check(r1,r2)

	bb1 = bounding_box_check(0, 0, 1, 1, 0.125, True, run_plot)
	bb2 = bounding_box_check(0, 0, 1, 1, 0.125, False, run_plot)
	bb3 = bounding_box_check(-1, 0.35, 0.68, -0.72, 0.125, True, run_plot)
	bb4 = bounding_box_check(-1, 0.35, 0.68, -0.72, 0.125, False, run_plot)

	command_tuple = cc.command_four_zumys(cc.Point2D(0,0), cc.Point2D(0,1), cc.Point2D(1,0), cc.Point2D(1,1), \
									 cc.Point2D(2,0), cc.Point2D(2,1), cc.Point2D(3,0), cc.Point2D(3,1))
	v1 = cc.Vector2D(cc.Point2D(0,0), cc.Point2D(0,1))
	v2 = cc.Vector2D(cc.Point2D(1,0), cc.Point2D(1,1))
	v3 = cc.Vector2D(cc.Point2D(2,0), cc.Point2D(2,1))
	v4 = cc.Vector2D(cc.Point2D(3,0), cc.Point2D(3,1))
	print command_tuple[1]
	if(run_plot > 0):
		plot_bounding_boxes(command_tuple[0], v1,v2,v3,v4, 0.125)

	command_tuple = cc.command_four_zumys(cc.Point2D(0,0), cc.Point2D(2,2), cc.Point2D(1,0), cc.Point2D(1,1), \
									 cc.Point2D(2,0), cc.Point2D(2,1), cc.Point2D(3,0), cc.Point2D(1,1))
	v1 = cc.Vector2D(cc.Point2D(0,0), cc.Point2D(2,2))
	v2 = cc.Vector2D(cc.Point2D(1,0), cc.Point2D(1,1))
	v3 = cc.Vector2D(cc.Point2D(2,0), cc.Point2D(2,1))
	v4 = cc.Vector2D(cc.Point2D(3,0), cc.Point2D(1,1))
	print command_tuple[1]
	if(run_plot > 0):
		plot_bounding_boxes(command_tuple[0], v1,v2,v3,v4, 0.125)



#   Failing rectangle case (can uncomment if you like)
	#v1 = cc.Vector2D(cc.Point2D(0,0), cc.Point2D(0,2))
	#v2 = cc.Vector2D(cc.Point2D(0,2), cc.Point2D(1,1))
	#v3 = cc.Vector2D(cc.Point2D(1,1), cc.Point2D(1,0))
	#v4 = cc.Vector2D(cc.Point2D(1,0), cc.Point2D(0,0))
	#rect_check(v1,v2,v3,v4, run_plot) # should fail, not 90 deg


