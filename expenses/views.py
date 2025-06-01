from django.shortcuts import render, redirect
from datetime import date, timedelta
from django.utils import timezone
from datetime import datetime
from .forms import ExpenseForm
from .models import Expense
from accounts.models import BudgetSetting
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
    daily_amount_total = [( date.strftime("%Y-%m-%d"), WEEKDAYS_JP[date.weekday()], daily_amount[date] ) for date in this_week]
    # daily_amount_total.append(("", "", week_total ))

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

    # 予算設定
    budgetSetting = BudgetSetting.objects.get(user=request.user)
    max_weekly_limit = budgetSetting.max_weekly_limit
    # 今月残量
    diff_amount = budgetSetting.max_weekly_limit - week_total
    expenses_json = json.dumps(expense_data_serialized)

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
        # "expenses": expenses_json,
        "daily_amount_total": daily_amount_total,
        # "datas": {"expenses": expense_data}
        "datas": json.dumps({"expenses": expense_data_serialized}, ensure_ascii=False),
        "nav_weekly_monthly": "weekly",
        "week_total": week_total,
        "max_weekly_limit": max_weekly_limit,
        "diff_amount": diff_amount
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

@login_required
def monthly(request):
    today = date.today()
    first = today.replace(day=1)  # 今月ついたちを取得
    start = first - timedelta(days=(first.weekday()+1)%7)  

    calendar_days = [(start + timedelta(days=i)) for i in range(35)]
    calendar_days_serialized = [day.strftime("%m/%d") for day in calendar_days]

    end = start + timedelta(days=35)
    expenses = Expense.objects.filter(
        user=request.user,
        date__range=(start, end)
    ).order_by('-date') 

    expense_amount = defaultdict(int)
    for expense in expenses:
        expense_amount[expense.date.strftime("%m/%d")] += expense.amount

    # 予算設定
    budgetSetting = BudgetSetting.objects.get(user=request.user)
    max_weekly_limit = budgetSetting.max_weekly_limit
    monthly_buffer = budgetSetting.monthly_buffer
    
    # 7日ごとに分割
    expense_monthly_amount = []
    week_data = []
    week_total = 0
    week_totals = []
    month_total = 0
    week_diff_amount = 0
    week_diff_amounts = []
    current_month_count = 0
    max_weekly_limits = []
    for i, day in enumerate(calendar_days_serialized):
        day_amount_in_thismonth = 0
        if day[:2] == today.strftime("%m"):
            day_amount_in_thismonth = expense_amount[day]
            month_total += day_amount_in_thismonth
            current_month_count += 1
        
        week_total += day_amount_in_thismonth
        week_data.append([day, day_amount_in_thismonth])
        if (i + 1) % 7 == 0:  # 7日ごとに区切る
            thisweek_max_limit_in_thismonth = int(max_weekly_limit * (current_month_count/7))
            week_diff_amount = thisweek_max_limit_in_thismonth - week_total
            week_diff_amounts.append(week_diff_amount)
            # week_diff_amounts.append(week_diff_amount)
            week_diff_amount = 0
            # week_totals.append(int(week_total * (current_month_count/7)))
            week_totals.append(week_total)
            week_total = 0
            max_weekly_limits.append(thisweek_max_limit_in_thismonth)
            expense_monthly_amount.append(week_data)
            week_data = []
            current_month_count  = 0
    # 最後の週が7日未満の場合も追加
    if week_data:
        expense_monthly_amount.append(week_data)

    sum_diff_amounts = sum(week_diff_amounts)
    sum_max_weekly_limits = sum(max_weekly_limits)
    sum_total_diff = sum_max_weekly_limits - month_total


    zipped_data = zip(expense_monthly_amount, max_weekly_limits, week_diff_amounts)

    context = {
        "nav_weekly_monthly": "monthly",
        "this_month": today.strftime("%m"),
        "calendar_days": calendar_days_serialized,
        "expense_monthly_amount": expense_monthly_amount,
        "week_totals": week_totals,
        "diff_amounts": week_diff_amounts,
        "sum_diff_amounts": sum_diff_amounts,
        "max_weekly_limits": max_weekly_limits,
        "sum_max_weekly_limits": sum_max_weekly_limits,
        "monthly_buffer": monthly_buffer,
        "zipped_data": zipped_data,
        "sum_total_diff": sum_total_diff,
        "month_total": month_total
    }
    return render(request, "expenses/monthly.html", context)
