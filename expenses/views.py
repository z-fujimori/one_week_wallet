from django.shortcuts import render, redirect
from datetime import date, timedelta
from django.utils import timezone
from datetime import datetime
from .forms import ExpenseForm
from .models import Expense
from collections import defaultdict  # 配列の初期値設定
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse



WEEKDAYS_JP = ['月', '火', '水', '木', '金', '土', '日']

# Create your views here.
@login_required
def index(request):
    if request.GET.get("day"):
        today = datetime.strptime(request.GET.get("day"), "%Y-%m-%d")
    else:
        today = timezone.localtime().replace(hour=0, minute=0, second=0, microsecond=0)
    weekday = (today.weekday()+1)%7
    start = today - timedelta(days=weekday) 
    this_week = [(start + timedelta(days=i)).date() for i in range(7)]
    end = today + timedelta(days=6-weekday)

    expenses = Expense.objects.filter(
            user=request.user,
            date__range=(start, end)
        ).order_by('-date')
    
    expense_data = defaultdict(list)
    
    week_total = 0
    daily_amount = defaultdict(int)  # 未定義のインデックスが呼び出された場合にエラーにならない
    for expense in expenses:
        daily_amount[expense.date] += expense.amount
        week_total += expense.amount
        expense_data[expense.date.isoformat()].append(expense)
    # daily_amount_total = sorted(daily_amount.items())
    daily_amount_total = [( date.strftime("%m-%d"), WEEKDAYS_JP[date.weekday()], daily_amount[date] ) for date in this_week]
    daily_amount_total.append(("", "", week_total ))

    expense_data_serialized = {
        date: [
            {
                "id": e.id,
                "title": e.title,
                "amount": e.amount,
                "tag": e.tag.name if e.tag else None,
                "date": e.date.isoformat()
            }
            for e in expense_list
        ]
        for date, expense_list in expense_data.items()
    }

    return render(request, "expenses/index.html",{
        "sun_day": this_week[0].strftime("%m-%d"),
        "sat_day": this_week[6].strftime("%m-%d"),
        "ymd_prev_sun_day": (this_week[0] - timedelta(days=7)).strftime("%Y-%m-%d"),
        "prev_sun_day": (this_week[0] - timedelta(days=7)).strftime("%m-%d"),
        "prev_sat_day": (this_week[6] - timedelta(days=7)).strftime("%m-%d"),
        "ymd_next_sun_day": (this_week[0] + timedelta(days=7)).strftime("%Y-%m-%d"),
        "next_sun_day": (this_week[0] + timedelta(days=7)).strftime("%m-%d"),
        "next_sat_day": (this_week[6] + timedelta(days=7)).strftime("%m-%d"),
        "today": date.today().isoformat(),
        "expenses": expense_data_serialized,
        "daily_amount_total": daily_amount_total,
        # "datas": {"expenses": expense_data}
        "datas": json.dumps({"expenses": expense_data_serialized}, ensure_ascii=False)
    })

@login_required
def get_week_data(request):
    standard_day = datetime.strptime(request.GET.get("day"), "%Y-%m-%d")
    print("-------------------------------------------------")
    print(standard_day)
    weekday = (standard_day.weekday()+1)%7
    print(weekday)
    start = standard_day - timedelta(days=weekday) 
    this_week = [(start + timedelta(days=i)).date() for i in range(7)]
    end = standard_day + timedelta(days=6-weekday)

    expenses = Expense.objects.filter(
            user=request.user,
            date__range=(start, end)
        ).order_by('-date')
    
    expense_data = defaultdict(list)
    
    week_total = 0
    daily_amount = defaultdict(int)  # 未定義のインデックスが呼び出された場合にエラーにならない
    for expense in expenses:
        daily_amount[expense.date] += expense.amount
        week_total += expense.amount
        expense_data[expense.date.isoformat()].append(expense)
    # daily_amount_total = sorted(daily_amount.items())
    daily_amount_total = [( date.strftime("%m-%d"), WEEKDAYS_JP[date.weekday()], daily_amount[date] ) for date in this_week]
    daily_amount_total.append(("", "", week_total ))

    expense_data_serialized = {
        date: [
            {
                "id": e.id,
                "title": e.title,
                "amount": e.amount,
                "tag": e.tag.name if e.tag else None,
                "date": e.date.isoformat()
            }
            for e in expense_list
        ]
        for date, expense_list in expense_data.items()
    }

    return JsonResponse({
        "sun_day": this_week[0].strftime("%m-%d"),
        "sat_day": this_week[6].strftime("%m-%d"),
        "ymd_prev_sun_day": (this_week[0] - timedelta(days=7)).strftime("%Y-%m-%d"),
        "prev_sun_day": (this_week[0] - timedelta(days=7)).strftime("%m-%d"),
        "prev_sat_day": (this_week[6] - timedelta(days=7)).strftime("%m-%d"),
        "ymd_next_sun_day": (this_week[0] + timedelta(days=7)).strftime("%Y-%m-%d"),
        "next_sun_day": (this_week[0] + timedelta(days=7)).strftime("%m-%d"),
        "next_sat_day": (this_week[6] + timedelta(days=7)).strftime("%m-%d"),
        "today": date.today().isoformat(),
        "expenses": expense_data_serialized,
        "daily_amount_total": daily_amount_total,
        # "datas": {"expenses": expense_data}
        "datas": json.dumps({"expenses": expense_data_serialized}, ensure_ascii=False)
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

