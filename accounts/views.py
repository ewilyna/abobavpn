import json
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import CustomUserCreationForm
from .forms import CustomAuthenticationForm
from decimal import Decimal
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import VPNPlan, UserSubscription
from django.http import JsonResponse
from django.utils import timezone

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('login')
        else:
            messages.error(request, 'Ошибка регистрации. Проверьте введённые данные.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Вы успешно вошли в аккаунт!')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка входа. Проверьте данные.')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def profile_view(request):
    profile = request.user.profile  # Получаем профиль пользователя
    subscriptions = UserSubscription.objects.filter(user=request.user)  # Получаем подписки пользователя
    plans = VPNPlan.objects.all()  # Доступные подписки

    return render(request, 'accounts/profile.html', {
        'profile': profile,
        'subscriptions': subscriptions,
        'plans': plans
    })



@csrf_exempt
@login_required
def add_balance(request):
    if request.method == 'POST':
        try:
            amount = Decimal(request.POST.get('amount', '0'))  # Приводим сумму к Decimal
            if amount > 0:
                profile = request.user.profile
                profile.balance += amount
                profile.save()
                return JsonResponse({'message': 'Баланс успешно пополнен!'})
            else:
                return JsonResponse({'message': 'Введите корректную сумму для пополнения.'}, status=400)
        except Exception as e:
            return JsonResponse({'message': f'Ошибка: {str(e)}'}, status=500)
    return JsonResponse({'message': 'Неверный метод запроса.'}, status=405)


@login_required
@csrf_exempt
def buy_plan(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            plan_id = data.get('plan_id')
            plan = VPNPlan.objects.get(pk=plan_id)

            if request.user.profile.balance < plan.price:
                return JsonResponse({'message': 'Недостаточно средств на балансе.'}, status=400)

            # Обновляем баланс
            request.user.profile.balance -= plan.price
            request.user.profile.save()

            # Создаем подписку
            UserSubscription.objects.create(
                user=request.user,
                plan=plan,
                end_date=timezone.now() + timezone.timedelta(days=30 * plan.duration_months)
            )

            return JsonResponse(
                {'message': f'План "{plan.name}" успешно куплен!', 'new_balance': request.user.profile.balance})
        except Exception as e:
            return JsonResponse({'message': f'Ошибка: {str(e)}'}, status=500)

    return JsonResponse({'message': 'Неверный метод запроса.'}, status=405)


from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy

class CustomPasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy('profile')  # Замените 'profile' на имя маршрута страницы профиля
