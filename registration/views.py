from django.shortcuts import render
from registration.forms import RegistrationForm
from registration.models import create_fingr_user, user_to_fingr
from django.core.mail import send_mail
import string
import random



def register(request):
    if request.POST:
        # load up the form with data from the POST request
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = create_fingr_user(form.cleaned_data['email'], form.cleaned_data['password'])
            verification(form.cleaned_data['email'], user)
            return render(request, 'register_result.html', {'email': user.username})
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})


def verification(email, user):
    """ send verification email
     random long (50bit) string should be enough for validation purposes
     link this string to the user, dont allow them to login until verified
    """
    link = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(50))
    user._set_v_code(link)
    user.save()
    #send_mail("UNSWFingr.me Verfication", "http://unswfingr.me/activate.html?user=" + email + "&code=" + link, EMAIL_HOST_USER, [email])