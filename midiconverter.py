from mido import MidiFile, tick2second

MIDI_FILE = r"C:/Users/max.valentin/Documents/TIATIL00S/ddrp/assets/audio/songs/LAmourToujours.mid"
OUTPUT_FILE = r"C:/Users/max.valentin/Documents/TIATIL00S/ddrp/assets/audio/songs/LAmourToujours_chart.txt"

ARROWS = ["LEFT","DOWN","UP","RIGHT"]
CHORD_WINDOW = 120   # ms – sätt så att harmonier blir ackord
MIN_INTERVAL = 120   # ms – minsta tid mellan pilar

mid = MidiFile(MIDI_FILE)
ticks_per_beat = mid.ticks_per_beat

# Sajna BPM själv
BPM = 139
tempo = int(60000000 / BPM)

# Plocka ett track med mest noter
tracks_notes = []
for track in mid.tracks:
    notes = sum(1 for msg in track if msg.type == "note_on" and msg.velocity > 0)
    tracks_notes.append(notes)

best_track_index = tracks_notes.index(max(tracks_notes))
track = mid.tracks[best_track_index]

events = []
current_tick = 0
for msg in track:
    current_tick += msg.time
    if msg.type == "note_on" and msg.velocity > 0:
        seconds = tick2second(current_tick, ticks_per_beat, tempo)
        ms = int(seconds * 1000)
        note_val = msg.note
        arrow = ARROWS[note_val % 4]    # enkel map
        events.append((ms, arrow))

events.sort()

# slå ihop väldigt nära noter till ackord
chart = []
current_time = None
current_arrows = []

for t,a in events:
    if current_time is None:
        current_time = t
        current_arrows = [a]
    elif t - current_time <= CHORD_WINDOW:
        if a not in current_arrows:
            current_arrows.append(a)
    else:
        chart.append((current_time, current_arrows))
        current_time = t
        current_arrows = [a]

if current_time is not None:
    chart.append((current_time, current_arrows))

# filtrera bort pilar som är för nära i tid
filtered = []
last_time = -MIN_INTERVAL

for t,a in chart:
    if t - last_time >= MIN_INTERVAL:
        filtered.append((t,a))
        last_time = t

# To relativ timing
relative = []
prev = 0

for t,a in filtered:
    delta = t - prev
    relative.append((delta,a))
    prev = t

with open(OUTPUT_FILE, "w") as f:
    f.write("chart = [\n")
    for d,a in relative:
        f.write(f"({d},{a}),\n")
    f.write("]\n")

print("Chart sparat till", OUTPUT_FILE)