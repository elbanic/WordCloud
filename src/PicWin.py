import os
import random as rd
from tkinter import font

import numpy as np

from src import Globals

imagePath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")

#from PIL import Image, ImageTk
import tkinter as tk


class PicWin(tk.Canvas):

    def __init__(self, master):
        super().__init__(master, bg="light grey", width=500, height=320) #bg="white"
        filename = os.path.join(imagePath, "wclogo2.gif")
        #if os.path.exists(filename):
            #file_out = self.resizeLogo(filename)
            #self.logo = tk.PhotoImage(file= os.path.abspath(imagePath) + '/' + file_out)
            #self.create_image(int(self.winfo_reqwidth()/2), int(self.winfo_reqheight()/2), anchor='center', image=self.logo)

#    def resizeLogo(self, filename):
#        sizeW = int(self.winfo_reqwidth() / 2)
#        sizeH = int(self.winfo_reqheight() / 2)
#        orglogo = Image.open(filename)
#        resized = orglogo.resize((int(sizeW), int(sizeH)), Image.ANTIALIAS)
#        transparency = resized.info['transparency']
#        file_out = '_resized.gif'
#        resized.save(os.path.abspath(imagePath) + '/' + file_out, "GIF", transparency=transparency)
#        print ("File saved as %s" %file_out)
#        return file_out

    def drawWordCloud(self, dict):
        self.delete("all")
        dictSorted = sorted(dict.items(), key=lambda x: x[1], reverse=True)        # dictionary sorted by key
        wordCount = len(dictSorted)
        if wordCount <= 0:
            return

        colorSet = set(Globals.Colors)
        colorId = rd.sample(colorSet, len(Globals.Colors) - 1)
        if len(colorId) < wordCount:
            for i in range(0, wordCount-len(colorId)):
                colorId.append(colorId[i])

        maxCount = dictSorted[0][1]
        sizeW, sizeH = int(self.winfo_reqwidth() / 2), int(self.winfo_reqheight() / 2)
        drawnArea = []
        posX, posY = 0, 0
        fSize = 0
        unit = 0
        for i in range(0, wordCount):
            if dictSorted[i][0] == "," or dictSorted[i][0] == "." or dictSorted[i][0] == "(" or dictSorted[i][0] == ")"\
                or dictSorted[i][0] == ":" or dictSorted[i][0] == ";" or dictSorted[i][0] == "[" or dictSorted[i][0] == "]":
               continue
            drawnCnt = len(drawnArea)
            if drawnCnt <= 0:
                charCount = len(str(dictSorted[i][0]))
                sizePerChar = sizeW / charCount
                fSize = -sizePerChar
                unit = -fSize / dictSorted[i][1]
            else:
                fSize += unit
            if fSize > -10:
                fSize = -10

            nextRect = []
            if drawnCnt <= 0:
                fontinfo = font.Font(family = "Times", size=int(fSize), underline=True)
            else:
                fontinfo = font.Font(family = "Times", size=int(fSize))
            w, h = fontinfo.measure(dictSorted[i][0].upper()), fontinfo.metrics("linespace")
            posX, posY = np.random.randint(self.winfo_reqwidth()-w), np.random.randint(self.winfo_reqheight()-h)
            while True:
                isinside = False
                if drawnCnt > 0:
                    for k in range(0, drawnCnt):
                        nextRect = [posX, posY, posX+w, posY+h]
                        if self.isOverlappedArea(drawnArea[k], nextRect) == True:
                            isinside = True
                            break
                if isinside == False:
                    break
                fontinfo = font.Font(family = "Times", size=int(fSize))
                w, h = fontinfo.measure(dictSorted[i][0].upper()), fontinfo.metrics("linespace")
                posX, posY = np.random.randint(self.winfo_reqwidth()-w), np.random.randint(self.winfo_reqheight()-h)
                fSize += 1
                if fSize > -10:
                    fSize = -10

            if len(nextRect) > 0:
                self.gravitatePosition(drawnArea, nextRect)
                posX, posY = nextRect[0], nextRect[1]
            self.create_text(posX, posY, font=fontinfo, fill=colorId[i], text=str(dictSorted[i][0]).upper(), anchor=tk.NW)
            #self.create_rectangle(posX, posY, posX + w, posY + h, outline=colorId[i])
            rect = [posX, posY, posX+w, posY+h]
            drawnArea.append(rect)

    def isOverlappedArea(self, rect1, rect2):
        xOverlap = self.isInsideRange(rect1[0], rect2[0], rect2[2]) or self.isInsideRange(rect2[0], rect1[0], rect1[2])
        yOverlap = self.isInsideRange(rect1[1], rect2[1], rect2[3]) or self.isInsideRange(rect2[1], rect1[1], rect1[3])
        return xOverlap and yOverlap

    def isInsideRange(self, var, min, max):
        return var >= min and var <= max

    def gravitatePosition(self, rectArray, nextRect):
        if len(rectArray) <= 0:
            return
        baseRect = rectArray[0]
        centerX = (baseRect[2]+baseRect[0])/2
        centerY = (baseRect[3]+baseRect[1])/2
        if nextRect[3] < centerY:
            self.downFall(rectArray, nextRect, centerY)
        else:
            self.upStair(rectArray, nextRect, centerY)

    def downFall(self, rectArray, nextRect, centerY):
        baseRect = rectArray[0]
        nh = nextRect[3]-nextRect[1]
        rectLower = []
        for i in range(0, len(rectArray)):
            if rectArray[i][1] <= centerY:
                rectLower.append(rectArray[i])

        changed = False
        if len(rectLower) > 0:
            lowerSort = sorted(rectLower, key=lambda x: x[3], reverse=False)
            for i in range(0, len(lowerSort)):
                if (nextRect[0] > lowerSort[i][0] and nextRect[0] <lowerSort[i][2])or(nextRect[2] > lowerSort[i][0] and nextRect[2] < lowerSort[i][2]):
                    nextRect[1] = lowerSort[i][1]-nh
                    nextRect[3] = lowerSort[i][1]
                    changed = True
                    break
                if (lowerSort[i][0] > nextRect[0] and lowerSort[i][0] < nextRect[2])or(lowerSort[i][2] > nextRect[0] and lowerSort[i][2] < nextRect[2]):
                    nextRect[1] = lowerSort[i][1]-nh
                    nextRect[3] = lowerSort[i][1]
                    changed = True
                    break
        if changed == False:
            if (nextRect[0] > baseRect[0] and nextRect[0] < baseRect[2])or(nextRect[2] > baseRect[0] and nextRect[2] < baseRect[2]):
                nextRect[1] = baseRect[1]-nh
                nextRect[3] = baseRect[1]
            else:
                nextRect[1] = centerY-nh
                nextRect[3] = centerY

    def upStair(self, rectArray, nextRect, centerY):
        baseRect = rectArray[0]
        nh = nextRect[3]-nextRect[1]
        rectUpper = []
        for i in range(0, len(rectArray)):
            if rectArray[i][3] > centerY:
                rectUpper.append(rectArray[i])

        changed = False
        if len(rectUpper) > 0:
            upperSort = sorted(rectUpper, key=lambda x: x[1], reverse=True)
            for i in range(0, len(upperSort)):
                if (nextRect[0] > upperSort[i][0] and nextRect[0] < upperSort[i][2])or(nextRect[2] > upperSort[i][0] and nextRect[2] < upperSort[i][2]):
                    nextRect[1] = upperSort[i][3]
                    nextRect[3] = upperSort[i][3]+nh
                    changed = True
                    break
                if (upperSort[i][0] > nextRect[0] and upperSort[i][0] < nextRect[2])or(upperSort[i][2] > nextRect[0] and upperSort[i][2] < nextRect[2]):
                    nextRect[1] = upperSort[i][3]
                    nextRect[3] = upperSort[i][3]+nh
                    changed = True
                    break
        if changed == False:
            if (nextRect[0] > baseRect[0] and nextRect[0] < baseRect[2])or(nextRect[2] > baseRect[0] and nextRect[2] < baseRect[2]):
                nextRect[1] = baseRect[3]
                nextRect[3] = baseRect[3]+nh
            else:
                nextRect[1] = centerY
                nextRect[3] = centerY+nh


    def stickLeft(self, rectArray, nextRect, centerX):
        baseRect = rectArray[0]
        nw = nextRect[2]-nextRect[0]
        leftRects = []
        for i in range(0, len(rectArray)):
            if rectArray[i][2] < centerX:
                leftRects.append(rectArray[i])

        changed = False
        if len(leftRects) > 0:
            leftSorted = sorted(leftRects, key=lambda x: x[2], reverse=False)
            for i in range(0, len(leftSorted)):
                if (nextRect[1] >= leftSorted[i][1] and nextRect[1] <= leftSorted[i][3])or(nextRect[3] >= leftSorted[i][1] and nextRect[3] <= leftSorted[i][3]):
                    nextRect[0] = leftSorted[i][0]-nw
                    nextRect[2] = leftSorted[i][0]
                    changed = True
                    break
                if (leftSorted[i][1] >= nextRect[1] and leftSorted[i][1] <= nextRect[3])or(leftSorted[i][3] >= nextRect[1] and leftSorted[i][3] <= nextRect[3]):
                    nextRect[0] = leftSorted[i][0]-nw
                    nextRect[2] = leftSorted[i][0]
                    changed = True
                    break
        if changed == False:
            if (nextRect[1] > baseRect[1] and nextRect[1] < baseRect[3])or(nextRect[3] > baseRect[1] and nextRect[3] < baseRect[3]):
                nextRect[0] = baseRect[0]-nw
                nextRect[2] = baseRect[0]
            else:
                nextRect[1] = centerX-nw
                nextRect[3] = centerX

    def stickRight(self, rectArray, nextRect, centerX):
        baseRect = rectArray[0]
        nw = nextRect[2]-nextRect[0]
        rightRects = []
        for i in range(0, len(rectArray)):
            if rectArray[i][1] > centerX:
                rightRects.append(rectArray[i])

        changed = False
        if len(rightRects) > 0:
            rightSorted = sorted(rightRects, key=lambda x: x[1], reverse=True)
            for i in range(0, len(rightSorted)):
                if (nextRect[1] >= rightSorted[i][1] and nextRect[1] <= rightSorted[i][3])or(nextRect[3] >= rightSorted[i][1] and nextRect[3] <= rightSorted[i][3]):
                    nextRect[0] = rightSorted[i][2]
                    nextRect[2] = rightSorted[i][2]+nw
                    changed = True
                    break
                if (rightSorted[i][1] >= nextRect[1] and rightSorted[i][1] <= nextRect[3])or(rightSorted[i][3] >= nextRect[1] and rightSorted[i][3] <= nextRect[3]):
                    nextRect[0] = rightSorted[i][2]
                    nextRect[2] = rightSorted[i][2]+nw
                    changed = True
                    break
        if changed == False:
            if (nextRect[1] > baseRect[1] and nextRect[1] < baseRect[3])or(nextRect[3] > baseRect[1] and nextRect[3] < baseRect[3]):
                nextRect[0] = baseRect[2]
                nextRect[2] = baseRect[2]+nw
            else:
                nextRect[1] = centerX
                nextRect[3] = centerX+nw

    def customizePolygon(self, polygon):
        nMaxX, nMaxY = 0, 0
        for i in polygon:
            if i[0] > nMaxX:
                nMaxX = i[0]
            if i[1] > nMaxY:
                nMaxY = i[1]

        nMinX, nMinY = nMaxX, nMaxY
        for i in polygon:
            if i[0] < nMinX:
                nMinX = i[0]
            if i[1] < nMinY:
                nMinY = i[1]

        nMaxX -= nMinX
        nMaxY -= nMinY
        xRatio, yRatio = self.winfo_reqwidth() / nMaxX, self.winfo_reqheight() / nMaxY
        customPolygon = []
        for i in polygon:
            point = [(i[0] - nMinX) * xRatio, (i[1] - nMinY) * yRatio]
            customPolygon.append(point)

        return customPolygon




