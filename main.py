from hash import ChainingHashTable
from package import Package
import csv

def loadPackageData(filename) :
    with open(filename) as packages:
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

            package = Package(pId, pAddress, pCity, pState, pZip, pDeadline, pMass, pNotes)

            pHash.insert(pId, package)

pHash = ChainingHashTable()

loadPackageData('WGUPS Package File.csv')

print(pHash.search('1'))