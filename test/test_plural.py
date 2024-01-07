"""Test [English plurals](https://en.wikipedia.org/wiki/English_plurals)."""

from inkfill import plural


def test_plural_sibilant() -> None:
    """Ends in sibilant."""
    assert plural("kiss") == "kisses"
    assert plural("phase") == "phases"
    assert plural("dish") == "dishes"
    assert plural("massage") == "massages"
    assert plural("witch") == "witches"
    assert plural("judge") == "judges"


def test_plural_voiceless_consonant() -> None:
    """Ends in voiceless consonant"""
    assert plural("lap") == "laps"
    assert plural("cat") == "cats"
    assert plural("clock") == "clocks"
    assert plural("cuff") == "cuffs"
    assert plural("death") == "deaths"
    assert plural("loch") == "lochs"


def test_plural_voiced_phoneme() -> None:
    """Ends in voiced phoneme."""
    assert plural("girl") == "girls"
    assert plural("chair") == "chairs"
    assert plural("boy") == "boys"


def test_plural_consonant_o() -> None:
    """Ends in consonant + o."""
    # assert plural("hero") == "heroes"
    # assert plural("potato") == "potatoes"
    # assert plural("volcano") == "volcanoes"

    # loan words
    assert plural("canto") == "cantos"
    assert plural("hetero") == "heteros"
    assert plural("photo") == "photos"
    assert plural("zero") == "zeros"
    assert plural("piano") == "pianos"
    assert plural("portico") == "porticos"
    assert plural("pro") == "pros"
    assert plural("quarto") == "quartos"
    assert plural("kimono") == "kimonos"


def test_plural_y() -> None:
    """End in -y."""
    assert plural("cherry") == "cherries"
    assert plural("lady") == "ladies"
    assert plural("sky") == "skies"

    # ends in -quy
    assert plural("colloquy") == "colloquies"
    assert plural("obsequy") == "obsequies"
    assert plural("soliloquy") == "soliloquies"

    # ends in vowel+y
    assert plural("day") == "days"
    assert plural("monkey") == "monkeys"


def test_plural_i() -> None:
    """ends in -i."""
    # ends in -i
    assert plural("alibi") == "alibis"
    assert plural("bikini") == "bikinis"
    assert plural("Israeli") == "Israelis"
    assert plural("chili") == "chilis"
    # assert plural("alkali") == "alkalies"


def test_plural_near_regular() -> None:
    """Near-regular plurals."""
    assert plural("bath") == "baths"
    assert plural("mouth") == "mouths"
    # assert plural("calf") == "calves"
    # assert plural("leaf") == "leaves"
    # assert plural("knife") == "knives"
    # assert plural("life") == "lives"
    assert plural("house") == "houses"
    assert plural("moth") == "moths"
    assert plural("proof") == "proofs"
    # assert plural("dwarf") == "dwarves"  # dwarfs
    # assert plural("hoof") == "hooves"  # hoofs
    # assert plural("elf") == "elves"  # elfs
    assert plural("roof") == "roofs"
    assert plural("staff") == "staffs"  # staves
    assert plural("turf") == "turfs"


def test_plural_irregular() -> None:
    """Irregular plurals."""
    # generally not supported


def test_plurals_en() -> None:
    """Plurals in -(e)n."""
    assert plural("ox") == "oxen"
    assert plural("child") == "children"
    assert plural("brother") == "brothers"  # not brethren
    #  dialectal, rare, or archaic usage skipped


def test_plural_apophonic() -> None:
    """Apophonic plurals."""
    assert plural("foot") == "feet"
    assert plural("goose") == "geese"
    assert plural("louse") == "lice"
    assert plural("dormouse") == "dormice"
    assert plural("man") == "men"
    assert plural("mouse") == "mice"
    assert plural("tooth") == "teeth"
    assert plural("woman") == "women"
    assert plural("mongoose") == "mongooses"  # counter-example


def test_plural_misc_irregular() -> None:
    """Misc irregular plurals."""
    assert plural("person") == "people"
    assert plural("die") == "dice"
    assert plural("penny") == "pence"


