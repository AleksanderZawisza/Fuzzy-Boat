import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
# import matplotlib.pyplot as plt

def fuzzy_driver():
    des_dir = ctrl.Antecedent(np.arange(-180, 181, 1), 'desired direction')
    turn = ctrl.Antecedent(np.arange(-50, 51, 1), 'turn')
    rudd_chng = ctrl.Consequent(np.arange(-20, 21, 1), 'rudder change', defuzzify_method='centroid')

    des_dir['strong left'] = fuzz.trapmf(des_dir.universe, [-180, -180, -100, -45])
    des_dir['left'] = fuzz.trimf(des_dir.universe, [-100, -45, 0])
    des_dir['middle'] = fuzz.trapmf(des_dir.universe, [-45, -15, 15, 45])
    des_dir['right'] = fuzz.trimf(des_dir.universe, [0, 45, 100])
    des_dir['strong right'] = fuzz.trapmf(des_dir.universe, [45, 100, 180, 180])

    turn['left'] = fuzz.trapmf(turn.universe, [-50, -50, -20, 0])
    turn['neutral'] = fuzz.trimf(turn.universe, [-20, 0, 20])
    turn['right'] = fuzz.trapmf(turn.universe, [0, 20, 50, 50])

    rudd_chng['strong left'] = fuzz.trapmf(rudd_chng.universe, [-20, -20, -10, -5])
    rudd_chng['left'] = fuzz.trimf(rudd_chng.universe, [-10, -5, 0])
    rudd_chng['keep'] = fuzz.trapmf(rudd_chng.universe, [-5, -2, 2, 5])
    rudd_chng['right'] = fuzz.trimf(rudd_chng.universe, [0, 5, 10])
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

    steering_ctrl = ctrl.ControlSystem(rules)
    return steering_ctrl

def rudder_change(steering_ctrl, desired_direction, turn):
    steering = ctrl.ControlSystemSimulation(steering_ctrl)
    steering.input['desired direction'] = desired_direction
    steering.input['turn'] = turn
    steering.compute()
    out = steering.output['rudder change']

    # des_dir.view(sim=steering)
    # plt.show()
    #
    # turn.view(sim=steering)
    # plt.show()
    #
    # rudd_chng.view(sim=steering)
    # plt.show()
    return out

if __name__ == "__main__":
    desired_direction = 50
    turn = -5
    steering_ctrl = fuzzy_driver()
    out = rudder_change(steering_ctrl, desired_direction, turn)
    print(out)





