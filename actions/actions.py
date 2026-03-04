# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

import random
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet



# Dictionary of quotes organized by category and mood
QUOTES_DATABASE = {
    "motivation": [
        {"text": "The only way to do great work is to love what you do.", "author": "Steve Jobs", "mood_boost": "high"},
        {"text": "Success is not final, failure is not fatal: it is the courage to continue that counts.", "author": "Winston Churchill", "mood_boost": "high"},
        {"text": "Believe you can and you're halfway there.", "author": "Theodore Roosevelt", "mood_boost": "high"},
        {"text": "Don't watch the clock; do what it does. Keep going.", "author": "Sam Levenson", "mood_boost": "high"},
        {"text": "The future depends on what you do today.", "author": "Mahatma Gandhi", "mood_boost": "medium"},
        {"text": "You miss 100% of the shots you don't take.", "author": "Wayne Gretzky", "mood_boost": "high"},
        {"text": "Act as if what you do makes a difference. It does.", "author": "William James", "mood_boost": "medium"},
        {"text": "Well done is better than well said.", "author": "Benjamin Franklin", "mood_boost": "medium"},
        {"text": "It is during our darkest moments that we must focus to see the light.", "author": "Aristotle", "mood_boost": "high"},
        {"text": "The only impossible journey is the one you never begin.", "author": "Tony Robbins", "mood_boost": "high"},
    ],
    "inspiration": [
        {"text": "The future belongs to those who believe in the beauty of their dreams.", "author": "Eleanor Roosevelt", "mood_boost": "high"},
        {"text": "It does not matter how slowly you go as long as you do not stop.", "author": "Confucius", "mood_boost": "medium"},
        {"text": "You are capable of amazing things.", "author": "Unknown", "mood_boost": "high"},
        {"text": "Great things never come from comfort zones.", "author": "Unknown", "mood_boost": "high"},
        {"text": "Dream it. Wish it. Do it.", "author": "Unknown", "mood_boost": "high"},
        {"text": "Success doesn't just find you. You have to go out and get it.", "author": "Unknown", "mood_boost": "medium"},
        {"text": "The harder you work for something, the greater you'll feel when you achieve it.", "author": "Unknown", "mood_boost": "medium"},
        {"text": "Dream bigger. Do bigger.", "author": "Unknown", "mood_boost": "high"},
        {"text": "Your limitation—it's only your imagination.", "author": "Unknown", "mood_boost": "high"},
        {"text": "Great things are done by people who believe in what they are doing.", "author": "Unknown", "mood_boost": "high"},
    ],
    "love": [
        {"text": "The heart has its reasons which reason knows nothing of.", "author": "Blaise Pascal", "mood_boost": "medium"},
        {"text": "To love oneself is the beginning of a lifelong romance.", "author": "Oscar Wilde", "mood_boost": "high"},
        {"text": "Love is composed of a single soul inhabiting two bodies.", "author": "Aristotle", "mood_boost": "medium"},
        {"text": "The greatest happiness of life is the conviction that we are loved.", "author": "Victor Hugo", "mood_boost": "high"},
        {"text": "Love all, trust a few, do wrong to none.", "author": "William Shakespeare", "mood_boost": "medium"},
        {"text": "The best and most beautiful things in this world cannot be seen or even heard, but must be felt with the heart.", "author": "Helen Keller", "mood_boost": "high"},
        {"text": "Love is not just looking at each other, it's looking in the same direction.", "author": "Antoine de Saint-Exupéry", "mood_boost": "medium"},
        {"text": "You don't love someone for their looks, or their clothes, or their fancy car, but because they sing a song only you can hear.", "author": "Oscar Wilde", "mood_boost": "high"},
    ],
    "success": [
        {"text": "Success is walking from failure to failure with no loss of enthusiasm.", "author": "Winston Churchill", "mood_boost": "high"},
        {"text": "The only impossible journey is the one you never begin.", "author": "Tony Robbins", "mood_boost": "high"},
        {"text": "Success is not about being the best, it's about being better than you were yesterday.", "author": "Unknown", "mood_boost": "medium"},
        {"text": "Success usually comes to those who are too busy to be looking for it.", "author": "Henry David Thoreau", "mood_boost": "medium"},
        {"text": "Don't aim for success if you want it; just do what you love and believe in, and it will come naturally.", "author": "David Frost", "mood_boost": "high"},
        {"text": "The way to get started is to quit talking and begin doing.", "author": "Walt Disney", "mood_boost": "high"},
        {"text": "Success is not final, failure is not fatal.", "author": "Winston Churchill", "mood_boost": "medium"},
        {"text": "Your success and happiness lies in you.", "author": "Unknown", "mood_boost": "medium"},
        {"text": "Success is a journey, not a destination.", "author": "Unknown", "mood_boost": "medium"},
    ],
    "funny": [
        {"text": "I told my computer I needed a break, and now it won't stop sending me Kit-Kat ads.", "author": "Unknown", "mood_boost": "high"},
        {"text": "Why did the scarecrow win an award? Because he was outstanding in his field!", "author": "Unknown", "mood_boost": "high"},
        {"text": "I'm not lazy, I'm just on energy-saving mode.", "author": "Unknown", "mood_boost": "high"},
        {"text": "My room is not dirty, it's just organized on a chaotic level that only I understand.", "author": "Unknown", "mood_boost": "high"},
        {"text": "I told my wife she was drawing her eyebrows too high. She looked surprised.", "author": "Unknown", "mood_boost": "high"},
        {"text": "I'm reading a book about anti-gravity. It's impossible to put down!", "author": "Unknown", "mood_boost": "high"},
        {"text": "I would avoid the sushi if I were you. It's a little fishy.", "author": "Unknown", "mood_boost": "medium"},
        {"text": "Time flies like an arrow. Fruit flies like a banana.", "author": "Unknown", "mood_boost": "medium"},
        {"text": "I used to play piano by ear, but now I use my hands.", "author": "Unknown", "mood_boost": "high"},
    ],
    "stress_relief": [
        {"text": "Rest when you're weary. Refresh your spirit. Take a moment for yourself.", "author": "Unknown", "mood_boost": "high"},
        {"text": "You cannot pour from an empty cup. Take time to fill yours first.", "author": "Unknown", "mood_boost": "high"},
        {"text": "It's okay to take a step back. Deep breaths, my friend.", "author": "Unknown", "mood_boost": "medium"},
        {"text": "This too shall pass. Better days are coming.", "author": "Unknown", "mood_boost": "high"},
        {"text": "Your mental health is a priority, not a luxury.", "author": "Unknown", "mood_boost": "high"},
        {"text": "Slow down. You don't have to do everything right now.", "author": "Unknown", "mood_boost": "high"},
    ],
    "resilience": [
        {"text": "It is not the mountain we conquer, but ourselves.", "author": "Sir Edmund Hillary", "mood_boost": "high"},
        {"text": "What lies behind us and what lies before us are tiny matters compared to what lies within us.", "author": "Ralph Waldo Emerson", "mood_boost": "high"},
        {"text": "The cave you fear to enter holds the treasure you seek.", "author": "Joseph Campbell", "mood_boost": "high"},
        {"text": "You are braver than you believe, stronger than you seem, and smarter than you think.", "author": "A.A. Milne", "mood_boost": "high"},
        {"text": "Out of suffering have emerged the strongest souls.", "author": "Khalil Gibran", "mood_boost": "high"},
    ]
}


