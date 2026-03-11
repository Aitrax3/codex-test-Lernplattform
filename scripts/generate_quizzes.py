import json
from textwrap import dedent


def generate_math():
    questions = []
    for i in range(1, 26):
        questions.append({
            "frage": f"Was ergibt {i} + {i + 2}?",
            "antwort": str(2 * i + 2)
        })
    for i in range(5, 30):
        questions.append({
            "frage": f"Was ergibt {i + 5} - {i}?",
            "antwort": str(5)
        })
    for i in range(2, 27):
        questions.append({
            "frage": f"Wieviel ist {i} mal {i + 1}?",
            "antwort": str(i * (i + 1))
        })
    for i in range(2, 27):
        questions.append({
            "frage": f"Wie viel ergibt {i * 2} geteilt durch 2?",
            "antwort": str(i)
        })
    return questions[:100]


def generate_geografie():
    capitals = [
        ("Frankreich", "Paris"),
        ("Spanien", "Madrid"),
        ("Italien", "Rom"),
        ("Österreich", "Wien"),
        ("Schweiz", "Bern"),
        ("Norwegen", "Oslo"),
        ("Schweden", "Stockholm"),
        ("Finnland", "Helsinki"),
        ("Portugal", "Lissabon"),
        ("Niederlande", "Amsterdam"),
        ("Belgien", "Brüssel"),
        ("Polen", "Warschau"),
        ("Tschechien", "Prag"),
        ("Ungarn", "Budapest"),
        ("Griechenland", "Athen"),
        ("Türkei", "Ankara"),
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
        ("Algerien", "Algier"),
    ]

    rivers = [
        ("Nil", "Ägypten"),
        ("Rhein", "Deutschland"),
        ("Donau", "Österreich"),
        ("Mississippi", "USA"),
        ("Amazonas", "Brasilien"),
        ("Yangtze", "China"),
        ("Ganges", "Indien"),
        ("Thames", "England"),
        ("Seine", "Frankreich"),
        ("Loire", "Frankreich"),
        ("Po", "Italien"),
        ("Zambezi", "Sambia"),
        ("Mekong", "Vietnam"),
        ("Salween", "Myanmar"),
        ("Yukon", "Kanada"),
        ("Columbia", "USA"),
        ("Tigris", "Irak"),
        ("Euphrat", "Syrien"),
        ("Volga", "Russland"),
        ("Dnjepr", "Ukraine"),
        ("Elbe", "Deutschland"),
        ("Po", "Italien"),
        ("Rhone", "Schweiz"),
        ("Tiber", "Italien"),
        ("Arno", "Italien"),
    ]

    mountains = [
        ("Mont Blanc", "Alpen"),
        ("Zugspitze", "Deutschland"),
        ("Matterhorn", "Schweiz"),
        ("K2", "Pakistan"),
        ("Mount Everest", "Nepal"),
        ("Kilimandscharo", "Tansania"),
        ("Denali", "USA"),
        ("Aconcagua", "Argentinien"),
        ("Elbrus", "Russland"),
        ("Fuji", "Japan"),
        ("Gipfel von Vulkane", "Island"),
        ("Atlasgebirge", "Marokko"),
        ("Ruwenzori", "Uganda"),
        ("Granite Peak", "USA"),
        ("Table Mountain", "Südafrika"),
        ("Himalaya", "Nepal"),
        ("Pindos", "Griechenland"),
        ("Carpathians", "Rumänien"),
        ("Apenninen", "Italien"),
        ("Pyrenäen", "Spanien"),
        ("Caucasus", "Georgien"),
        ("Anden", "Chile"),
        ("Rockys", "Kanada"),
        ("Sierra Nevada", "Spanien"),
        ("Drakensberge", "Südafrika"),
    ]

    regions = [
        ("Skandinavien", "Norden Europas"),
        ("Balkan", "Südosteuropa"),
        ("Kaukasus", "Südwestasien"),
        ("Sahara", "Nordafrika"),
        ("Kalifornien", "USA"),
        ("Amazonasbecken", "Südamerika"),
        ("Migrierende Kontinente", "Pazifik"),
        ("Britische Inseln", "Atlantik"),
        ("Sizilien", "Mittelmeer"),
        ("Korsika", "Mittelmeer"),
        ("Lappland", "Nordeuropa"),
        ("Gibraltar", "Spanien"),
        ("Kanarische Inseln", "Atlantik"),
        ("Kreta", "Mittelmeer"),
        ("Isle of Man", "Nordsee"),
        ("Sardinien", "Mittelmeer"),
        ("Korfu", "Ionisches Meer"),
        ("Bretagne", "Frankreich"),
        ("Andalusien", "Spanien"),
        ("Normandie", "Frankreich"),
        ("Provence", "Frankreich"),
        ("Toskana", "Italien"),
        ("Piemont", "Italien"),
        ("Istrien", "Adria"),
        ("Dalmatien", "Adria"),
    ]

    questions = []
    for country, capital in capitals:
        questions.append({
            "frage": f"Was ist die Hauptstadt von {country}?",
            "antwort": capital
        })
    for river, country in rivers:
        questions.append({
            "frage": f"Welcher Fluss fließt durch {country}?",
            "antwort": river
        })
    for mountain, location in mountains:
        questions.append({
            "frage": f"In welchem Land liegt {mountain}?",
            "antwort": location
        })
    for region, location in regions:
        questions.append({
            "frage": f"Zu welcher Gegend gehört {region}?",
            "antwort": location
        })
    return questions[:100]


