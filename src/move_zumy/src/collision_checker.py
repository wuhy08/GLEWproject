import math

# This code will later be imported as a collision checker.
# Currently the key features are three classes: Point2D, Vector2D, and Rectangle2D.
# Using these classes, I try to make a collision checking function, isCollision,
# between 2 Zumys.  command_four_zumys uses this collision function to provide a bool value
# to tell each Zumy whether they can move forward or not.

# Contents: Helper functions, Point2D class, Vector2D class, Rectangle2D, isCollision function, command_four_zumys function, main

#***** Helper function section - should be mostly self explanatory *****#
#***********************************************************************#
DEBUG = False
def print_debug(s):
	if DEBUG:
		print s

def e_dist(del_x, del_y):
	return math.sqrt(del_x*del_x + del_y*del_y)

def isBetween(value, endpoint1, endpoint2):
	if(value > endpoint1-0.000001) and (value < endpoint2+0.000001):
		return True
	if(value < endpoint1+0.000001) and (value > endpoint2-0.000001):
		return True
	return False

def isEqual(flt1, flt2):
	# only for floats at the moment
	if not (isinstance(flt1, float) and isinstance(flt2, float)):
		raise TypeError
	return isBetween(flt1, flt2, flt2)

def getMin(x1, x2):
	if(x1 > x2): 
		return x2
	return x1

def getMax(x1,x2):
	if(x1 > x2):
		return x1
	return x2
#******************************************#
#***** End of helper function section *****#

#***** Classes: Point2D and Vector2D *****#
#**********************************************#
class Point2D:
	def __init__(self, x, y):
		self.x = float(x)
		self.y = float(y)
	def e_dist(self, other):
		return e_dist(self.x - other.x, self.y - other.y)
	def isEqualPt(self, other):
		# It looks like a threshold is needed for float to avoid strange cases where
		# values should be equal but are off by some very tiny amount (e.g. 1E-15)
		x_equal = isEqual(self.x, other.x)
		y_equal = isEqual(self.y, other.y)
		return(x_equal and y_equal)

