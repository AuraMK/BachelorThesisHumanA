import cv2
import numpy as np
import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pylab as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import networkx as nx
from pathlib import Path


print("We will use the database 1, named HumanA_Exp1.") 
db_path = Path('/home/mafalda/Desktop/DataBases/HumanA_Exp1.db')

# connect to database
connection = sqlite3.connect(db_path)
cr = connection.cursor()

def get_nodes_and_coordinates_trial(n):
    sql_instruction = """
        SELECT dp.node, gc.nodeCentroid_x, gc.nodeCentroid_z
        FROM dataPoints_reduced dp
        JOIN graph_coordinates gc ON dp.node = gc.nodeNr
        WHERE dp.TrialId = """ + str(n) + """ AND dp.validDatapoint = 'VALID' AND dp.AdditionalInfo = 'FirstDPofNode'
        ORDER BY dp.timeStampDataPointStart ASC
        """
    cr.execute(sql_instruction)
    nodes_and_coordinates = cr.fetchall()
    nodes_coor = [nodes_and_coordinates[0]]
    for i in range(1, len(nodes_and_coordinates)):
        if nodes_and_coordinates[i] != nodes_and_coordinates[i - 1]:
            nodes_coor.append(nodes_and_coordinates[i])
    
    return nodes_coor

print("For which trial would you like to see the sequence of nodes?")
trial_number = int(input())

nodes_and_coordinates = get_nodes_and_coordinates_trial(trial_number)

nodes = []
coor_x = []
coor_y = []

for node, x, z in nodes_and_coordinates:
    nodes.append(node)
    coor_x.append(x)
    coor_y.append(z)

    #print("Node:", node, "Coordinates (x, z):", x, z)
#print(nodes)
#print(nodes_and_coordinates)


import matplotlib.pyplot as plt

def plot_coordinate_points(image, x_coords, y_coords):

    image = cv2.imread(image_path)
    img_height, img_width, _ = image.shape

    n = 5.1

    # Decrease the image size by n
    img_width /= n
    img_height /= n
    
    plt.figure(figsize=(14.5, 22)) 

    # Plot the points
    plt.imshow(image, extent=[0, img_width, 0, img_height])  # Set extent to match image dimensions
    plt.scatter(x_coords, y_coords, color='blue')
    plt.grid(True)
    
    # Add labels and title
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.title('Coordinate Points Plot')
    
    # Show the plot
    plt.grid(True)
    plt.show()


image_path = '/home/mafalda/A.png'
plot_coordinate_points(image_path, coor_x, coor_y)

print(nodes)