import random


class EnemyLogic:

    # Selecting a card is based on multiple layers of logic, each which select cards to play targeting a specific
    # scenario and add it to a list of possible plays. Ultimately a random card is picked from the possible plays
    # list.

    # This means that the AI won't always pick the best possible play but by controlling how many instances of each
    # card are in the possible plays array, you can increase the odds of a specific card being played.

    # The AI should not be allowed to cheat by looking at information it otherwise wouldn't have, such as the players
    # Current hand! If we want to implement extreme logic it could card count and try to predict a pattern, but it must
    # not just look.
    @staticmethod
    def select_card(enemy, player_health, game_difficulty):
        cards_in_cost = [card for card in enemy.deck.hand if card.cost <= enemy.cost]

        possible_plays = []
        possible_plays += cards_in_cost  # Add any card which can be played

        # The following methods add best play scenarios
        possible_plays += EnemyLogic.cards_that_kill(cards_in_cost, player_health) * game_difficulty
        possible_plays += EnemyLogic.heal_cards_worth_playing(cards_in_cost, enemy)

        best_card_allows_another_to_be_played = EnemyLogic.best_card_that_allows_another_card_to_be_played(
            cards_in_cost, enemy)
        if best_card_allows_another_to_be_played is not None:
            possible_plays.append(best_card_allows_another_to_be_played)

        if not possible_plays:
            return None  # No possible plays, enemy should end their turn

        return random.choice(possible_plays)

    # Identifies any cards that would allow the enemy to kill the player
    @staticmethod
    def cards_that_kill(playable_cards, player_health):
        return [card for card in playable_cards if card.card_type == "attack" and card.power >= player_health]

    """
    Identifies any heal cards that are worth playing.
    
    If the enemy's current health is below 30% of their max health, all healing cards are considered worth playing.
    
    Otherwise, a card is considered worth playing if the amount of healing power that would exceed the enemy's maximum 
    health is less than or equal to 20% of the card's total healing power. AKA up to 20% of the cards total heal can be
    wasted due to max health before it decides the card is not worth playing
    """

    @staticmethod
    def heal_cards_worth_playing(playable_cards, enemy):
        # Determine the threshold for excess healing
        excess_healing_threshold = 0.2

        # If the enemy's current health is less than 50% of max, all heal cards are worth playing
        if enemy.cur_health <= 0.3 * enemy.max_health:
            return [card for card in playable_cards if card.card_type == "heal"]

        # Otherwise, use the previous logic
        heal_cards_worth_playing = []
        for card in playable_cards:
            if card.card_type == "heal":
                # Calculate how much the card would heal beyond the current health
                excess_healing = max(0, card.power - (enemy.max_health - enemy.cur_health))
                # Check if the card's excess healing is within the acceptable threshold
                if excess_healing / card.power <= excess_healing_threshold:
                    heal_cards_worth_playing.append(card)

        return heal_cards_worth_playing

    # Identifies a single card that has the highest power and allows another card to be played
    @staticmethod
    def best_card_that_allows_another_card_to_be_played(playable_cards, enemy):
        # Sort cards by power in descending order.
        cards = sorted(playable_cards, key=lambda enemy_card: enemy_card.power, reverse=True)
        for card in cards:
            # Check if there's at least one more card that could be played after this one
            if any(card.cost <= (enemy.cost - other_cards.cost) for other_cards in cards if other_cards != card):
                return card
            # If no card fulfills the criteria, return None
            return None
