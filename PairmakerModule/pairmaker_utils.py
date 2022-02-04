class PairedAnswer:
    def __init__(self, left: int, right: int):
        self.left = left
        self.right = right

    def check_left(self, other):
        if not self.left and not other.left:
            return True
        return self.left == other.left or self.left == other.right

    def check_right(self, other):
        if not self.right and not other.right:
            return True
        return self.right == other.left or self.right == other.right


class UserSelector:
    start_stage: int = 7

    def __init__(self, params: tuple):
        self.values = self._preprocess(params)

    def juxtaposition(self, params: tuple) -> int:
        stage = UserSelector.start_stage
        our = self.values
        their = self._preprocess(params)
        if our[0] != their[0]:
            stage -= 1
        if not our[1].check_left(their[1]):
            stage -= 1
        if not our[1].check_right(their[1]):
            stage -= 1
        if not our[2].check_left(their[2]):
            stage -= 1
        if not our[2].check_right(their[2]):
            stage -= 1
        if not our[3].check_left(their[3]):
            stage -= 1
        if not our[3].check_right(their[3]):
            stage -= 1
        return stage

    @staticmethod
    def _preprocess(params: tuple) -> list:
        return [
            params[1],
            PairedAnswer(params[2], params[3]),
            PairedAnswer(params[4], params[5]),
            PairedAnswer(params[6], params[7])
        ]
