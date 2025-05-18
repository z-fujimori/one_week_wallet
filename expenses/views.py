from django.shortcuts import render, redirect
from datetime import date, timedelta
from django.utils import timezone
from .forms import ExpenseForm
from .models import Expense
from collections import defaultdict  # 配列の初期値設定
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
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
    
    week_total = 0
    daily_amount = defaultdict(int)  # 未定義のインデックスが呼び出された場合にエラーにならない
    for expense in expenses:
        daily_amount[expense.date] += expense.amount
        week_total += expense.amount
    # daily_amount_total = sorted(daily_amount.items())
    daily_amount_total = [( date, daily_amount[date] ) for date in this_week]
    daily_amount_total.append(( "", week_total ))

    return render(request, "expenses/index.html",{
        "today": date.today().isoformat,
        "expenses": expenses,
        "daily_amount_total": daily_amount_total
    })

@login_required
def create_expense(request):
    if request.method == 'POST':

        form = ExpenseForm(request.POST)
        if form.is_valid():
    
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('expenses:index')
    else:

        form = ExpenseForm()
        return redirect('expenses:index')

def monthly(request):
    return render(request, "expenses/monthly.html")


