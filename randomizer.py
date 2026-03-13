import random

WORD_LISTS = {
    "anatomy": [
        "abs focus", "belly", "belly button", "chest", "skin",
        "eyes", "hair", "lips", "mouth", "neck", "brown skin", "dark skin",
        "stomach", "tongue", "waist", "soft skin", "warm skin", "blonde hair",
        "hips", "legs", "smooth legs", "thick thighs", "thigh gap", "thighs", "red hair",
    ],
    "clothing_base": [
        "clothing", "dress", "hosiery", "skirt", "socks", "stockings", 
        "hero", "superhero", "latex", "leather", "leather outfit", 
        "lycra", "satin", "silk", "spandex", "vinyl",
        "boots", "high heels", "police uniform", "uniform", 
        "stiletto", "maid outfit",
    ],
    "sensory_tactile_and_food": [
        "biting", "flavor", "ice on skin", "honey",
        "texture", "grapes", "truffles", "chili peppers",
        "strawberries", "caramel", "maple syrup", "mango", "pomegranate", "kiwi",
        "red wine",
    ],
    "power_dynamics": [
        "command her", "command him", "control", "serve", 
        "dominant", "goddess", "master", "obey", "obedient servant",
    ],
    "fantasy_scenarios": [
        "in a nightclub", "in a parking lot", "on the plane", "airplain",
        "in a bar", "in a cafe", "vampire bite fantasy", "in a car", "in a taxi", 
        "public transportation", "in the forest", "on the roof", "on the beach", 
        "on the balcony", "crowded metro", "crowded train", "crowded bus", 
        "crowded subway", "crowded restaurant", "on the metro", "on the train", 
        "on the bus", "on the subway", "in a restaurant", "in the library", 
        "in the locker room", "in the changing room",
    ],
    "generic_stuff": [
        "close up view", "zoom in on", "wet", "sweaty", "focus closely on", 
        "focus on her", "snowing", "focus on his", "in detail", "very detailed", 
        "sensual", "seductive", "snow",
    ],
}

def randomizer() -> str:
    all_keys = list(WORD_LISTS.keys())
    num_categories = len(all_keys)
    count = random.randint(3, num_categories - 1)
    chosen_keys = random.sample(all_keys, k=count)
    words = [random.choice(WORD_LISTS[key]) for key in chosen_keys]
    random.shuffle(words)
    always_include = ", realistic, high quality"
    return ", ".join(words) + always_include

if __name__ == "__main__":
    result = randomizer()
    print("Randomized output:", result)
