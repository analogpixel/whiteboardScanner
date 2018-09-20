#!/usr/bin/env python

# install
# pip install opencv-python
# pip install opencv-contrib-python
# pip install munch
# pip install Pillow
# brew install imagemagick
# brew install tesseract

# maybe? brew install opencv3 --with-contrib --with-python3

import numpy as np
import cv2
import cv2.aruco as aruco
import pprint
import munch
import datetime
import os

class markerDetection:
  def __init__(self, imageName):
    self.imageName = imageName
    self.detect()

  def sortPoints(self,corners, ids):  
      debug=False
      points = {'ul': 3, 'll': 2, 'lr': 1, 'ur': 0}

      xmin = 9000
      ymin = 9000
      xmax = 0
      ymax = 0
      for c in corners:
          for point in c[0]:
              if point[0] > xmax:
                  xmax = point[0]
              if point[0] < xmin:
                  xmin = point[0]
              if point[1] > ymax:
                  ymax = point[1]
              if point[1] < ymin:
                  ymin = point[1]

      if debug:
          print("xmax:", xmax)
          print("xmin:", xmin)
          print("ymax:", ymax)
          print("ymin:", ymin)

      xmid = (xmax+xmin) / 2
      ymid = (ymax+ymin) / 2
      ret = {}

      i=0
      for c in corners:
          p1_x = c[0][1][0]
          p1_y = c[0][1][1]

          if (p1_x <= xmid)  and (p1_x >= xmin) and (p1_y <= ymid) and (p1_y >= ymin):
              q = 'q1'
          if (p1_x <= xmax)  and (p1_x > xmid)  and (p1_y <= ymid) and (p1_y >= ymin):
              q = 'q2'
          if (p1_x <= xmid)  and (p1_x >= xmin) and (p1_y <= ymax)  and (p1_y > ymid):
              q = 'q3'
          if (p1_x <= xmax)  and (p1_x > xmid)  and (p1_y <= ymax)  and (p1_y > ymid):
              q = 'q4'

          ret[q]  = {'id': ids[i][0] }
          for p in points:
              ret[q][p] = [c[0][ points[p] ][0], c[0][ points[p] ][1]]

          i +=1
      return munch.Munch.fromDict(ret)

  def detect(self):
      os.system("/usr/local/bin/convert {} -auto-orient -strip {}".format(self.imageName, self.imageName))
      img = cv2.imread(self.imageName)
      height, width, channels = img.shape
      
      aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
      parameters =  aruco.DetectorParameters_create()
      corners, ids, rejectedImgPoints = aruco.detectMarkers(img, aruco_dict, parameters=parameters)

      if len(corners) != 4:
          print(corners)
          print("Not enough corners")
          import sys
          sys.exit()

      sp =  self.sortPoints( corners, ids) 


      pts1 = np.float32(  [sp.q1.lr, sp.q2.ll, sp.q3.ur, sp.q4.ul])
      pts2 = np.float32([[0,0],[width,0],[0,height],[width,height]])

      M = cv2.getPerspectiveTransform(pts1,pts2)
      dst = cv2.warpPerspective(img, M, (width,height) )

      self.exportFile = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"
      cv2.imwrite("cache/" + self.exportFile, dst)

if __name__ == "__main__":
   m = markerDetection("test.jpg")
   
