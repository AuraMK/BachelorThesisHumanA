from PIL import Image
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

# path to databases
print("To which Databases should the table of nodes and coordinates be added?")
experiment = int(input())
if experiment == 1:
    db_path = Path('/home/mafalda/Desktop/DataBases/HumanA_Exp1.db')

elif experiment == 2:
    db_path = Path('/home/mafalda/Desktop/DataBases/HumanA_Exp2.db')
elif experiment == 3:
    db_path = Path('/home/mafalda/Desktop/DataBases/Test_Data.db')

# connect to database
connection=sqlite3.connect(db_path)
cr=connection.cursor()


def get_coordinates():
    sql_instruction = """
        SELECT X_Coor, Z_Coor
        FROM graph_coordinates"""
    cr.execute(sql_instruction)
    # Fetch the result
    result = cr.fetchall()
    connection.close()
    return result
    

image_path = '/home/mafalda/A.png'
coordinates = get_coordinates()

def visualize_nodes(image_path, node_coordinates):
    # Read the image
    image = Image.open(image_path)
    img_height, img_width = image.size

    n = 5

    # Decrease the image size by n
    img_width /= n
    img_height /= n

    x = [row[0] for row in node_coordinates]
    y = [row[1] for row in node_coordinates]

    plt.imshow(image, extent=[0, img_width, 0, img_height])  # Set extent to match image dimensions
    plt.scatter(x, y, color='red', s=10)  # Scatter points on top of the image
    plt.title('Overlaying SQL Data on Image')
    plt.grid(True)
    #plt.gca().invert_yaxis()
    # Show the plot
    plt.show()


# Example usage
visualize_nodes(image_path, coordinates)

# Close the connection
