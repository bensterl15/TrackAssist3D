from datetime import date


class Chain:
    def __init__(self, time, initial_label):
        self.starting_time = time
        self.last_time = time
        self.last_index = initial_label
        self.initial_label = initial_label
        self.unique_id = str(time) + ':' + str(date.today())[4:].replace('-', '') + ':' + str(initial_label)[:5]
        self.data = [initial_label]

    def append(self, protrusion_id, current_time):
        self.data.append(protrusion_id)
        self.last_index = protrusion_id
        self.last_time = current_time

    def print_contents(self):
        print('t0 = ' + str(self.starting_time))
        print(self.data)
        print('tend = ' + str(self.last_time))
