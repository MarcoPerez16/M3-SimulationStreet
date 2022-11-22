from agents import Building, Traffic_Light, Street, Cars
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from model import Model
import Skins
import mesa


def agent_portrayal(agent):
    portrayal = {}
    if type(agent) is Building:
        portrayal = {
            "Shape": "Skins/Pasto.jpg",
            "Color": "blue",
            "Filled": "true",
            "Layer": 0,
            "w": 1,
            "h": 1,
        }
    if type(agent) is Traffic_Light:
        if agent.horiz == True:
            w, h = .25, .5
            color = 'green'
        else:
            w, h = .5, .25
            color = 'red'
        if agent.current_cycle == 1:
            color = 'green'
        else:
            color = 'red'
        portrayal = {
            "Shape": "rect",
            "Color": color,
            "Filled": "true",
            "Layer": 3,
            "w": w,
            "h": h,
        }
    if type(agent) is Street:
        portrayal = {
            "Shape": "rect",
            "Color": 'gray',
            "Filled": "true",
            "Layer": 1,
            "w": 1,
            "h": 1,
        }
    if type(agent) is Cars:
        portrayal = {
            "Shape": "circle",
            "Color": 'purple',
            "Filled": "true",
            "Layer": 2,
            "r": 0.5
        }
    return portrayal


chart = mesa.visualization.ChartModule(
    [{"Label": "Total moves", "Color": "Black"}],
    data_collector_name="datacollector",
    canvas_height=60,
    canvas_width=80,
)

chart2 = mesa.visualization.ChartModule(
    [{"Label": "Total lights moves", "Color": "Green"}],
    data_collector_name="datacollector",
    canvas_height=60,
    canvas_width=80,
)
chart3 = mesa.visualization.ChartModule(
    [{"Label": "Total cars", "Color": "Red"}],
    data_collector_name="datacollector",
    canvas_height=60,
    canvas_width=80,
)


rs, cs = 20, 20
cs += 1
rs += 1

grid = CanvasGrid(agent_portrayal, rs, cs, 600, 600)
server = mesa.visualization.ModularServer(Model, [grid, chart, chart2, chart3], "M3. Actividad",
                                          {
    'n_agents_per_iter': 2,
    'width': rs,
    'height': cs
}
)
server.port = 6996
server.launch()
