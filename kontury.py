# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 21:04:09 2020

@author: HP
"""

import cv2
import numpy as np

#Wykrycie konturów na obrazie
def detect_edges(image):
    image_HSV=cv2.cvtColor(image,cv2.COLOR_BGR2HSV) #Zamiana obrazu na HSV(TEN SAM KOLOR MIMO ODCIENIU)
    lower_blue = np.array([20, 40, 40]) #Dolna granica koloru na skali HUE
    upper_blue = np.array([40, 255, 255])#Gorna granica koloru(to jest pierwszy parametr, reszta bez zmian!!)
    mask = cv2.inRange(image_HSV, lower_blue, upper_blue)#Zostawiam tylko kolory o okreslonych granicach
    edges = cv2.Canny(mask, 200, 400)#Funkcja znajduje kontury(Parametry zostaja bez zmian!!!)
    return edges

#Wymazanie czesci obrazu ktory nas nie interesuje
def erased_area(image):
    height, width=image.shape#Wymiary obrazu
    mask=np.zeros_like(edges)#Tablica zer wielkosci obrazu
    polygon = np.array([[(0, height * 1 / 2), 
                         (width, height * 1 / 2),
                         (width, height), 
                         (0, height),]], np.int32)#Funkcja okresla obszar wymazywania(np.1/2)
    cv2.fillPoly(mask, polygon, 255)#Dopasowanie obszaru zer do wymiaru
    cropped_edges = cv2.bitwise_and(edges, mask)#Wymazanie obszaru ktory nas nie interesuje
    return cropped_edges

#Wykrywa fragmenty lini 
def detect_line_segments(image):
    rho=1 #Dystans od poczatku dla transformacji Hough'a
    angle=np.pi/180 #precyzja kata w radianach
    min_threshold=10 #minimal number of votes to consider as a line
    segments=cv2.HoughLinesP(image, rho, angle, min_threshold,
                             np.array([]),  minLineLength=8, maxLineGap=4)
    return segments
    
def make_points(image, line):
    height, width, _ = image.shape
    slope, intercept = line
    y1 = height  # bottom of the frame
    y2 = int(y1 * 1 / 2)  # make points from middle of the frame down

    # bound the coordinates within the frame
    x1 = max(-width, min(2 * width, int((y1 - intercept) / slope)))
    x2 = max(-width, min(2 * width, int((y2 - intercept) / slope)))
    return [[x1, y1, x2, y2]]


def creating_two_lanes(image, segments):
    """
    This function combines line segments into one or two lane lines
    If all line slopes are < 0: then we only have detected left lane
    If all line slopes are > 0: then we only have detected right lane
    """
    lane_lines = []
    if segments is None:
        print('No line_segment segments detected')
        return lane_lines
    
    height, width, _ = image.shape
    left_fit = []
    right_fit = []
    #Regions of lines
    boundary = 1/3 #Dziele ekran na czesci w ktorych powinny byc linie
    left_region_boundary = width * (1 - boundary)  # left lane line segment should be on left 2/3 of the screen
    right_region_boundary = width * boundary # right lane line segment should be on left 2/3 of the screen

    for line_segment in segments:
        for x1, y1, x2, y2 in line_segment:
            if x1 == x2:
               #print('skipping vertical line segment (slope=inf): %s' % line_segment)
                continue
            fit = np.polyfit((x1, x2), (y1, y2), 1)
            slope = fit[0]
            intercept = fit[1]
            if slope < 0:
                if x1 < left_region_boundary and x2 < left_region_boundary:
                    left_fit.append((slope, intercept))
            else:
                if x1 > right_region_boundary and x2 > right_region_boundary:
                    right_fit.append((slope, intercept))

    left_fit_average = np.average(left_fit, axis=0)
    if len(left_fit) > 0:
        lane_lines.append(make_points(image, left_fit_average))

    right_fit_average = np.average(right_fit, axis=0)
    if len(right_fit) > 0:
        lane_lines.append(make_points(image, right_fit_average))

    print('land lines: %s' % lane_lines) #Wypisuje wspolrzedne linii

    return lane_lines

def display_lines(image, lines, line_color=(0, 255, 0), line_width=4):
    line_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(line_image, (x1, y1), (x2, y2), line_color, line_width)
    line_image = cv2.addWeighted(image, 0.8, line_image, 1, 1)
    return line_image


def Position_control(image, lines):
    height, width, _ = image.shape
    _, _, left_line, _ = lines[0][0]
    _, _, right_line, _ = lines[1][0]
    center_start=(int((left_line+right_line)/2), int(height-height/10))
    center_end=(int((left_line+right_line)/2), int(2*height/3))
    center=(int(width/2), int(4*height/5))
    text_coordinates=(int(width-width/8), int(height-height/10))
    
    image = cv2.arrowedLine(image, center_start, center_end, (0, 255, 0), 5)
    image=cv2.circle(image, center, 15, (255, 0, 0), 4)
    
    offset=center[0]-center_start[0] #Dodatni offset->skret w lewo
    
    if offset>0:
        cv2.putText(image,'Lewo '+ str(offset) , text_coordinates, cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 3)
    else:
        cv2.putText(image,'Prawo '+ str(offset) , text_coordinates, cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 3)

    return image


image=cv2.imread('Kontur_test1.jpg')# Wczytuje obraz

edges=detect_edges(image)#Zaznaczam kontury
edges=erased_area(edges)
segments=detect_line_segments(edges)
land_lanes=creating_two_lanes(image, segments)

ready_image = display_lines(image, land_lanes)
ready_image=Position_control(ready_image, land_lanes)


cv2.imshow('IMAGE', ready_image)
cv2.waitKey(0)
cv2.destroyAllWindows()



