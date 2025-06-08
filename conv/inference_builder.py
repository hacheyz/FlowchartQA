from typing import List, Tuple


class InferenceBuilder:
    @staticmethod
    def build_nextok_inference(cur_state: str, next_state: str, next_states: List[str], reachable: bool) -> str:
        # Step 1: list all possible next states
        if next_states:
            next_states_str = ', '.join(next_states)
            step1 = f"Step 1: Find all possible next states from {cur_state}. " + \
                    f"The possible next states are {next_states_str}. "
        else:
            step1 = f"Step 1: Find all possible next states from {cur_state}. " + \
                    f"There are no possible next states. "
        # Step 2: check if the next state is among them
        if reachable:
            step2 = f"Step 2: Check if {next_state} is among them. " + \
                    f"Since {next_state} is in the list, the answer is yes."
        else:
            step2 = f"Step 2: Check if {next_state} is among them. " + \
                    f"Since {next_state} is NOT in the list, the answer is no."
        return '\n'.join([step1, step2])

    @staticmethod
    def build_allnext_inference(cur_state: str, next_states: List[str]) -> str:
        if next_states:
            next_states_str = ', '.join(next_states)
            step1 = f"Step 1: Find all outgoing edges from {cur_state}. " + \
                    f"The outgoing edges point to {next_states_str}. "

            explanations = []
            for state in next_states:
                explanations.append(f"- {cur_state} can transition to {state}.")
            step2 = "Step 2: Explain each outgoing edge:\n" + "\n".join(explanations) + " "

            step3 = f"Step 3: Summarize. " + \
                    f"The possible next states from {cur_state} are {next_states_str}."
        else:
            step1 = f"Step 1: Find all outgoing edges from {cur_state}. " + \
                    f"There are no outgoing edges. "
            step2 = f"Step 2: No edges to explain. "
            step3 = f"Step 3: Summarize. There are no possible next states from {cur_state}."

        return '\n'.join([step1, step2, step3])

    @staticmethod
    def build_allprev_inference(cur_state: str, prev_states: List[str]) -> str:
        if prev_states:
            prev_states_str = ', '.join(prev_states)
            step1 = f"Step 1: Find all incoming edges to {cur_state}. " + \
                    f"The incoming edges come from {prev_states_str}. "

            explanations = []
            for state in prev_states:
                explanations.append(f"- There is an edge from {state} to {cur_state}.")
            step2 = "Step 2: Explain each incoming edge:\n" + "\n".join(explanations) + " "

            step3 = f"Step 3: Summarize. " + \
                    f"The possible previous states leading to {cur_state} are {prev_states_str}."
        else:
            step1 = f"Step 1: Find all incoming edges to {cur_state}. " + \
                    f"There are no incoming edges. "
            step2 = f"Step 2: No edges to explain. "
            step3 = f"Step 3: Summarize. There are no possible previous states leading to {cur_state}."

        return '\n'.join([step1, step2, step3])

    @staticmethod
    def build_cond_inference(cur_state: str, value: str, branches: List[Tuple[str, str]]) -> str:
        """
        branches: List of (condition_value, next_state)
        """
        if branches:
            all_branches_str = ', '.join([f"{cond}->{state}" for cond, state in branches])
            step1 = f"Step 1: List all conditional branches from {cur_state}. " + \
                    f"The branches are: {all_branches_str}. "

            matched_states = [state for cond, state in branches if cond.lower() == value.lower()]
            if matched_states:
                matched_states_str = ', '.join(matched_states)
                step2 = f"Step 2: Identify branches where the condition is {value}. " + \
                        f"The matching branches lead to {matched_states_str}. "
                step3 = f"Step 3: Summarize. When the condition is {value}, " + \
                        f"the possible next states from {cur_state} are {matched_states_str}."
            else:
                step2 = f"Step 2: Identify branches where the condition is {value}. " + \
                        f"No branches match this condition. "
                step3 = f"Step 3: Summarize. When the condition is {value}, " + \
                        f"there are no next states from {cur_state}."
        else:
            step1 = f"Step 1: List all conditional branches from {cur_state}. " + \
                    f"There are no conditional branches. "
            step2 = f"Step 2: Identify branches where the condition is {value}. " + \
                    f"No branches exist. "
            step3 = f"Step 3: Summarize. No possible next states from {cur_state}."

        return '\n'.join([step1, step2, step3])

    @staticmethod
    def build_valid_reasoning(matrix, node_data, sequence: List[int]) -> str:
        sequence_str = '->'.join([node_data[node_id].name for node_id in sequence])

        step1 = f"Step 1: Check the transition between each pair of consecutive states in {sequence_str}. " + \
                f"The transitions are: "
        transitions = []
        for i in range(len(sequence) - 1):
            transitions.append(f"{node_data[sequence[i]].name} -> {node_data[sequence[i + 1]].name}")
        step1 += ', '.join(transitions) + "."

        step2 = f"Step 2: Verify if each transition is valid."
        if_valid = True
        invalid_transitions = []
        for i in range(len(sequence) - 1):
            if matrix[sequence[i]][sequence[i + 1]] != 0:
                step2 += f"\nThe transition from {node_data[sequence[i]].name} to {node_data[sequence[i + 1]].name} is valid."
            else:
                step2 += f"\nThe transition from {node_data[sequence[i]].name} to {node_data[sequence[i + 1]].name} is NOT valid."
                invalid_transitions.append(f"{node_data[sequence[i]].name} -> {node_data[sequence[i + 1]].name}")
                if_valid = False

        if if_valid:
            step3 = (f"Step 3: Final answer. "
                     f"Since all transitions are valid, the sequence {sequence_str} is valid.")
        else:
            step3 = (f"Step 3: Final answer. "
                     f"Since transitions {', '.join(invalid_transitions)} are NOT valid, "
                     f"the sequence {sequence_str} is NOT valid.")

        return '\n'.join([step1, step2, step3])
