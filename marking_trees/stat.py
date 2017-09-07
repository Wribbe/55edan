#!/usr/bin/env python3
import numpy
import sys
import json
import math

import matplotlib.pyplot as plt

if __name__ == "__main__":
  args = sys.argv[1:]
  filemames = args
  data = {}
  for filename in filemames:
    data.update(json.load(open(filename)))


  x_to_plot = []
  y_to_plot = []
  
  table_list = []

  for N in sorted(data, key=int):
#    x_to_plot.append(int(N))
    print("Current N: {}".format(N))
    key_values = []
    for key in ["R1","R2","R3"]:
      data_dict = data[N]
      iterations = data_dict[key]
      
      # Calculate mean.
      mean = numpy.mean(iterations)

      std = numpy.std(iterations)
      std_div_n = numpy.divide(std, int(N))
      print("Mean for {} = {:.2f}, std = {:.2f}, std/N = {}".format(key, mean, std, std_div_n))

      # Try this one? --> n/4 * log ( n/4 ) + (n/4)*gamma.
      key_values.append((mean, std))
      
      if key == "R1":

        Npart = (1.0/4.0)*int(N)

        #theoretical_distrb = Npart*math.log(Npart, 2)
        gamma = 0.5772156649
        theoretical_distrb = Npart * (math.log(Npart) + gamma) + 1/2 + 1/Npart

        y_to_plot.append(mean)
        x_to_plot.append(theoretical_distrb)
        print("Theoretical distribution for R1? -- {}".format(theoretical_distrb))
        print("theo / mean = {}".format(theoretical_distrb / mean))
        print("mean / N = {}".format(mean/int(N)))
    print("")
    table_list.append((N, key_values))
  for N, data_list in table_list:
    output_line = ["{:<7}: ".format(N)]
    for index, (mean, std) in enumerate(data_list, start=1):
      output_line.append("R{}: {:.2E} +/- {:.2E} | ".format(index, mean, std))
    print(' '.join(output_line))
      



#  x_to_plot = [math.log(x, 2) for x in x_to_plot]
#  y_to_plot = [math.log(y, 2) for y in y_to_plot]
#  plt.plot(x_to_plot, y_to_plot)
#  plt.x_axis = "N"
#  plt.show()
