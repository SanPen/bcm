
from blockchain import BlockChain


class Offer:

    def __init__(self, seller, minimum, maximum, price):
        """
        Offer object
        :param seller: Owner of the offer
        :param minimum: minimum amount
        :param maximum: maximum amount
        :param price: price per unit of amount
        """

        self.seller = seller

        self.minimum = minimum

        self.maximum = maximum

        self.price = price

    def buy_from(self, buyer, amount, block_chain: BlockChain):
        """
        Buy from this offer
        :param buyer: ID of the potential buyer
        :param amount: amount to be bought
        :param block_chain: Block chain object
        :return: if the transaction was stored
        """

        if amount > self.minimum:

            self.maximum -= amount

            block_chain_index = block_chain.new_transaction(self.seller, buyer, amount, self.price)

            delete_offer = self.maximum == self.minimum

        else:

            block_chain_index = -1
            delete_offer = False

        return block_chain_index, delete_offer


class Market:

    def __init__(self, block_chain: BlockChain, timestamp=None, name=''):
        """
        Market instance
        :param block_chain:
        :param timestamp:
        :param name:
        """

        self.ame = name

        self.block_chain = block_chain

        self.timestamp = timestamp

        self.offers = list()

    def get_offers(self):

        return self.offers

    def add_offer(self, seller, minimum, maximum, price):
        """
        Add a new offer
        :param seller: Owner of the offer
        :param minimum: minimum amount
        :param maximum: maximum amount
        :param price: price per unit of amount
        :returns index of the offer
        """
        offer = Offer(seller=seller, minimum=minimum, maximum=maximum, price=price)

        self.offers.append(offer)

        return len(self.offers) - 1

    def buy_from_offer(self, buyer, amount, offer_idx):
        """
        Buying operation
        :param buyer: Buyer id
        :param amount: amount to attempt to buy
        :param offer_idx: offer index
        :return: block_chain_index, if it is -1, the transaction was not fulfilled
        """

        block_chain_index, delete_offer = self.offers[offer_idx].buy_from(buyer, amount, self.block_chain)

        if delete_offer:
            self.offers.pop(offer_idx)
        else:
            pass

        return block_chain_index, delete_offer
