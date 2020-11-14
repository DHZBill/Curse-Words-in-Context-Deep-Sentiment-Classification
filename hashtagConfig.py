sentiments = {0: "positive", 1: "sad", 2: "angry", 3: "fear", 4: "sarcasm"}

cursewordsCatg = {
    0: "general",
    1: "race",
    2: "gender-sexuality",
    3: "religion",
    4: "other-body-parts",
    5: "ableist",
    6: "problem-words",
    7: "multiple-worded",
}

allCurseWords = [
    set(["fuck", "fu*k", "f*ck", "f**k", "sh*t", "shit", "pissed", "screw"]),
    set(["nigger", "n*gga", "n*gger", "n*gg*r", "chink", "niglet", "wetback"]),
    set(
        [
            "dick",
            "di*k",
            "d*ck",
            "cunt",
            "pussy",
            "pu**y",
            "fag ",
            "queer",
            "qu**r",
            "boner",
            "dong",
            "slut",
            "sl*t",
            "dyke",
            "pimp",
            "whore",
            " hoe ",
            "bitch",
            "b*tch",
            "bi*ch",
            "cock",
            "tramp",
            "cum ",
            "schlong",
            "spunk",
            "skank",
            "motherfucker",
            " tit ",
            " gay ",
            "mothafucker",
            "blowjob",
        ]
    ),
    set(["hell", "damn"]),
    set([" ass ", "queaf", "shart", "urine", "rimming", "arse", "shat ", "crap "]),
    set(["retard", "spaz"]),
    set([" tit ", " hoe ", "chink", "gay "]),
    set(["son of a bitch", "doggie style", "fucked up"]),
]

allHashtags = [
    set(
        [
            "happy",
            "funny",
            "greatmood",
            "superhappy",
            "atlast",
            "ecstatic",
            "thankful",
            "feelinggood",
            "love",
            "loveyou",
            "joy",
            "yay",
            "blessed",
            "thrilled",
            "lol",
            "motivation",
            "positive",
            "positivethinking",
            "excited",
            "exciting",
            "fun",
        ]
    ),
    set(
        [
            "sad",
            "heartbroken",
            "leftout",
            "sadness",
            "depressed",
            "disappointment",
            "disappointed",
            "unhappy",
            "foreveralone",
        ]
    ),
    set(
        [
            "pissed",
            "angry",
            "pissedoff",
            "furious",
            "mad",
            "hateyou",
            "annoying",
            "ugh",
            "anger",
            "fuming",
            "heated",
            "angrytweet",
            "aggressive",
            "godie",
            "pieceofshit",
            "irritated",
        ]
    ),
    set(
        [
            "afraid",
            "petrified",
            "scared",
            "anxious",
            "worried",
            "frightened",
            "freakedout",
            "haunted",
        ]
    ),
    set(["sarcasm"]),
]


allEmojis = [
    set(
        [
            " ;) ",
            ":)))",
            " =) ",
            " :] ",
            " :P ",
            " :-P ",
            " :D ",
            " ;D ",
            ":>",
            ":3 ",
            ";-)",
            ":-D",
        ]
    ),
    set([" :( ", " :(((", " =(((", " =( ", ":-(", ":^(", ":'(", ":-<"]),
    set([" >:S ", " >:{ ", " >: ", " x-@", " :@ ", ":-@ ", " :-/ ", ":/ "]),
    set(
        [
            " :-o ",
            " :$ ",
            " :-O ",
            " o_O ",
            " O_o ",
            " :‑O ",
            " :O ",
            " :‑o ",
            " :o ",
            " :-0 ",
            " 8‑0 ",
            ">:O",
            " :-l ",
            " ,:-| ",
        ]
    ),
]

sentimentToNumber = {
    "surprise": 3,
    "fear": 3,
    "sadness": 1,
    "anger": 2,
    "joy": 0,
}


