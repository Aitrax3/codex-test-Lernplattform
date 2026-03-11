import json


def arithmetic_questions():
    questions = []
    for i in range(1, 26):
        questions.append({
            "frage": f"Was ergibt {i} + {i + 3}?", "antwort": str(2 * i + 3)
        })
    for i in range(10, 37):
        questions.append({
            "frage": f"Was ergibt {i + 4} - {i}?", "antwort": str(4)
        })
    for i in range(20, 45):
        questions.append({
            "frage": f"Subtrahiere {i - 8} von {i}", "antwort": str(8)
        })
    return questions[:25]


def multiplication_questions():
    return [
        {"frage": f"Wieviel ist {a} mal {b}?", "antwort": str(a * b)}
        for a in range(2, 12)
        for b in range(2, 12)
    ][:25]


def division_questions():
    return [
        {"frage": f"Wie viel ergibt {a * b} geteilt durch {b}?", "antwort": str(a)}
        for a in range(2, 12)
        for b in range(2, 12)
    ][:25]


def equation_questions():
    questions = []
    for x in range(2, 27):
        questions.append({
            "frage": f"Löse: {x}x - {x} = {x * (x - 1)}", "antwort": str(x)
        })
        questions.append({
            "frage": f"Löse: 3x + {x} = {4 * x}", "antwort": str(x)
        })
    return questions[:25]


def generate_math():
    return {
        "Arithmetik": arithmetic_questions(),
        "Multiplikation": multiplication_questions(),
        "Division": division_questions(),
        "Gleichungen": equation_questions(),
    }


def capital_questions():
    pairs = [
        ("Frankreich", "Paris"),
        ("Spanien", "Madrid"),
        ("Italien", "Rom"),
        ("Österreich", "Wien"),
        ("Schweiz", "Bern"),
        ("Portugal", "Lissabon"),
        ("Belgien", "Brüssel"),
        ("Niederlande", "Amsterdam"),
        ("Polen", "Warschau"),
        ("Ungarn", "Budapest"),
        ("Tschechien", "Prag"),
        ("Norwegen", "Oslo"),
        ("Kroatien", "Zagreb"),
        ("Rumänien", "Bukarest"),
        ("Bulgarien", "Sofia"),
        ("Russland", "Moskau"),
        ("Kanada", "Ottawa"),
        ("Brasilien", "Brasília"),
        ("Argentinien", "Buenos Aires"),
        ("Japan", "Tokio"),
        ("China", "Peking"),
        ("Indien", "Neu-Delhi"),
        ("Australien", "Canberra"),
        ("Ägypten", "Kairo"),
        ("Südafrika", "Pretoria"),
        ("Marokko", "Rabat"),
    ]
    return [
        {"frage": f"Was ist die Hauptstadt von {country}?", "antwort": capital}
        for country, capital in pairs
    ][:25]


def river_questions():
    flows = [
        ("Nil", "Ägypten"),
        ("Donau", "Österreich"),
        ("Rhein", "Deutschland"),
        ("Thames", "England"),
        ("Amazonas", "Brasilien"),
        ("Yangtze", "China"),
        ("Ganges", "Indien"),
        ("Mekong", "Vietnam"),
        ("Volga", "Russland"),
        ("Euphrat", "Syrien"),
        ("Tigris", "Irak"),
        ("Seine", "Frankreich"),
        ("Elbe", "Deutschland"),
        ("Hudson", "USA"),
        ("Orinoco", "Venezuela"),
        ("Loire", "Frankreich"),
        ("Weser", "Deutschland"),
        ("Colorado", "USA"),
        ("Tajo", "Spanien"),
    ]
    return [
        {"frage": f"Welcher Fluss fließt durch {country}?", "antwort": river}
        for river, country in flows
    ][:25]


