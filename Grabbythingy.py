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
    br.driveForDistance(
        distance=450, speedPct=80, then=Stop.BRAKE, waiting=True
    )
    br.moveRightAttachmentMotorForDegrees(degrees=-250, speedPct=80)
    # br.turnInPlace(angle=5, speedPct=45)
    # br.driveForDistance(distance=100, speedPct=80, then=Stop.BRAKE, waiting=True)
    br.driveForDistance(
        distance=-45, speedPct=80, then=Stop.BRAKE, waiting=True
    )
    br.moveRightAttachmentMotorForDegrees(degrees=150, speedPct=10)
    # br.driveForDistance(
    #     distance=30, speedPct=80, then=Stop.BRAKE, waiting=True
    # )
    # br.moveRightAttachmentMotorForDegrees(degrees=70, speedPct=80)
    br.driveForDistance(
        distance=-20, speedPct=80, then=Stop.NONE, waiting=True
    )
    br.moveRightAttachmentMotorForDegrees(degrees=-300, speedPct=70)
    br.driveForDistance(
        distance=-600, speedPct=80, then=Stop.BRAKE, waiting=True
    )


# Leave everything below here and don't type anything below this line
# If running this program directly (not from the master program), this is
# how we know it is running directly. In which case, this method will
# create a BaseRobot and run the Run(br) method above.
# In other words, keep these three lines at the bottom of your code and
# everything will be fine.
if __name__ == "__main__":
    br = BaseRobot()
    Run(br)
