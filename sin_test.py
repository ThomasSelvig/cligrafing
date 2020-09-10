import math

from cligrafing import Screen


def main():
	s = Screen(scope=(-3, -3, 16/9 * 6, 6))
	
	s.graph_gen(math.sin, pen_color=(0, 139, 139))
	
	print(s.render())
	

if __name__ == "__main__":
	main()