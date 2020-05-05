from room import Room
from player import Player
from world import World
from util import Queue, Stack

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)
# print("CR", player.current_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']

# Starting Room
# get list of open exits of current room
traversal_path = []

reverse_direction = {'n': 's', 'e': 'w', 's': 'n', 'w': 'e'}


def graph_traversal(starting_room, visited=set()):

    path_taken = []

    # get all possible exits in current_room
    for direction in player.current_room.get_exits():
        # player travel to room in direction of exit
        player.travel(direction)

        # check if new room has been visited
        if player.current_room.id not in visited:
            # room has not been visited
            # mark as visited
            visited.add(player.current_room.id)
            # add new direction to path_taken
            path_taken.append(direction)
            # print("path_taken 56", path_taken)
            # recurse with new current_room and add to path_taken
            path_taken = path_taken + \
                graph_traversal(player.current_room.id, visited)
            # print("path_taken 60", path_taken)
            # backtrack and go to different room
            player.travel(reverse_direction[direction])
            # add backtrack to path_taken to keep track of steps
            path_taken.append(reverse_direction[direction])

        else:
            # Room already visited so backtrack and go to different room
            player.travel(reverse_direction[direction])

    return path_taken


traversal_path = graph_traversal(player.current_room.id)


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")

    # stack = Stack()
    # stack.push([starting_room])
    # traversedRooms = {}

    # while stack.size() > 0:
    #     path = stack.pop()
    #     currentRoom = path[-1]
    #     if currentRoom not in traversedRooms:
    #         traversedRooms[currentRoom.id] = {}
    #         # get exits of current room player is in
    #         availableExits = player.current_room.get_exits()
    #         # print("Available Exits:", availableExits)
    #         for exits in availableExits:
    #             room = player.current_room.get_room_in_direction(exits)
    #             if room is not None:
    #                 traversedRooms[currentRoom.id] = {exits: room.id}
    #                 # print("traversal_path 63:", traversal_path)
    #                 # print("Traversed Rooms 64:", traversedRooms)
    #                 newPath = list(path)
    #                 newPath.append(room)
    #                 stack.push(newPath)
    #             else:
    #                 traversedRooms[currentRoom.id] = {exit: "?"}
    #         player.travel(random.choice(availableExits))