def mountain_questions():
    peaks = [
        ("Zugspitze", "Deutschland"),
        ("Matterhorn", "Schweiz"),
        ("Mont Blanc", "Frankreich"),
        ("Kilimandscharo", "Tansania"),
        ("Denali", "USA"),
        ("Fuji", "Japan"),
        ("Mount Everest", "Nepal"),
        ("K2", "Pakistan"),
        ("Piz Buin", "Österreich"),
        ("Himalaya", "Nepal"),
        ("Anden", "Chile"),
        ("Rocky Mountains", "Kanada"),
        ("Drakensberge", "Südafrika"),
        ("Pindos", "Griechenland"),
        ("Apenninen", "Italien"),
        ("Pyrenäen", "Spanien"),
    ]
    return [
        {"frage": f"In welchem Land liegt {mountain}?", "antwort": country}
        for mountain, country in peaks
    ][:25]


def generate_geografie():
    return {
        "Hauptstädte": capital_questions(),
        "Flüsse": river_questions(),
        "Gebirge": mountain_questions(),
        "Regionen": [
            {"frage": f"Zu welcher Region gehört {region}?", "antwort": location}
            for region, location in [
                ("Skandinavien", "Nordeuropa"),
                ("Balkan", "Südosteuropa"),
                ("Kaukasus", "Südwestasien"),
                ("Sahara", "Nordafrika"),
                ("Kanarische Inseln", "Atlantik"),
                ("Lappland", "Nordeuropa"),
                ("Sizilien", "Mittelmeer"),
                ("Normandie", "Frankreich"),
                ("Provence", "Frankreich"),
                ("Toskana", "Italien"),
                ("Dalmatien", "Adria"),
                ("Korsika", "Mittelmeer"),
                ("Andalusien", "Spanien"),
                ("Rheinland", "Deutschland"),
                ("Sardinien", "Mittelmeer"),
            ]
        ][:25],
    }


def translate_pairs():
    return [
        ("house", "Haus", ["Wohnhaus"]),
        ("school", "Schule", ["Lehranstalt"]),
        ("book", "Buch", ["Lesestoff"]),
        ("apple", "Apfel", []),
        ("friend", "Freund", ["Kumpel"]),
        ("music", "Musik", []),
        ("song", "Lied", []),
        ("movie", "Film", ["Kinofilm"]),
        ("sun", "Sonne", []),
        ("moon", "Mond", []),
        ("water", "Wasser", []),
        ("fire", "Feuer", []),
        ("cold", "kalt", []),
        ("hot", "heiß", []),
        ("laugh", "lachen", []),
        ("cry", "weinen", []),
        ("read", "lesen", []),
        ("write", "schreiben", []),
        ("run", "rennen", ["laufen"]),
        ("walk", "gehen", []),
        ("eat", "essen", []),
        ("drink", "trinken", []),
        ("learn", "lernen", []),
        ("teach", "unterrichten", []),
        ("question", "Frage", []),
        ("answer", "Antwort", []),
        ("color", "Farbe", []),
        ("family", "Familie", []),
        ("happy", "glücklich", ["fröhlich"]),
    ]


def build_vocab_templates(word, translation):
    return [
        f"Was bedeutet '{word}' auf Deutsch?",
        f"Wie lautet das englische Wort für '{translation}'?",
        f"Wie würdest du '{translation}' auf Englisch sagen?",
        f"Welches englische Wort beschreibt '{translation}'?",
    ]


def generate_english_vocab():
    questions = []
    for word, translation, aliases in translate_pairs():
        for template in build_vocab_templates(word, translation):
            entry = {
                "frage": template,
                "antwort": word if "englische" in template or "beschreibt" in template else translation,
            }
            if aliases and "englische" not in template:
                entry["aliases"] = aliases
            questions.append(entry)
    return questions[:60]


