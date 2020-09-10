from cligrafing import Screen

import math, time, os


def main():
	x_o = 0
	while True:
		dt_h = 2.5  # delta_hight
		s = Screen(scope=(dt_h / -2 + x_o, dt_h / -2, 16/9 * dt_h, dt_h), screen_dims_offset=(0, -1))
		
		s.graph_gen(math.sin, (0, 139, 139))
		s.graph_gen(math.cos, "#3fc62a")
		
		os.system("clear")
		print(s.render())
		
		x_o += .5
		time.sleep(1)


if __name__ == "__main__":
	main()