class Solution:
    def __init__(self, solution: list[int | None]):
        self.solution: list[int | None] = solution

    def __call__(self):
        return self.solution

    def __getitem__(self, index):
        return self.solution[index]

    def __len__(self):
        return len(self.solution)