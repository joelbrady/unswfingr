from django.contrib.auth.models import User

def search(user):

	# check the username exists
	found = User.objects.filter(username=user)
	
	# display the found users
	
	return found