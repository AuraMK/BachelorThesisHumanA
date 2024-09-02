from pathlib import Path
import sqlite3
import numpy as np
from numpy import sqrt
import math

# path to database
print("We will use the database 1, named HumanA_Exp1.") 
db_path = Path('/home/mafalda/Desktop/DataBases/HumanA_Exp1.db')

# connect to database
connection = sqlite3.connect(db_path)
cr = connection.cursor()

def get_nodes_and_coordinates():
    sql_instruction = """
        SELECT dp.TrialId, dp.node, gc.nodeCentroid_x, gc.nodeCentroid_z
        FROM dataPoints_reduced dp
        JOIN graph_coordinates gc ON dp.node = gc.nodeNr
        WHERE dp.validDatapoint = 'VALID' AND dp.AdditionalInfo = 'FirstDPofNode'
            AND dp.TrialId IN (SELECT DISTINCT TrialId FROM dataPoints_reduced ORDER BY TrialId LIMIT 2)
        ORDER BY dp.TrialId, dp.timeStampDataPointStart ASC
        """
    cr.execute(sql_instruction)
    nodes_and_coordinates = cr.fetchall()
    nodes_coor = [nodes_and_coordinates[0]]
    for i in range(1, len(nodes_and_coordinates)):
        if nodes_and_coordinates[i] != nodes_and_coordinates[i - 1]:
            nodes_coor.append(nodes_and_coordinates[i])
    
    return nodes_coor

nodes_and_coordinates = get_nodes_and_coordinates()

nodes = []
coor_x = []
coor_y = []

print(nodes_and_coordinates)