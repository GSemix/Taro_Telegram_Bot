"""
Some quick functions
"""
# Возвращает строку в формате: [s] text
def get_log(s: str, text: str) -> str:
    """Returns a string in the form: [s] text

    :param s: A string characterizing the mood of the log
    :type s: str
    :param text: Main log text
    :type text: str
    :returns: f"[{s}] {text}"
    :rtype: str
    """

    return f"[{s}] {text}"

# Возвращает строку в формате: id : [s] text
def get_log_with_id(id: int, s: str, text: str) -> str:
    """Returns a string in the form: id : [s] text

    :param id: User's id
    :type id: int
    :param s: A string characterizing the mood of the log
    :type s: str
    :param text: Main log text
    :type text: str
    :returns: f"{id} : [{s}] {text}"
    :rtype: str
    """

    return f"{id} : [{s}] {text}"

# Проверяет, можно ли преобразовать строку в int
def isInt(s: str) -> bool:
    """Returns can str be converted to int

    :param s: A string for examination
    :type s: str
    :returns: True/False
    :rtype: bool
    :raises ValueError: If s contains more than just numbers
    """

    try:
        int(s)
        return True
    except ValueError:
        return False
    
# Проверяет, можно ли преобразовать строку в float
def isFloat(s: str) -> bool:
    """Returns can str be converted to float

    :param s: A string for examination
    :type s: str
    :returns: True/False
    :rtype: bool
    :raises ValueError: If s contains more than just numbers and '.'
    """

    try:
        float(s)
        return True
    except ValueError:
        return False