class Vector2D:
	# Initialize a vector using two Point2Ds.  point2d_1 is considered the start and point2d_2 is the end.
	def __init__(self, point2d_1, point2d_2):
		if not isinstance(point2d_1, Point2D):
			raise TypeError
		if not isinstance(point2d_2, Point2D):
			raise TypeError
		self.point1 = point2d_1
		self.point2 = point2d_2

	def isEqualVect(self, other):
		# I will consider a vector to be equivalent if it has the same endpoints.
		# The direction may be opposite - this will be allowed.
		
		spt1_check = self.point1.isEqualPt(other.point1) or self.point1.isEqualPt(other.point2)
		spt2_check = self.point2.isEqualPt(other.point1) or self.point2.isEqualPt(other.point2)

		return (spt1_check and spt2_check)
				

	# Provides 2 normal vectors to this Vector2D
	# The length of these normal vector is scaled to satisfy the desired_norm
	# Both normal vectors start at the origin to allow easier vector addition in client functions
	def getPerpVectors(self, desired_norm):
		del_x = self.point2.x - self.point1.x
		del_y = self.point2.y - self.point1.y
		
		del_xn = del_x/e_dist(del_x, del_y) * desired_norm
		del_yn = del_y/e_dist(del_x, del_y) * desired_norm
		v1 = Vector2D(Point2D(0.0, 0.0), Point2D(-del_yn, del_xn))
		v2 = Vector2D(Point2D(0.0, 0.0), Point2D(del_yn, -del_xn))
		return v1, v2

	# Function to calculate dot product of this vector with another one.
	def dotProduct(self, other):
		del_x = self.point2.x - self.point1.x
		del_y = self.point2.y - self.point1.y
		
		del_xo = other.point2.x - other.point1.x
		del_yo = other.point2.y - other.point1.y

		return abs(del_x*del_xo + del_y*del_yo)

	# Function to check if two vectors are perpendicular.
	def isPerp(self,other):
		if(self.dotProduct(other) < 0.00001):
			return True
		return False
		
	# Function to check if two vectors form a right angle shape as a corner of a rectangle.
	def isRightAngle(self, other):
		# check that self and other are perpendicular but also share a common endpoint
		endpoint_intersection = self.point1.isEqualPt(other.point1) or self.point1.isEqualPt(other.point2) or \
								self.point2.isEqualPt(other.point1) or self.point2.isEqualPt(other.point2)
		return (endpoint_intersection and self.isPerp(other))

	# *This is one of the key functions used for collision checking.  Helps to draw this out. *
	# Checks for intersection between 2 LINE SEGMENTS.
	# Like above, there are multiple cases:
	# 1) Both vectors are vertical: are the x's the same and do they overlap?
	# 2) One vector is vertical: compute the slope-intercept form and see what value sloped line takes at x' of vertical line
	#    Couple things to check: At x', is y of the sloped line on the vertical line?  And is the sloped line segment even valid at x'?
	# 3) Both vectors are not vertical, but //: get this by computing slope.  If slope is the same, we check if the // line segments overlap.
	# 4) Both vectors are not vertical and are not //: Compute slope-intercept form and look for intersection point.  Check that this 			intersection point actually occurs on both line segments and is valid	
	def check_intersection(self, other):
		if (isEqual(self.point1.x, self.point2.x)):
			if (isEqual(other.point1.x,other.point2.x)):
				# Case 1
				print_debug("both vertical")
				overlap = (isBetween(other.point1.y, self.point1.y, self.point2.y) or isBetween(other.point2.y, self.point1.y, self.point2.y))
				return (isEqual(self.point1.x,other.point1.x) and overlap) 
				# Both are fully vertical.  Intersect iff x's are the same and there is overlap.
			else:
				# Case 2
				m_other = (other.point2.y - other.point1.y)/(other.point2.x - other.point1.x) # m = (y2 - y1)/(x2 - x1)
				b_other = other.point1.y - m_other*other.point1.x # (y-y1) = m(x-x1) so b = y1 -m*x1
				y_check = m_other * self.point1.x + b_other # This would be the intersection value of y if there is an intersection.
				print_debug("first vector vertical sol x y %f %f" % (self.point1.x, y_check))
				validx_on_sloped_line = isBetween(self.point1.x, other.point1.x, other.point2.x)
				validy_on_sloped_line = isBetween(y_check, other.point1.y, other.point2.y) # guarantees y_check is on Vector other
				validy_on_vert_line = isBetween(y_check, self.point1.y, self.point2.y)	  # guarantees y_check is on Vector self
				return (validx_on_sloped_line and validy_on_sloped_line and validy_on_vert_line)
		elif (isEqual(other.point1.x,other.point2.x)):
			# Case 2
			m_self = (self.point2.y - self.point1.y)/(self.point2.x - self.point1.x) # m = (y2 - y1)/(x2 - x1)
			b_self = self.point1.y - m_self*self.point1.x # (y-y1) = m(x-x1) so b = y1 -m*x1
			y_check = m_self * other.point1.x + b_self # This would be the intersection value of y if there is an intersection.
			print_debug("second vector vertical sol x y %f %f" % (other.point1.x, y_check))
			validx_on_sloped_line = isBetween(other.point1.x, self.point1.x, self.point2.x)
			validy_on_sloped_line = isBetween(y_check, self.point1.y, self.point2.y) # guarantees y_check is on Vector self
			validy_on_vert_line = isBetween(y_check, other.point1.y, other.point2.y) # guarantees y_check is on Vector self
			return (validx_on_sloped_line and validy_on_sloped_line and validy_on_vert_line)
		else:
			# General case: Self and other are both NOT vertical vectors
			m_self = (self.point2.y - self.point1.y)/(self.point2.x - self.point1.x) # m = (y2 - y1)/(x2 - x1)
			m_other = (other.point2.y - other.point1.y)/(other.point2.x - other.point1.x)
			b_self = self.point1.y - m_self*self.point1.x # (y-y1) = m(x-x1) so b = y1 -m*x1
			b_other = other.point1.y - m_other*other.point1.x

			if(isEqual(m_self,m_other)): # parallel line segments, check that one of the endpoints intersect this line
				# Case 3
				y_check1 = m_self*other.point1.x + b_self # does the self vector go through either endpoint of other?
				y_check2 = m_self*other.point2.x + b_self
				x_valid1 = isBetween(other.point1.x, self.point1.x, self.point2.x)
				x_valid2 = isBetween(other.point2.x, self.point1.x, self.point2.x)
				check1 = isEqual(y_check1, other.point1.y) and x_valid1
				check2 = isEqual(y_check2, other.point2.y) and x_valid2
				print_debug("parallel")
				return (check1 or check2)
			else:	#not parallel
				# Case 4
				x_test = (b_other - b_self)/(m_self-m_other) # Sol to y = m1*x+b1 = m2*x+b2. 
				y_test1 = m_self*x_test + b_self
				y_test2 = m_other*x_test + b_other
				# Need to check if this a valid solution or not - is x_test a valid point on each segment and do the y's match up?
				print_debug("skew, sol x y1 y2 %f %f %f" % (x_test, y_test1, y_test2))
				is_valid_x = (isBetween(x_test, self.point1.x, self.point2.x) and isBetween(x_test, other.point1.x, other.point2.x))
				return (isEqual(y_test1,y_test2) and is_valid_x) 
