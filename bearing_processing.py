import math

radian = math.pi / 180

# This is just to get the example angles that would otherwise be detected
target_lat = 52.38357295014132 #52.347186141064434 #52.279676617334
target_long = -1.560884717814845 #-1.5831466072307527 #-1.5852070446352

angle1 = math.atan2(target_long - -1.583893926455627, target_lat - 52.34902873378519) / radian
if angle1 < 0:
    angle1 = 360 - abs(angle1)
m1 = (1 / math.tan(angle1 * radian))
c1 = 52.34902873378519 - (m1 * -1.583893926455627)

print("Detector 1:")
print(angle1)
print("y - 52.34902873378519 =", m1, "(x + 1.583893926455627)")
print("y -", m1, "x =", c1)

angle2 = math.atan2(target_long - -1.5790015774080997, target_lat - 52.34618433354199) / radian
if angle2 < 0:
    angle2 = 360 - abs(angle2)
m2 = (1 / math.tan(angle2 * radian))
c2 = 52.34618433354199 - (m2 * -1.5790015774080997)

print("\nDetector 2:")
print(angle2)
print("y - 52.34618433354199 =", m2, "(x + 1.5790015774080997)")
print("y -", m2, "x =", c2)

angle3 = math.atan2(target_long - -1.586258129005962, target_lat - 52.34612155627798) / radian
if angle3 < 0:
    angle3 = 360 - abs(angle3)
m3 = (1 / math.tan(angle3 * radian))
c3 = 52.34612155627798 - (m3 * -1.586258129005962)

print("\nDetector 3:")
print(angle3)
print("y - 52.34612155627798 =", m3, "(x + 1.586258129005962)")
print("y -", m3, "x =", c3)