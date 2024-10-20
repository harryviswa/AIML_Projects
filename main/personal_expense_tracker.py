import csv
import traceback

import pandas as pd
import datetime
from abc import abstractmethod, ABC
import os.path

monthly_budget = 0
expenses = []

class expense_abc(ABC):

    @abstractmethod
    def add_expense_details(): pass

    @abstractmethod
    def display_expenses(): pass

    @abstractmethod
    def update_monthly_budget(): pass

    @abstractmethod
    def track_budget(): pass

    @abstractmethod
    def save_expenses(expenses, filename): pass

    @abstractmethod
    def load_expenses(filename): pass

1
class personal_expense(expense_abc):

    def __init__(self):
        global monthly_budget
        monthly_budget = 200.00
        self.load_expenses()

    def add_expense_details(self):
        global expenses
        try:
            try:
                date = input("When did you spent? (YYYY-MM-DD): ")
                date = datetime.datetime.strptime(date, '%Y-%m-%d')
            except:
                ty=datetime.date.today().strftime('%Y-%m-%d 00:00:00')
                print('Incorrect date format, resetting to todays date: ',ty)
                #traceback.print_exc()
                date = ty
            category = input("Expense category please (e.g., Food, Travel): ")
            amount = float(input("What's your spent amount: $"))
            description = input("Add your additional note for this expense: ")
            expense = {
                'Date': date,
                'Category': category,
                'Amount': amount,
                'Description': description
            }
            expenses.append(expense)
        except:
            print('Incorrect inputs provided and so skipped adding this invalid expense entry')
        return

    def display_expenses(self):
        global expenses
        if not expenses:
            print("No expenses found, let's try to add one!")
            self.add_expense_details()

        for x in expenses:
            if len(str(x['Date'])) > 0 and len(x['Category']) > 0 and 'Amount' in x and len(x['Description']) > 0:
                continue
            else:
                print("Missing details found and will be skipped from your expense calculation")
                print(f"{x}")

        if expenses:
            print(pd.DataFrame(expenses).to_markdown())
        return

    def calculate_total_expenses(self, monthly_budget, expenses):
        ty = datetime.date.today().strftime('%Y-%m')
        total_expenses = sum(float(expense['Amount']) for expense in expenses if 'Amount' in expense and 'Date' in expense and datetime.datetime.strptime(str(expense['Date'])[:-9],'%Y-%m-%d').strftime('%Y-%m') == ty)
        print('Your current expense is: ', total_expenses, ' for this month [', ty, '] with the monthly budget as $',
              monthly_budget)
        return total_expenses

    def track_budget(self):
        global monthly_budget
        global expenses
        total_expenses = self.calculate_total_expenses(monthly_budget, expenses)
        if total_expenses > monthly_budget:
            print("You have exceeded your budget!")
        else:
            remaining_balance = monthly_budget - total_expenses
            print(f"You have {remaining_balance:.2f} left for the month.")

    def update_monthly_budget(self):
        global monthly_budget
        ty = datetime.date.today().strftime('%Y-%m')
        monthly_budget = float(input(f"Enter the total budget amount for this month '{ty}': "))
        me = open("monthly_expense.txt", "w")
        me.write(str(monthly_budget))
        me.close()
        print('Budget set successfully.\n\n')
        self.track_budget()
        return

    def save_expenses(self, filename="expense.csv"):
        global expenses
        if not expenses: return
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Date', 'Category', 'Amount', 'Description'])
            for expense in expenses:
                writer.writerow(expense.values())
        print('Successfully saved your personal expense details')
        return

    def load_expenses(self, filename="expense.csv"):
        global expenses
        loadedExpenses = []
        try:
            with open(filename, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader: loadedExpenses.append(row)
            expenses = loadedExpenses
        except:
            print('No expense file found. Seems like you are using for the first time. Dont forget to save your expense details.')
        self.load_budget()
        return loadedExpenses

    def load_budget(self, filename="monthly_expense.txt"):
        global monthly_budget
        if os.path.isfile(filename):
            me = open(filename, 'r')
            monthly_budget = float(me.readline())
            me.close()
        else:
            print('Looks like you have not set the budget so far, let me try to capture it.')
            self.update_monthly_budget()

    def display_options(self):
        print('################################################')
        print('Please select an option from the below list')
        print('1. View Expense')
        print('2. Add Expense')
        print('3. Track Budget')
        print('4. Set Budget')
        print('5. Save Expenses')
        print('6. Exit\n\n')
        return int(input('Your option: #'))

    def load_application(self):
        option = 1
        while (option > 0 and option < 6):
            try:
                option = self.display_options()
                if option == 1:
                    self.display_expenses()
                elif option == 2:
                    self.add_expense_details()
                elif option == 3:
                    self.track_budget()
                elif option == 4:
                    self.track_budget()
                    self.update_monthly_budget()
                elif option == 5:
                    self.save_expenses()
                elif option == 6:
                    print('Thanks for using this personal expense tracker system')
                    return
                else:
                    print('Invalid input, please try again')
                    option = 1
            except:
                print('\n\nAre you trying to break me, kindly provide valid inputs to help you.\n\n')
                # traceback.print_exc()

if __name__=="__main__":
    personal_expense = personal_expense()
    personal_expense.load_application()