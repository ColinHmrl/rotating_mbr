# MBR
import numpy as np

class RotatingMbr():
    """Find the minimum bounding rectangle of a point cloud

    Args:
        pointCloud (pointCloud): point cloud to search for mbr
        rotatingStep (int, optional): rotating step in degrees to find mbr. Defaults to 1.
    """

    def __init__(self,pointCloud,step=1):

        self.pointCloud = pointCloud
        self.bestMbrPoints,self.bestMbrArea = calculateMbr(pointCloud)
        self.bestMbrAngle = 0
        self.center = (self.bestMbrPoints.p1 + self.bestMbrPoints.p3) / 2



    def rotatePoint(origin, point, angle):
        """
        Rotate a point counterclockwise by a given angle around a given origin.

        The angle should be given in degree.
        """
        angle = math.radians(angle)
        ox, oy, oz = origin
        px, py, pz = point

        qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
        qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
        return qx, qy, pz
        
    def rotatePointCloud(cloud,angle,center):
        """
        Rotate Every point of the cloud around the center by an angle
        """
        origin = np.mean(cloud, axis=0)
        cloud_rotated = np.array([rotate_point(center,point,angle) for point in cloud])
        return cloud_rotated     


    def calculateMbr(self):
        min_x,min_y,min_z = np.min(cloud, axis=0)
        max_x,max_y,max_z = np.max(cloud, axis=0)
        p1 = np.array([min_x,min_y,-.2])
        p2 = np.array([max_x,min_y,-.2])
        p3 = np.array([max_x,max_y,-.2])
        p4 = np.array([min_x,max_y,-.2])
        area = (max_x-min_x)*(max_y-min_y)
        return {"p1" : p1,
                "p2" : p2,
                "p3" : p3,
                "p4" : p4},area
