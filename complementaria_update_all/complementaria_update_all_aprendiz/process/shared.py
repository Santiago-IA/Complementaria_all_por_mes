def get_class_name(module_name):
    words_module = module_name.split(".")[1]
    words_module = words_module.split(" ")
    words_capitalize = [word.capitalize() for word in words_module]
    words_capitalize = "".join(words_capitalize)
    return words_capitalize
