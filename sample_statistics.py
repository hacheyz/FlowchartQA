from constant import *

class SampleStatistics:
    def __init__(self):
        self.nextok = {"yes": 0, "no": 0}
        self.allnext = [0 for _ in range(max_node_num)]
        self.prev = [0 for _ in range(max_node_num)]
        self.cond = 0
        self.valid = {"yes": 0, "no": 0}
        self.valid_len = [0 for _ in range(max_node_num)]

    def nextof_num(self):
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
        return (self.nextof_num() + self.allnext_num() + self.prev_num() +
                self.cond_num() + self.valid_num())
    
    def show_nextok(self):
        return (f"--- nextok ---"
              f"\nyes: {self.nextok['yes']}"
              f"\nno: {self.nextok['no']}"
              f"\nall: {self.nextof_num()}")
        
    def show_allnext(self):
        last_non_zero = 0
        for i in range(max_node_num):
            if self.allnext[i] != 0:
                last_non_zero = i
        return (f"--- allnext ---"
              f"\n{self.allnext[:last_non_zero + 1]}"
              f"\nall: {self.allnext_num()}")
        
    def show_prev(self):
        last_non_zero = 0
        for i in range(max_node_num):
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
        for i in range(max_node_num):
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