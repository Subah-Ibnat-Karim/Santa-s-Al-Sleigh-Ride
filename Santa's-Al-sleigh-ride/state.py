from map import Map


class State:

    def __init__(self, santa: tuple, gifts=[]):
        self.santa = santa
        self.gifts = gifts

    def __eq__(self, other):
        return self.gifts == other.gifts and self.santa == other.santa

    def __str__(self):
        return '"santa at: ' + str(self.santa) + ' gifts at: ' + str(self.gifts) + '"'

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        h = hash(self.santa)
        for i in self.gifts:
            h += hash(i)
        return h

    @staticmethod
    def successor(state: 'State', map_object: Map) -> list[tuple['State', tuple, int]]:
        map_array = map_object.map
        points = map_object.points
        w, h = map_object.w, map_object.h
        next_states = []
        santa_y, santa_x = state.santa[0], state.santa[1]

        def try_move_santa(y: int, x: int):
            """ Tries to move santa and push gifts and saves new state in next_states array. """

            # Checking diagonal movement
            if x * y != 0:
                raise Exception('Diagonal moving is not allowed.')

            # Checking bounds
            if map_object.check_out_of_bounds(santa_y + y, santa_x + x):
                return

            # Checking blocks
            if map_object.is_block(santa_y + y, santa_x + x):
                return

            # Checking if there is a gift around
            if (santa_y + y, santa_x + x) not in state.gifts:  # There is no gifts around
                next_states.append((
                    State((santa_y + y, santa_x + x), state.gifts.copy()),
                    (y, x),
                    max(int(map_array[santa_y + y][santa_x + x]), int(map_array[santa_y][santa_x]))
                ))
            else:  # There is a gift around
                # gift not on bound condition
                if (y == -1 and santa_y != 1) or (y == 1 and santa_y != h - 2) or \
                        (x == -1 and santa_x != 1) or (x == 1 and santa_x != w - 2):

                    # If gift is on a point
                    if (santa_y + y, santa_x + x) in points:
                        return

                    # if there is block or another gift behind the gift
                    r2y, r2x = santa_y + 2 * y, santa_x + 2 * x
                    if map_object.is_block(r2y, r2x) or ((r2y, r2x) in state.gifts):
                        return

                    # Moving gift
                    new_gifts = state.gifts.copy()
                    new_gifts.remove((santa_y + y, santa_x + x))
                    new_gifts.append((r2y, r2x))
                    next_states.append((
                        State((santa_y + y, santa_x + x), new_gifts),
                        (y, x),
                        max(int(map_array[santa_y + y][santa_x + x]), int(map_array[santa_y][santa_x]))
                    ))

        try_move_santa(1, 0)
        try_move_santa(0, 1)
        try_move_santa(-1, 0)
        try_move_santa(0, -1)

        return next_states

    @staticmethod
    def predecessor(state: 'State', map_object: Map) -> list[tuple['State', tuple, int]]:
        next_states = []
        santa_y, santa_x = state.santa[0], state.santa[1]

        def try_move_santa(y: int, x: int):
            """ Tries to move the santa in possible direction. """

            # Checking diagonal movement
            if x * y != 0:
                raise Exception('Diagonal moving is not allowed.')

            # Checking bounds
            if map_object.check_out_of_bounds(santa_y + y, santa_x + x):
                return

            # Checking blocks
            if map_object.is_block(santa_y + y, santa_x + x):
                return

            # If there is a gift forward
            if (santa_y + y, santa_x + x) in state.gifts:
                return

            # Just moving and not pulling gift
            next_states.append((
                State((santa_y + y, santa_x + x), state.gifts.copy()),
                (y, x),
                max(int(map_object.map[santa_y + y][santa_x + x]), int(map_object.map[santa_y][santa_x]))
            ))

            # If there is a gift backward
            if (santa_y - y, santa_x - x) in state.gifts:
                # Pulling gift
                new_gifts = state.gifts.copy()
                new_gifts.remove((santa_y - y, santa_x - x))
                new_gifts.append((santa_y, santa_x))
                next_states.append((
                    State((santa_y + y, santa_x + x), new_gifts),
                    (y, x),
                    max(int(map_object.map[santa_y + y][santa_x + x]), int(map_object.map[santa_y][santa_x]))
                ))

        try_move_santa(1, 0)
        try_move_santa(0, 1)
        try_move_santa(-1, 0)
        try_move_santa(0, -1)

        return next_states

    @staticmethod
    def is_goal(state: 'State', points: list[tuple]):
        for gift in state.gifts:
            if gift not in points:
                return False
        return True
