import math, random
from cligrafing import Screen
from argparse import ArgumentParser


def main(args):
	s = Screen(scope=(args.x, args.y, 16/9 * args.s, args.s))
	
	for i, f_str in enumerate(args.f):
		f = eval(f"lambda x: {f_str}")
		
		if i < len(args.c):
			s.graph_gen(f, pen_color=args.c[i])
		else:
			s.graph_gen(f)
	
	print(s.render())


if __name__ == "__main__":
	parser = ArgumentParser()
	
	parser.add_argument("f", nargs="+", help="f(x) definition (lambda x prepended)")
	parser.add_argument("-c", nargs="*", help="colors to use for the passed expressions", default=[])
	
	parser.add_argument("-x", type=float, help="scope left pos", default=-3)
	parser.add_argument("-y", type=float, help="scope bottom pos", default=-3)
	parser.add_argument("-s", type=float, help="scope size", default=6)
	
	main(parser.parse_args())
	