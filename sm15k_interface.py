from deltaelektronika import SM15K
import time

# IP Address of the power supply, can be obtain the device itself.
IPV4 = '0.0.0.0' 

# To activate debugging option. Creates system-log file and logs there
SM15K.activateDebugLogger = True 

# To use colorful printing at console.
ColorPrint = SM15K.ColorPrinter()
ColorPrint.printFeedback(message="Your message to print to console as feedback!")
ColorPrint.printComment(message="Your message to print to console as comment!")
ColorPrint.printError(message="Your message to print to console as error!")
ColorPrint.printNormal(message="Your message to print to console as normal!")
ColorPrint.printColorful(message="Your message to print to console as colorful!", colour="purple")
# Available colors for printColorful method are "purple", "blue", "cyan", "green", "red", "yellow", "normal"

# To use all comments for SM15K
sm15k = SM15K.SM15K(IPV4=IPV4)
"""
# Source related comments
sm15k.source."SourceRelatedComments"()
sm15k.source.ReadPowerSet()
sm15k.source.SetCurrent(current=20)

# Measure related comments
sm15k.measure."MeasureRelatedComments"()
sm15k.measure.MeasurePower()
sm15k.measure.SetAhMeasurementState(setting="ON")

# Output related comments
sm15k.output."OutputRelatedComments"()
sm15k.output.ReadOutputSet()
sm15k.output.SetOutput(setting="ON")

# System related comments
sm15k.system."SystemRelatedComments"()
sm15k.system.ReadWatchdogSet()
sm15k.system.SetPowerLimit(powerlimit=2000, setting="ON")

# Shutdown related comments
sm15k.shutdown."ShutdownRelatedComments"()
sm15k.shutdown.limitShutdownValues()
sm15k.shutdown.setShutdownOutput()
"""