def generate_english_verbs():
    verbs = [
        ("run", "rennen", ["laufen"]),
        ("jump", "springen", []),
        ("swim", "schwimmen", []),
        ("dance", "tanzen", []),
        ("sing", "singen", []),
        ("paint", "malen", []),
        ("write", "schreiben", []),
        ("read", "lesen", []),
        ("sleep", "schlafen", []),
        ("stand", "stehen", []),
        ("play", "spielen", []),
        ("think", "denken", []),
        ("build", "bauen", []),
    ]
    return [
        {"frage": f"Was bedeutet '{word}' auf Deutsch?", "antwort": translation}
        for word, translation, _ in verbs
    ][:25]


def generate_english_phrases():
    return [
        {"frage": "Wie sagt man 'Danke' auf Englisch?", "antwort": "thank you"},
        {"frage": "Was bedeutet 'Please'?", "antwort": "Bitte"},
        {"frage": "Wie lautet 'Gute Nacht' auf Englisch?", "antwort": "good night"},
        {"frage": "Was heißt 'Excuse me'?", "antwort": "Entschuldigung"},
        {"frage": "Wie sagt man 'Ich verstehe nicht'?", "antwort": "I don't understand"},
        {"frage": "Was bedeutet 'See you later'?", "antwort": "Bis später"},
        {"frage": "Wie lautet 'Was kostet das?' auf Englisch?", "antwort": "How much is this?"},
        {"frage": "Was heißt 'Hilfe' auf Englisch?", "antwort": "help"},
        {"frage": "Wie sagt man 'Ich habe Hunger'?", "antwort": "I'm hungry"},
        {"frage": "Was bedeutet 'I'm tired'?", "antwort": "Ich bin müde"},
    ]


def generate_english():
    return {
        "Grundwortschatz": generate_english_vocab(),
        "Verben": generate_english_verbs(),
        "Phrasen": generate_english_phrases(),
        "Farben": [
            {"frage": "Wie heißt 'blau' auf Englisch?", "antwort": "blue"},
            {"frage": "Wie lautet 'rot' auf Englisch?", "antwort": "red"},
            {"frage": "Wie lautet 'gelb' auf Englisch?", "antwort": "yellow"},
            {"frage": "Wie lautet 'grün' auf Englisch?", "antwort": "green"},
            {"frage": "Was heißt 'rosa' auf Englisch?", "antwort": "pink"},
        ],
    }


