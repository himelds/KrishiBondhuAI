def get_advice(data):
    disease = data["disease"]["disease"]
    weather = data["weather"]

    if weather["rain"]:
        spray = "এখন স্প্রে করবেন না"
    else:
        spray = "এখন স্প্রে করা যেতে পারে"

    return f"""
এই ধানে {disease} রোগ দেখা গেছে।

চিকিৎসা:
উপযুক্ত ছত্রাকনাশক ব্যবহার করুন।

পরামর্শ:
{spray}

সতর্কতা:
উচ্চ আর্দ্রতায় রোগের ঝুঁকি বেশি।
"""