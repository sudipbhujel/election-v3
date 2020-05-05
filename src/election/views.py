from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from election.forms import ElectionFillForm
from accounts.models import User
from django.contrib import messages
from election.models import ElectionForm
from django.core.exceptions import ValidationError

from election.choices import genders, provinces, districts 


@login_required
def home(request):
    context = {}
    return render(request, "election/home.html", context)


@login_required
def election_fill_form_view(request, citizenship_number):
    if request.method == 'POST':
        form = ElectionFillForm(request.POST, request.FILES)


        if form.is_valid():
            form_item = form.save(commit=False)
            voter_qs = User.objects.filter(
                citizenship_number=citizenship_number, is_form_filled=False)
            if not voter_qs.exists():
                messages.success(
                    request, 'You may already have submitted form.')
                return redirect('election:home')
            voter = voter_qs.first()
            form_item.voter = voter

            voter.first_name = form.cleaned_data['first_name']
            voter.middle_name = form.cleaned_data['middle_name']
            voter.last_name = form.cleaned_data['last_name']
            voter.save()
            form_item.save()
            messages.success(request, 'You filled form successfully!')
            return redirect('election:home')
    else:
        form = ElectionFillForm()

    user = get_object_or_404(User, citizenship_number=citizenship_number)
    context = {
        'form': form,
        'user': user,
        'genders': genders,
        'provinces': provinces,
        'districts': districts
    }
    return render(request, 'election/election_form.html', context)