def generate_history():
    entries = {
        "Deutschland": [
            {"frage": "Wer war der erste Bundeskanzler der Bundesrepublik Deutschland?", "antwort": "Konrad Adenauer"},
            {"frage": "In welchem Jahr fiel die Berliner Mauer?", "antwort": "1989"},
            {"frage": "Wann trat das Grundgesetz in Kraft?", "antwort": "1949"},
            {"frage": "Wann wurde Deutschland offiziell wiedervereinigt?", "antwort": "1990"},
            {"frage": "In welchem Jahr wurde Willy Brandt Bundeskanzler?", "antwort": "1969"},
            {"frage": "Wann trat Gerhard Schröder sein Amt als Kanzler an?", "antwort": "1998"},
        ],
        "Weltgeschichte": [
            {"frage": "Wann begann der Zweite Weltkrieg?", "antwort": "1939"},
            {"frage": "In welchem Jahr endete der Erste Weltkrieg?", "antwort": "1918"},
            {"frage": "Wann wurde die Magna Carta unterzeichnet?", "antwort": "1215"},
            {"frage": "Wann landete der erste Mensch auf dem Mond?", "antwort": "1969"},
            {"frage": "Wann fiel das Weströmische Reich?", "antwort": "476"},
            {"frage": "Wann begann die Kalte Krieg-Ära zwischen Ost und West?", "antwort": "1947"},
        ],
        "Epochen": [
            {"frage": "Wann begann die Renaissance in Italien?", "antwort": "1400"},
            {"frage": "Wann begann die Industrielle Revolution in Großbritannien?", "antwort": "1760"},
            {"frage": "Wann begann die Französische Revolution?", "antwort": "1789"},
            {"frage": "Wann wurde die Allgemeine Erklärung der Menschenrechte verabschiedet?", "antwort": "1948"},
            {"frage": "Wann veröffentlichte Isaac Newton die Principia?", "antwort": "1687"},
            {"frage": "Wann begann die Aufklärung mit der Glorious Revolution?", "antwort": "1688"},
        ],
        "Entdeckungen": [
            {"frage": "Wann wurde Amerika von Kolumbus entdeckt?", "antwort": "1492"},
            {"frage": "In welchem Jahr erfand Gutenberg den Buchdruck?", "antwort": "1450"},
            {"frage": "Wann wurde das Weltall erstmals betreten?", "antwort": "1961"},
            {"frage": "Wann wurde das Römische Reich im Westen gestürzt?", "antwort": "476"},
            {"frage": "Wann entdeckte Alexander von Humboldt Amerika?", "antwort": "1799"},
            {"frage": "Wann wurde Penicillin von Alexander Fleming entdeckt?", "antwort": "1928"},
        ],
        "Kriege": [
            {"frage": "Wann endete die Schlacht von Waterloo?", "antwort": "1815"},
            {"frage": "In welchem Jahr begann der Dreißigjährige Krieg?", "antwort": "1618"},
            {"frage": "Wann begann der Amerikanische Bürgerkrieg?", "antwort": "1861"},
            {"frage": "In welchem Jahr wurde der Frieden von Westfalen geschlossen?", "antwort": "1648"},
            {"frage": "Wann begann der Kriegszustand zwischen Deutschland und Polen (Zweiter Weltkrieg)?", "antwort": "1939"},
            {"frage": "Wann endete die Sowjetblockade Berlins (Luftbrücke)?", "antwort": "1949"},
        ],
        "Wissenschaft": [
            {"frage": "Wann veröffentlichte Darwin die Evolutionstheorie?", "antwort": "1859"},
            {"frage": "In welchem Jahr entdeckte Marie Curie das Radium?", "antwort": "1898"},
            {"frage": "Wann wurde Albert Einsteins Relativitätstheorie bekannt?", "antwort": "1905"},
            {"frage": "Wann gelang die erste Vollnarkose mit Äther?", "antwort": "1846"},
            {"frage": "In welchem Jahr startete der erste Satellit Sputnik?", "antwort": "1957"},
            {"frage": "Wann wurde das menschliche Genom entschlüsselt?", "antwort": "2003"},
        ],
        "Politik": [
            {"frage": "Wann wurde die UNO gegründet?", "antwort": "1945"},
            {"frage": "In welchem Jahr trat der Vertrag von Maastricht in Kraft?", "antwort": "1993"},
            {"frage": "Wann wurde die NATO gegründet?", "antwort": "1949"},
            {"frage": "Wann verabschiedete der Bundestag den Zwei-plus-Vier-Vertrag?", "antwort": "1990"},
            {"frage": "Wann trat die Berliner Luftbrücke in Kraft?", "antwort": "1948"},
            {"frage": "In welchem Jahr endete die Apartheid in Südafrika?", "antwort": "1994"},
        ],
        "Kultur": [
            {"frage": "Wann wurde die sogenannte Gutenberg-Bibel gedruckt?", "antwort": "1455"},
            {"frage": "In welchem Jahr feierte Beethoven seine erste Sinfonie?", "antwort": "1800"},
            {"frage": "Wann wurde das Bauhaus gegründet?", "antwort": "1919"},
            {"frage": "Wann wurde die Berliner Philharmonie eröffnet?", "antwort": "1963"},
            {"frage": "Wann fand die erste Berlinale statt?", "antwort": "1951"},
            {"frage": "Wann wurde der Rundfunk in Deutschland offiziell gestartet?", "antwort": "1923"},
        ],
    }
    return entries


def main():
    payload = {
        "Mathematik": generate_math(),
        "Geografie": generate_geografie(),
        "Englisch": generate_english(),
        "Geschichte": generate_history(),
    }
    with open("quizzes.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
