import mesa
import agents
from agents import Cars


class Model(mesa.Model):
    streets = [
        ((0, 10), (21, 10)),
        ((20, 11), (-1, 11)),
        ((10, 20), (10, -1)),
        ((11, 0), (11, 21)),
    ]

    def __init__(self, n_agents_per_iter=2, max_agents=9, road_list=streets, width=21, height=21):
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.schedule = mesa.time.RandomActivation(self)
        self.n_agents_per_iter = n_agents_per_iter
        self.iter = 0
        self.max_agents = max_agents
        self.contador = 0
        self.n_agents = 0
        self.vehicles = []
        self.lights = []
        self.contador_lights = 0
        self.datacollector = mesa.DataCollector(
            model_reporters={
                "Total moves": self.get_total_moves,
                "Total lights moves": self.get_lights,
                "Total cars": self.count_cars,

            },
            agent_reporters={
                "Cells cleaned": "cells_cleaned",
                "Moves": "moves",
            },
        )
        for x in range(width):
            for y in range(height):
                build = agents.Building(x, y)
                self.grid.place_agent(build, (x, y))
        for road in road_list:
            start, end = road
            calcX = end[0] - start[0]
            calcY = end[1] - start[1]
            goes = ''
            cond = None
            if not calcX == 0:
                if calcX > 0:
                    goes = 'R'
                    cond = 0
                else:
                    goes = 'L'
                    cond = 1
            elif not calcY == 0:
                if calcY > 0:
                    goes = 'U'
                    cond = 0
                else:
                    goes = 'D'
                    cond = 1
            x = start[0]
            y = start[1]
            while x != end[0]:
                cell = self.grid.get_cell_list_contents((x, y), True)
                if any(isinstance(elem, agents.Building) for elem in cell):
                    self.grid.remove_agent(cell[0])
                if any(isinstance(elem, agents.Street) for elem in cell):
                    cell[0].dir.append(goes)
                else:
                    r = agents.Street(0, self)
                    r.dir.append(goes)
                    self.grid.place_agent(r, (x, y))
                if cond == 0:
                    x += 1
                else:
                    x -= 1
            while y != end[1]:
                cell = self.grid.get_cell_list_contents((x, y), True)
                if any(isinstance(elem, agents.Building) for elem in cell):
                    self.grid.remove_agent(cell[0])
                if any(isinstance(elem, agents.Street) for elem in cell):
                    cell[0].dir.append(goes)
                else:
                    r = agents.Street(1, self)
                    r.dir.append(goes)
                    self.grid.place_agent(r, (x, y))
                if cond == 0:
                    y += 1
                else:
                    y -= 1
        self.traff = (9, 10)
        self.grid.get_cell_list_contents((11, 20), True)[0].dir[0] = 'L'
        self.grid.get_cell_list_contents((10, 0), True)[0].dir[0] = 'R'
        self.grid.get_cell_list_contents((19, 10), True)[0].dir[0] = 'U'
        self.grid.get_cell_list_contents((0, 11), True)[0].dir[0] = 'D'
        self.traffic_light = agents.Traffic_Light(0, self, self.traff, True)
        self.grid.place_agent(self.traffic_light, self.traff)
        self.traff2 = (10, 12)
        self.traffic_light2 = agents.Traffic_Light(1, self, self.traff2, False)
        self.grid.place_agent(self.traffic_light2, self.traff2)
        self.traffic_light.lights.append(self.traffic_light2)
        self.traffic_light2.lights.append(self.traffic_light)
        self.lights.append(self.traffic_light)
        self.lights.append(self.traffic_light2)
        self.running = True

    def rand_vehicles(self):
        pos = [(0, 10), (11, 0)]
        if self.iter == 5:
            for i in range(self.n_agents_per_iter):
                if self.n_agents == self.max_agents:
                    continue
                else:
                    cell = self.grid.get_cell_list_contents(pos[i], True)
                    if not any(isinstance(elem, agents.Cars) for elem in cell):
                        self.vehicle = agents.Cars(i, self, pos[i])
                        self.grid.place_agent(self.vehicle, pos[i])
                        self.vehicles.append(self.vehicle)
                        self.n_agents += 1
            self.iter = 0
        else:
            self.iter += 1

    def get_total_moves(self):
        return self.contador

    def get_lights(self):
        return self.contador_lights

    def step(self):
        self.rand_vehicles()
        ps = []
        self.contador = self.contador + 1

        for vehicle in self.vehicles:
            vehicle.move()
            xy = vehicle.pos
            p = [xy[0], xy[1], 0]
            ps.append(p)
        for light in self.lights:
            light.check()
            self.contador_lights += 1
        self.schedule.step()
        return ps

    def run_model(self, n):
        for i in range(n):
            self.step()

    def count_cars(self):
        # Cuenta el número de celdas boxe
        cars = 0
        for cell in self.grid.coord_iter():
            cell_content, x, y = cell
            if any(isinstance(agent, Cars) for agent in cell_content):
                cars += 1
        return cars
