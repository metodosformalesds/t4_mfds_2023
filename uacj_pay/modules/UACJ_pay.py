from interfaces.SPEI_interface import SPEIInterfaces

class PaymentInformation:
    def __init__(self, amount:float, name:str, account:str, institution:str, concept:str, reference:str):
        self.amount = amount
        self.name = name
        self.account = account
        self.institution = institution
        self.concept = concept
        self.reference = reference

        def __str__(self):
            return f"PaymentInformation {self.amount},{self.account},{self.institution}"

class UACJ_pay(SPEIInterface):
    def __generate_pay_link(self, payment_info):
        
        return reverse(PAYMENT_URL, args=(hash))
        pass
    
    #Override
    def codi(self, payment_information:PaymentInformation)->str:
        payment_information = {
                monto:2.2,
                nombre:"",#beneficiario del cobro
                cuenta:"",
                institucion:"",
                concepto:"",
                referencia:"2", #son hasta 7 digitos que nos permiten identificar el cobro
            }

        link = self.__generate_pay_link(payment_information)
        raise NotImplementedError
        pass
