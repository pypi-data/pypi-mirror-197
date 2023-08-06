from datetime import date
from datetime import datetime as dt
from financemodule.models import (
    Finance,
    FinanceAccounting,
    Exchangerate,
    Loanaccount,
    Interestaccount,
    FloatingInterestRate,
)
from .exception import (
    ModelNotFound,
    ValueTypeException,
    AccountInformException,
    RepaymentValuesException
)
from .enum import (
    ProgramTypeChoices,
    ModelTypeChoices,
    UserTypeChoices,
    InterestTypeChoices,
    InterestPaidByChoices,
    AccountTypeChoice,
    StatusChoices
)
from dataclasses import dataclass 
import contextlib 
from typing import Optional




# DEFAULT VALUES

MODEL_TYPE = [
    "REPAYMENT",
    "FINANCING"
]

INTEREST_PAID_BY = [
    "OWNPARTY",
    "COUNTERPARTY"
]





@dataclass
class FinanceModuleHandler:

    # BASE CONSTRUCTOR #
    

    finance_req_id : int or str
    program_type: str
    anchor_party: str
    counterparty: str
    due_date: str
    model_type : str
    invoice_amount : Optional[int] = None
    finance_amount: Optional[int] = None
    repayment_amount : Optional[int] = None
    settlement_amount : Optional[int] = None
    margin : Optional[int] = None
    account_info_1 : Optional[dict] = None
    account_info_2 : Optional[dict] = None
    repayment_account : Optional[int] = None
    repayment_currency : Optional[str] = None
    invoice_currency : Optional[str] = None
    finance_currency : Optional[str] = None
    settlement_currency: Optional[str] = None
    base_currency : Optional[str] = None
    interest_type : Optional[str] = None
    interest_rate_type: Optional[str] = None
    interest_paid_by : Optional[str] = None


    # @interest_paid_by.setter
    # def interest_paid_by(self,d):
    #     if d not d : raise ValueError("model type must be ownparty")
    #     self._interest_paid_by = d

    def __post_init__(self):
        if self.model_type not in MODEL_TYPE:
            raise ModelNotFound()
        if self.interest_paid_by not in INTEREST_PAID_BY:
            raise ModelNotFound()
        if type(self.account_info_1) and type(self.account_info_2) is not dict :
            raise ValueTypeException()
        if "currency" not in self.account_info_2 :
            raise AccountInformException()
        if (
            self.model_type == ModelTypeChoices.REPAYMENT
            and (self.repayment_currency
            and self.repayment_amount) is None
        ):
            raise RepaymentValuesException()



        

    def gets_loan_account(self):
        obj , created = Loanaccount.objects.get_or_create(customer = self.anchor_party , 
        program_type = self.program_type , currency = self.finance_currency)
        return obj


    def gets_rounded_values(self,amount):
        if self.finance_currency or self.base_currency == "JPY" :
            final_amount  = "{:.3f}".format(amount)
        final_amount = "{:.2f}".format(amount)
        return final_amount
    

    def calculated_interest_amount(self , amount ):
        current_date = date.today()
        calculated_date = (
            dt.strptime(str(self.due_date), "%Y-%m-%d")
            - dt.strptime(str(current_date), "%Y-%m-%d")
        ).days
        if self.interest_type == InterestTypeChoices.FIXED:
            interest_rate = self.margin
        if self.interest_type == InterestTypeChoices.FLOATING:
            interest_rate_type = FloatingInterestRate.objects.get(
                currency__description = self.finance_currency , interest_rate_type = self.interest_rate_type 
            )
            # 0 - 30 days
            if 0 < calculated_date <= 30:
                    interest_rate = self.margin + float(list(interest_rate_type.period.values())[0])
            # 30 - 60 days
            if 30 < calculated_date <= 60:
                    interest_rate = self.margin + float(list(interest_rate_type.period.values())[1])
            # 60 - 180 days
            if 60 < calculated_date <= 180:
                    interest_rate = self.margin + float(list(interest_rate_type.period.values())[2])
            # 180 - 360 days
            if calculated_date > 180:
                    interest_rate = self.margin + float(list(interest_rate_type.period.values())[3])
        interest_amount = (amount * interest_rate) * (calculated_date / 365)
        return interest_amount, interest_rate


    def gets_exchange_rate(self, currency ):
        return Exchangerate.objects.get(rate_currency = currency)


    # def amount_round(self):
    #     return 



    def calculated_interest_values(self):
        exchange_rate_queryset =  self.gets_exchange_rate(self.finance_currency)
        if self.model_type == ModelTypeChoices.FINANCING or ModelTypeChoices.REPAYMENT  and self.program_type == ProgramTypeChoices.APF :
            # finance_currency
            if Interestaccount.objects.filter(program_type=self.program_type , currency=self.finance_currency).exists():
                return self.calculated_interest_amount(amount=self.finance_amount)[0], self.finance_currency 
            # base_currency 
            elif Interestaccount.objects.filter(program_type=self.program_type , currency=self.base_currency).exists():
                return self.calculated_interest_amount(amount=self.finance_amount)[0] * exchange_rate_queryset.rate_mid  , self.base_currency
        else:
            raise ValueError("something went wrong")


    def gets_interest_account(self):
        # return Interestaccount.objects.get_or_create(program_type=self.program_type , currency=self.finance_currency or self.base_currency)
        obj , created = Interestaccount.objects.get_or_create(program_type=self.program_type , currency=self.finance_currency )
        return obj
    

    def currency_conversion(self , from_currency , from_amount , to_currency , from_rate = None, to_rate = None ,exch_rate = None) -> None:
        exchange_rate_queryset = Exchangerate.objects.get(rate_currency=from_currency)
        exchange_rate_queryset_2 = Exchangerate.objects.get(rate_currency=to_currency)
        from_rate = from_rate or exchange_rate_queryset.rate_mid
        to_rate = to_rate or exchange_rate_queryset_2.rate_mid
        if from_currency and to_currency != self.base_currency:
            if exch_rate:
                to_amount = from_amount * exch_rate
            to_amount = (from_amount * from_rate ) / to_rate
            exch_rate = to_amount / from_amount
        elif from_currency:
            to_amount = from_amount 
            exch_rate = 1
        elif from_currency == self.base_currency:
            if not exch_rate:
                exch_rate = to_rate
            to_amount = from_amount / exch_rate
        else:
            if not exch_rate:
                exch_rate = from_rate
            to_amount = from_amount * exch_rate
        return to_amount , exch_rate


    def base_currency_calculation(self , currency , amount , exch_rate):
        if self.base_currency == currency :
            return amount , 1
        return amount * exch_rate , exch_rate



    def create_finance(self):

        current_interest_amount = self.calculated_interest_amount(amount=self.finance_amount)

        
        calculated_amount = self.finance_amount - current_interest_amount[0]

        final_amount = self.currency_conversion(self.finance_currency , calculated_amount , self.account_info_2['currency'])[0]
        
        exchange_rate_queryset_1 = self.gets_exchange_rate(self.finance_currency)
        exchange_rate_queryset_2 = self.gets_exchange_rate(self.account_info_2['currency'])

        if self.program_type != ProgramTypeChoices.APF:
            raise ValueError("program type should be APF , RF or DF")
        finance_model = Finance.objects.create(
                finance_request_id = self.finance_req_id,
                program_type = self.program_type,
                anchor_party = self.anchor_party,
                counterparty = self.counterparty,
                due_date = self.due_date,
                invoice_currency = self.invoice_currency,
                invoice_amount = self.invoice_amount ,
                finance_currency = self.finance_currency,
                finance_amount = self.finance_amount,
                settlement_currency = self.settlement_currency,
                settlement_amount = self.settlement_amount,
                repayment_account = self.repayment_account,
                interest_type = self.interest_type,
                interest_rate_type = self.interest_rate_type,
                margin = self.margin,
                interest_paid_by = self.interest_paid_by,
                own_party_account_info = self.account_info_1,
                remittance_info = self.account_info_2,
                status = ModelTypeChoices.FINANCING
        )


        if self.interest_paid_by == InterestPaidByChoices.OWNPARTY:

            currency_conversion_remittance = self.currency_conversion(self.finance_currency, self.finance_amount, self.account_info_2['currency'] )[0]
            finance_account_query = FinanceAccounting.objects.bulk_create([

            # type DEBIT Finance loan account
            FinanceAccounting(
            contract_ref = self.finance_req_id,
            finance_model = finance_model ,
            stage = ModelTypeChoices.FINANCING ,
            type =  AccountTypeChoice.DEBIT , 
            currency=self.finance_currency,
            interest_paid_by = self.interest_paid_by, 
            amount = self.finance_amount , 
            account = self.gets_loan_account().account , 
            account_type= UserTypeChoices.CUSTOMER,
            base_currency= self.base_currency ,
            base_currency_amount = self.base_currency_calculation(self.finance_currency ,self.finance_amount , exchange_rate_queryset_1.rate_mid)[0] ,
            exch_rate = self.base_currency_calculation(self.finance_currency , self.finance_amount , exchange_rate_queryset_1.rate_mid)[1] 
            ),

            # type CREDIT remittance account
            # replace amount in base_ccy_amount from the above calculated
            FinanceAccounting(
            contract_ref = self.finance_req_id,
            finance_model = finance_model ,
            stage = ModelTypeChoices.FINANCING,
            interest_paid_by = self.interest_paid_by, 
            type = AccountTypeChoice.CREDIT ,
            currency = self.account_info_2['currency'] ,
            amount = currency_conversion_remittance,
            account = self.account_info_1 , 
            account_type= UserTypeChoices.CUSTOMER,
            base_currency= self.base_currency ,
            base_currency_amount=self.base_currency_calculation(self.account_info_2['currency'] , currency_conversion_remittance , exchange_rate_queryset_2.rate_mid)[0] ,
            exch_rate = self.base_currency_calculation(self.account_info_2['currency'] , currency_conversion_remittance , exchange_rate_queryset_2.rate_mid)[1] 
            )
            
            ])

            # this required when finance_currency !=  base_currency else bb_ccy_amoun = finance_amount 
            # this required when remittance_currency !=  base_currency else bb_ccy_amoun = remittance_amount 
            

            # change on_save for the base_currency_amount

        if self.interest_paid_by == InterestPaidByChoices.COUNTERPARTY:

            FinanceAccounting.objects.bulk_create([

            # type DEBIT Finance Amount
            FinanceAccounting(
            contract_ref = self.finance_req_id,
            finance_model = finance_model,
            stage = ModelTypeChoices.FINANCING , 
            type =  AccountTypeChoice.DEBIT  , 
            interest_paid_by = self.interest_paid_by, 
            currency=self.finance_currency,
            amount=self.finance_amount , 
            account = self.gets_loan_account().account , 
            account_type= UserTypeChoices.CUSTOMER,
            base_currency= self.base_currency,
            base_currency_amount=self.base_currency_calculation( self.finance_currency ,self.finance_amount , exchange_rate_queryset_1.rate_mid)[0] ,
            exch_rate = self.base_currency_calculation(self.finance_currency ,self.finance_amount , exchange_rate_queryset_1.rate_mid)[1] 
            ),

            # type CREDIT (amount less interest account)

            # doing it for remittance
            FinanceAccounting(
            contract_ref = self.finance_req_id,
            finance_model = finance_model  ,
            stage = ModelTypeChoices.FINANCING,
            type =  AccountTypeChoice.CREDIT  , 
            currency = self.account_info_2['currency'] ,
            amount = final_amount, 
            interest_paid_by = self.interest_paid_by, 
            account = self.account_info_1 , 
            account_type= UserTypeChoices.CUSTOMER,
            base_currency= self.base_currency,
            base_currency_amount=self.base_currency_calculation(self.account_info_2['currency'] , final_amount , exchange_rate_queryset_2.rate_mid)[0] ,
            exch_rate = self.base_currency_calculation(self.account_info_2['currency'], final_amount , exchange_rate_queryset_2.rate_mid)[1] 
            ),

            # credit interest amount
            FinanceAccounting(
            contract_ref = self.finance_req_id, 
            finance_model = finance_model ,
            stage = ModelTypeChoices.FINANCING,
            type =  AccountTypeChoice.CREDIT ,
            interest_paid_by = self.interest_paid_by, 
            currency = self.calculated_interest_values()[1] , 
            amount = self.calculated_interest_values()[0], 
            account = self.gets_interest_account().account , 
            account_type= UserTypeChoices.INTERNAL ,
            base_currency= self.base_currency,
            base_currency_amount=self.base_currency_calculation( self.calculated_interest_values()[1] ,self.calculated_interest_values()[0] , self.gets_exchange_rate(self.calculated_interest_values()[1]).rate_mid)[0] ,
            exch_rate = self.base_currency_calculation( self.calculated_interest_values()[1] ,self.calculated_interest_values()[0] , self.gets_exchange_rate(self.calculated_interest_values()[1]).rate_mid)[1]
            ),

            ])

        return (
            self.gets_rounded_values(current_interest_amount[0]) , 
            current_interest_amount[1] , 
            finance_model.finance_date.date().isoformat() , 
            finance_model.id , 
            StatusChoices.FINANCED.value
        )



    def repayment(self):

        current_interest_amount = self.calculated_interest_amount(amount=self.finance_amount)
        # do the following currency conversion before adding repayment 
        # final_amount = self.currency_conversion(self.repayment_currency, self.repayment_amount, self.finance_currency)[0]
        final_amount = self.currency_conversion(self.finance_currency, current_interest_amount[0] , self.repayment_currency)[0]
        calculated_amount = self.repayment_amount + final_amount
        

        exchange_rate_queryset_1 = self.gets_exchange_rate(self.finance_currency)
        exchange_rate_queryset_2 = self.gets_exchange_rate(self.repayment_currency)

        final_currency_conversion = self.currency_conversion(self.repayment_currency, self.repayment_amount, self.finance_currency)
        
        if self.program_type != ProgramTypeChoices.APF:
            raise ValueError("program type should be APF , RF or DF")
        obj , created  = Finance.objects.update_or_create(
                finance_request_id = self.finance_req_id,
                defaults={
                    "program_type" : self.program_type,
                    "due_date": self.due_date,
                    "invoice_currency": self.invoice_currency,
                    "invoice_amount": self.invoice_amount,
                    "finance_currency": self.finance_currency,
                    "finance_amount": self.finance_amount,
                    "settlement_currency": self.settlement_currency,
                    "repayment_currency" : self.repayment_currency,
                    "repayment_account": self.repayment_account,
                    "settlement_amount" : self.settlement_amount,
                    "interest_type": self.interest_type,
                    "interest_rate_type": self.interest_rate_type,
                    "margin": self.margin,
                    "interest_paid_by": self.interest_paid_by,
                    "own_party_account_info": self.account_info_1,
                    "remittance_info":  self.account_info_2,
                    "status": ModelTypeChoices.REPAYMENT
                }
            )
        
        obj.settlement_amount = self.repayment_amount + obj.settlement_amount
        obj.save()

        if self.interest_paid_by == InterestPaidByChoices.OWNPARTY:
                
               
                FinanceAccounting.objects.bulk_create([
                
                # type Debit Repayment Amount + Interest Amount
                FinanceAccounting(
                contract_ref = self.finance_req_id, 
                finance_model = obj ,
                stage = ModelTypeChoices.REPAYMENT ,
                type =  AccountTypeChoice.DEBIT ,
                currency=self.repayment_currency,
                interest_paid_by = self.interest_paid_by, 
                amount = calculated_amount, 
                account = self.repayment_account , 
                account_type= UserTypeChoices.CUSTOMER,
                base_currency= self.base_currency ,
                base_currency_amount = self.base_currency_calculation( self.repayment_currency , calculated_amount , exchange_rate_queryset_2.rate_mid)[0],
                exch_rate = self.base_currency_calculation(self.repayment_currency , calculated_amount  , exchange_rate_queryset_2.rate_mid)[1]
                ),

                # type CREDIT loan account

                # currency -> loan_amount_currency 
                # repayment_amount in loan_account currency 

                # need to do cc
                FinanceAccounting(
                contract_ref = self.finance_req_id,
                finance_model = obj ,
                stage = ModelTypeChoices.REPAYMENT,
                type = AccountTypeChoice.CREDIT , 
                interest_paid_by = self.interest_paid_by, 
                currency=self.finance_currency,
                amount= final_currency_conversion[0], 
                account = self.gets_loan_account().account , 
                account_type= UserTypeChoices.CUSTOMER,
                base_currency= self.base_currency ,
                base_currency_amount = self.base_currency_calculation(self.finance_currency ,final_currency_conversion[0] , exchange_rate_queryset_1.rate_mid)[0],
                exch_rate = self.base_currency_calculation(self.finance_currency ,final_currency_conversion[0] , exchange_rate_queryset_1.rate_mid)[1] 
                ),

                # credit interest amount

                FinanceAccounting(
                contract_ref = self.finance_req_id,
                finance_model = obj,
                stage = ModelTypeChoices.REPAYMENT,
                type =  AccountTypeChoice.CREDIT,
                interest_paid_by = self.interest_paid_by, 
                currency = self.calculated_interest_values()[1] , 
                amount = self.calculated_interest_values()[0], 
                account = self.gets_interest_account().account , 
                account_type= UserTypeChoices.INTERNAL,
                base_currency= self.base_currency,
                base_currency_amount = self.base_currency_calculation(self.calculated_interest_values()[1] , self.calculated_interest_values()[0] , self.gets_exchange_rate(self.calculated_interest_values()[1]).rate_mid)[0] ,
                exch_rate = self.base_currency_calculation(self.calculated_interest_values()[1] , self.calculated_interest_values()[0] , self.gets_exchange_rate(self.calculated_interest_values()[1]).rate_mid )[1]),
                
                ])

                # change on_save for the base_currency_amount

        if self.interest_paid_by == InterestPaidByChoices.COUNTERPARTY:
                
                FinanceAccounting.objects.bulk_create([
                
                # type DEBIT finance amount
                FinanceAccounting(
                contract_ref = self.finance_req_id,
                finance_model = obj,
                stage = ModelTypeChoices.REPAYMENT ,
                type =  AccountTypeChoice.DEBIT , 
                currency=self.repayment_currency,
                amount = self.repayment_amount , 
                interest_paid_by = self.interest_paid_by, 
                account = self.repayment_account , 
                account_type= UserTypeChoices.CUSTOMER,
                base_currency= self.base_currency ,
                base_currency_amount = self.base_currency_calculation(self.repayment_currency ,self.repayment_amount , exchange_rate_queryset_2.rate_mid)[0] ,
                exch_rate = self.base_currency_calculation(self.repayment_amount ,self.repayment_amount , exchange_rate_queryset_2.rate_mid)[1] 
                ),

                # type CREDIT finance amount

                # need to CC
                FinanceAccounting(
                contract_ref = self.finance_req_id,
                finance_model = obj,
                stage = ModelTypeChoices.REPAYMENT,
                type = AccountTypeChoice.CREDIT,
                currency=self.finance_currency,
                amount= final_currency_conversion[0],
                interest_paid_by = self.interest_paid_by, 
                account = self.gets_loan_account().account , 
                account_type = UserTypeChoices.CUSTOMER,
                base_currency = self.base_currency ,
                base_currency_amount=self.base_currency_calculation(self.finance_currency ,final_currency_conversion[0] , exchange_rate_queryset_1.rate_mid)[0] ,
                exch_rate = self.base_currency_calculation(self.finance_currency , final_currency_conversion[0],exchange_rate_queryset_1.rate_mid)[1] 
                ),

                ])

        if obj.settlement_amount != self.finance_amount:
            status = StatusChoices.PARTIALLY_SETTLED.value
        status = StatusChoices.SETTLED.value
        return (
            self.gets_rounded_values(current_interest_amount[0]),
            current_interest_amount[1] , 
            obj.finance_date.date().isoformat() , 
            obj.id ,
            status
        )





from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated , AllowAny

from rest_framework.response import Response


class testapiview(APIView):
    permission_classes = [AllowAny]

    def get(self,request, *args, **kwargs):

        financing_module_handler = FinanceModuleHandler(
            finance_req_id = 1,
            program_type = "APF",
            anchor_party = "1",
            counterparty = "2" ,
            due_date = "2023-04-28",
            model_type = "REPAYMENT",
            invoice_currency = "USD" , 
            finance_currency = "USD" ,
            base_currency = "USD" , 
            invoice_amount = 1234,
            finance_amount = 1111,
            settlement_amount = 25252,
            account_info_1 = {"test" : "test", "currency" : "AED"},
            account_info_2 = {"test" : "test", "currency" : "AED"},
            interest_type = "FIXED" , 
            repayment_currency = "USD",
            repayment_amount = 1234,
            interest_rate_type = None, 
            margin = 90 ,
            interest_paid_by="OWNPARTY"
        ).repayment()
        print(financing_module_handler)
        return Response({"status": "SUCCESS", "data": "data" })
        