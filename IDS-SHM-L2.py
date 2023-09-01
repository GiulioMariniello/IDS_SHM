# Title: Define IDS for Executive Design of SHM system using data form Preliminary Design
# Authors: Giulio Mariniello
# Affiliation: Department of Structures for Engineering and Architecture - University of Naples
# E-mail: giulio.mariniello@unina.it


import csv
import numpy as np
import xml.etree.ElementTree as ET

# Define the CSV file and function for searching for values
csv_coordination = r"C:\Users\Giulio\Downloads\Loin_coordination2.csv"

def search_vertical(values_to_search, file_name):
    found_results = []
    long_results = []
    with open(file_name, 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=';')
        for row in reader:
            if row[0].strip() in values_to_search:
                found_results.append(row[1])
            if len(row[0]) == 0:
                long_results.append(row[1])
    return found_results, long_results


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
Sensor_Properties, Others = search_vertical(header[2:-1], csv_coordination)


if len(header[2:-1]) != len(header[2:-1]):
    print(header[2:-1])
    print(Sensor_Properties)
    print(max_values)
    print('ERRORE!!!!')


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

    # Create the "ids:value" element with a restriction based on the sensor type
    value = ET.SubElement(property_, 'ids:value')
    restriction = ET.SubElement(value, 'xs:restriction', attrib={
        'base': 'xs:integer'
    })
    min_inclusive = ET.SubElement(restriction, 'xs:minInclusive', attrib={
        'value': str(max_values[i])
    })
    max_inclusive = ET.SubElement(restriction, 'xs:maxInclusive', attrib={
        'value': '10000'
    })

    # Increment the counter variable
    i += 1

# Create "ids:property" elements for Others
i = 0
for Sensor_Property in Others:
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

    # Create the "ids:value" element with a restriction based on the sensor type
    value = ET.SubElement(property_, 'ids:value')
    restriction = ET.SubElement(value, 'xs:restriction', attrib={
        'base': 'xs:integer'
    })
    min_inclusive = ET.SubElement(restriction, 'xs:minInclusive', attrib={
        'value': '0'
    })
    max_inclusive = ET.SubElement(restriction, 'xs:maxInclusive', attrib={
        'value': '1000000000'
    })

    # Increment the counter variable
    i += 1

# Write the XML tree to a file named "IDS.xml"
ET.ElementTree(ids).write('IDS3.xml')

