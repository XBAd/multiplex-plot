"""
Unit tests for the :class:`text.annotation.TextAnnotation` class.
"""

import matplotlib.pyplot as plt
import os
import sys
import unittest

path = os.path.join(os.path.dirname(__file__), '..')
if path not in sys.path:
	sys.path.insert(1, path)

import drawable
import util

class TestTextAnnotation(unittest.TestCase):
	"""
	Unit tests for the :class:`text.annotation.TextAnnotation` class.
	"""

	def test_text(self):
		"""
		Test that the text is written correctly.
		"""

		text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team.'
		viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
		lines = viz.draw_text_annotation(text.split())

		drawn_text = self._reconstruct_text(lines)
		self.assertEqual(text, drawn_text)

	def test_text_vertically_aligned(self):
		"""
		Test that each line is vertically-aligned (the y-coordinate is the same for each line's tokens).
		"""

		text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team.'
		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		lines = viz.draw_text_annotation(text.split())

		for _, tokens in lines:
			y = 0
			for i, token in enumerate(tokens):
				bb = util.get_bb(viz.figure, viz.axis, token)
				if i > 0:
					self.assertEqual(y, bb.y0)
				else:
					y = bb.y0

	def test_text_does_not_overlap(self):
		"""
		Test that the lines do not overlap.
		"""

		text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		lines = viz.draw_text_annotation(text.split())

		for i, (_, tokens) in enumerate(lines):
			y = 0
			bb = util.get_bb(viz.figure, viz.axis, tokens[0])
			if i > 0:
				self.assertLessEqual(y, bb.y0)

			y = bb.y1

	def test_align_left(self):
		"""
		Test that when aligning text left, all lines start at the same x-coordinate.
		"""

		text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		lines = viz.draw_text_annotation(text.split(), align='left')

		x = 0
		for i, (_, tokens) in enumerate(lines):
			bb = util.get_bb(viz.figure, viz.axis, tokens[0])
			if i == 0:
				x = bb.x0

			self.assertEqual(x, bb.x0)

	def test_align_right(self):
		"""
		Test that when aligning text right, all lines end at the same x-coordinate.
		"""

		text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		lines = viz.draw_text_annotation(text.split(), align='right')

		x = 0
		for i, (_, tokens) in enumerate(lines):
			bb = util.get_bb(viz.figure, viz.axis, tokens[-1])
			if i == 0:
				x = bb.x1

			self.assertEqual(x, bb.x1)

	def test_align_center(self):
		"""
		Test that when centering text, all of the lines' centers are the same.
		"""

		text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		lines = viz.draw_text_annotation(text.split(), align='center')

		x = 0
		for i, (_, tokens) in enumerate(lines[:-1]):
			bb0 = util.get_bb(viz.figure, viz.axis, tokens[0])
			bb1 = util.get_bb(viz.figure, viz.axis, tokens[-1])
			center = (bb0.x0 + bb1.x1) / 2.
			if i == 0:
				x = center

			self.assertEqual(round(x, 5), round(center, 5))

	def test_align_justify(self):
		"""
		Test that when justifying text, all lines start and end at the same x-coordinate.
		The calculation is made on the center since the bboxes of text do not start or end at the exact same coordinate.
		"""

		text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		lines = viz.draw_text_annotation(text.split(), align='justify')

		x = 0
		for i, (_, tokens) in enumerate(lines[:-1]): # skip the last line as it is not justified
			bb0 = util.get_bb(viz.figure, viz.axis, tokens[0])
			bb1 = util.get_bb(viz.figure, viz.axis, tokens[-1])
			center = (bb0.x0 + bb1.x1) / 2.
			if i == 0:
				x = center

			self.assertEqual(round(x, 5), round(center, 5))

	def test_align_invalid(self):
		"""
		Test that when an invalid alignment is given, a :class:`ValueError` is raised.
		"""

		text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		self.assertRaises(ValueError, viz.draw_text_annotation, text.split(), align='invalid')

	def _reconstruct_text(self, lines):
		"""
		Reconstruct the visualization text from a list of lines.
		The method expects nested lists.
		Each high-level list is a tuple, where the second element is a list of tokens.

		:param lines: A list of lists, each list a line of tokens.
		:type lines: list of list

		:return: The re-constructed text.
		:rtype: str
		"""

		return ' '.join([ ' '.join([ token.get_text() for token in line ]) for _, line in lines ])