import graphviz

class Digraph:
    def __init__(self, n):
        self.__num_vertex = n
        self.__adjacent = {_ : [] for _ in range(n)}

    def add_edge(self, start, end):
        self.__adjacent[start].append(end)
    
    def adj(self, v):
        return self.__adjacent[v]

    def num_vertex(self):
        return self.__num_vertex
    
    def reverse(self):
        dg = Digraph(self.__num_vertex)
        for v in range(self.__num_vertex):
            for w in self.adj(v):
                dg.add_edge(w, v)
        return dg


class FiniteAutomata:
    def __init__(self, reg):
        self.reg = self.__reg_preprocess(reg)
        self.g = self.__build_graph(self.reg)
        self.rg = self.g.reverse()

    def __reg_preprocess(self, reg):
        exp = []
        current_ptr = 0
        while current_ptr < len(reg):
            if reg[current_ptr] in ['(', ')', '|', '?']:
                exp.append(reg[current_ptr])
                current_ptr += 1
            else:
                forward_ptr = current_ptr + 1
                if reg[current_ptr] != ' ':
                    while forward_ptr < len(reg) and \
                            reg[forward_ptr] not in ['(', ')', '|', '?', ' ']:
                        forward_ptr += 1
                    exp.append(reg[current_ptr:forward_ptr])
                current_ptr = forward_ptr
        print(exp)
        return exp

    def __build_graph(self, reg):
        g = Digraph(len(reg) + 1)
        stack = []
        ors = []
        cached = None
        for i, c in enumerate(reg):
            if c == '(':
                stack.append(i)
                g.add_edge(i, i + 1)
            elif c == ')':
                assert len(stack) != 0, 'parentheses does not match'
                cached = stack.pop(-1)
                g.add_edge(i, i + 1)
            elif c == '?':
                prev = cached if cached is not None else i - 1
                g.add_edge(i, i + 1)
                g.add_edge(i + 1, prev)
            elif c == '|':
                prev = cached if cached is not None else i - 1
                # g.add_edge(i, i + 1)
                g.add_edge(prev, i + 1)
                ors.append(i)
            else:
                cached = None
                while len(ors) != 0:
                    o = ors.pop(-1)
                    if reg[i - 1] == '|':
                        g.add_edge(o, i + 1)
                    else:
                        g.add_edge(o, i)
        while len(ors) != 0:
            o = ors.pop(-1)
            g.add_edge(o, g.num_vertex() - 1)
        return g

    def __transition(self, v):
        table = {}
        queue = [v]
        marked = set()
        ops_tokens = ['(', ')', '|', '?']
        while len(queue) != 0:
            w = queue.pop(0)
            if w not in marked:
                if w > 0:
                    token = self.reg[w - 1]
                    if token not in ops_tokens:
                        table[w - 1] = token
                queue.extend(self.rg.adj(w))
                marked.add(w)
        return table

    def transitions(self):
        tables = {}
        for v in range(self.g.num_vertex()):
            tables[v] = self.__transition(v)
        return tables
    
    def visualize(self):
        f = graphviz.Digraph('finite_state_machine')
        f.attr(rankdir='LR', size='8,5')
        for v in range(self.g.num_vertex()):
            source = 'S{}'.format(v)
            for w in self.g.adj(v):
                target = 'S{}'.format(w)
                f.edge(source, target, color='red')
        for i in range(len(self.reg)):
            if self.reg[i] not in ['(', ')', '|', '?']:
                source = 'S{}'.format(i)
                target = 'S{}'.format(i + 1)
                f.edge(source, target, label=self.reg[i])
        return f