def test_plural_latin() -> None:
    """Latin plurals."""
    # -a => -ae
    # assert plural("alumna") == "alumnae"
    # assert plural("antenna") == "antennae"
    assert plural("aurora") == "auroras"
    assert plural("formula") == "formulas"
    assert plural("encyclopedia") == "encyclopedias"
    # assert plural("larva") == "larvae"
    # assert plural("supernova") == "supernovae"

    # -ex, -ix => -ices
    assert plural("index") == "indices"
    assert plural("matrix") == "matrices"
    assert plural("vertex") == "vertices"

    # -is => -es
    assert plural("axis") == "axes"
    assert plural("genesis") == "geneses"
    assert plural("nemesis") == "nemeses"
    assert plural("crisis") == "crises"
    assert plural("testis") == "testes"
    assert plural("thesis") == "theses"
    assert plural("parenthesis") == "parentheses"
    # assert plural("clitoris") == "clitorises"

    # -polis => -poleis
    assert plural("acropolis") == "acropoleis"

    # -ies => -ies
    assert plural("series") == "series"
    assert plural("species") == "species"

    # -um => -a
    assert plural("addendum") == "addenda"
    assert plural("agendum") == "agenda"
    assert plural("corrigendum") == "corrigenda"
    assert plural("curriculum") == "curricula"
    assert plural("datum") == "data"
    assert plural("forum") == "fora"
    assert plural("medium") == "media"
    assert plural("memorandum") == "memoranda"
    assert plural("millennium") == "millennia"
    assert plural("ovum") == "ova"
    assert plural("referendum") == "referendums"
    assert plural("spectrum") == "spectra"
    assert plural("stadium") == "stadiums"
    assert plural("stratum") == "strata"

    # -us => -i
    assert plural("alumnus") == "alumni"
    assert plural("cactus") == "cacti"
    assert plural("campus") == "campuses"
    # assert plural("corpus") == "corpora"
    # assert plural("census") == "censuses"
    assert plural("focus") == "foci"
    assert plural("fungus") == "fungi"
    # assert plural("genus") == "genera"
    # assert plural("hippopotamus") == "hippopotamuses"
    assert plural("octopus") == "octopuses"
    assert plural("platypus") == "platypuses"
    assert plural("prospectus") == "prospectuses"
    assert plural("radius") == "radii"
    assert plural("succubus") == "succubi"
    assert plural("stylus") == "styluses"
    assert plural("syllabus") == "syllabi"
    assert plural("terminus") == "termini"
    assert plural("uterus") == "uteruses"
    # assert plural("viscus") == "viscera"
    assert plural("virus") == "viruses"
    # assert plural("meatus") == "meatuses"
    assert plural("status") == "statuses"
    # assert plural("apparatus") == "apparatuses"


def test_plural_greek() -> None:
    """Greek plurals."""
    # -on => -a
    assert plural("automaton") == "automata"
    assert plural("criterion") == "criteria"
    assert plural("phenomenon") == "phenomena"
    assert plural("polyhedron") == "polyhedra"

    # -as => -antes
    # assert plural("Atlas") == "Atlantes"
    # assert plural("atlas") == "atlases"

    # -ma => -s (or -mata)
    assert plural("stigma") == "stigmas"
    assert plural("stoma") == "stomas"
    assert plural("schema") == "schemas"
    assert plural("dogma") == "dogmas"
    assert plural("lemma") == "lemmas"
    assert plural("magma") == "magmas"
    assert plural("anathema") == "anathemas"
    assert plural("enema") == "enemas"


def test_plural_french() -> None:
    """French plurals."""
    assert plural("beau") == "beaus"  # beaux
    assert plural("bureau") == "bureaus"  # bureaux
    assert plural("château") == "châteaus"  # châteaux # spell-checker: disable-line
    assert plural("milieu") == "milieus"  # milieux
    assert plural("tableau") == "tableaus"  # tableaux


def test_plural_italian() -> None:
    """Italian plurals."""
    # spell-checker: disable
    # assert plural("cello") == "celli"
    # assert plural("timpano") == "timpani"
    # assert plural("biscotto") == "biscotti"
    # spell-checker: enable


def test_plural_slavic() -> None:
    """Slavic plurals."""
    # spell-checker: disable
    assert plural("kniazhestvo") == "kniazhestvos"  # kniazhestva
    assert plural("kobzar") == "kobzars"  # kobzari
    assert plural("oblast") == "oblasts"  # oblasti
    # spell-checker: enable


def test_plural_hebrew() -> None:
    """Hebrew plurals."""
    assert plural("cherub") == "cherubs"  # cherubim
    assert plural("seraph") == "seraphs"  # seraphim
    assert plural("matzah") == "matzahs"  # matzot
    assert plural("kibbutz") == "kibbutzes"  # kibbutzim


def test_plural_japanese() -> None:
    """Japanese plurals."""
    # assert plural("bentō") == "bentō" # spell-checker: disable-line
    # assert plural("otaku") == "otaku" # spell-checker: disable-line
    assert plural("samurai") == "samurai"
    assert plural("kimono") == "kimonos"
    assert plural("ninja") == "ninjas"
    assert plural("futon") == "futons"
    assert plural("tsunami") == "tsunamis"


def test_plural_maori() -> None:
    """Maori plurals."""
    # spell-checker: disable
    assert plural("kiwi") == "kiwis"  # kiwi
    assert plural("kowhai") == "kowhais"  # kowhai
    assert plural("Māori") == "Māori"
    # assert plural("marae") == "marae"
    assert plural("tui") == "tuis"
    assert plural("waka") == "waka"
    # spell-checker: enable


def test_plural_inuktitut() -> None:
    """Inuktitut plurals."""
    # spell-checker: disable
    # assert plural("Inuk") == "Inuit"
    # assert plural("inukshuk") == "inukshuit"
    # assert plural("Iqalummiuq") == "Iqalummiut"
    # assert plural("Nunavimmiuq") == "Nunavimmiut"
    # assert plural("Nunavummiuq") == "Nunavummiut"
    # spell-checker: enable


