import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt


class BoatDriver:
    def __init__(self, mom=False):
        des_dir = ctrl.Antecedent(np.arange(-180, 181, 1), 'desired direction')
        turn = ctrl.Antecedent(np.arange(-50, 51, 1), 'turn')
        if mom:
            # mean of maximum czyli zawsze wartosci ze srodku najwiekszego wyniku ktory wychodzi,
            # mniej wartosci ale pewnie bardziej stabilne
            defuzzify_method = 'mom'
        else:  # wiecej wartosci
            defuzzify_method = 'centroid'
        rudd_chng = ctrl.Consequent(np.arange(-20, 21, 1), 'rudder change', defuzzify_method=defuzzify_method)

        des_dir['strong left'] = fuzz.trapmf(des_dir.universe, [-180, -180, -100, -45])
        des_dir['left'] = fuzz.trimf(des_dir.universe, [-100, -30, 0])
        des_dir['middle'] = fuzz.trapmf(des_dir.universe, [-30, -5, 5, 30])
        des_dir['right'] = fuzz.trimf(des_dir.universe, [0, 30, 100])
        des_dir['strong right'] = fuzz.trapmf(des_dir.universe, [45, 100, 180, 180])

        turn['left'] = fuzz.trapmf(turn.universe, [-50, -50, -20, 0])
        turn['neutral'] = fuzz.trimf(turn.universe, [-20, 0, 20])
        turn['right'] = fuzz.trapmf(turn.universe, [0, 20, 50, 50])

        rudd_chng['strong left'] = fuzz.trapmf(rudd_chng.universe, [-20, -20, -10, -5])
        rudd_chng['left'] = fuzz.trimf(rudd_chng.universe, [-10, -3, 0])
        rudd_chng['keep'] = fuzz.trimf(rudd_chng.universe, [-3, 0, 3])
        rudd_chng['right'] = fuzz.trimf(rudd_chng.universe, [0, 3, 10])
        rudd_chng['strong right'] = fuzz.trapmf(rudd_chng.universe, [5, 10, 20, 20])

        rules = [ctrl.Rule(des_dir['strong left'] & turn['left'], rudd_chng['left']),
                 ctrl.Rule(des_dir['left'] & turn['left'], rudd_chng['keep']),
                 ctrl.Rule(des_dir['middle'] & turn['left'], rudd_chng['right']),
                 ctrl.Rule(des_dir['right'] & turn['left'], rudd_chng['strong right']),
                 ctrl.Rule(des_dir['strong right'] & turn['left'], rudd_chng['strong right']),

                 ctrl.Rule(des_dir['strong left'] & turn['neutral'], rudd_chng['strong left']),
                 ctrl.Rule(des_dir['left'] & turn['neutral'], rudd_chng['left']),
                 ctrl.Rule(des_dir['middle'] & turn['neutral'], rudd_chng['keep']),
                 ctrl.Rule(des_dir['right'] & turn['neutral'], rudd_chng['right']),
                 ctrl.Rule(des_dir['strong right'] & turn['neutral'], rudd_chng['strong right']),

                 ctrl.Rule(des_dir['strong left'] & turn['right'], rudd_chng['strong left']),
                 ctrl.Rule(des_dir['left'] & turn['right'], rudd_chng['strong left']),
                 ctrl.Rule(des_dir['middle'] & turn['right'], rudd_chng['left']),
                 ctrl.Rule(des_dir['right'] & turn['right'], rudd_chng['keep']),
                 ctrl.Rule(des_dir['strong right'] & turn['right'], rudd_chng['right']),
                 ]

        self.des_dir = des_dir
        self.turn = turn
        self.rudd_chng = rudd_chng
        self.steering_ctrl = ctrl.ControlSystem(rules)

    def rudder_change(self, desired_direction, turn, visualization=False):
        steering = ctrl.ControlSystemSimulation(self.steering_ctrl)
        steering.input['desired direction'] = desired_direction
        steering.input['turn'] = turn
        steering.compute()
        out = steering.output['rudder change']
        if visualization:
            self.des_dir.view(sim=steering)
            self.turn.view(sim=steering)
            self.rudd_chng.view(sim=steering)
            plt.show()
        return out


if __name__ == "__main__":
    driver = BoatDriver()
    desired_direction = 5
    turn = -5
    out = driver.rudder_change(desired_direction, turn, True)
    print(out)
