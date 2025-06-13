"""W tym przykładzie mamy klasę abstrakcyjną PaymentStrategy, która definiuje metodę pay. 
Następnie mamy dwie konkretne strategie: CreditCardPayment i PayPalPayment, które dziedziczą po PaymentStrategy i implementują metodę pay.
Klasa ShoppingCart reprezentuje koszyk zakupowy, który ma możliwość dodawania przedmiotów i określania strategii płatności.
Klient może wybrać odpowiednią strategię płatności, a następnie wywołać checkout dla dokonania płatności.
Dzięki wzorcowi Strategii klient ma elastyczność wyboru różnych strategii płatności, a klasa ShoppingCart nie musi wiedzieć, 
jakie konkretne strategie są dostępne i jak są implementowane. To umożliwia zmiany i rozszerzenia w przyszłości bez wprowadzania zmian w istniejącym kodzie."""

class PaymentStrategy:
    def pay(self, amount):
        pass
class CreditCardPayment(PaymentStrategy):
    def pay(self, amount):
        print(f"Paid {amount} dollars with credit card")
class PayPalPayment(PaymentStrategy):
    def pay(self, amount):
        print(f"Paid {amount} dollars with PayPal")
class ShoppingCart:
    def __init__(self):
        self.total_amount = 0
        self.payment_strategy = None

    def set_payment_strategy(self, payment_strategy):
        self.payment_strategy = payment_strategy

    def add_item(self, price):
        self.total_amount += price

    def checkout(self):
        if self.payment_strategy:
            self.payment_strategy.pay(self.total_amount)
        else:
            print("Please select a payment method before checkout")
# Użycie wzorca Strategii
cart = ShoppingCart()

cart.add_item(50)
cart.add_item(30)

cart.checkout()

cart.set_payment_strategy(CreditCardPayment())
cart.checkout()

cart.set_payment_strategy(PayPalPayment())
cart.checkout()