#***********************************************#
#***** End of Point2D and Vector2D classes *****#

#***** Rectangle2D class *****#
#*****************************#
class Rectangle2D:
	def __init__(self, v1, v2, v3, v4):
		if not (isinstance(v1,Vector2D) and isinstance(v2,Vector2D) and isinstance(v3,Vector2D) and isinstance(v4,Vector2D)):
			raise TypeError
		if not (v1.isRightAngle(v2) and \
			v1.isRightAngle(v4) and \
			v2.isRightAngle(v1) and \
			v2.isRightAngle(v3) and \
			v3.isRightAngle(v2) and \
			v3.isRightAngle(v4) and \
			v4.isRightAngle(v3) and \
			v4.isRightAngle(v1)):
			# Check that this is actually a rectangle.  
			# Not sure if I missed some edge case where vectors are perp but don't form a rectangle.
			print "Error with 4 vectors. Please check order.  Arg 1 and 3 should be parallel and Arg 2 and 4 should be parallel."
			raise ValueError		
		self.side1 = v1
		self.side2 = v2
		self.side3 = v3
		self.side4 = v4

	def isEqualRect(self, other):
		# I will consider a rectangle the same if it has the same four endpoints.  The vectors for both
		# may be added in a different order; this is not an issue as long as the four endpoints are the same.

		check_side1 = (self.side1.isEqualVect(other.side1) or self.side1.isEqualVect(other.side2) or \
					  self.side1.isEqualVect(other.side3) or self.side1.isEqualVect(other.side4))
		check_side2 = (self.side2.isEqualVect(other.side1) or self.side2.isEqualVect(other.side2) or \
					  self.side2.isEqualVect(other.side3) or self.side2.isEqualVect(other.side4))
		check_side3 = (self.side3.isEqualVect(other.side1) or self.side3.isEqualVect(other.side2) or \
					  self.side3.isEqualVect(other.side3) or self.side3.isEqualVect(other.side4))
		check_side4 = (self.side4.isEqualVect(other.side1) or self.side4.isEqualVect(other.side2) or \
					  self.side4.isEqualVect(other.side3) or self.side4.isEqualVect(other.side4))

		return (check_side1 and check_side2 and check_side3 and check_side4)

	def isRectIntersection(self, other):
		# Idea is if any of the sides of the rectangle intersect a side of the other rectangle, then there should be some overlap.
		intersects = False
		intersects = \
		(self.side1.check_intersection(other.side1)	or \
		self.side1.check_intersection(other.side2)  or \
		self.side1.check_intersection(other.side3)  or \
		self.side1.check_intersection(other.side4)  or \
		self.side2.check_intersection(other.side1)  or \
		self.side2.check_intersection(other.side2)  or \
		self.side2.check_intersection(other.side3)  or \
		self.side2.check_intersection(other.side4)  or \
		self.side3.check_intersection(other.side1)	or \
		self.side3.check_intersection(other.side2)  or \
		self.side3.check_intersection(other.side3)  or \
		self.side3.check_intersection(other.side4)  or \
		self.side4.check_intersection(other.side1)  or \
		self.side4.check_intersection(other.side2)  or \
		self.side4.check_intersection(other.side3)  or \
		self.side4.check_intersection(other.side4))
		return intersects
