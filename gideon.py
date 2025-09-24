from base_robot import *

# Add good comments, such as what the mission is supposed to do,
# how to align the robot in home, any initial starting instructions,
# such as how it should be loaded with anything, arm positions, etc.


# When we run this program from the master program, we will call this
# "Run(br)" method.
def Run(br: BaseRobot):
    # Your mission code goes here, step-by-step
    # It MUST be indented just like the lines below

    br.driveArcDist(radius=3000, dist=700, speedPct=60, then=Stop.BRAKE, waiting=True, gyro=False)
    br.moveLeftAttachmentMotorForDegrees(degrees=-500, speedPct=100) # neg deg = lower the arm
    dist = 110
    br.driveForDistance(distance=-dist, speedPct=80, then=Stop.BRAKE, waiting=True)
    for pushes in range(7):
        br.driveForDistance(distance=dist, speedPct=80, then=Stop.BRAKE, waiting=True)
        br.driveForDistance(distance=-dist + 40, speedPct=80, then=Stop.BRAKE, waiting=True)

    # br.moveRightAttachmentMotorForMillis(millis=6000, speedPct=-80)
    # br.moveLeftAttachmentMotorForDegrees(degrees=-4500, speedPct=100) # pos deg = raise the arm
    # br.driveForDistance(distance=-700, speedPct=100, then=Stop.BRAKE, waiting=True)


# Leave everything below here and don't type anything below this line
# If running this program directly (not from the master program), this is
# how we know it is running directly. In which case, this method will
# create a BaseRobot and run the Run(br) method abe.
# In other words, keep these three lines at the bottom of your code and
# everything will be fine.
if __name__ == "__main__":
    br = BaseRobot()
    Run(br)
