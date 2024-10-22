class Dog:
    def __init__(self, name):
        self.name = name
        print(f'이름은 {self.name}, 발이 4개다.')

    def speak(self):
        return '멍멍'