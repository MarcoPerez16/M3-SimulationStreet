import random
import mesa


class Street(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.dir = []


class Building(mesa.Agent):
    def __init__(self, x, y):
        super().__init__(x, y)


class Traffic_Light(mesa.Agent):
    def __init__(self, u_id, model, pos, horiz=True):
        super().__init__(u_id, model)
        self.pos = pos
        self.horiz = horiz
        self.lights = []
        self.current_cycle = 1
        self.counter = 0

    def status(self):
        if self.lights[0].current_cycle == 0:
            self.current_cycle = 1
        else:
            self.current_cycle = 0

    def check(self):
        self.status()
        dirRoad = self.model.grid.get_cell_list_contents(
            (self.pos[0], self.pos[1]), True)[0].dir
        if 'D' in dirRoad:
            self.x = 0
            self.y = 1
        elif 'U' in dirRoad:
            self.x = 0
            self.y = -1
        elif 'R' in dirRoad:
            self.x = -1
            self.y = 0
        elif 'L' in dirRoad:
            self.x = 1
            self.y = 0
        vehicle_cell = self.model.grid.get_cell_list_contents(
            (self.pos[0] + self.x, self.pos[1] + self.y), True)
        if self.counter == 3:
            self.current_cycle = 0
            self.counter = 0
            self.lights[0].current_cycle = 1
        for vehicle in vehicle_cell:
            if type(vehicle) == Cars:
                if self.current_cycle == 1:
                    vehicle.canMove = True
                else:
                    vehicle.canMove = False
                self.counter = 0
            else:
                self.counter += 1


class Cars(mesa.Agent):
    def __init__(self, u_id, model, pos):
        super().__init__(u_id, model)
        self.original_pos = pos
        self.pos = self.original_pos
        self.x = self.pos[0]
        self.y = self.pos[1]
        self.canMove = True
        self.contador = 0

    def step(self):
        self.move()

    def move(self):
        cell = self.model.grid.get_cell_list_contents(
            (self.x, self.y), True)[0].dir
        self.contador = self.contador + 1
        if len(cell) > 1 and self.canMove:
            pick = cell[random.randint(0, len(cell)-1)]
            if pick == 'R':
                self.x += 1
            elif pick == 'L':
                self.x -= 1
            elif pick == 'D':
                self.y -= 1
            elif pick == 'U':
                self.y += 1
            if self.canMove:
                self.model.grid.move_agent(self, (self.x, self.y))
        else:
            self.checkFront()

    def checkFront(self):
        cell = self.model.grid.get_cell_list_contents(
            (self.x, self.y), True)[0].dir

        if 'R' in cell and self.canMove:
            if self.model.grid.out_of_bounds((self.x + 1, self.y)):
                self.x = self.original_pos[0]
                self.y = self.original_pos[1]
                self.model.grid.move_agent(self, (self.x, self.y))
                return
            if not (any(isinstance(x, Cars) for x in self.model.grid.get_cell_list_contents((self.x + 1, self.y), True))):
                self.x += 1

        elif 'D' in cell and self.canMove:
            if self.model.grid.out_of_bounds((self.x + 1, self.y)):
                self.x = self.original_pos[0]
                self.y = self.original_pos[1]
                self.model.grid.move_agent(self, (self.x, self.y))
                return
            if not (any(isinstance(x, Cars) for x in self.model.grid.get_cell_list_contents((self.x, self.y - 1), True))):
                self.y -= 1

        elif 'L' in cell and self.canMove:
            if self.model.grid.out_of_bounds((self.x + 1, self.y)):
                self.x = self.original_pos[0]
                self.y = self.original_pos[1]
                self.model.grid.move_agent(self, (self.x, self.y))
                return
            if not (any(isinstance(x, Cars) for x in self.model.grid.get_cell_list_contents((self.x - 1, self.y), True))):
                self.x -= 1

        elif 'U' in cell and self.canMove:
            if self.model.grid.out_of_bounds((self.x + 1, self.y)):
                self.x = self.original_pos[0]
                self.y = self.original_pos[1]
                self.model.grid.move_agent(self, (self.x, self.y))
                return
            if not (any(isinstance(x, Cars) for x in self.model.grid.get_cell_list_contents((self.x, self.y + 1), True))):
                self.y += 1

        if self.canMove:
            self.model.grid.move_agent(self, (self.x, self.y))
