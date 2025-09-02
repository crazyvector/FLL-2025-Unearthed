from base_robot import *

# Add good comments, such as what the mission is supposed to do,
# how to align the robot in home, any initial starting instructions,
# such as how it should be loaded with anything, arm positions, etc.


# When we run this program from the master program, we will call this
# "Run(br)" method.
def Run(br: BaseRobot):
    # Your mission code goes here, step-by-step
    # It MUST be indented just like the lines below

    # to
  br.driveForDistance(distance=230, speedPct=80, then=Stop.NONE. BRAKE, waiting=True)
  br.driveArcDist(radius=-125, dist=200, speedPct=80, then=Stop. NONE. BRAKE, waiting=True)
  br.driveForDistance(distance=300, speedPct=80, then=Stop.BRAKE, waiting=True)
  br.turnInPlace(angle=93, speedPct=45)
  br.driveForDistance(distance=67, speedPct=80, then=Stop.BRAKE, waiting=True)
  br.moveRightAttachmentMotorForDegrees(degrees=-75, speedPct=100)

# Leave everything below here and don't type anything below this line
# If running this program directly (not from the master program), this is
# how we know it is running directly. In which case, this method will
# create a BaseRobot and run the Run(br) method above.
# In other words, keep these three lines at the bottom of your code and
# everything will be fine.
if __name__ == "__main__":
    br = BaseRobot()
    Run(br)