#************************************#
#***** End of Rectangle2D class *****#


#***** Collision checking helper function to Zumy "traffic controlling" function.  Forms a bounding box. *****#
#*************************************************************************************************************#
def getBoundingBox(path_vector, infl_robot_radius, isMoving):
	# Two cases:
	# 1) Robot is moving: then bounding box is a rectangle that fully encloses "ellipse" shape formed by dragging robot	
	#    from the start to the goal point along path_vector.  
	#    Side lengths are 2*infl_robot_radius and 2*infl_robot_radius + norm(path_vector)
	# 2) Robot is not moving: then bounding box is simple a square with side length 2*infl_robot_radius.  Square is aligned
	#	 with the path_vector.
	# Basically, a bounding box is the smallest rectangle that fully encloses a robot's potential position assuming perfect
	# movement on the path_vector.  
	# We use an inflated robot radius (>= robot's actual radius) to account for errors in traveling to the goal point.
	corner1 = Point2D(0,0)
	corner2 = Point2D(0,0)
	corner3 = Point2D(0,0)
	corner4 = Point2D(0,0)
	perp1, perp2 = path_vector.getPerpVectors(infl_robot_radius)

	pv_del_x = path_vector.point2.x  -path_vector.point1.x
	pv_del_y = path_vector.point2.y  -path_vector.point1.y
	# If you draw this out, the robot_tangent_boundary_pt is the point that you get from going backwards along the path_vector
	# by infl_robot_radius amount.  This is basically the back of the robot, if we assumed the robot's heading is in the same
	# direction as the path vector.  This point is the midpoint of the rectangle side representing the back of the robot start position.
	rbt_tangent_boundary_ptx = path_vector.point1.x - pv_del_x* (infl_robot_radius/e_dist(pv_del_x, pv_del_y))
	rbt_tangent_boundary_pty = path_vector.point1.y - pv_del_y* (infl_robot_radius/e_dist(pv_del_x, pv_del_y))

	# Corner1 is one of the two points along the back of the robot's start position.  
	corner1.x = rbt_tangent_boundary_ptx + perp1.point2.x
	corner1.y = rbt_tangent_boundary_pty + perp1.point2.y

	# Corner2 is one of the two points along the back of the robot's start position
	corner2.x = rbt_tangent_boundary_ptx + perp2.point2.x
	corner2.y = rbt_tangent_boundary_pty + perp2.point2.y

	# Corner3 and corner4 are the corners of the bounding box near the robot's goal point
	if isMoving:
		robot_normal_vector_dist = 2*infl_robot_radius + e_dist(pv_del_x, pv_del_y)
		# To fully enclose the robot's goal position, then we need the rectangle side length to be
		# 2*infl_robot_radius + the length of the path_vector.	
		corner3.x = corner1.x + (robot_normal_vector_dist)*pv_del_x/e_dist(pv_del_x, pv_del_y)
		corner3.y = corner1.y + (robot_normal_vector_dist)*pv_del_y/e_dist(pv_del_x, pv_del_y)
		corner4.x = corner2.x + (robot_normal_vector_dist)*pv_del_x/e_dist(pv_del_x, pv_del_y)
		corner4.y = corner2.y + (robot_normal_vector_dist)*pv_del_y/e_dist(pv_del_x, pv_del_y)
	else:
		# Corner3 and Corner4 form a side parallel to corner1 and corner2 that bounds the front of the robot's start position.
		corner3.x = corner1.x + (2*infl_robot_radius)*pv_del_x/e_dist(pv_del_x, pv_del_y)
		corner3.y = corner1.y + (2*infl_robot_radius)*pv_del_y/e_dist(pv_del_x, pv_del_y)
		corner4.x = corner2.x + (2*infl_robot_radius)*pv_del_x/e_dist(pv_del_x, pv_del_y)
		corner4.y = corner2.y + (2*infl_robot_radius)*pv_del_y/e_dist(pv_del_x, pv_del_y)
		
	side1 = Vector2D(corner1, corner3)
	side2 = Vector2D(corner3, corner4)
	side3 = Vector2D(corner4, corner2)
	side4 = Vector2D(corner2, corner1)
	return(Rectangle2D(side1, side2, side3, side4))
