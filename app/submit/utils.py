from app.utils.colors_enum import Color
import sys

def get_result(verdicts):
    if 'RE' in verdicts:
        return 'Chyba počas kompilácie'
    if 'WA' in verdicts:
        return 'Zlá odpoveď'
    if 'TLE' in verdicts:
        return 'Prekročený časový limit'
    return 'Akceptovaný'

def get_result_color(verdicts):
    if all(verdict == 'AC' for verdict in verdicts):
        return Color.ACCEPTED.value
    if 'TLE' in verdicts:
        return Color.TIME_LIMIT_EXCEEDED.value
    return Color.WRONG_ANSWER.value

def get_result_color_helper(verdict):
    if verdict == 'AC':
        return Color.ACCEPTED.value
    if verdict == 'TLE':
        return Color.TIME_LIMIT_EXCEEDED.value
    return Color.WRONG_ANSWER.value

def verdict_to_word(verdicts):
    res = []
    for i in verdicts:
        if i == 'AC':
            res.append('Akceptovaný')
        elif i == 'RE':
            res.append('Chyba počas kompilácie')
        elif i == 'WA':
            res.append('Zlá odpoveď')
        elif i == 'TLE':
            res.append('Prekročený časový limit')
    return res

def get_verdicts_colors(verdicts):
    res = []
    for i in verdicts:
        res.append(get_result_color_helper(i))
    return res