import scipy.integrate as integrate
import math

class PlanePathCalculator():
	def __init__(self, heading, ascentAirSpd, ascentRate, engFailTime, descentAirSpd, descentRate, windSpd, windDirection):
		self.heading = math.radians(heading)
		self.ascentAirSpd = ascentAirSpd
		self.ascentRate = ascentRate
		self.engFailTime = engFailTime
		self.descentAirSpd = descentAirSpd
		self.descentRate = descentRate
		self.windSpd = windSpd
		self.windDirection = math.radians(windDirection)


	def ascentMovement(self):
		distance = self.engFailTime * self.ascentAirSpd
		Ydistance = math.cos(self.heading) * distance
		Xdistance = math.sin(self.heading) * distance

		return (Xdistance, Ydistance)

	def descentMovement(self):
		airTime = self.ascentRate * self.engFailTime / self. descentRate
		distance = airTime * self.descentAirSpd
		Ydistance = math.cos(self.heading) * distance
		Xdistance = math.sin(self.heading) * distance

		return (Xdistance, Ydistance) 

	def windMovement(self):
		airTime = self.ascentRate * self.engFailTime / self. descentRate
		result = integrate.quad(lambda t: -(1/720)*t**2 + 25, 0, airTime)
		Ydistance = math.cos(self.windDirection) * result[0]
		Xdistance = math.sin(self.windDirection) * result[0]

		return (Xdistance, Ydistance) 

	def totalMovement(self):

		return (self.ascentMovement()[0] + self.descentMovement()[0] + self.windMovement()[0], self.ascentMovement()[1] + self.descentMovement()[1] + self.windMovement()[1])

	def searchLocation(self):
		movement = self.totalMovement()
		distance = math.sqrt(movement[0]**2 + movement[1]**2)
		degree = math.degrees(math.atan(movement[1]/movement[0]))

		return (distance, degree)


		
def main():

    heading = int(input("Heading: "))
    ascentAirSpd = int(input("Ascent Air Speed: "))
    ascentRate = int(input("Ascent Rate: "))
    engFailTime = int(input("Engine Failure Time: "))
    descentAirSpd = int(input("Descent Air Speed: "))
    descentRate = int(input("Descent Rate: "))
    windSpd = int(input("Wind Speed: "))
    windDirection = int(input("Wind Direction: "))
    
    calc = PlanePathCalculator(heading, ascentAirSpd, ascentRate, engFailTime, descentAirSpd, descentRate, windSpd, windDirection)

    search = calc.searchLocation()
    print("Reported Search Zone: %f in direction %f degrees from take off" % (search[0], search[1]))

if __name__ == "__main__":
    main()