#******************************************************#
#***** End of collision checking helper function. *****#

#***** Obstacle bounding box helper function for A* case with obstacles in environment ***********************#
#*************************************************************************************************************#
def getObsBoundingBox(path_vector, width):
	corner1 = Point2D(0,0)
	corner2 = Point2D(0,0)
	corner3 = Point2D(0,0)
	corner4 = Point2D(0,0)
	perp1, perp2 = path_vector.getPerpVectors(width/2.0)

	pv_del_x = path_vector.point2.x  -path_vector.point1.x
	pv_del_y = path_vector.point2.y  -path_vector.point1.y

	# Path_vector.point1 is the start point of the vector linking
	# one edge of the rectangle to the other edge of the rectangle
	# Both path_vector.point1 and path_vector.point2 bisect the side
	# they are on, so need to find the corners of those sides.	
	# We add the scaled perpendicular vectors (which start at (0,0))
	# to find corner 1 and corner 2 near the start point (point1).
	corner1.x = path_vector.point1.x + perp1.point2.x
	corner1.y = path_vector.point1.y + perp1.point2.y
	corner2.x = path_vector.point1.x + perp2.point2.x
	corner2.y = path_vector.point1.y + perp2.point2.y

	# Corner 3 and Corner 4 are analogous to corner 1 and corner 2
	# but are near the end point of the path_vector.
	# Thus, we can simply translate by the path_vector to find
	# corner 3 and corner 4.
	corner3.x = corner1.x + pv_del_x
	corner3.y = corner1.y + pv_del_y
	corner4.x = corner2.x + pv_del_x
	corner4.y = corner2.y + pv_del_y
		
	side1 = Vector2D(corner1, corner3)
	side2 = Vector2D(corner3, corner4)
	side3 = Vector2D(corner4, corner2)
	side4 = Vector2D(corner2, corner1)
	return(Rectangle2D(side1, side2, side3, side4))
#******************************************************#
#***** End of obstacle bounding box function. *****#

