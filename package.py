class Package:
    def __init__(self, id, address, city, state, zip, deadline, mass, notes):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.mass = mass
        self.notes = notes
        self.status = 'At Hub'
        self.deliverTime = None
        self.truck = None
        self.loadTime = None

    def __str__ (self):
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s" % (self.id, self.address, self.city,
                                                          self.state, self.zip, self.deadline,
                                                          self.mass, self.notes, self.status,
                                                          self.deliverTime, self.truck, self.loadTime)