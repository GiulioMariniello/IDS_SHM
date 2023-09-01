# Title: Define IDS for Preliminary Design of SHM system using data form LOIN definitions
# Authors: Giulio Mariniello
# Affiliation: Department of Structures for Engineering and Architecture - University of Naples
# E-mail: giulio.mariniello@unina.it


import csv
import numpy as np
import xml.etree.ElementTree as ET

# Define the CSV file and function for searching for values
csv_coordination = r"C:\Users\Giulio\Downloads\Loin_coordination_v4.csv"

def Loin_Preliminary(file_name):
    found_results = []
    r = 0
    with open(file_name, 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=';', dialect='excel')
        for row in reader:
            if r > 0:
                if row[0] != '':
                    found_results.append(row[0])
            r += 1
    return found_results


# Read the CSV file
with open('results.csv', newline='') as f:
    reader = csv.reader(f)
    rows = list(reader)

# Extract the header
header = rows[0]

# Create a list containing all rows except the first (the header)
data = rows[1:]
numbers = np.array([x[2:] for x in data])
array = np.array(numbers).astype(int)
max_values = np.amax(array, axis=0)

# Create a matrix that reads the first-level properties and puts the second-level ones
Sensor_Properties = Loin_Preliminary(csv_coordination)
print(Sensor_Properties)



import xml.etree.ElementTree as ET

# Create the root element of the IDS
ids = ET.Element('ids:ids', attrib={
    'xmlns:ids': 'http://standards.buildingsmart.org/IDS',
    'xmlns:xs': 'http://www.w3.org/2001/XMLSchema',
    'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
    'xsi:schemaLocation': 'http://standards.buildingsmart.org/IDS  ids_09.xsd'
})

# Create the info element with the title, copyright, and date
info = ET.SubElement(ids, 'ids:info')
title = ET.SubElement(info, 'ids:title')
title.text = 'Preliminary Design - SHM - IDS'
copyright = ET.SubElement(info, 'ids:copyright')
copyright.text = 'University of Naples'
date = ET.SubElement(info, 'ids:date')
date.text = '2023-03-17'

# Create the specifications element
specifications = ET.SubElement(ids, 'ids:specifications')

# Create the specification element with the entity "IFCSENSOR"
specification = ET.SubElement(specifications, 'ids:specification', attrib={
    'ifcVersion': 'IFC4',
    'name': 'Sensors_Specification',
    'minOccurs': '1'
})
applicability = ET.SubElement(specification, 'ids:applicability')
entity = ET.SubElement(applicability, 'ids:entity')
name = ET.SubElement(entity, 'ids:name')
simple_value = ET.SubElement(name, 'ids:simpleValue')
simple_value.text = 'IFCSENSOR'

# Create the "ids:requirements" element with the "Accuracy_min" property
requirements = ET.SubElement(specification, 'ids:requirements')

# Create "ids:property" elements for Sensor_Properties
i = 0
for Sensor_Property in Sensor_Properties:
    # Create the "ids:property" element with the required attributes
    property_ = ET.SubElement(requirements, 'ids:property', attrib={
        'minOccurs': '1',
        'measure': 'IfcText'
    })

    # Create the "ids:propertySet" element and set its value
    property_set = ET.SubElement(property_, 'ids:propertySet')
    simple_value = ET.SubElement(property_set, 'ids:simpleValue')
    simple_value.text = 'Pset_Sensor_Requirements'

    # Create the "ids:name" element and set its value
    name = ET.SubElement(property_, 'ids:name')
    simple_value = ET.SubElement(name, 'ids:simpleValue')
    simple_value.text = Sensor_Property



# Write the XML tree to a file named "IDS.xml"
ET.ElementTree(ids).write('IDS - Preliminary Design_v2.xml')

