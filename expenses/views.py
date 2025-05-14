from django.shortcuts import render, redirect
from datetime import date, timedelta
from django.utils import timezone
from .forms import ExpenseForm
from .models import Expense
from collections import defaultdict  # 配列の初期値設定

# Create your views here.
def index(request):
    today = timezone.localtime()
    weekday = (today.weekday()+1)%7
    print(weekday)
    start = today - timedelta(days=weekday) 
    this_week = [(start + timedelta(days=i)).date() for i in range(7)]

    expenses = Expense.objects.filter(
            user=request.user,
            date__range=(start, today)
        ).order_by('-date')
    
    daily_amount = defaultdict(int)  # 未定義のインデックスが呼び出された場合にエラーにならない
    for expense in expenses:
        daily_amount[expense.date] += expense.amount
    # daily_amount_total = sorted(daily_amount.items())
    daily_amount_total = [( date, daily_amount[date] ) for date in this_week]

    return render(request, "expenses/index.html",{
        "today": date.today().isoformat,
        "expenses": expenses,
        "daily_amount_total": daily_amount_total
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

