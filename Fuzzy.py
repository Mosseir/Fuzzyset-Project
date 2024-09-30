import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
import sys
import io

# Setting stdout to encoding with utf-8 (for TH language)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Define input parameter
temperature = ctrl.Antecedent(np.arange(0, 41, 1), 'temperature')
humidity = ctrl.Antecedent(np.arange(0, 101, 1), 'humidity')

# Define output parameter
curtain = ctrl.Consequent(np.arange(0, 101, 1), 'curtain')

# Define fuzzy sets for input and output
temperature['cold'] = fuzz.trimf(temperature.universe, [0, 0, 20])
temperature['moderate'] = fuzz.trimf(temperature.universe, [15, 25, 35])
temperature['hot'] = fuzz.trimf(temperature.universe, [30, 40, 40])

humidity['low'] = fuzz.trimf(humidity.universe, [0, 0, 50])
humidity['medium'] = fuzz.trimf(humidity.universe, [30, 50, 70])
humidity['high'] = fuzz.trimf(humidity.universe, [60, 100, 100])

curtain['open'] = fuzz.trimf(curtain.universe, [0, 0, 50])
curtain['partial'] = fuzz.trimf(curtain.universe, [30, 50, 70])
curtain['closed'] = fuzz.trimf(curtain.universe, [60, 100, 100])

# Rules
rule1 = ctrl.Rule(temperature['cold'] & humidity['high'], curtain['closed'])
rule2 = ctrl.Rule(temperature['moderate'] & humidity['medium'], curtain['partial'])
rule3 = ctrl.Rule(temperature['hot'] & humidity['low'], curtain['open'])

# Create control system
curtain_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
curtain_simulation = ctrl.ControlSystemSimulation(curtain_ctrl)

# Read file from input (.txt)
def read_simulation_data(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            #Skip the comment line
            if line.startswith("#") or not line.strip():
                continue
            temp, hum = map(float, line.split(','))
            data.append((temp, hum))
    return data

# Import data from input file
file_path = 'input_data.txt'
input_data = read_simulation_data(file_path)

# Looping for run the simulation
for idx, (temp, hum) in enumerate(input_data, 1):
    curtain_simulation.input['temperature'] = temp
    curtain_simulation.input['humidity'] = hum
    curtain_simulation.compute()
    if 'curtain' in curtain_simulation.output:
        print(f"กรณีที่ {idx}: อุณหภูมิ {temp}°C, ความชื้นสัมพัทธ์ {hum}% -> เปอร์เซ็นต์การเปิดม่าน: {curtain_simulation.output['curtain']:.2f}%")
    else:
        print(f"กรณีที่ {idx}: ระบบไม่สามารถคำนวณค่าได้")



# Showing graph fuzzy for input and output
# Member function of Temperature
temperature.view()

# Member function
humidity.view()

# Member function of output (Curtain)
curtain.view()

plt.show()
