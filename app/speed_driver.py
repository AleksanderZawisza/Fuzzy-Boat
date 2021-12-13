import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt


class BoatSpeedDriver:
    def __init__(self, mom=False):
        distance = ctrl.Antecedent(np.arange(0, 1001, 1), 'distance')
        angle = ctrl.Antecedent(np.arange(-180, 181, 1), 'angle')
        if mom:
            # mean of maximum czyli zawsze wartosci ze srodku najwiekszego wyniku ktory wychodzi,
            # mniej wartosci ale pewnie bardziej stabilne
            defuzzify_method = 'mom'
        else:  # wiecej wartosci
            defuzzify_method = 'centroid'

        speed = ctrl.Consequent(np.arange(0, 41, 1), 'speed', defuzzify_method=defuzzify_method)

        distance['very close'] = fuzz.trapmf(distance.universe, [0, 0, 20, 80])
        distance['close'] = fuzz.trimf(distance.universe, [20, 80, 200])
        distance['medium'] = fuzz.trimf(distance.universe, [80, 200, 400])
        distance['far'] = fuzz.trimf(distance.universe, [200, 400, 800])
        distance['very far'] = fuzz.trapmf(distance.universe, [400, 800, 1000, 1000])

        angle['strong left'] = fuzz.trapmf(angle.universe, [-180, -180, -70, -20])
        angle['left'] = fuzz.trimf(angle.universe, [-70, -20, 0])
        angle['keep'] = fuzz.trapmf(angle.universe, [-20, -5, 5, 20])
        angle['right'] = fuzz.trimf(angle.universe, [0, 20, 70])
        angle['strong right'] = fuzz.trapmf(angle.universe, [20, 70, 180, 180])

        speed['small'] = fuzz.trapmf(speed.universe, [0, 0, 3, 5])
        speed['medium'] = fuzz.trimf(speed.universe, [3, 5, 15])
        speed['high'] = fuzz.trimf(speed.universe, [5, 15, 20])
        speed['very high'] = fuzz.trapmf(speed.universe, [15, 20, 40, 40])

        rules = [ctrl.Rule(distance['very close'] & angle['strong left'], speed['small']),
                 ctrl.Rule(distance['close'] & angle['strong left'], speed['small']),
                 ctrl.Rule(distance['medium'] & angle['strong left'], speed['small']),
                 ctrl.Rule(distance['far'] & angle['strong left'], speed['small']),
                 ctrl.Rule(distance['very far'] & angle['strong left'], speed['medium']),

                 ctrl.Rule(distance['very close'] & angle['left'], speed['small']),
                 ctrl.Rule(distance['close'] & angle['left'], speed['small']),
                 ctrl.Rule(distance['medium'] & angle['left'], speed['medium']),
                 ctrl.Rule(distance['far'] & angle['left'], speed['medium']),
                 ctrl.Rule(distance['very far'] & angle['left'], speed['high']),

                 ctrl.Rule(distance['very close'] & angle['keep'], speed['small']),
                 ctrl.Rule(distance['close'] & angle['keep'], speed['medium']),
                 ctrl.Rule(distance['medium'] & angle['keep'], speed['high']),
                 ctrl.Rule(distance['far'] & angle['keep'], speed['very high']),
                 ctrl.Rule(distance['very far'] & angle['keep'], speed['very high']),

                 ctrl.Rule(distance['very close'] & angle['right'], speed['small']),
                 ctrl.Rule(distance['close'] & angle['right'], speed['small']),
                 ctrl.Rule(distance['medium'] & angle['right'], speed['medium']),
                 ctrl.Rule(distance['far'] & angle['right'], speed['medium']),
                 ctrl.Rule(distance['very far'] & angle['right'], speed['high']),

                 ctrl.Rule(distance['very close'] & angle['strong right'], speed['small']),
                 ctrl.Rule(distance['close'] & angle['strong right'], speed['small']),
                 ctrl.Rule(distance['medium'] & angle['strong right'], speed['small']),
                 ctrl.Rule(distance['far'] & angle['strong right'], speed['small']),
                 ctrl.Rule(distance['very far'] & angle['strong right'], speed['medium']),
                 ]

        self.distance = distance
        self.angle = angle
        self.speed = speed
        self.speed_ctrl = ctrl.ControlSystem(rules)

    def update_speed(self, distance, angle, visualization=False):
        steering = ctrl.ControlSystemSimulation(self.speed_ctrl)
        steering.input['distance'] = distance
        steering.input['angle'] = angle
        steering.compute()
        out = steering.output['speed']
        if visualization:
            self.distance.view(sim=steering)
            self.angle.view(sim=steering)
            self.speed.view(sim=steering)
            plt.show()
        return out


if __name__ == "__main__":
    driver = BoatSpeedDriver()
    distances = [0, 3, 15, 30, 50, 80, 400, 700, 1000, 1500, 800, 800]
    angles = [0, 10, -20, -160, -100, -120, 30, 50, -20, 40, 10, 20]
    for d, a in zip(distances, angles):
        print(d, a, driver.update_speed(d, a, False))
