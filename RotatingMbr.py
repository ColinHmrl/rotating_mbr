# MBR
import numpy as np
import math
import matplotlib.pyplot as plt



class RotatingMbr():
    """Find the minimum bounding rectangle of a point cloud

    Args:
        pointCloud (pointCloud): point cloud to search for mbr
        rotatingStep (int, optional): rotating step in degrees to find mbr. Defaults to 1.
    """
    def __init__(self,pointCloud,step=1):

        self.pointCloud = pointCloud
        self.bestMbrPoints,self.bestMbrArea = self.calculateMbr(pointCloud)
        self.bestMbrAngle = 0
        self.center = (self.bestMbrPoints[0] + self.bestMbrPoints[2]) / 2
        self.step = step
        self.calculateRotatingMbr(pointCloud)

    def __repr__(self):
        return f"bestMbrPoints : {self.bestMbrPoints} \n bestMbrArea : {self.bestMbrArea} \n bestMbrAngle : {self.bestMbrAngle}"


    def rotatePoint(self,origin, point, angle):
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
        
    def rotatePointCloud(self,cloud,angle,center):
        """
        Rotate Every point of the cloud around the center by an angle
        """
        origin = np.mean(cloud, axis=0)
        cloud_rotated = np.array([self.rotatePoint(center,point,angle) for point in cloud])
        return cloud_rotated     


    def calculateMbr(self,cloud):
        min_x,min_y,min_z = np.min(cloud, axis=0)
        max_x,max_y,max_z = np.max(cloud, axis=0)
        p1 = np.array([min_x,min_y,0])
        p2 = np.array([max_x,min_y,0])
        p3 = np.array([max_x,max_y,0])
        p4 = np.array([min_x,max_y,0])
        area = (max_x-min_x)*(max_y-min_y)
        return [p1,p2,p3,p4],area

    def calculateRotatingMbr(self,cloud):
        for angle in range(0,90,self.step):
            cloud_rotated = self.rotatePointCloud(cloud,angle,self.center)
            mbrPoints,mbrArea = self.calculateMbr(cloud_rotated)
            if mbrArea < self.bestMbrArea:
                self.bestMbrPoints = self.rotatePointCloud(mbrPoints,-angle,self.center)
                self.bestMbrArea = mbrArea
                self.bestMbrAngle = angle

    def show(self):
        # animate the mbr by plotting every step with a color gradient, from red to green where red is the worst mbr and green is the best mbr, best mbr is the lowest area
        # first we need to calculate the mbr for every angle
        points = []
        angles = []
        areas = []
        for angle in range(0,90,self.step):
            cloud_rotated = self.rotatePointCloud(self.pointCloud,angle,self.center)
            mbrPoints,mbrArea = self.calculateMbr(cloud_rotated)
            points.append(self.rotatePointCloud(mbrPoints,-angle,self.center))
            angles.append(angle)
            areas.append(mbrArea)
        
        # then we need to calculate the color gradient depend of the area on green to red scale
        colors = []
        for area in areas:
            color = (area-min(areas))/(max(areas)-min(areas))
            colors.append((color,1-color,0))

        #calculate min_x,min_y and max_x,max_y in points
        min_x,min_y,min_z = np.min(self.pointCloud, axis=0)
        max_x,max_y,max_z = np.max(self.pointCloud, axis=0)

        for point in points:
            for p in point:
                if p[0] < min_x:
                    min_x = p[0]
                if p[0] > max_x:
                    max_x = p[0]
                if p[1] < min_y:
                    min_y = p[1]
                if p[1] > max_y:
                    max_y = p[1]


        # then we need to plot the mbrs with the color gradient
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_title('Rotating MBR lowest to highest area')
        ax.set_xlim(min_x-.2,max_x+.2)
        ax.set_ylim(min_y-.2,max_y+.2)



        # sorting from the biggest area to the smallest area
        areas,points,colors = zip(*sorted(zip(areas,points,colors),reverse=True,key=lambda x: x[0]))

        #use rectangle shapes
        for i in range(len(points)):
            x = [p[0] for p in points[i]]
            y = [p[1] for p in points[i]]
            ax.add_patch(plt.Polygon(np.array([x,y]).T, closed=True, fill=False, edgecolor=colors[i], linewidth=2))

        
        x = [p[0] for p in self.pointCloud]
        y = [p[1] for p in self.pointCloud]

        ax.scatter(x,y,c='black',zorder=10)

        #plot the best
        x = [p[0] for p in self.bestMbrPoints]
        y = [p[1] for p in self.bestMbrPoints]
        ax.add_patch(plt.Polygon(np.array([x,y]).T, closed=True, fill=False, edgecolor='green', linewidth=2))


        legend_elements = [ plt.Line2D([0], [0], color=colors[0], lw=4, label='Worst MBR'),
                            plt.Line2D([0], [0], color='green', lw=4, label='Best MBR'),
                            plt.Line2D([0], [0], marker='o', color='w', label='Point Cloud',
                                    markerfacecolor='black', markersize=10)]

        ax.legend(handles=legend_elements, loc='upper right')



        plt.show()

        
