from cligrafing import Screen
import math


def main():
	s = Screen(scope=(-1.5, -1.5, 16/9 * 3, 3))
	
	# circle functions
	f_circle_pos = lambda x: (1**2 - x**2)**.5
	f_circle_neg = lambda x: -f_circle_pos(x)
	
	# paint graphs with specified color
	s.graph_gen(f_circle_pos, pen_color="orange")
	s.graph_gen(f_circle_neg, pen_color="salmon")
	s.graph_gen(math.sin, pen_color=(0, 139, 139))
	
	# paint basic
	s.graph_gen(lambda x: x/4)
	
	# print final render
	print(s.render())
	

if __name__ == "__main__":
	main()