#main



# class InsideButton:
#     def __init__(self, target_floor, special_button):
#         self.target_floor = target_floor
#         self.special_button = special_button
    
#     def send_elevator(elv_on_floor, floors_queued, target_floor):
        
#         if floors_queued == []:
#             floors_queued.append(target_floor)
elv_on_floor = 0
elv_queue = []

def call_elevator(self_floor, elv_on_floor, elv_queue):
    if elv_queue == []:
        if self_floor > elv_on_floor:
            while elv_on_floor != self_floor:
                elv_on_floor += 1
                print(elv_on_floor)
        elif self_floor < elv_on_floor:
            while elv_on_floor != self_floor:
                elv_on_floor -= 1
                print(elv_on_floor)

while True:
    task = input("""Vad vill du göra?
                    
                    "c" for calltomyfloor """)
    if task == "c":
        self_floor = int(input("Enter your floor"))
        call_elevator(self_floor, elv_on_floor, elv_queue)