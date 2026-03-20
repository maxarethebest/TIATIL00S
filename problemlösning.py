input_text = input("Mata in text: ")
små = ["a","b","c","d","e","f","g","h", "i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
stora = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

def case_upper(input_text):
    finished = ""
    for i in input_text:
        if i in små:
            finished += stora[små.index(i)]
        else:
            finished += i
    return finished
    
print(case_upper(input_text))