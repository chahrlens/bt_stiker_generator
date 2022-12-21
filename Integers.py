class INTEGERS:
    def __init__(self):
        self.num = 0
    def int_from_string(self, string = '') -> int:
        try:
            self.num = int(string)
        except ValueError:
            print("Oops!  That was no valid number.  Try again...")
        return self.num
    def get_int(self) -> int:
        try:
            self.num = int(input())
        except ValueError:
            print("Oops!  That was no valid number.  Try again...")
        return self.num
    
    def get_int_wmsg(self, string = '') -> int:
        n = None
        while n == None:
            try:
                self.num = int(input(string))
                n = 1
            except ValueError:
                print("Oops!  That was no valid number.  Try again...")
                n = None
        return self.num
