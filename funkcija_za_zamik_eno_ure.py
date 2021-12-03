
def eno_uro_nazaj(ura):

    if ura[17:19] == "00":
        return ura[:17] + "23" + ura[19:]

    elif ura[17:19] == "10":
        return ura[:17] + "09" + ura[19:]

    elif ura[17:18] == "0":
        return ura[:17] + "0" + str(int(ura[17:19]) - 1) + ura[19:]
    else:
        return ura[:17] + str(int(ura[17:19])-1) + ura[19:]

