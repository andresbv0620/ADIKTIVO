import json
from django.http import Http404, HttpResponse

def more_todo(request):
	if request.is_ajax():
	else
		raise Http404


def add_todo(request):
	if request.is_ajax() and request.POST:
		data={'message':"%s added" % request.POST.get('item')}
		return HttpResponse(json.dumps(data), content_type='application/json')
	else:
		raise Http404
