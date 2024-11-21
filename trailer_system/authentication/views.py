from django.shortcuts import render

# Create your views here.


from django.http import HttpResponse
from authentication.models import Trailer
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.contrib.auth import logout
from django.shortcuts import redirect
from datetime import datetime, timedelta


from django.core.paginator import Paginator

from django.utils import timezone


def home_view(request):
    return render(request, 'home.html')

from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    template_name = 'login.html'


# authentication/views.py

def custom_logout(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logging out



@login_required
def main_dashboard(request):
    return render(request, 'main_dashboard.html')


@login_required
def trailer_list(request):
    trailers = Trailer.objects.all()

    # Get current date for rent due calculations
    today = datetime.today().date()

    # Retrieve filters from query parameters
    status_filter = request.GET.get('status', 'all')  # Default to 'all'
    rent_due_filter = request.GET.get('rent_due', 'all')  # Default to 'all'
    search_query = request.GET.get('search', '')  # Default to empty string

    # Apply status filter
    if status_filter and status_filter != 'all':
        trailers = trailers.filter(status=status_filter)

    # Apply rent due filter
    if rent_due_filter == 'asc':
        trailers = trailers.order_by('rent_due')
    elif rent_due_filter == 'desc':
        trailers = trailers.order_by('-rent_due')
    elif rent_due_filter == '15_days':
        trailers = trailers.filter(rent_due__lte=today + timedelta(days=15))
    elif rent_due_filter == '1_month':
        trailers = trailers.filter(rent_due__lte=today + timedelta(days=30))
    elif rent_due_filter == '3_months':
        trailers = trailers.filter(rent_due__lte=today + timedelta(days=90))
    elif rent_due_filter == '6_months':
        trailers = trailers.filter(rent_due__lte=today + timedelta(days=180))
    elif rent_due_filter == 'greater_6_months':
        trailers = trailers.filter(rent_due__gt=today + timedelta(days=180))

    # Apply search query independently
    if search_query:
        trailers = trailers.filter(name__icontains=search_query)

    # Paginate the trailers (e.g., 5 per page)
    paginator = Paginator(trailers, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Pass all necessary context
    context = {
        'trailers': page_obj,  # Paginated trailer list
        'status_filter': status_filter,
        'rent_due_filter': rent_due_filter,
        'search_query': search_query,
        'today': timezone.now().date(),
    }
    return render(request, 'trailer_list.html', context)

from django.shortcuts import redirect


from .forms import TrailerForm  #TrailerForm is created for adding trailers

@login_required
def add_trailer(request):
    if request.method == 'POST':
        form = TrailerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('trailer-list')
    else:
        form = TrailerForm()
    return render(request, 'add_trailer.html', {'form': form})

from django.shortcuts import get_object_or_404
from .models import Trailer
from .forms import TrailerForm

@login_required
def edit_trailer(request, trailer_id):
    # Retrieve the specific trailer by ID or return a 404 if not found
    trailer = get_object_or_404(Trailer, id=trailer_id)

    if request.method == 'POST':
        form = TrailerForm(request.POST, instance=trailer)  # Load form with trailer instance
        if form.is_valid():
            form.save()  # Save the updated data
            return redirect('trailer-list')  # Redirect to the trailer list
    else:
        form = TrailerForm(instance=trailer)  # Initialize form with trailer data for GET request

    return render(request, 'edit_trailer.html', {'form': form, 'trailer': trailer})

@login_required
def delete_trailer(request, trailer_id):
    # Retrieve the specific trailer by ID or return a 404 if not found
    trailer = get_object_or_404(Trailer, id=trailer_id)

    if request.method == 'POST':
        trailer.delete()  # Delete the trailer
        return redirect('trailer-list')  # Redirect to the trailer list after deletion

    return render(request, 'delete_trailer.html', {'trailer': trailer})



