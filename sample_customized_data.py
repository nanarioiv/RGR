
'''sample_customized_data.py'''

import random
from gavrptw.core import run_gavrptw
from plot_generate import plot_routes
def main():
    '''main()'''
    random.seed(64)

    instance_name = 'Customized_Data'

    unit_cost = 3.3
    init_cost = 3000.0
    wait_cost = 5.5
    delay_cost = 5.5

    ind_size = 38
    pop_size = 500
    cx_pb = 0.85
    mut_pb = 0.1
    n_gen = 300

    export_csv = True
    customize_data = True

    run_gavrptw(instance_name=instance_name, unit_cost=unit_cost, init_cost=init_cost, \
        wait_cost=wait_cost, delay_cost=delay_cost, ind_size=ind_size, pop_size=pop_size, \
        cx_pb=cx_pb, mut_pb=mut_pb, n_gen=n_gen, export_csv=export_csv, \
        customize_data=customize_data)


if __name__ == '__main__':
    main()
