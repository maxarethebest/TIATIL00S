# songs.py - Filn med alla låtar.
# __author__: Max Valentin
# __version__: 1.0
# __email__: max.valentin@elev.ga.dbgy.se

BlinkaLillaStjärna = {
    "name": "Blinka lilla stjärna",
    "music": "ddrp/assets/audio/songs/BlinkaLillaStjärna.mp3",

    #Tid till första noten i ms
    "start_offset": 3000,


    #Hur pilarna ska spawnas i "({tid efter föregående pil i ms},["{direction på pilen}"])"
    "chart" : 
[
(0,[]),
(600,['LEFT']),
(750,['LEFT']),
(750,['DOWN']),
(750,['DOWN']),
(750,['UP']),
(750,['UP']),
(750,['DOWN']),

(1500,['DOWN']),
(750,['DOWN']),
(750,['UP']),
(750,['UP']),
(750,['RIGHT']),
(750,['RIGHT']),
(750,['UP']),

(1500,['UP']),
(750,['UP']),
(750,['RIGHT']),
(750,['RIGHT']),
(750,['LEFT']),
(750,['LEFT']),
(750,['RIGHT']),

(1500,['UP']),
(750,['UP']),
(750,['RIGHT']),
(750,['RIGHT']),
(750,['LEFT']),
(750,['LEFT']),
(750,['RIGHT']),

(1500,['LEFT']),
(750,['LEFT']),
(750,['DOWN']),
(750,['DOWN']),
(750,['UP']),
(750,['UP']),
(750,['DOWN']),

(1500,['DOWN']),
(750,['DOWN']),
(750,['UP']),
(750,['UP']),
(750,['RIGHT']),
(750,['RIGHT']),
(750,['UP']),
]
}

SONGS = [
    BlinkaLillaStjärna,
]
