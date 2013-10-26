from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.template.loader import render_to_string
from registration.forms import RegistrationForm
from registration.models import create_fingr_user
from django.core.mail import send_mail
import string
import random
from profile.models import Profile

DEFAULT_FROM_ADDRESS = "noreply@unswfingr.me"


def register(request):
    if request.POST:
        # load up the form with data from the POST request
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = create_fingr_user(form.cleaned_data['email'], form.cleaned_data['password'])

            verification(form.cleaned_data['email'], user, request)

            profile = Profile(fingr_user = user)
            profile.save()

            return render(request, 'register_result.html', {'email': user.username})
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})


def verification(email, fingr_user, request):
    """ send verification email
     random long (50 char) string should be enough for validation purposes
    """
    # http://stackoverflow.com/questions/2257441/python-random-string-generation-with-upper-case-letters-and-digits
    link = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(50))
    fingr_user.v_code = link
    fingr_user.save()
    context = {'email': fingr_user.email, 'code': fingr_user.v_code,
               'abs_path': request.build_absolute_uri(reverse('main.views.activate'))}
    t = render_to_string('verification_email.html', context)
    send_mail("UNSWFingr.me Verification",
              t,
              DEFAULT_FROM_ADDRESS,
              [email])
