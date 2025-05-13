from django.shortcuts import render, redirect
from datetime import date
from .forms import ExpenseForm
from .models import Expense

# Create your views here.
def index(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    return render(request, "expenses/index.html",{
        "today": date.today().isoformat,
        "expenses": expenses
    })

def create_expense(request):
    print("print1")
    if request.method == 'POST':
        print("print2")
        form = ExpenseForm(request.POST)
        if form.is_valid():
            print("print3")
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('expenses:index')
    else:
        print("print0")
        form = ExpenseForm()
        return redirect('expenses:index')

