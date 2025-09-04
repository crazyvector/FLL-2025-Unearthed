from base_robot import *

# Add good comments, such as what the mission is supposed to do,
# how to align the robot in home, any initial starting instructions,
# such as how it should be loaded with anything, arm positions, etc.


# When we run this program from the master program, we will call this
# "Run(br)" method.
def Run(br: BaseRobot):
    # Your mission code goes here, step-by-step
    # It MUST be indented just like the lines below

    br.driveForDistance(
        distance=650, speedPct=80, then=Stop.BRAKE, waiting=True
    )

    # br.driveArcDist(radius=-1800, dist=-200, speedPct=80, then=Stop.BRAKE, waiting=True)
    # negative move right
    # br.waitForMillis(1000)
    br.driveForDistance(distance=-50, speedPct=100)
    br.turnInPlace(angle=53, speedPct=45)
    br.moveLeftAttachmentMotorForDegrees(degrees=170, speedPct=1, waiting=False)
    br.driveForDistance(distance=500, speedPct=80, then=Stop.BRAKE, waiting=True
    )
    br.moveLeftAttachmentMotorForDegrees(degrees=-170, speedPct=100)
    br.driveForDistance(distance=-200, speedPct=80, then=Stop.BRAKE, waiting=True)
    br.turnInPlace(angle=53, speedPct=45)
    br.driveForDistance(distance=-300, speedPct=100, then=Stop.BRAKE, waiting=True)
    br.turnInPlace(angle=70, speedPct=45)
    br.driveForDistance(distance=700, speedPct=100, then=Stop.BRAKE, waiting=True)
    # br.driveForDistance(
        # distance=-700, speedPct=80, then=Stop.BRAKE, waiting=True
    # )


# Leave everything below here and don't type anything below this line
# If running this program directly (not from the master program), this is
# how we know it is running directly. In which case, this method will
# create a BaseRobot and run the Run(br) method above.
# In other words, keep these three lines at the bottom of your code and
# everything will be fine.
if __name__ == "__main__":
    br = BaseRobot()
    Run(br)