def generate_englisch():
    vocab = [
        ("house", "Haus", ["Wohnhaus"]),
        ("school", "Schule", ["Lehranstalt"]),
        ("book", "Buch", ["Lesestoff"]),
        ("car", "Auto", ["Wagen"]),
        ("friend", "Freund", ["Kumpel"]),
        ("teacher", "Lehrer", ["Lehrkraft"]),
        ("student", "Schüler", ["Studierende"]),
        ("apple", "Apfel", []),
        ("morning", "Morgen", []),
        ("night", "Nacht", []),
        ("sun", "Sonne", []),
        ("moon", "Mond", []),
        ("water", "Wasser", []),
        ("food", "Essen", ["Nahrung"]),
        ("eat", "essen", []),
        ("drink", "trinken", []),
        ("play", "spielen", []),
        ("run", "laufen", []),
        ("walk", "gehen", []),
        ("read", "lesen", []),
        ("write", "schreiben", []),
        ("song", "Lied", ["Melodie"]),
        ("music", "Musik", []),
        ("movie", "Film", ["Kinofilm"]),
        ("city", "Stadt", []),
        ("country", "Land", []),
        ("river", "Fluss", []),
        ("ocean", "Ozean", ["Meer"]),
        ("mountain", "Berg", []),
        ("tree", "Baum", []),
        ("flower", "Blume", []),
        ("bird", "Vogel", []),
        ("fish", "Fisch", []),
        ("dog", "Hund", []),
        ("cat", "Katze", []),
        ("pencil", "Bleistift", []),
        ("chair", "Stuhl", []),
        ("table", "Tisch", []),
        ("door", "Tür", []),
        ("window", "Fenster", []),
        ("schoolbag", "Schultasche", []),
        ("homework", "Hausaufgabe", []),
        ("lesson", "Lektion", []),
        ("red", "rot", []),
        ("blue", "blau", []),
        ("green", "grün", []),
        ("yellow", "gelb", []),
        ("orange", "orange", []),
        ("purple", "lila", ["violett"]),
        ("black", "schwarz", []),
        ("white", "weiß", []),
        ("gray", "grau", []),
        ("pink", "rosa", []),
        ("brown", "braun", []),
        ("short", "kurz", []),
        ("long", "lang", []),
        ("fast", "schnell", []),
        ("slow", "langsam", []),
        ("hot", "heiß", []),
        ("cold", "kalt", []),
        ("happy", "glücklich", ["fröhlich"]),
        ("sad", "traurig", []),
        ("laugh", "lachen", []),
        ("cry", "weinen", []),
        ("dance", "tanzen", []),
        ("sing", "singen", []),
        ("run", "rennen", []),
        ("smile", "lächeln", []),
        ("hug", "umarmen", []),
        ("help", "helfen", []),
        ("learn", "lernen", []),
        ("teach", "unterrichten", []),
        ("remember", "erinnern", []),
        ("forget", "vergessen", []),
        ("start", "beginnen", []),
        ("finish", "beenden", []),
        ("begin", "anfangen", []),
        ("end", "enden", []),
        ("beginner", "Anfänger", []),
        ("expert", "Experte", []),
        ("question", "Frage", []),
    ]
    questions = []
    for word, translation, aliases in vocab:
        entry = {"frage": f"Wie lautet das englische Wort für '{translation}'?", "antwort": word}
        if aliases:
            entry["aliases"] = aliases
        questions.append(entry)
        entry2 = {"frage": f"Was bedeutet '{word}' auf Deutsch?", "antwort": translation}
        questions.append(entry2)
    return questions[:100]


