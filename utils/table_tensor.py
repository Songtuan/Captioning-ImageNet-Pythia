import torch

class TableTensor:
    def __init__(self, vocab, tables):
        self.tables = tables
        self.vocab = vocab

    def __to_tensor(self, v):
        table = self.tables[v]
        table_tensor = torch.ones(len(self.tables), self.vocab.get_size())
        for v, token in table.items():
            if token == '.':
                table_tensor[v] = 0
            else:
                if token in self.vocab.get_stoi():
                    token_id = self.vocab.get_stoi()[token]
                    table_tensor[v][token_id] = 0
        return table_tensor.bool()

    def to_tensors(self):
        tensors = {}
        for v in range(len(self.tables)):
            tensors[v] = self.__to_tensor(v)
        return tensors