def test_plural_other_languages() -> None:
    """Other language plurals."""
    # spell-checker: disable
    assert plural("canoe") == "canoes"
    assert plural("cwm") == "cwms"  # not cwmyth
    assert plural("goulash") == "goulashes"  # not gulyasok
    assert plural("igloo") == "igloos"  # not igluit
    assert plural("kangaroo") == "kangaroos"
    assert plural("kayak") == "kayaks"  # kayait
    assert plural("kindergarten") == "kindergartens"  # not Kindergärten
    assert plural("ninja") == "ninjas"  # not ninja
    assert plural("pizza") == "pizzas"  # not pizze
    assert plural("sauna") == "saunas"  # not saunat
    # spell-checker: enable


def test_plural_compound_nouns() -> None:
    """Compound noun plurals (skipped)"""


def test_plural_letters() -> None:
    """Plurals of letters and abbreviations."""
    assert plural("h") == "h's"
    assert plural("p") == "p's"
    assert plural("q") == "q's"
    assert plural("i") == "i's"
    assert plural("t") == "t's"
    assert plural("1990") == "1990s"
    assert plural("but") == "buts"
    assert plural("MP") == "MPs"
    assert plural("p.") == "pp."
    assert plural("l.") == "ll."
    assert plural("f.") == "ff."
    assert plural("h.") == "hh."
    assert plural("P.") == "PP."
    assert plural("S.") == "SS."
    assert plural("s.") == "ss."
    assert plural("§") == "§§"
    assert plural("v.") == "vv."
    # assert plural("MS") == "MSS"
    # assert plural("op.") == "opp."


def test_plural_headless_nouns() -> None:
    """Headless nouns."""
    assert plural("lowlife") == "lowlifes"
    assert plural("sabretooth") == "sabretooths"  # spell-checker: disable-line
    assert plural("still life") == "still lifes"  # spell-checker: disable-line
    assert plural("tenderfoot") == "tenderfoots"
    # assert plural("Blackfoot") == "Blackfeet"


def test_plural_without_singular() -> None:
    """Plurals without singular."""
    assert plural("glasses") == "glasses"
    assert plural("pants") == "pants"
    assert plural("panties") == "panties"
    assert plural("pantyhose") == "pantyhose"
    assert plural("pliers") == "pliers"
    assert plural("scissors") == "scissors"
    assert plural("shorts") == "shorts"
    assert plural("tongs") == "tongs"
    assert plural("trousers") == "trousers"
    assert plural("clothes") == "clothes"


def test_plural_rare_singular() -> None:
    """Plurals with rare singular."""
    assert plural("nuptial") == "nuptials"
    # assert plural("phalanx") == "phalanges"
    assert plural("tiding") == "tidings"
    assert plural("victual") == "victuals"
    # assert plural("viscus") == "viscera"


def test_plural_mass_nouns() -> None:
    """Plurals of mass nouns (skipped)."""


def test_plural_as_singular() -> None:
    """Singulars as plural an d plurals as singular (skipped)."""


def test_plural_in_form_but_singular() -> None:
    """Plural in form but singular in construction."""
    # assert plural("billiards") == "billiards"
    # assert plural("measles") == "measles"
    # assert plural("news") == "news"
    # assert plural("mathematics") == "mathematics"
    # assert plural("physics") == "physics"
    # assert plural("aesthetics") == "aesthetics"


def test_plural_became_singular() -> None:
    """Plural form became a singular form."""
    assert plural("agenda") == "agendas"
    assert plural("algae") == "algae"
    # assert plural("biscotti") == "biscotti"
    assert plural("candelabra") == "candelabras"
    assert plural("data") == "data"
    # assert plural("graffiti") == "graffiti"
    assert plural("insignia") == "insignias"
    assert plural("opera") == "operas"
    assert plural("panini") == "paninis"
    # assert plural("paparazzi") == "paparazzi"
    # assert plural("spaghetti") == "spaghetti"
    # assert plural("taliban") == "taliban"
    assert plural("zucchini") == "zucchinis"

    assert plural("magazine") == "magazines"  # from Arabic via French

    assert plural("criterion") == "criteria"
    assert plural("phenomenon") == "phenomena"


def test_plural_back_formation() -> None:
    """Singulars via back-formation (skipped)."""


def test_plural_geographic() -> None:
    """Geographical plurals used as singular (skipped)."""


def test_plural_singular_collective() -> None:
    """Singulars with collective meaning treated as plural (skipped)."""


def test_plural_numbers() -> None:
    """Plurals of numbers (skipped)."""


def test_plural_determiners() -> None:
    """Determiner plurals."""
    assert plural("this") == "these"
    assert plural("that") == "those"


def test_plural_other() -> None:
    """Other plurals."""
    assert plural("yo-yo") == "yo-yos"