def generate_history():
    events = [
        {
            "answer": "Konrad Adenauer",
            "aliases": ["Adenauer"],
            "variants": [
                "Wer war der erste Bundeskanzler der Bundesrepublik Deutschland?",
                "Nenne den Kanzler, der die erste Regierung der Bundesrepublik aufbaute.",
                "Welche Person führte Deutschland zwischen 1949 und 1963 als Kanzler?",
                "Wer leitete die Regierung direkt nach dem Zweiten Weltkrieg?",
            ],
        },
        {
            "answer": "1989",
            "variants": [
                "In welchem Jahr fiel die Berliner Mauer?",
                "Wann öffnete sich die Grenze zwischen Ost- und Westberlin dauerhaft?",
                "Welches Jahr markierte das Ende der Teilung Berlins?",
                "Wann begann die offizielle Wiedervereinigung durch den Mauerfall?",
            ],
        },
        {
            "answer": "1939",
            "variants": [
                "Wann begann der Zweite Weltkrieg?",
                "In welchem Jahr rückten deutsche Truppen in Polen ein?",
                "Welches Jahr war der Auftakt zum Zweiten Weltkrieg?",
                "Wann startete der globale Konflikt, der bis 1945 dauerte?",
            ],
        },
        {
            "answer": "1914",
            "variants": [
                "Wann begann der Erste Weltkrieg?",
                "In welchem Jahr wurde das Attentat von Sarajevo und damit der Erste Weltkrieg ausgelöst?",
                "Welches Jahr markierte den Ausbruch des großen Krieges 1914?",
                "Wann begann der Konflikt, der bis 1918 dauerte?",
            ],
        },
        {
            "answer": "1990",
            "variants": [
                "Wann wurde Deutschland offiziell wiedervereinigt?",
                "In welchem Jahr wurde die Deutsche Demokratische Republik in die Bundesrepublik aufgenommen?",
                "Welches Jahr steht für die politische Wiedervereinigung nach dem Mauerfall?",
                "Wann trat die Volkskammer dem Bundestag bei?",
            ],
        },
        {
            "answer": "1776",
            "variants": [
                "Wann erklärten die Vereinigten Staaten ihre Unabhängigkeit?",
                "In welchem Jahr unterzeichneten die Gründerväter die Unabhängigkeitserklärung?",
                "Welches Jahr steht für die Geburt der USA als eigenständiger Staat?",
                "Wann wurden die dreizehn Kolonien unabhängig von England?",
            ],
        },
        {
            "answer": "1789",
            "variants": [
                "Wann begann die Französische Revolution mit dem Sturm auf die Bastille?",
                "In welchem Jahr rief Frankreich die Republik nach der Revolution aus?",
                "Welches Jahr markierte den Anfang der Revolution in Paris?",
                "Wann wurde die Monarchie in Frankreich durch revolutionäre Kräfte herausgefordert?",
            ],
        },
        {
            "answer": "1969",
            "variants": [
                "In welchem Jahr setzte der Mensch erstmals seinen Fuß auf den Mond?",
                "Wann landete die Apollo-11-Mission auf dem Mond?",
                "Welches Jahr steht für die erste Mondlandung?",
                "Wann sprach Neil Armstrong seinen berühmten Satz auf dem Mond?",
            ],
        },
        {
            "answer": "1215",
            "variants": [
                "Wann wurde die Magna Carta unterzeichnet?",
                "In welchem Jahr legte König Johann ohne Land die Rechte unter Druck der Barone fest?",
                "Welches Jahr steht für die erste formale Begrenzung der königlichen Macht in England?",
                "Wann begann das moderne Verständnis von Recht in England mit der Magna Carta?",
            ],
        },
        {
            "answer": "476",
            "variants": [
                "In welchem Jahr fiel das Weströmische Reich?",
                "Wann endete die Antike mit dem Sturz des letzten Kaisers?",
                "Welches Jahr markiert den Fall von Rom im Westen?",
                "Wann kollabierte das Imperium, das über Jahrhunderte von Rom regiert wurde?",
            ],
        },
        {
            "answer": "1760",
            "variants": [
                "Wann begann die Industrielle Revolution in Großbritannien?",
                "In welchem Jahr lief die erste Textilmaschine in Serie?",
                "Welches Jahr steht für den Start der Massenproduktion in industrieller Form?",
                "Wann setzte der Wandel von Handarbeit zu Maschinenarbeit ein?",
            ],
        },
        {
            "answer": "1993",
            "variants": [
                "Wann trat der Vertrag von Maastricht in Kraft und gründete die EU?",
                "In welchem Jahr wurde die Europäische Union offiziell als Institution genannt?",
                "Welches Jahr markiert den Beginn der Europäischen Union?",
                "Wann wurde das Europäische Gemeinschaften-System zur EU weiterentwickelt?",
            ],
        },
        {
            "answer": "1815",
            "variants": [
                "In welchem Jahr wurde die Schlacht von Waterloo geschlagen?",
                "Wann besiegten die Alliierten Napoleon endgültig?",
                "Welches Jahr beendete Napoleons Herrschaft?",
                "Wann wurde die französische Armee bei Waterloo zurückgeschlagen?",
            ],
        },
        {
            "answer": "1517",
            "variants": [
                "Wann schlug Martin Luther seine 95 Thesen an die Schlosskirche in Wittenberg?",
                "In welchem Jahr begann die Reformation?",
                "Welches Jahr steht für den Beginn der protestantischen Bewegung?",
                "Wann forderte ein Mönch die Kirche zur Reform heraus?",
            ],
        },
        {
            "answer": "1948",
            "variants": [
                "Wann wurde die Allgemeine Erklärung der Menschenrechte von der UN verabschiedet?",
                "In welchem Jahr verabschiedete die UN die Grundrechte für alle Menschen?",
                "Welches Jahr steht für die weltweite Charta der Menschenrechte?",
                "Wann wurden die Menschenrechte nach dem Zweiten Weltkrieg kodifiziert?",
            ],
        },
        {
            "answer": "1961",
            "variants": [
                "Wann flog Yuri Gagarin als erster Mensch ins All?",
                "In welchem Jahr umkreiste ein Kosmonaut erstmals die Erde?",
                "Welches Jahr steht für den ersten bemannten Raumflug?",
                "Wann startete das Weltraumzeitalter mit dem Menschen an Bord?",
            ],
        },
        {
            "answer": "1521",
            "variants": [
                "In welchem Jahr fiel das Aztekenreich an die Spanier?",
                "Wann eroberten die Konquistadoren Tenochtitlán?",
                "Welches Jahr markiert das Ende des aztekischen Reiches?",
                "Wann brach die spanische Besetzung der Hauptstadt Mexikos an?",
            ],
        },
        {
            "answer": "1400",
            "variants": [
                "Wann begann die Renaissance in Italien?",
                "In welchem Jahr zeichnete sich der kulturelle Wandel zur Renaissance ab?",
                "Welches Jahr steht für den Neubeginn der Kunst und Wissenschaft in Europa?",
                "Wann erlebte Europa den Übergang vom Mittelalter zur Renaissance?",
            ],
        },
        {
            "answer": "1947",
            "variants": [
                "Wann begann der Kalte Krieg zwischen Ost und West?",
                "In welchem Jahr entwickelte sich die Spannungen zwischen USA und Sowjetunion nach dem Zweiten Weltkrieg zu einem ideologischen Konflikt?",
                "Welches Jahr markierte den offiziellen Start des Kalten Krieges?",
                "Wann wurde der Kalte Krieg mit Truman und Stalin spürbar?",
            ],
        },
        {
            "answer": "1919",
            "variants": [
                "Wann trat die Weimarer Verfassung in Kraft?",
                "In welchem Jahr wurde die erste demokratische Verfassung Deutschlands nach dem Krieg verabschiedet?",
                "Welches Jahr steht für die Gründung der Weimarer Republik?",
                "Wann trat die neue Verfassung der deutschen Republik in Kraft?",
            ],
        },
        {
            "answer": "1948",
            "variants": [
                "Wann begann die Berliner Luftbrücke?",
                "In welchem Jahr versorgten Flugzeuge West-Berlin während der Blockade?",
                "Welches Jahr steht für die logistische Aktion zur Versorgung Berliner Bürger?",
                "Wann löste die Luftbrücke die sowjetische Blockade?",
            ],
        },
        {
            "answer": "1949",
            "variants": [
                "In welchem Jahr wurde das Grundgesetz der Bundesrepublik Deutschland verkündet?",
                "Wann trat das Grundgesetz als provisorische Verfassung in Kraft?",
                "Welches Jahr steht für den Beginn der Bundesrepublik als Rechtsstaat?",
                "Wann wurde das Grundgesetz durch den Parlamentarischen Rat verabschiedet?",
            ],
        },
        {
            "answer": "1919",
            "variants": [
                "Wann wurde der Vertrag von Versailles unterschrieben?",
                "In welchem Jahr endete der Erste Weltkrieg durch einen Friedensvertrag?",
                "Welches Jahr ist mit dem Vertrag verbunden, der Deutschland harte Bedingungen auferlegte?",
                "Wann öffnete der Vertrag die neue Friedensordnung Europas nach 1918?",
            ],
        },
        {
            "answer": "1861",
            "variants": [
                "Wann wurde Italien offiziell als geeinter Nationalstaat gegründet?",
                "In welchem Jahr erklärte Viktor Emanuel II. das Königreich Italien?",
                "Welches Jahr markiert das Ende mehrerer unabhängiger Königreiche in Italien?",
                "Wann erfuhr Italien seine nationale Einigung?",
            ],
        },
        {
            "answer": "1347",
            "variants": [
                "Wann breitete sich der Schwarze Tod nach Europa aus?",
                "In welchem Jahr wütete die Pest besonders heftig?",
                "Welches Jahr ist mit dem Auftreten der Pest in Mittelitalien verbunden?",
                "Wann begann die große Pestwelle, die Millionen Menschen forderte?",
            ],
        },
    ]
    questions = []
    for event in events:
        for question in event["variants"]:
            entry = {"frage": question, "antwort": event["answer"]}
            if event.get("aliases"):
                entry["aliases"] = event["aliases"]
            questions.append(entry)
    return questions[:100]


def main():
    payload = {
        "Mathematik": generate_math(),
        "Geografie": generate_geografie(),
        "Englisch": generate_englisch(),
        "Geschichte": generate_history(),
    }
    with open("quizzes.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
