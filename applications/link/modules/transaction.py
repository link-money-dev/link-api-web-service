class Transaction():
    def __init__(self, id, fromer, toer, amount, dt, code, issuer):
        self.id = id
        self.fromer = fromer
        self.toer = toer
        self.amount = amount
        self.dt = dt
        self.code=code
        self.issuer=issuer