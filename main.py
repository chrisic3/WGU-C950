# Chris Stelly 000650837

from hash import ChainingHashTable
from package import Package
from datetime import datetime, timedelta
import csv


# FUNCTIONS
# Takes the package file and inserts each package into the hash table
def loadPackageData(hashTable, fileName):
    with open(fileName) as packages:
        packageData = csv.reader(packages, delimiter=',')
        for package in packageData:
            pId = int(package[0])
            pAddress = package[1]
            pCity = package[2]
            pState = package[3]
            pZip = package[4]
            pDeadline = package[5]
            pMass = package[6]
            pNotes = package[7]

            #change address for package 9
            if pId == 9:
                pAddress = '410 S State St'
                pZip = '84111'

            # Create package object
            package = Package(pId, pAddress, pCity, pState, pZip, pDeadline,
                              pMass, pNotes)

            # Insert package object into hash table
            hashTable.insert(pId, package)

# Takes the distance file and appends each row into the distance array
def loadDistanceData(list, fileName):
    with open(fileName) as distances:
        distanceData = csv.reader(distances, delimiter=',')
        for row in distanceData:
            list.append(row)

# Takes the address file and loads it into the address dictionary
def loadAddressData(dict, fileName):
    index = 0
    with open(fileName) as addresses:
        addressData = csv.reader(addresses, delimiter=',')
        for row in addressData:
            dict[row[0]] = index
            index += 1

# Used to determine the position in the distance array for the distance between two addresses
def addressDistance(addr1, addr2):
    row = addressData[addr1]
    col = addressData[addr2]
    return distanceData[row][col]

# This is the main delivery algorithm based on Nearest Neighbor
def deliver(truckList, truckNumber, loadTime, distanceTraveled):
    truckTime = loadTime
    truckLocation = list(addressData.keys())[0]

    # Load truck and initialize remaining package fields
    for i in truckList:
        package = packageData.search(i) #O(n)
        package.truck = truckNumber
        package.status = 'On Truck'
        package.loadTime = loadTime

    # Loop through the truckList until it it empty
    while len(truckList) > 0:
        # Reset the minPackage and minDistance
        minPackage = None
        minDistance = 500
        # Compare the distance of the current package of the current truckList to the minDistance
        for i in truckList:
            currentPackage = packageData.search(i)
            currentDistance = float(
                addressDistance(truckLocation, currentPackage.address))
            # Make the current package the minimum if it is
            if currentDistance < minDistance:
                minDistance = currentDistance
                minPackage = currentPackage

        # This section calculates the current time after delivery and updates various package fields
        currentTime = (minDistance / 18) * 60
        truckTime += timedelta(minutes=currentTime)
        minPackage.deliverTime = truckTime
        minPackage.status = 'Delivered'
        truckLocation = minPackage.address
        truckList.pop(truckList.index(minPackage.id))
        distanceTraveled += minDistance
    return distanceTraveled, truckTime


# HASH TABLE AND LIST INSTANTIATION AND DATA LOADING
packageData = ChainingHashTable()
distanceData = []
addressData = {}

# Load data structures
loadPackageData(packageData, 'packages.csv')
loadDistanceData(distanceData, 'distances.csv')
loadAddressData(addressData, 'addresses.csv')

# LOAD TRUCKS
truck1 = [13, 14, 15, 16, 19, 20, 23, 24, 26, 27, 33, 34, 35, 37, 39, 40] # 16
truck2 = [1, 3, 17, 18, 21, 22, 29, 30, 31, 36, 38] # 11
truck3 = [2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 25, 28, 32] # 13

startTime = datetime(1900, 1, 1, 8, 00)
distanceTraveled = 0

# Run delivery for each truck. The start time for truck 3 is the finish time for truck 1.
distanceTraveled, truck1FinishTime = deliver(truck1, 1, startTime, distanceTraveled)
distanceTraveled, truck2FinishTime = deliver(truck2, 2, startTime, distanceTraveled)
distanceTraveled, truck3FinishTime = deliver(truck3, 3, truck1FinishTime, distanceTraveled)

# INTERFACE
# Get user selection for mode
choice = input("Press 1 to list all packages, 2 to list a single package, or 3 to print the total distance travled:\n")
# Display all packages
if choice == '1':
    time_string = input("Please input a time to check (format H:M:S):\n")
    # Convert the string time to datetime
    time = datetime.strptime(time_string, "%H:%M:%S").time()
    
    # Print the formatted header line
    print("| {:<14} | {:<12} | {:<9} | {:<8} | {:<14} | {:<38} | {:<16} | {:<5} | {:<5} | {:<10}".format(
        "Package Number", "Truck Number", "Load Time", "Deadline", "Delivered Time", "Address", 
        "City", "Zip", "Weight", "Status"))

    # Loop through all packages and print details
    for i in range(0, 40): # I prefer to start ranges at 0
        status = ''
        package = packageData.search(i + 1) # Adding 1 to i to match the package id because I started the range at 0
        if package.loadTime.time() > time:
            status = "At the hub"
        elif package.deliverTime.time() <= time:
            status = "Delivered"
        else:
            status = "On truck"

        # Print the formatted package details
        print("| {:<14} | {:<12} | {:<9} | {:<8} | {:<14} | {:<38} | {:<16} | {:<5} | {:<6} | {:<10}".format(
            package.id, package.truck, package.loadTime.strftime("%H:%M:%S"),
            package.deadline, package.deliverTime.strftime("%H:%M:%S"), 
            package.address, package.city, package.zip, package.mass, status))

# Display single package
elif choice == '2':
    time_string = input("Please input a time to check (format H:M:S):\n")
    # Convert the string time to datetime
    time = datetime.strptime(time_string, "%H:%M:%S").time()
    # Get and convert the wanted package id
    id = int(input("Please input the package id:\n"))

    # Print the formatted header line
    print("| {:<14} | {:<12} | {:<9} | {:<8} | {:<14} | {:<38} | {:<16} | {:<5} | {:<5} | {:<10}".format(
        "Package Number", "Truck Number", "Load Time", "Deadline", "Delivered Time", "Address", 
        "City", "Zip", "Weight", "Status"))
    
    status = ''
    package = packageData.search(id)
    if package.loadTime.time() > time:
        status = "At the hub"
    elif package.deliverTime.time() <= time:
        status = "Delivered"
    else:
        status = "On truck"

    # Print the formatted package details
    print("| {:<14} | {:<12} | {:<9} | {:<8} | {:<14} | {:<38} | {:<16} | {:<5} | {:<6} | {:<10}".format(
        package.id, package.truck, package.loadTime.strftime("%H:%M:%S"),
        package.deadline, package.deliverTime.strftime("%H:%M:%S"), 
        package.address, package.city, package.zip, package.mass, status))

# Print total distance traveled
elif choice == '3':
    print("\nTotal distance traveled: " + str(distanceTraveled))
else:
    print("Invalid choice.\n")
