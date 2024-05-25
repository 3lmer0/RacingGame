class CollisionRect:
    def __init__(self, pos, w, h):
        self.position = pos
        self.width = w
        self.height = h

    def overlap(self, other):
        return (
            abs(self.position[0] - other.position[0]) <= self.width / 2 + other.width / 2 and
            
            abs(self.position[1] - other.position[1]) <= self.height / 2 + other.height / 2
        )


    def __str__(self):
        return "(" + str(self.position[0]) + ", " + str(self.position[1]) + "), " + str(self.width) + ", " + str(self.height)