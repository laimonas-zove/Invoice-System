def amount_to_words(amount):
    units = ["nulis", "vienas", "du", "trys", "keturi", "penki", "šeši", "septyni", "aštuoni", "devyni"]
    teens = ["dešimt", "vienuolika", "dvylika", "trylika", "keturiolika", "penkiolika",
             "šešiolika", "septyniolika", "aštuoniolika", "devyniolika"]
    tens = ["", "", "dvidešimt", "trisdešimt", "keturiasdešimt", "penkiasdešimt",
            "šešiasdešimt", "septyniasdešimt", "aštuoniasdešimt", "devyniasdešimt"]
    hundreds = ["", "vienas šimtas", "du šimtai", "trys šimtai", "keturi šimtai", "penki šimtai",
                "šeši šimtai", "septyni šimtai", "aštuoni šimtai", "devyni šimtai"]

    def number_to_words(num):
        if num == 0:
            return "nulis"
        elif num < 10:
            return units[num]
        elif num < 20:
            return teens[num - 10]
        elif num < 100:
            u = num % 10
            return f"{tens[num // 10]} {units[u]}" if u != 0 else tens[num // 10]
        elif num < 1000:
            r = num % 100
            return f"{hundreds[num // 100]} {number_to_words(r)}" if r != 0 else hundreds[num // 100]
        elif num < 10000:
            t = num // 1000
            r = num % 1000
            t_part = "vienas tūkstantis" if t == 1 else f"{units[t]} tūkstančiai"
            return f"{t_part} {number_to_words(r)}" if r != 0 else t_part
        elif num < 100000:
            t = num // 1000
            r = num % 1000
            t_part = number_to_words(t) + " tūkstančių"
            return f"{t_part} {number_to_words(r)}" if r != 0 else t_part
        else:
            return "Skaičius per didelis"

    def euro_suffix(amount):
        if amount == 1:
            return "euras"
        elif 2 <= amount % 10 <= 9 and not (11 <= amount % 100 <= 19):
            return "eurai"
        else:
            return "eurų"

    def cent_suffix(amount):
        if amount == 1:
            return "centas"
        elif 2 <= amount % 10 <= 9 and not (11 <= amount % 100 <= 19):
            return "centai"
        else:
            return "centų"

    euros = int(amount)
    cents = int(round((amount - euros) * 100))

    words = f"{number_to_words(euros)} {euro_suffix(euros)} ir {cents:02d} {cent_suffix(cents)}"
    return words.capitalize()