#***** Main functions that will be called by clients as a "traffic controller" for Zumys *****#
#********************************************************************************************#
def command_four_zumys(zumy1_start, zumy1_goal, zumy2_start, zumy2_goal, zumy3_start, zumy3_goal, zumy4_start, zumy4_goal):
	# To Do: Check that user gave an input of Point2D - else need to construct Point2Ds here.
	
	# Hard-coded configuration parameter for now.  Maybe use config.py for this.
	# Equal to the radius of the robot + radius error margin.
	dist_thresh = 0.06
	
	# Priority based assignment with collision avoidance.

	# Step 1: Assume R1 has highest priority and can move.  All robots with lower priority are stopped.
	zumy1BoundingBox = getBoundingBox(Vector2D(zumy1_start, zumy1_goal), dist_thresh, True)
	zumy2BoundingBox = getBoundingBox(Vector2D(zumy2_start, zumy2_goal), dist_thresh, False)
	zumy3BoundingBox = getBoundingBox(Vector2D(zumy3_start, zumy3_goal), dist_thresh, False)
	zumy4BoundingBox = getBoundingBox(Vector2D(zumy4_start, zumy4_goal), dist_thresh, False)

	# Step 2: See if R1's path will intersect with any of the stopped robots.
	zumy1_intersection = zumy1BoundingBox.isRectIntersection(zumy2BoundingBox) or \
						 zumy1BoundingBox.isRectIntersection(zumy3BoundingBox) or \
						 zumy1BoundingBox.isRectIntersection(zumy4BoundingBox)

	# Step 3: Update R1's path based on whether it has permission to move or not.
	zumy1BoundingBox = getBoundingBox(Vector2D(zumy1_start, zumy1_goal), dist_thresh, (not zumy1_intersection))

	# Repeat Steps 1-3 for R2.  R1 can move or not according to above.  R3 and R4 are stopped.
	zumy2BoundingBox = getBoundingBox(Vector2D(zumy2_start, zumy2_goal), dist_thresh, True)
	zumy2_intersection = zumy2BoundingBox.isRectIntersection(zumy1BoundingBox) or \
						 zumy2BoundingBox.isRectIntersection(zumy3BoundingBox) or \
						 zumy2BoundingBox.isRectIntersection(zumy4BoundingBox)

	zumy2BoundingBox = getBoundingBox(Vector2D(zumy2_start, zumy2_goal), dist_thresh, (not zumy2_intersection))

	# Repeat Steps 1-3 for R3.  R1 and R2 may be dynamic or static.  R4 is stopped.
	zumy3BoundingBox = getBoundingBox(Vector2D(zumy3_start, zumy3_goal), dist_thresh, True)

	zumy3_intersection = zumy3BoundingBox.isRectIntersection(zumy1BoundingBox) or \
						 zumy3BoundingBox.isRectIntersection(zumy2BoundingBox) or \
						 zumy3BoundingBox.isRectIntersection(zumy4BoundingBox)

	zumy3BoundingBox = getBoundingBox(Vector2D(zumy3_start, zumy3_goal), dist_thresh, (not zumy3_intersection))

	# Repeat Steps 1-3 for R4.  It is the lowest priority robot so all other robots are either moving or stopped.
	zumy4BoundingBox = getBoundingBox(Vector2D(zumy4_start, zumy4_goal), dist_thresh, True)

	zumy4_intersection = zumy4BoundingBox.isRectIntersection(zumy1BoundingBox) or \
						 zumy4BoundingBox.isRectIntersection(zumy2BoundingBox) or \
						 zumy4BoundingBox.isRectIntersection(zumy3BoundingBox)

	zumy4BoundingBox = getBoundingBox(Vector2D(zumy4_start, zumy4_goal), dist_thresh, (not zumy4_intersection))

	boundingBoxList = [zumy1BoundingBox, zumy2BoundingBox, zumy3BoundingBox, zumy4BoundingBox]
	print {'zumy1_go': (not zumy1_intersection), 'zumy2_go': (not zumy2_intersection), \
		    'zumy3_go': (not zumy3_intersection), 'zumy4_go': (not zumy4_intersection)}
	return (boundingBoxList, {'zumy1_go': (not zumy1_intersection), 'zumy2_go': (not zumy2_intersection), \
		    'zumy3_go': (not zumy3_intersection), 'zumy4_go': (not zumy4_intersection)})

