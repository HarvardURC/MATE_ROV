import pygame, sys
from pygame.locals import *



# Define some colors
BLACK	= (   0,   0,   0)
WHITE	= ( 255, 255, 255)

# This is a simple class that will help us print to the screen
# It has nothing to do with the joysticks, just outputting the
# information.
class TextPrint:
	def __init__(self):
		self.reset()
		self.font = pygame.font.Font(None, 20)

	def print(self, screen, textString):
		textBitmap = self.font.render(textString, True, BLACK)
		screen.blit(textBitmap, [self.x, self.y])
		self.y += self.line_height
		
	def reset(self):
		self.x = 10
		self.y = 10
		self.line_height = 15
		
	def indent(self):
		self.x += 10
		
	def unindent(self):
		self.x -= 10

pygame.init()
pygame.joystick.init()
pygame.display.init()
size = [500, 700]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("PyGame")

done = False
clock = pygame.time.Clock()
textPrint = TextPrint()

njoysticks = pygame.joystick.get_count()
if njoysticks == 0:
	print("No joysticks found")
	pygame.quit()
else:
	joylist = []
	for n in range(0, njoysticks):
		joylist.append(pygame.joystick.Joystick(n))
		joylist[n].init()
		print(joylist[n].get_name())
	logitech = joylist[0]
	while done==False:






		# EVENT PROCESSING STEP
		for event in pygame.event.get(): # User did something
			if event.type == pygame.QUIT: # If user clicked close
				done=True # Flag that we are done so we exit this loop
			
			# Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
			# if event.type == pygame.JOYAXISMOTION:
			#	 print("Joystick axis moved.")
		
		# DRAWING STEP
		# First, clear the screen to white. Don't put other drawing commands
		# above this, or they will be erased with this command.
		screen.fill(WHITE)
		textPrint.reset()

		buttonA = logitech.get_button(1)
		buttonB = logitech.get_button(2)
		buttonX = logitech.get_button(0)
		buttonY = logitech.get_button(3)
		buttonLB = logitech.get_button(4)
		buttonRB = logitech.get_button(5)
		buttonLT = logitech.get_button(6)
		buttonRT = logitech.get_button(7)
		# -1 <= up < 0 < down <= +1
		if buttonLB:
			y = 0.
			z = logitech.get_axis(1)
		else:
			y = logitech.get_axis(1)
			z = 0.
		pitch = logitech.get_axis(3)

		# -1 <= left < 0 < right <= +1
		if buttonRB:
			yaw = 0.
			roll = logitech.get_axis(2)
		else:
			yaw = logitech.get_axis(2)
			roll = 0.
		x = logitech.get_axis(0)

		textPrint.print(screen, "x: {:>6.3f}".format(x))
		textPrint.print(screen, "y: {:>6.3f}".format(y))
		textPrint.print(screen, "z: {:>6.3f}".format(z))
		textPrint.print(screen, "roll: {:>6.3f}".format(roll))
		textPrint.print(screen, "pitch: {:>6.3f}".format(pitch))
		textPrint.print(screen, "yaw: {:>6.3f}".format(yaw))

		# Get count of joysticks
		joystick_count = pygame.joystick.get_count()

		textPrint.print(screen, "Number of joysticks: {}".format(joystick_count) )
		textPrint.indent()
		
		# For each joystick:
		for i in range(joystick_count):
			joystick = pygame.joystick.Joystick(i)
			joystick.init()
		
			textPrint.print(screen, "Joystick {}".format(i) )
			textPrint.indent()
		
			# Get the name from the OS for the controller/joystick
			name = joystick.get_name()
			textPrint.print(screen, "Joystick name: {}".format(name) )
			
			# Usually axis run in pairs, up/down for one, and left/right for
			# the other.
			axes = joystick.get_numaxes()
			textPrint.print(screen, "Number of axes: {}".format(axes) )
			textPrint.indent()
			
			for i in range( axes ):
				axis = joystick.get_axis( i )
				textPrint.print(screen, "Axis {} value: {:>6.3f}".format(i, axis) )
			textPrint.unindent()
				
			buttons = joystick.get_numbuttons()
			textPrint.print(screen, "Number of buttons: {}".format(buttons) )
			textPrint.indent()

			for i in range( buttons ):
				button = joystick.get_button( i )
				textPrint.print(screen, "Button {:>2} value: {}".format(i,button) )
			textPrint.unindent()
				
			# Hat switch. All or nothing for direction, not like joysticks.
			# Value comes back in an array.
			hats = joystick.get_numhats()
			textPrint.print(screen, "Number of hats: {}".format(hats) )
			textPrint.indent()

			for i in range( hats ):
				hat = joystick.get_hat( i )
				textPrint.print(screen, "Hat {} value: {}".format(i, str(hat)) )
			textPrint.unindent()
			
			textPrint.unindent()

		
		# ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
		
		# Go ahead and update the screen with what we've drawn.
		pygame.display.flip()

		# Limit to 20 frames per second
		clock.tick(20)
		
	# Close the window and quit.
	# If you forget this line, the program will 'hang'
	# on exit if running from IDLE.
	pygame.quit ()
	
