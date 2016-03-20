from datetime import timedelta


class title_criteria:
    def __init__(self, title, min_score, user_account_time):
        self.title = title
        self.min_score = min_score
        self.time = user_account_time

    def meets_min_score(self, score):
        if self.min_score:
            if score > self.min_score:
                return True
            else:
                return False
        return True  # no min score

    def meets_account_time(self, new_time):
        if self.time:
            if self.time > new_time:
                return True
            else:
                return False
        return True



titles = [title_criteria("Grand Punmaster", 100, None),
          title_criteria("Punter", 10, timedelta(days=5)),
          title_criteria("Punzodia", 500, None),
          title_criteria("Noob", 1, timedelta(days=5)),
          title_criteria("poop", 1, None)]
