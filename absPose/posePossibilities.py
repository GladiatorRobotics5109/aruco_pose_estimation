from fieldTag import FieldTag
from numpy import pi

length = 16.4592
width = 8.2296

poses = {
    1 : FieldTag(1, 0, 15.513558 - (length/2), 1.071626 - (width/2), 0.462788),
    2: FieldTag(2, 0, 15.513558 - (length/2), 2.748026 - (width/2), 0.462788),
    3: FieldTag(3, 0, 15.513558 - (length/2), 3.738626 - (width/2), 0.462788),
    6: FieldTag(6, pi, 1.02743 - (length/2), 3.738626  - (width/2), 0.462788),
    7: FieldTag(7, pi, 1.02743 - (length/2), 2.748026  - (width/2), 0.462788),
    8: FieldTag(8, pi, 1.02743 - (length/2), 1.071626 - (width/2), 0.462788)
}