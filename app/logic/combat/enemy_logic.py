import random


class EnemyLogic:

    # Selecting a card is based on multiple layers of logic, each which select cards to play targeting a specific
    # scenario and add it to a list of possible plays. Ultimately a random card is picked from the possible plays
    # list.

    # This means that the AI won't always pick the best possible play but by controlling how many instances of each
    # card are in the possible plays array, you can increase the odds of a specific card being played.
    @staticmethod
    def select_card(enemy, player):

        cards_in_cost = [card for card in enemy.deck.hand if card.cost <= enemy.cost]

        possible_plays = []
        possible_plays += cards_in_cost  # Add any card which can be played, this adds an element of 'Dumb AI'

        # The following methods add best play scenarios
        possible_plays += EnemyLogic.cards_that_kill(cards_in_cost, player)
        possible_plays += EnemyLogic.cards_allow_to_survive(cards_in_cost, enemy, player)

        best_card_allows_another_to_be_played = EnemyLogic.best_card_that_allows_another_card_to_be_played(cards_in_cost, enemy)
        if best_card_allows_another_to_be_played is not None:
            possible_plays.append(best_card_allows_another_to_be_played)

        return random.choice(possible_plays)

    # Identifies any cards that would allow the enemy to kill the player
    @staticmethod
    def cards_that_kill(playable_cards, player):
        return [card for card in playable_cards if card.card_type == "attack" and card.power >= player.cur_health]

    # Identifies any shield cards that would allow the player to survive a players attack
    @staticmethod
    def cards_allow_to_survive(playable_cards, enemy, player):
        cards_that_allow_to_survive = []
        for enemy_card in playable_cards:  # For each of the playable enemy cards
            if enemy_card.card_type == "shield":  # That would give shield
                for player_card in player.deck.hand:  # Check each of the players cards
                    if player_card.card_type == "attack":  # For attacks
                        if enemy.cur_health + enemy_card.power > player_card.power > enemy.cur_health:  # That by playing a shield card would allow the enemy to live
                            cards_that_allow_to_survive.append(enemy_card)

            return cards_that_allow_to_survive

    # Identifies a single card that has the highest power and allows another card to be played
    @staticmethod
    def best_card_that_allows_another_card_to_be_played(playable_cards, enemy):
        # Sort cards by power in descending order.
        cards = sorted(playable_cards, key=lambda x: x.power, reverse=True)

        for card in cards:
            # Check if there's at least one more card that could be played after this one
            if any(card.cost <= (enemy.cost - other_cards.cost) for other_cards in cards if other_cards != card):
                return card
            # If no card fulfills the criteria, return None
            return None




