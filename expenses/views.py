from django.shortcuts import render, redirect
from datetime import date, timedelta
from django.utils import timezone
from .forms import ExpenseForm
from .models import Expense
from collections import defaultdict  # 配列の初期値設定
from django.contrib.auth.decorators import login_required

WEEKDAYS_JP = ['月', '火', '水', '木', '金', '土', '日']

# Create your views here.
@login_required
def index(request):
    today = timezone.localtime().replace(hour=0, minute=0, second=0, microsecond=0)
    weekday = (today.weekday()+1)%7
    print(weekday)
    start = today - timedelta(days=weekday) 
    this_week = [(start + timedelta(days=i)).date() for i in range(7)]
    end = today + timedelta(days=6-weekday)

    expenses = Expense.objects.filter(
            user=request.user,
            date__range=(start, end)
        ).order_by('-date')
    
    print(type(this_week[0]))
    
    week_total = 0
    daily_amount = defaultdict(int)  # 未定義のインデックスが呼び出された場合にエラーにならない
    for expense in expenses:
        daily_amount[expense.date] += expense.amount
        week_total += expense.amount
    # daily_amount_total = sorted(daily_amount.items())
    daily_amount_total = [( date, WEEKDAYS_JP[date.weekday()], daily_amount[date] ) for date in this_week]
    daily_amount_total.append(("", "", week_total ))

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


