import random

class AIJokeGenerator:
    def __init__(self):
        self.jokes = [
            "Why did the AI go to school? Because it wanted to be a neural scholar!",
            "Why don't AI agents tell secrets? Because they can't keep anything private!",
            "What do you call a machine learning model that plays the drums? A beat-learning algorithm!",
            "Why was the AI so bad at tennis? It couldn't find the optimal serve!",
            "Why was the AI programmer always broke? They kept losing their cache!",
            "Why did the AI refuse to play cards? It was afraid of the high stakes in poker!",
            "How did the computer scientist cure their insomnia? With neural REST!",
            "Why did the neural network go to the doctor? It had a bad case of overfitting!",
            "Why do AI agents make terrible comedians? They always forget the punch line!",
            "Why did the AI cross the road? To get to the other side of the data set!",
        ]

    def get_joke(self):
        return random.choice(self.jokes)

if __name__ == "__main__":
    joke_generator = AIJokeGenerator()
    print(joke_generator.get_joke())
