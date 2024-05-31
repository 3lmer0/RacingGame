class CollisionRect:
    def __init__(self, pos, w, h):
        '''
        Note: in order to find position from the image,
        dist from the top right corner of the image to the pixel where position is determined to be divided by a multiplier
        (in this case multiplier is 20)
        width and height are found similarly, in which their distances in pixels are divided by 20 in order to find the
        w and h values to be used for collision rectangles.
        '''
        self.position = pos #Center of the rectangle
        self.width = w
        self.height = h

    def overlap(self, other): #method is detecting if x and y are close enough and if both are close enough return true
        return (
            abs(self.position[0] - other.position[0]) <= self.width / 2 + other.width / 2 and
            
            abs(self.position[1] - other.position[1]) <= self.height / 2 + other.height / 2
        )


    def __str__(self):
        return "(" + str(self.position[0]) + ", " + str(self.position[1]) + "), " + str(self.width) + ", " + str(self.height)