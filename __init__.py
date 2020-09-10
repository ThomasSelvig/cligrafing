from colr import color
import os


class Screen:
	def __init__(self, scope=(-1.5, -1.5, 16/9 * 3, 3), screen_dims_offset=(0, -2)):
		self.scope = scope
		
		_screen_dims = list(reversed([int(i) for i in os.popen('stty size', 'r').read().split()]))
		# offset is amount of rows / columns to add to the final render size
		self.screen_dims = [dim+dim_offset for dim, dim_offset in zip(_screen_dims, screen_dims_offset)]
		
		# list of rows to print
		# indexable by: self.screen[y][x]
		self.screen = [[" " for x in range(self.screen_dims[0])] for y in range(self.screen_dims[1])]
		
	def graph_gen(self, exp, pen_color=None):
		sc_x, sc_y, sc_w, sc_h = self.scope
		# check all "renderable" columns (col) for possible f(x) value
		for col in range(self.screen_dims[0]):
			x = col / self.screen_dims[0] * sc_w + sc_x
			y = exp(x)
			
			try:
				# check if this x value has a corresponding f(x) in scope
				# this is in a try-except because passed "exp" might return y val of type "complex"
				row = self._screen_pos(y=y)
			except TypeError:
				row = None
			
			if row is not None:
				# found f(x) for this col
				ink = "#" if not pen_color else color("#", fore=pen_color)
				self.screen[self.screen_dims[1] - 1 - row][col] = ink  # indexing the screen: flip y value
		
		return self  # enable chaining
		
	def _screen_pos(self, x=None, y=None):
		""":returns: row, col"""
		sc_x, sc_y, sc_w, sc_h = self.scope
		values = []
		
		if x is not None:
			if self._in_scope(x=x):
				values.append(int((x - sc_x) / sc_w * self.screen_dims[0] ))
			else:
				values.append(None)

		if y is not None:
			if self._in_scope(y=y):
				values.append(int( (y - sc_y) / sc_h * self.screen_dims[1] ))
			else:
				values.append(None)
				
		return tuple(values) if len(values) > 1 else values[0]
		
	def _in_scope(self, x=None, y=None):
		""":returns: if the given arg is in scope"""
		assert x is not None or y is not None and not x is not None and y is not None, "pass only one arg"
		sc_x, sc_y, sc_w, sc_h = self.scope
		
		if x is not None:
			return x >= sc_x and x <= sc_x + sc_w
		
		if y is not None:
			return y >= sc_y and y <= sc_y + sc_h

	def _paint_axes(self):
		# paint x and y axis if in scope
		# x
		if self._in_scope(y=0):
			row = self.screen_dims[1] - 1 - self._screen_pos(y=0)
			for col in range(self.screen_dims[0]):
				ink_before = self.screen[row][col]
				self.screen[row][col] = color(ink_before, back="blue")
		# y
		if self._in_scope(x=0):
			col = self._screen_pos(x=0)
			for row in range(self.screen_dims[1]):
				ink_before = self.screen[row][col]
				self.screen[row][col] = color(ink_before, back="red")
		
	def _paint_overlay(self):
		sc_x, sc_y, sc_w, sc_h = self.scope
		sc_x2 = sc_x + sc_w
		sc_y2 = sc_y + sc_h
		
		to_overlay = [  # (string, row, col)
			(str(round(sc_x, 2)), self.screen_dims[1] // 2, 0),
			(str(sc_x2), self.screen_dims[1] // 2, self.screen_dims[0]-len(str(round(sc_x2, 2)))),
			
			(str(round(sc_y2, 2)), 0, self.screen_dims[0] // 2),
			(str(round(sc_y, 2)), self.screen_dims[1]-1, self.screen_dims[0] // 2)
		]

		for string, row, col in to_overlay:
			for i, c in enumerate(string):
				if col + i < self.screen_dims[0]:
					self.screen[row][col + i] = color(c, "red", "white")
		
	
	def render(self, paint_all=True):
		if paint_all:
			self._paint_axes()
			self._paint_overlay()
			
		compiled_rows = ["".join(row) for row in self.screen]
		#return "".join(compiled_rows)
		return "\n".join(compiled_rows)

