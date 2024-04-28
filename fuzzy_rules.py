import re
import utils

class Rule:
    def __init__(self):
        pass

    
    @staticmethod
    def operator(val1, val2, op):
        match op:
            case 'and':
                return min(val1, val2)
            case 'or':
                return max(val1, val2)
            case 'not':
                if val1 is not None:
                    return 1 - val1
                elif val2 is not None:
                    return 1 - val2
                else:
                    return None
            case default:
                return None

    def calculate(self, dictionary):

        # AND -> min()
        # OR -> max()
        # NOT -> 1 - x
        education = dictionary['education']
        experience = dictionary['experience']
        soft_skills = dictionary['soft_skills']
        volunteering = dictionary['volunteering']
        suitability = dict()

        #suitability['very low'] = Rule.calc_very_low(education, experience, soft_skills, volunteering)
        suitability['low'] = Rule.calc_low(education, experience, soft_skills, volunteering)
        suitability['average'] = Rule.calc_average(education, experience, soft_skills, volunteering)
        suitability['good'] = Rule.calc_good(education, experience, soft_skills, volunteering)
        return suitability

    @staticmethod
    def calc_low(education, experience, soft_skills, volunteering):
        r1 = Rule.lowr1(education, experience, soft_skills, volunteering)
        r2 = Rule.lowr2(education, experience, soft_skills, volunteering)
        return max(r1, r2)

    @staticmethod
    def calc_average(education, experience, soft_skills, volunteering):
        r1 = Rule.avgr1(education, experience, soft_skills, volunteering)
        r2 = Rule.avgr2(education, experience, soft_skills, volunteering)
        r3 = Rule.avgr3(education, experience, soft_skills, volunteering)
        return max(r1, r2, r3)

    @staticmethod
    def calc_good(education, experience, soft_skills, volunteering):
        r1 = Rule.goodr1(education, experience, soft_skills, volunteering)
        r2 = Rule.goodr2(education, experience, soft_skills, volunteering)
        r3 = Rule.goodr3(education, experience, soft_skills, volunteering)
        return max(r1, r2, r3)

    #
    # ----------------------- GOOD ------------------------------
    #
    @staticmethod
    def goodr1(education, experience, soft_skills, volunteering):
        p1 = Rule.operator(education['high'], experience['high'], 'and')
        p2 = Rule.operator(soft_skills['low'], None, 'not')
        p3 = Rule.operator(p1, p2, 'and')
        return p3

    @staticmethod
    def goodr2(education, experience, soft_skills, volunteering):
        p1 = Rule.operator(education['high'], experience['average'], 'and')
        p2 = Rule.operator(p1, soft_skills['great'], 'and')
        return p2

    @staticmethod
    def goodr3(education, experience, soft_skills, volunteering):
        p1 = Rule.operator(experience['high'], experience['average'], 'or')
        p2 = Rule.operator(education['average'], p1, 'and')
        p3 = Rule.operator(p2, soft_skills['great'], 'and')
        return p3

    #
    # ------------------------ AVERAGE -------------------------
    #
    @staticmethod
    def avgr1(education, experience, soft_skills, volunteering):
        p1 = Rule.operator(education['high'], experience['average'], 'and')
        p2 = Rule.operator(p1, soft_skills['decent'], 'and')
        return p2

    @staticmethod
    def avgr2(education, experience, soft_skills, volunteering):
        p1 = Rule.operator(education['high'], education['average'], 'or')
        p2 = Rule.operator(p1, experience['low'], 'and')
        p3 = Rule.operator(p2, soft_skills['great'], 'and')
        return p3

    @staticmethod
    def avgr3(education, experience, soft_skills, volunteering):
        p1 = Rule.operator(experience['high'], experience['average'], 'or')
        p2 = Rule.operator(p1, education['low'], 'and')
        p3 = Rule.operator(p2, soft_skills['great'], 'and')
        return p3

    #
    # ------------------------- LOW ------------------------------
    #
    @staticmethod
    def lowr1(education, experience, soft_skills, volunteering):
        return Rule.operator(education['low'], experience['low'], 'and')

    @staticmethod
    def lowr2(education, experience, soft_skills, volunteering):
        p1 = Rule.operator(education['high'], education['average'], 'or')
        p2 = Rule.operator(experience['high'], experience['average'], 'or')
        p3 = Rule.operator(p1, p2, 'and')
        p4 = Rule.operator(p3, soft_skills['low'], 'and')
        return p4












                              