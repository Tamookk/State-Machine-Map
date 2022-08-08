import copy
import random
import graphviz
import socket
import time


# State class, for storing state machine states
class State:
    def __init__(self, value):
        """
        Initialize state.
        :param value: value of the state.
        """
        self.value = value
        self.transitions = []
        self.transition_nums = []

    def add_transition(self, value, number):
        """
        Add a transition to this state.
        :param value: transition state.
        :param number: the number sent to the server to find this state.
        """
        # Return if we already have 3 transitions (only 3 transitions per
        # state).
        if self.get_number_transitions() >= 3:
            return
        # Return if we already have this transition
        elif number in self.transitions:
            return

        self.transitions.append(value)
        self.transition_nums.append(number)

    def get_transitions(self):
        """
        Return transitions from this state.
        :return: transitions list.
        """
        return self.transitions

    def get_transition_numbers(self):
        """
        Return transition numbers we have explored from this state.
        :return: transition_nums list.
        """
        return self.transition_nums

    def get_number_transitions(self):
        """
        Get the number of transitions this state has.
        :return: number of transitions.
        """
        return len(self.transitions)


# Main function
if __name__ == '__main__':
    start_time = round(time.time() * 1000)

    # Dictionary of states, and the steps to reach them from A
    states = {}

    # Dictionary of State objects
    state_objects = {}

    # Dictionary of states, and whether all 3 of their transitions
    # have been found.
    states_found = {}

    # List of states, and how many transitions we have found for them
    state_transition_count = {}

    # Host IP and port
    HOST = ''

    with open('settings.txt', 'r') as f:
        HOST = f.readline()
        f.close()

    PORT = 65432

    # Create graph object
    dot = graphviz.Digraph(comment="MEQ")

    # Initialize dictionaries
    for i in range(ord('A'), ord('Z') + 1):
        state_transition_count[chr(i)] = 0
        dot.node(chr(i))
        state_objects[chr(i)] = State(chr(i))
        states_found[chr(i)] = False

    # 0 move to reach state A - it is the starting point
    states['A'] = [0]

    # Create starting data variable
    data = 'A'

    # Connect to host
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        # Receive starting point
        data = s.recv(1024).decode('utf-8')[0]
        old_data = data

        # Current run of state transitions
        current_run_transitions = []

        # Set initial request value
        request = random.randint(1, 3)

        # Number of states we have "completed" (finished finding the
        # transitions for).
        num_completed = 0

        # Append initial request value to the list
        current_run_transitions.append(request)

        # Loop until we have finished searching the state machine
        while num_completed < 25:
            # Generate request number
            request = random.randint(1, 3)

            # If we haven't found all of the transitions from the previous
            # state, choose a request number that we haven't chosen yet.
            if state_transition_count[old_data] < 3:
                num_chosen = False
                while request \
                        in state_objects[old_data].get_transition_numbers():
                    request = random.randint(1, 3)

            # Append request number to the list
            current_run_transitions.append(request)

            # Send request to server and receive new state
            s.sendall(str.encode(str(request) + '\n'))
            data = s.recv(1024).decode('utf-8')[0]

            # Add transition to the state object
            state_objects[old_data].add_transition(data, request)

            # Update state transition count
            state_transition_count[old_data] = \
                state_objects[old_data].get_number_transitions()

            # If we have finished searching this state, mark it as `complete`
            if state_transition_count[old_data] == 3 \
                    and not states_found[old_data]:
                num_completed += 1
                print("Finished searching " + str(num_completed) + " states.")
                states_found[old_data] = True

            # Update previous state value
            old_data = data

            # If we haven't found a path to this state from A yet, add
            # it to the list.
            if data not in states.keys():
                states[data] = copy.deepcopy(current_run_transitions)

            # If state is Z
            if data == 'Z':
                # Grab A and update the old state
                data = s.recv(1024).decode('utf-8')[0]
                old_data = 'A'

                # Clear current run data
                current_run_transitions.clear()

                # If we have finished searching A, navigate directly
                # to the next state we have not finished searching.
                if state_transition_count['A'] == 3:
                    # Find the next state that we haven't completed searching,
                    # but know how to get to.
                    for state in state_transition_count.keys():
                        if 0 < state_transition_count[state] < 3:
                            value = state
                            break

                    # Navigate to that state
                    for transition in states[value]:
                        s.sendall(str.encode(str(transition) + '\n'))
                        data = s.recv(1024).decode('utf-8')[0]
                    old_data = data

        # Go through each state object and add its transitions to graphviz
        for state in state_objects.keys():
            for value in state_objects[state].get_transitions():
                dot.edge(state, value)

        # Render the graph output to a PDF
        dot.render('output')

        time_taken = (round(time.time() * 1000) - start_time) / 1000
        print("Took " + str(time_taken) + " seconds")
