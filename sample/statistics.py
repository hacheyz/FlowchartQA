from constant import MAX_NODE_NUM, NEXTOK_TYPE, ALLNEXT_TYPE, ALLPREV_TYPE, COND_TYPE, VALID_TYPE
from sample.sample import Sample


class SampleStatistics:
    def __init__(self):
        self.nextok = {"yes": 0, "no": 0}
        self.allnext = [0 for _ in range(MAX_NODE_NUM)]
        self.prev = [0 for _ in range(MAX_NODE_NUM)]
        self.cond = 0
        self.valid = {"yes": 0, "no": 0}
        self.valid_len = [0 for _ in range(MAX_NODE_NUM)]

    def add_sample(self, sample: Sample):
        if sample.question_type == NEXTOK_TYPE:
            if sample.ground_truth[0] == "yes":
                self.nextok["yes"] += 1
            else:
                self.nextok["no"] += 1
        elif sample.question_type == ALLNEXT_TYPE:
            self.allnext[len(sample.ground_truth)] += 1
        elif sample.question_type == ALLPREV_TYPE:
            self.prev[len(sample.ground_truth)] += 1
        elif sample.question_type == COND_TYPE:
            self.cond += 1
        elif sample.question_type == VALID_TYPE:
            if sample.ground_truth[0] == "yes":
                self.valid["yes"] += 1
            else:
                self.valid["no"] += 1
            self.valid_len[sample.sequence_len] += 1
        else:
            raise ValueError(f"Unknown sample type: {sample.question_type}")

    def nextok_num(self):
        return sum(self.nextok.values())

    def allnext_num(self):
        return sum(self.allnext)

    def prev_num(self):
        return sum(self.prev)

    def cond_num(self):
        return self.cond

    def valid_num(self):
        return sum(self.valid.values())

    def all_num(self):
        return (self.nextok_num() + self.allnext_num() + self.prev_num() +
                self.cond_num() + self.valid_num())

    def show_nextok(self):
        return (f"--- nextok ---"
                f"\nyes: {self.nextok['yes']}"
                f"\nno: {self.nextok['no']}"
                f"\nall: {self.nextok_num()}")

    def show_allnext(self):
        last_non_zero = 0
        for i in range(MAX_NODE_NUM):
            if self.allnext[i] != 0:
                last_non_zero = i
        return (f"--- allnext ---"
                f"\n{self.allnext[:last_non_zero + 1]}"
                f"\nall: {self.allnext_num()}")

    def show_prev(self):
        last_non_zero = 0
        for i in range(MAX_NODE_NUM):
            if self.prev[i] != 0:
                last_non_zero = i
        return (f"--- prev ---"
                f"\n{self.prev[:last_non_zero + 1]}"
                f"\nall: {self.prev_num()}")

    def show_cond(self):
        return (f"--- cond ---"
                f"\nall: {self.cond_num()}")

    def show_valid(self):
        last_non_zero = 0
        for i in range(MAX_NODE_NUM):
            if self.valid_len[i] != 0:
                last_non_zero = i
        return (f"--- valid ---"
                f"\n{self.valid_len[:last_non_zero + 1]}"
                f"\nyes: {self.valid['yes']}"
                f"\nno: {self.valid['no']}"
                f"\nall: {self.valid_num()}")

    def show_all(self):
        return ("\n".join([self.show_nextok(),
                           self.show_allnext(),
                           self.show_prev(),
                           self.show_cond(),
                           self.show_valid()])
                + f"\n--- all ---\n{self.all_num()}")

    def save(self, file):
        with open(file, "w") as f:
            f.write(self.show_all())
        f.close()
