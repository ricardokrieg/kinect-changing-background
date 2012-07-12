#!/usr/bin/python

import pygame
from pygame.locals import *
from pygame.color import THECOLORS
from openni import *
import numpy
import cv
import sys

XML_FILE = 'config.xml'
MAX_DEPTH_SIZE = 10000

context = Context()
context.init_from_xml_file(XML_FILE)

depth_generator = DepthGenerator()
depth_generator.create(context)

image_generator = ImageGenerator()
image_generator.create(context)

user_generator = UserGenerator()
user_generator.create(context)

user_generator.alternative_view_point_cap.set_view_point(image_generator)

context.start_generating_all()

pygame.init()

screen = pygame.display.set_mode((640, 480))
background = pygame.image.load('hell.png')

grayscale_palette = tuple([(i, i, i) for i in range(256)])
palette = [(0, 0, 0), (255, 0, 0), (255, 0, 0), (255, 0, 0)]

pygame.display.set_caption('Kinect Simple Viewer')

running = True
histogram = None
depth_map = None
image_count = 0
total_time = 0

print "Image dimensions ({full_res[0]}, {full_res[1]})".format(full_res=depth_generator.metadata.full_res)

def capture_rgb(mask):
	rgb_frame = numpy.fromstring(image_generator.get_raw_image_map_bgr(), dtype=numpy.uint8).reshape(480, 640, 3)

	image = cv.fromarray(rgb_frame)
	cv.CvtColor(cv.fromarray(rgb_frame), image, cv.CV_BGR2RGB)
	pyimage = pygame.image.frombuffer(image.tostring(), cv.GetSize(image), 'RGB')

	return pyimage
# capture_rgb

while running:
	for event in pygame.event.get():
		if event.type == KEYDOWN and event.key == K_ESCAPE: running = False
	# for

	screen.fill(THECOLORS['white'])
	context.wait_any_update_all()
	cv.WaitKey(10)

	start_time = pygame.time.get_ticks()

	screen.blit(background, (0, 0))

	mask = numpy.asarray(user_generator.get_user_pixels(0)).reshape(480, 640)
	x = pygame.transform.rotate(pygame.transform.flip(pygame.surfarray.make_surface(mask), True, False), 90)
	x.set_palette(palette)
	x.set_colorkey(THECOLORS['red'])

	rgb_frame = capture_rgb(mask)
	rgb_frame.blit(x, (0, 0))
	rgb_frame.set_colorkey(THECOLORS['black'])
	screen.blit(rgb_frame, (0, 0))

	image_count += 1
	total_time += pygame.time.get_ticks() - start_time

	pygame.display.flip()
# while

context.stop_generating_all()
sys.exit(0)