def command_n_zumys(zumy_vect_dict, zumy_prior_list, dist_thresh):
	# zumy_vect_dict is a dictionary with key <zumy_name> and value <Vector2D> (point1 = start, point2 = end)
	# zumy_prior_dict is a dictionary with key <zumy_name> and value <int> encoding priority
	# dist_thresh is the inflated radius for the robot.

	# Check input validity.
	for vect in zumy_vect_dict.values():
		if not isinstance(vect, Vector2D):
			print "Values to input dictionaries should be Point2D!"
			raise ValueError
	if not isinstance(dist_thresh, float):
		print "Inflated robot radius should be a float!"
		raise ValueError

	zumy_BBox_Dict = {}
	intersect_Dict = {}
	move_permission_Dict = {}
 	for curr_zumy_ID in zumy_prior_list:
		zumy_BBox_Dict[curr_zumy_ID] = getBoundingBox(zumy_vect_dict[curr_zumy_ID], dist_thresh, False)
		intersect_Dict[curr_zumy_ID] = False	
	for curr_zumy_ID in zumy_prior_list:
		zumy_BBox_Dict[curr_zumy_ID] = getBoundingBox(zumy_vect_dict[curr_zumy_ID], dist_thresh, True)
		for curr_zumy_ID2 in zumy_prior_list:
			if curr_zumy_ID2 == curr_zumy_ID:
				pass
			else:
				intersect_Dict[curr_zumy_ID] = intersect_Dict[curr_zumy_ID] or \
									zumy_BBox_Dict[curr_zumy_ID].isRectIntersection(zumy_BBox_Dict[curr_zumy_ID2])
		zumy_BBox_Dict[curr_zumy_ID] = getBoundingBox(zumy_vect_dict[curr_zumy_ID], dist_thresh, not intersect_Dict[curr_zumy_ID])
		move_permission_Dict[curr_zumy_ID] = not intersect_Dict[curr_zumy_ID]

	return (zumy_BBox_Dict, move_permission_Dict)        

#****************************************************#
#***** End of main traffic controlling function *****#

#***** A* multi-robot collision checking function *****#
#******************************************************#
# Class to hold robot position data (essentially the same as Pose2D).
# Theta is in radians.
class Zumy_Pose:
	def __init__(self, x, y, thetad):
		self.x = float(x)
		self.y = float(y)
		self.thetad = float(thetad)
		self.thetar = self.thetad * math.pi/180.0
		# theta should be in radians, maybe can add a check for this when used.

	def __eq__(self, pose):
		return self.x == pose.x and self.y == pose.y and self.thetad == pose.thetad and self.thetar == pose.thetar


def create_BBox(zumy_pose, infl_robot_radius, lin_buffer_dist):

	bbox = None

	if(lin_buffer_dist > 0.0):
		# Construct path vector with some delta in front and delta in back for the bounding box.
		pv_endx = rbt.x+lin_buffer_dist*math.cos(rbt.thetar)
		pv_endy = rbt.y+lin_buffer_dist*math.sin(rbt.thetar)
		pv_stx = rbt.x-lin_buffer_dist*math.cos(rbt.thetar)
		pv_sty = rbt.y-lin_buffer_dist*math.sin(rbt.thetar)
	else:
		# Construct a unit vector to encode robot's position and heading.  Bounding box just circumscribes
		# robot's current position.
		pv_endx = rbt.x+math.cos(rbt.thetar)
		pv_endy = rbt.y+math.sin(rbt.thetar)
		pv_stx = rbt.x
		pv_sty = rbt.y
		
	
	path_vector = Vector2D(Point2D(pv_stx, pv_sty), Point2D(pv_endx, pv_endy))

	if(lin_buffer_dist > 0.0):
		# Enclose entire path vector.
		bbox = getBoundingBox(path_vector, infl_robot_radius, True)
	else:			
		# Only enclose robot's current position with a square.
		bbox = getBoundingBox(path_vector, infl_robot_radius, False)

	return bbox

	
def check_zumy_static_collision(zumy_pose, zumy_pose_list, infl_robot_radius, lin_buffer_dist):
	# zumy_collision_dict = dict()

	zumy_BBox = create_BBox(zumy_pose, infl_robot_radius, lin_buffer_dist)


class Obstacle:
	def __init__(self, x, y, thetad, width ,length):
		self.x = float(x)
		self.y = float(y)
		self.thetad = float(thetad)
		self.thetar = self.thetad * math.pi/180.0
		# theta should be in radians, maybe can add a check for this when used.

		self.width = width
		self.length = length
		print self.width
		print self.length
		print ""
		# length = dist of rectangle along its heading
		# width = dist of rectangle perpendicular to its heading


