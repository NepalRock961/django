from django.shortcuts import redirect
def redirect_back(request):
	return redirect(request.META.get('HTTP_REFERER'))