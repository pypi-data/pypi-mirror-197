

class RenkoPatternFinder:
    def __init__(self, data):
        self.data = data

    def check_patterns(self):
        if self.check_bullish_one_back():
            print("Bullish one back found")
        elif self.check_bearish_one_back():
            print("Bearish one back found")
        elif self.check_bullish_zig_zag():
            print("Bullish zig zag found")
        elif self.check_bearish_zig_zag():
            print("Bearish zig zag found")
        elif self.check_bullish_two_back():
            print("Bullish two back found")
        elif self.check_bearish_two_back():
            print("Bearish two back found")
        elif self.check_bullish_swing_breakout():
            print("Bullish swing breakout found")
        elif self.check_bearish_swing_breakout():
            print("Bearish swing breakout found")
        else:
            print("No patterns found")

    def check_bullish_one_back(self):
        if (
                self.data[-1]["type"] == "up" and
                self.data[-2]["type"] == "up" and
                self.data[-3]["type"] == "down" and
                self.data[-4]["type"] == "up" and
                self.data[-5]["type"] == "up"):
            return True
        else:
            return False

    def check_bearish_one_back(self):
        if (
                self.data[-1]["type"] == "down"
                and self.data[-2]["type"] == "down"
                and self.data[-3]["type"] == "up"
                and self.data[-4]["type"] == "down"
                and self.data[-5]["type"] == "down"):
            return True
        else:
            return False

    def check_bullish_zig_zag(self):
        if (
                self.data[-1]["type"] == "up" and
                self.data[-2]["type"] == "up" and
                self.data[-3]["type"] == "down" and
                self.data[-4]["type"] == "up" and
                self.data[-5]["type"] == "down"):
            return True
        else:
            return False

    def check_bearish_zig_zag(self):
        if (
                self.data[-1]["type"] == "down" and
                self.data[-2]["type"] == "down" and
                self.data[-3]["type"] == "up" and
                self.data[-4]["type"] == "down" and
                self.data[-5]["type"] == "up"):
            return True
        else:
            return False

    def check_bullish_two_back(self):
        if (
                self.data[-1]["type"] == "up" and
                self.data[-2]["type"] == "up" and
                self.data[-3]["type"] == "up" and
                self.data[-4]["type"] == "down" and
                self.data[-5]["type"] == "down" and
                self.data[-6]["type"] == "up" and
                self.data[-7]["type"] == "up" and
                self.data[-8]["type"] == "up"):
            return True
        else:
            return False

    def check_bearish_two_back(self):
        if (
                self.data[-1]["type"] == "down" and
                self.data[-2]["type"] == "down" and
                self.data[-3]["type"] == "down" and
                self.data[-4]["type"] == "up" and
                self.data[-5]["type"] == "up" and
                self.data[-6]["type"] == "down" and
                self.data[-7]["type"] == "down" and
                self.data[-8]["type"] == "down"):
            return True
        else:
            return False

    def check_bullish_swing_breakout(self):
        if self.data[-1]["type"] == "up":
            temp_data = self.data
            temp_data.reverse()
            up_count = 0
            for b in temp_data:
                if b["type"] == "up":
                    up_count = up_count + 1
                else:
                    break

            down_count = 0
            down_reached = False
            for b in temp_data:
                if b["type"] == "up" and down_reached is False:
                    continue
                elif b["type"] == "up" and down_reached is True:
                    break
                else:
                    down_count = down_count + 1
                    down_reached = True

            if up_count - down_count == 1:
                return True
        else:
            return False

    def check_bearish_swing_breakout(self):
        if self.data[-1]["type"] == "down":
            temp_data = self.data
            temp_data.reverse()
            down_count = 0
            for b in temp_data:
                if b["type"] == "down":
                    down_count = down_count + 1
                else:
                    break

            up_count = 0
            up_reached = False
            for b in temp_data:
                if b["type"] == "down" and up_reached is False:
                    continue
                elif b["type"] == "down" and up_reached is True:
                    break
                else:
                    up_count = up_count + 1
                    up_reached = True

            if down_count - up_count == 1:
                return True
        else:
            return False