def create_obstacle_bb_list(obstacle_list):
	obs_BBox_List = []
	for obs in obstacle_list:
		if not isinstance(obs, Obstacle):
			print "Error: First input should be a list of Zumy_Pose classes"
			raise TypeError

		pv_endx = obs.x + obs.length/2.0 * math.cos(obs.thetar)
		pv_endy = obs.y + obs.length/2.0 * math.sin(obs.thetar)
		pv_stx  = obs.x - obs.length/2.0 * math.cos(obs.thetar)
		pv_sty  = obs.y - obs.length/2.0 * math.sin(obs.thetar)

		path_vector = Vector2D(Point2D(pv_stx, pv_sty), Point2D(pv_endx, pv_endy))

		# Enclose entire path vector.
		obs_BBox_List.append(getObsBoundingBox(path_vector, obs.width))
	return obs_BBox_List

def check_zumy_obstacle_collision(zumy_pose, infl_robot_radius, lin_buffer_dist, obstacle_bb_list):
	if not isinstance(zumy_pose, Zumy_Pose):
		print "Error: First input should be a list of Zumy_Pose classes"
		raise TypeError

	if(lin_buffer_dist > 0.0):
		pv_endx = zumy_pose.x+lin_buffer_dist*math.cos(zumy_pose.thetar)
		pv_endy = zumy_pose.y+lin_buffer_dist*math.sin(zumy_pose.thetar)
		pv_stx = zumy_pose.x-lin_buffer_dist*math.cos(zumy_pose.thetar)
		pv_sty = zumy_pose.y-lin_buffer_dist*math.sin(zumy_pose.thetar)
	else:
		pv_endx = zumy_pose.x+math.cos(zumy_pose.thetar)
		pv_endy = zumy_pose.y+math.sin(zumy_pose.thetar)
		pv_stx = zumy_pose.x
		pv_sty = zumy_pose.y
		
	path_vector = Vector2D(Point2D(pv_stx, pv_sty), Point2D(pv_endx, pv_endy))
	if(lin_buffer_dist > 0.0):
		# Enclose entire path vector.
		zumy_bbox = getBoundingBox(path_vector, infl_robot_radius, True)
	else:			
		# Only enclose robot's current position with a square.
		zumy_bbox = getBoundingBox(path_vector, infl_robot_radius, False)

	for obs_rect in obstacle_bb_list:
		if not isinstance(obs_rect, Rectangle2D):
			print "Make sure the last input is a list of Rectangle2Ds representing the obstacle!"
			raise TypeError
		if zumy_bbox.isRectIntersection(obs_rect):
			return (True, zumy_bbox)

	return (False, zumy_bbox)
		

def check_zumy_static_collision(zumy_pose_list, infl_robot_radius, lin_buffer_dist):
	zumy_BBox_List = []
	zumy_Permission_List = []

	index_in_list = -1

	for rbt, i in zip(zumy_pose_list, range(len(zumy_pose_list)):
		if rbt == zumy_pose:
			index_in_list = i
			continue

		if not isinstance(rbt, Zumy_Pose):
			print "Error: First input should be a list of Zumy_Pose classes"
			raise TypeError

		zumy_BBox_List.append(create_BBox(rbt, infl_robot_radius, lin_buffer_dist))

	for rbt_j in range(0, len(zumy_BBox_List)):
		if rbt_j == index_in_list:
			continue

		if (zumy_BBox.isEqualRect(zumy_BBox_List[rbt_j])):
			print_debug("match")
			print_debug(rbt_i)
			print_debug(rbt_j)
			print_debug("match_end")
			continue
		# Iterate through every unique pairing of robots in the list.
		if (zumy_BBox.isRectIntersection(zumy_BBox_List[rbt_j])):
			return True

	return False

