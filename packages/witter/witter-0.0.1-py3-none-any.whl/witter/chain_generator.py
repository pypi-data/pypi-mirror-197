from random import choices, random


class ChainGenerator:
    def __init__(self, source):
        self.source = source
        self.cached_chains = {}
        self.cached_chain_length = None

    def chains(self, chain_length):
        """
        Take the items in self.source, and divide them into chains of length chain_length.
        Store them as key in a dictionary, with each key referencing another dictionary
        of key:next item, value:number of times that this item has followed a matching chain.
        :param chain_length:
        :return:
        """

        if chain_length != self.cached_chain_length:
            chains = {}
            for chain_start_index in range(0, len(self.source) - chain_length + 1):
                chain = self.source[
                    chain_start_index : chain_start_index + chain_length
                ]
                next_character = (
                    self.source[chain_start_index + chain_length]
                    if chain_start_index + chain_length < len(self.source)
                    else None
                )

                if not next_character:
                    if chain not in chains:
                        chains[chain] = {}
                else:
                    if chain not in chains:
                        chains[chain] = {next_character: 1}
                    elif next_character not in chains[chain]:
                        chains[chain][next_character] = 1
                    else:
                        chains[chain][next_character] = (
                            chains[chain][next_character] + 1
                        )

            print(
                "Chains: {} created from {} characters.".format(
                    len(chains), len(self.source)
                )
            )

            self.cached_chains = chains
            self.cached_chain_length = chain_length

        return self.cached_chains

    def choose_next_item(self, options):
        """

        :param options: A dictionary of possible options key: item, value: count of items from original source.
        :return: An item chosen at random with a weighting towards the counts of original occurrences.
        """

        return choices(list(options.keys()), weights=list(options.values()))[0]

    def generate_chain(self, chain_length, target_length):
        # Choose the first chain - starts with a character not a space, and
        # all first chains are equally likely.
        # Also, the first word must have at least one letter, and that must be a capital.
        chains = self.chains(chain_length)
        chains_to_start = [
            k for k in chains.keys() if " " not in k[:1] and k[0].isupper()
        ]
        current_chain = chains_to_start[int(random() * len(chains_to_start))]

        result = current_chain

        finished = False
        output_count = 0

        while not finished:
            if not chains[current_chain]:
                finished = True
                break
            key_exists = False
            while not key_exists:
                chosen_next_item = self.choose_next_item(chains[current_chain])
                potential_chain = current_chain[1:] + chosen_next_item
                key_exists = potential_chain in chains
                if key_exists:
                    current_chain = potential_chain

            result = result + chosen_next_item
            output_count = output_count + 1

            if output_count >= target_length and chosen_next_item == ".":
                finished = True

        return result
