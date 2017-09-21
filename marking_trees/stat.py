#!/usr/bin/env python3
import numpy
import sys
import json
import math

import matplotlib.pyplot as plt

def H(n):
  n = int(n)
  value = 0
  for k in range(1,n+1):
    value += 1.0/k
  return value

if __name__ == "__main__":
  args = sys.argv[1:]
  filemames = args
  data = {}
  for filename in filemames:
    data.update(json.load(open(filename)))



  plot_data = {}
  key_plot_x = 'x'
  key_plot_y = 'y'
  key_plot_y_theoretical = 'y_theo'

  table_list = []

  def theoretical(key, N):
    if key == "R1":
      Npart = (1.0/4.0)*int(N)
      return 2 * Npart * H(Npart)
    elif key == "R2":
      return int(N)
    elif key == "R3":
      return (1.0/2.0)*int(N)


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

      theoretical_distrb = theoretical(key, N)
      key_values.append((mean, std, theoretical_distrb))

      data_dict = plot_data.get(key)
      if not data_dict:
        data_dict = plot_data[key] = {
              key_plot_x: [],
              key_plot_y: [],
              key_plot_y_theoretical: [],
            }

      data_dict[key_plot_y].append(mean)
      data_dict[key_plot_y_theoretical].append(theoretical_distrb)
      data_dict[key_plot_x].append(int(N))

      if key == "R1":

        print("Theoretical distribution for R1? -- {}".format(theoretical_distrb))
        print("theo / mean = {}".format(theoretical_distrb / mean))
        print("mean / N = {}".format(mean/int(N)))
    print("")
    table_list.append((N, key_values))

  for N, data_list in table_list:
    # LaTeX format.
    output_line = [N, '&']
    for mean, std, _ in data_list:
        output_line.append("{:.2e}".format(mean))
        if std:
            output_line.append("$\\pm$ {:.2e}".format(std))
        output_line.append('&')
    output_line.append("{:.2e}".format(data_list[0][-1]))
    output_line.append('&')
    output_line.append('\\\\')
    print(' '.join(output_line))
#    output_line = ["{:<7}: ".format(N)]
#    for index, (mean, std) in enumerate(data_list, start=1):
#      output_line.append("R{}: {:.2E} +/- {:.2E} | ".format(index, mean, std))
#    print(' '.join(output_line))


  def plot_theo(plt, x_to_plot, y_theoretical, **kwargs):
    y_theoretical = [0 if y==0 else math.log(y) for y in y_theoretical]
    plt.plot(x_to_plot, y_theoretical, **kwargs)

  for algo_name, plot_data in plot_data.items():

    x_to_plot = plot_data[key_plot_x]
    y_to_plot = plot_data[key_plot_y]

    x_to_plot = [math.log(x) for x in x_to_plot]
    y_to_plot = [math.log(y) for y in y_to_plot]

    plt.plot(x_to_plot, y_to_plot, marker='o', label="Experimental")
    plt.suptitle("Values for algorithm {}".format(algo_name))
    plt.xlabel('log(N)')
    plt.ylabel('log(mean(iterations))')

    y_theoretical = plot_data[key_plot_y_theoretical]

    if algo_name == "R1":
      theo_label = "Theoretical (2 * 1/4 * n * H(n))"
      plot_theo(plt, x_to_plot, y_theoretical, marker='x', label=theo_label)
    elif algo_name == "R2":
      theo_label = "Theoretical (n)"
      plot_theo(plt, x_to_plot, y_theoretical, marker='x', label=theo_label)
      y_theoretical = [0.5*n for n in y_theoretical]
      theo_label = "Theoretical (1/2 * n)"
      plot_theo(plt, x_to_plot, y_theoretical, marker='x', label=theo_label)
    elif algo_name == "R3":
      theo_label = "Theoretical (1/2 * n)"
      plot_theo(plt, x_to_plot, y_theoretical, marker='x', label=theo_label)

    plt.legend()
    #plt.show()
    plt.savefig('values_{}.pdf'.format(algo_name))
    plt.clf()
