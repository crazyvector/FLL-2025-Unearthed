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
    br.driveArcDist(
        radius=-550, dist=-850, speedPct=80, then=Stop.BRAKE, waiting=True
    )
    br.moveRightAttachmentMotorForDegrees(degrees=200, speedPct=80)
    br.driveForDistance(
        distance=-420, speedPct=80, then=Stop.NONE, waiting=True
    )
    # br.turnInPlace(angle=-55, speedPct=45)
    # br.driveForDistance(distance=40, speedPct=80, then=Stop.BRAKE, waiting=True)
    # br.moveRightAttachmentMotorForDegrees(degrees=-380, speedPct=100)
    # br.driveForDistance(distance=-700, speedPct=80, then=Stop.BRAKE, waiting=True)
    br.driveArcDist(
        radius=150, dist=-230, speedPct=80, then=Stop.NONE, waiting=True
    )
    br.driveForDistance(
        distance=-300, speedPct=80, then=Stop.BRAKE, waiting=True
    )
    br.driveForDistance(
        distance=130, speedPct=80, then=Stop.BRAKE, waiting=True
    )
    br.moveRightAttachmentMotorForDegrees(degrees=-200, speedPct=100)
    br.waitForMillis(millis=600)
    br.moveRightAttachmentMotorForDegrees(degrees=210, speedPct=100)
    br.turnInPlace(angle=-94, speedPct=45)
    br.driveForDistance(
        distance=200, speedPct=80, then=Stop.BRAKE, waiting=True
    )
    br.moveRightAttachmentMotorForDegrees(degrees=-200, speedPct=100)
    br.driveForDistance(
        distance=-50, speedPct=80, then=Stop.BRAKE, waiting=True
    )
    br.moveRightAttachmentMotorForDegrees(degrees=200, speedPct=100)
    # br.driveForMillis(millis=1500, speedPct=80)
    # br.driveForDistance(distance=-60, speedPct=80, then=Stop.BRAKE, waiting=True)
    # br.turnInPlace(angle=-55, speedPct=45)


# Leave everything below here and don't type anything below this line
# If running this program directly (not from the master program), this is
# how we know it is running directly. In which case, this method will
# create a BaseRobot and run the Run(br) method above.
# In other words, keep these three lines at the bottom of your code and
# everything will be fine.
if __name__ == "__main__":
    br = BaseRobot()
    Run(br)