class QuoteAction(Action):
    """Base action that selects a random quote from a named category.

    Subclasses simply set the `category` class variable to one of the
    keys defined in `QUOTES_DATABASE` and the inherited `name` method will
    return the appropriate action name.
    """

    category: Text = ""  # must be overridden by subclasses

    def name(self) -> Text:
        return f"action_deliver_{self.category}"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # choose a random quote for this action's category
        quotes = QUOTES_DATABASE.get(self.category, [])
        if not quotes:
            dispatcher.utter_message(text="Sorry, I don't have any quotes right now.")
            return []

        # avoid repeating quotes already shown in this session
        used = tracker.get_slot("used_quotes") or []
        # flat list of texts; simply filter by text
        available = [q for q in quotes if q["text"] not in used]
        if not available:
            # everything used already, reset for this category only
            available = quotes
            used = []
        quote = random.choice(available)
        used.append(quote["text"])

        # construct a human-friendly prefix (handle vowel-starting categories)
        article = "an" if self.category and self.category[0].lower() in "aeiou" else "a"
        prefix_word = self.category
        # make category more readable for user if needed
        if self.category == "motivation":
            prefix_word = "motivational"
        elif self.category == "inspiration":
            prefix_word = "inspirational"
        message = f"Here's {article} {prefix_word} quote for you:\n\"{quote['text']}\" - {quote['author']}"
        dispatcher.utter_message(text=message)
        # persist used quotes so the same quote isn't shown twice
        return [SlotSet("used_quotes", used)]


# MOOD-BASED RECOMMENDATION ACTION
class ActionMoodBasedRecommendation(Action):
    """Action that recommends quotes based on the user's mood."""

    def name(self) -> Text:
        return "action_mood_based_recommendation"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # Get the user's mood from the mood slot
        mood = tracker.get_slot("mood")

        if not mood:
            dispatcher.utter_message(text="I didn't catch your mood. Could you tell me how you're feeling?")
            return []

        # Map moods to appropriate quote categories
        mood_quote_mapping = {
            "great": ["funny", "success", "inspiration"],
            "good": ["motivation", "inspiration", "success"],
            "neutral": ["motivation", "inspiration"],
            "sad": ["stress_relief", "resilience", "love", "inspiration"],
            "unhappy": ["resilience", "stress_relief", "motivation", "love"],
            "stressed": ["stress_relief", "resilience", "funny"],
            "anxious": ["stress_relief", "resilience", "inspiration"],
        }

        # Select quote categories based on mood
        categories = mood_quote_mapping.get(mood, ["motivation", "inspiration"])
        category = random.choice(categories)

        # Get a random quote from the selected category
        quotes = QUOTES_DATABASE.get(category, [])
        if not quotes:
            dispatcher.utter_message(text="I'm sorry, I couldn't find a suitable quote for your mood right now.")
            return []

        quote = random.choice(quotes)
        
        # Personalize the message based on mood
        mood_messages = {
            "great": "That's amazing! Here's something to celebrate your great mood:",
            "good": "Wonderful! Here's a thought to brighten your good day:",
            "neutral": "Let me share something to inspire you:",
            "sad": "I'm sorry you're feeling down. Here's something to lift your spirits:",
            "unhappy": "Things can get better. Here's a message of hope for you:",
            "stressed": "Take a moment. Here's something to help ease your stress:",
            "anxious": "You've got this! Here's a reminder of your strength:",
        }
        
        prefix = mood_messages.get(mood, "Here's a quote for you:")
        message = f"{prefix}\n\n\"{quote['text']}\" - {quote['author']}"
        dispatcher.utter_message(text=message)
        return []


# concrete actions ----
class ActionDeliverMotivation(QuoteAction):
    category = "motivation"


class ActionDeliverInspiration(QuoteAction):
    category = "inspiration"


class ActionDeliverLove(QuoteAction):
    category = "love"


class ActionDeliverSuccess(QuoteAction):
    category = "success"


class ActionDeliverFunny(QuoteAction):
    category = "funny"
