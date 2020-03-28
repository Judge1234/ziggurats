LARGE_ZIG = 5
SMALL_ZIG = 3


class Layout:
    def __init__(self, width, height, layout, p1_spawn_locations, p2_spawn_locations):
        self.width = width
        self.height = height
        self.layout = layout                            # List of lists 
        self.p1_spawn_locations = p1_spawn_locations    # List of lists
        self.p2_spawn_locations = p2_spawn_locations    # List of lists


Small_Standard_Layout = Layout(13, 17, [["D6", LARGE_ZIG]],
                                       [["king", "A6", "P1"],
                                        ["king", "A7", "P1"], 
                                        ["king", "A8", "P1"], 
                                        ["king", "A9", "P1"],
                                        ["king", "A10", "P1"]],
                                       [["king", "K6", "P2"],
                                        ["king", "K7", "P2"],
                                        ["king", "K8", "P2"],
                                        ["king", "K9", "P2"],
                                        ["king", "K10", "P2"]])


