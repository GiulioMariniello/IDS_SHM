# Title: Read property from preliminary SHM design ifc model
# Authors: Giulio Mariniello
# Affiliation: Department of Structures for Engineering and Architecture - University of Naples
# E-mail: giulio.mariniello@unina.it


import ifcopenshell
import csv

# Set the path to the IFC file
file_path = r"C:\Users\Giulio\Downloads\Modello Revit4.3.ifc"

# Open the IFC file
ifc_file = ifcopenshell.open(file_path)

# Define the object class name and the property set name to search for
class_name = 'IfcSensor'
pset_name = 'Pset_Sensor_Requirements'

# Create an empty list for the results
results = []

# Find all instances of the specified object class
for instance in ifc_file.by_type(class_name):
    # Find the desired property set for this instance
    pset = None
    for property_set in instance.IsDefinedBy:
        if property_set.is_a('IfcRelDefinesByProperties'):
            relating_object = property_set.RelatingPropertyDefinition
            if relating_object.is_a('IfcPropertySet') and relating_object.Name == pset_name:
                pset = relating_object
                break

    if pset:
        # Extract the values of the desired properties
        property_values = {}
        for property in pset.HasProperties:
            property_name = property.Name
            property_value = property.NominalValue.wrappedValue
            property_values[property_name] = property_value

        # Add the results to the list
        results.append({'Element': instance.Name, 'Pset': pset_name, 'Properties': property_values})

# Save the results to a CSV file
with open('results.csv', 'w', newline='') as csvfile:
    if len(results) > 0:
        fieldnames = ['Element', 'Pset'] + list(results[0]['Properties'].keys())
    else:
        fieldnames = ['Element', 'Pset']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for result in results:
        row = {'Element': result['Element'], 'Pset': result['Pset']}
        row.update(result['Properties'])
        writer.writerow(row)
