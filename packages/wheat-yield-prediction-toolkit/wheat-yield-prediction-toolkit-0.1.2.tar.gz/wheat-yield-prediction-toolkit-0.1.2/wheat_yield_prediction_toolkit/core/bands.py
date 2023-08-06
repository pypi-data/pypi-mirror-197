def addAllBandsSentinal(image):
    ndvi = image.normalizedDifference(["B8", "B4"]).rename("NDVI")

    evi = image.expression(
        "2.5 * ((nir - red) / (nir + 6 * red - 7.5 * blue + 1))",
        {"nir": image.select("B8"), "red": image.select("B4"), "blue": image.select("B2")},
    ).rename("EVI")

    savi = image.expression(
        "((nir - red) / (nir + red + L)) * (1 + L)",
        {"nir": image.select("B8"), "red": image.select("B4"), "L": 0.5},
    ).rename("SAVI")

    arvi = image.expression(
        "(nir - (red - 1 * (blue - red))) / (nir + (red - 1 * (blue - red)))",
        {"nir": image.select("B8"), "red": image.select("B4"), "blue": image.select("B2")},
    ).rename("ARVI")
    gci = image.expression(
        "(nir / green) - 1", {"nir": image.select("B8"), "green": image.select("B3")}
    ).rename("GCI")

    gmr = image.expression("(g - r)", {"g": image.select("B3"), "r": image.select("B4")}).rename(
        "GMR"
    )

    exg = image.expression(
        "2.0 * green - red - blue",
        {"green": image.select("B3"), "red": image.select("B4"), "blue": image.select("B2")},
    ).rename("EXG")

    gdvi = image.normalizedDifference(["B8", "B3"]).rename("GDVI")
    rvi = image.expression(
        "nir / red", {"nir": image.select("B8"), "red": image.select("B4")}
    ).rename("RVI")

    grvi = image.expression(
        "nir / green", {"nir": image.select("B8"), "green": image.select("B3")}
    ).rename("GRVI")

    cigreen = image.expression(
        "(nir / green) - 1", {"nir": image.select("B8"), "green": image.select("B3")}
    ).rename("CIgreen")

    gr = image.expression(
        "green / red", {"green": image.select("B3"), "red": image.select("B4")}
    ).rename("GR")

    gb = image.expression(
        "green / blue", {"green": image.select("B3"), "blue": image.select("B2")}
    ).rename("GB")

    nri = image.expression(
        "red / (red + green + blue)",
        {"red": image.select("B4"), "green": image.select("B3"), "blue": image.select("B2")},
    ).rename("NRI")

    ngi = image.expression(
        "green / (red + green + blue)",
        {"green": image.select("B3"), "red": image.select("B4"), "blue": image.select("B2")},
    ).rename("NGI")

    rdvi = image.expression(
        "(nir - red) / sqrt(nir + red)", {"nir": image.select("B8"), "red": image.select("B4")}
    ).rename("RDVI")

    msr = image.expression(
        "(nir / red - 1) / sqrt(nir / red + 1)",
        {"nir": image.select("B8"), "red": image.select("B4")},
    ).rename("MSR")

    list_of_bands = [
        ndvi,
        evi,
        savi,
        arvi,
        gci,
        gmr,
        exg,
        gdvi,
        rvi,
        grvi,
        cigreen,
        gb,
        nri,
        ngi,
        rdvi,
        msr,
        gr,
    ]

    return image.addBands(list_of_bands)


def addAllBandsLandsat(image):
    """
    Use the following bands to calculate vegeterien indecies :
        - SR_B1 : Band 1 (blue) surface reflectance
        - SR_B2 : Band 2 (green) surface reflectance
        - SR_B3 : Band 3 (red) surface reflectance
        - SR_B4 : Band 4 (near-infrared) surface reflectance
        - SR_B5 : Band 5 (shortwave infrared 1) surface reflectance
        - SR_B7 : Band 7 (shortwave infrared 2) surface reflectance
    """

    ndvi = image.normalizedDifference(["SR_B4", "SR_B3"]).rename("NDVI")

    evi = image.expression(
        "2.5 * ((nir - red) / (nir + 6 * red - 7.5 * blue + 1))",
        {"nir": image.select("SR_B4"), "red": image.select("SR_B3"), "blue": image.select("SR_B1")},
    ).rename("EVI")

    savi = image.expression(
        "((nir - red) / (nir + red + L)) * (1 + L)",
        {"nir": image.select("SR_B4"), "red": image.select("SR_B3"), "L": 0.5},
    ).rename("SAVI")

    arvi = image.expression(
        "(nir - (red - 1 * (blue - red))) / (nir + (red - 1 * (blue - red)))",
        {"nir": image.select("SR_B4"), "red": image.select("SR_B3"), "blue": image.select("SR_B1")},
    ).rename("ARVI")
    gci = image.expression(
        "(nir / green) - 1", {"nir": image.select("SR_B4"), "green": image.select("SR_B2")}
    ).rename("GCI")

    gmr = image.expression(
        "(g - r)", {"g": image.select("SR_B2"), "r": image.select("SR_B3")}
    ).rename("GMR")

    exg = image.expression(
        "2.0 * green - red - blue",
        {
            "green": image.select("SR_B2"),
            "red": image.select("SR_B3"),
            "blue": image.select("SR_B1"),
        },
    ).rename("EXG")

    gdvi = image.normalizedDifference(["SR_B4", "SR_B2"]).rename("GDVI")
    rvi = image.expression(
        "nir / red", {"nir": image.select("SR_B4"), "red": image.select("SR_B3")}
    ).rename("RVI")

    grvi = image.expression(
        "nir / green", {"nir": image.select("SR_B4"), "green": image.select("SR_B2")}
    ).rename("GRVI")

    cigreen = image.expression(
        "(nir / green) - 1", {"nir": image.select("SR_B4"), "green": image.select("SR_B2")}
    ).rename("CIgreen")

    gr = image.expression(
        "green / red", {"green": image.select("SR_B2"), "red": image.select("SR_B3")}
    ).rename("GR")

    gb = image.expression(
        "green / blue", {"green": image.select("SR_B2"), "blue": image.select("SR_B1")}
    ).rename("GB")

    nri = image.expression(
        "red / (red + green + blue)",
        {
            "red": image.select("SR_B3"),
            "green": image.select("SR_B2"),
            "blue": image.select("SR_B1"),
        },
    ).rename("NRI")

    ngi = image.expression(
        "green / (red + green + blue)",
        {
            "green": image.select("SR_B2"),
            "red": image.select("SR_B3"),
            "blue": image.select("SR_B1"),
        },
    ).rename("NGI")

    rdvi = image.expression(
        "(nir - red) / sqrt(nir + red)",
        {"nir": image.select("SR_B4"), "red": image.select("SR_B3")},
    ).rename("RDVI")

    msr = image.expression(
        "(nir / red - 1) / sqrt(nir / red + 1)",
        {"nir": image.select("SR_B4"), "red": image.select("SR_B3")},
    ).rename("MSR")

    list_of_bands = [
        ndvi,
        evi,
        savi,
        arvi,
        gci,
        gmr,
        exg,
        gdvi,
        rvi,
        grvi,
        cigreen,
        gb,
        nri,
        ngi,
        rdvi,
        msr,
        gr,
    ]

    return image.addBands(list_of_bands)
