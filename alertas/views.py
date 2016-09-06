from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
import requests
import json

from .models import User
from .models import Alert, Match
from .forms import AlertForm


# Create your views here.

class AlertView(LoginRequiredMixin, View):

	form_class = AlertForm
	initial = {'key': 'value'}
	template_name = 'alertas/alertas_form.html'

	def get(self, request, *args, **kwargs):
		form=self.form_class()
		saludo="Cuentanos que carro estas buscando"
		context={
		"saludo": saludo,
		"form": form,
		}
		return render(request, "alertas/alertas_form.html", context)

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():
			instance=form.save(commit=False)
			alertModel = Alert.objects.create(
				user=request.user,
				main_category=instance.main_category,
				brand=instance.brand,
				model=instance.model,
				location=instance.location,
				year_min=instance.year_min,
				year_max=instance.year_max,
				price_min=instance.price_min,
				price_max=instance.price_max,
				mileage=instance.mileage
				)
			saludo="Alerta Creada exitosamente, te avisaremos cuando publiquen carros como el que estas buscando"
			context={
			"saludo": saludo,
			"form": self.form_class(),
			}
			return render(request, self.template_name, context)
			#return HttpResponseRedirect('/success/')

		saludo="Corrige los errores"
		context={
		"saludo": saludo,
		"form": form,
		}
		return render(request, self.template_name, context)


def check_match(request):
	alerts = Alert.objects.all()
	if len(alerts):
    	#print alerts

	    #Se genera el listado de fichas o secciones
	    for alert in alerts:
	    	alertaObject={}
	    	alertaObject['id'] = alert.id
	    	alertaObject['user'] = alert.user
	    	alertaObject['model'] = alert.model
	    	if alert.model=="" and alert.brand=="":
	    		categoryalert = alert.main_category
    		elif alert.model=="":
    			categoryalert = alert.brand
    		else:
				categoryalert = alert.model

	    	r = requests.get('https://api.mercadolibre.com/sites/MCO/search?category='+categoryalert+'&price='+alert.price_min+'-'+alert.price_max+'&years='+alert.year_min+'-'+alert.year_max+'&state='+alert.location+'')
    		json = r.json()
    		
    		carList=[]
    		for resultresult in json['results']:
    			carObject={}
		        carObject['external_id']=resultresult['id']
		        carObject['title']=resultresult['title']
		        carObject['category_id']=categoryalert
		        carObject['price']=resultresult['price']
		        carObject['stop_time']=resultresult['stop_time']
		        carObject['permalink']=resultresult['permalink']
		        carObject['thumbnail']=resultresult['thumbnail']
		        carObject['location']=resultresult['location']['city']['name']
		        for attribute in resultresult['attributes']:
		        	if attribute['id']=='MCO1744-KMTS':
		        		carObject['mileage']=attribute['value_name']
	        		if attribute['id']=='MCO1744-YEAR':
		        		carObject['year']=attribute['value_name']

		        carList.append(carObject)
		        if not Match.objects.filter(external_id=carObject['external_id']).exists():
		        	match=Match.objects.create(
						external_id =carObject['external_id'],
						title =carObject['title'],
						category_id =carObject['category_id'],
						price =carObject['price'],
						start_time ='',
						stop_time =carObject['stop_time'],
						permalink =carObject['permalink'],
						thumbnail =carObject['thumbnail'],
						last_updated ='',
						year =carObject['year'],
						mileage =carObject['mileage'],
						location =carObject['location'],
			        	)	
			        match.save()
			        match.alerts.add(alert)
			        subject_email="Nuevo carro publicado"
			        message_email="""
			        Encontramos el siguiente carro %s
			        """ %(carObject['title'])
			        from_email="andres@adiktivo.com"
			        to_email=[alert.user.email,"andresbuitragof@gmail.com"]
			        html_email="""
			        <h1>Buenas noticias</h1>

			        <div class='container'>
						<div class='row'>
								<div class='col-sm-6 col-md-3 col-lg-3'>
									<div class='thumbnail'>
										<img src='"""+carObject['thumbnail']+"""' alt='"""+carObject['title']+"""' width='150px'>
										<div class='caption'>
											<h3>$ """+str(carObject['price'])+"""</h3>
											<p>"""+carObject['title']+"""</p>
											<p>"""+str(carObject['year'])+""" | """+str(carObject['mileage'])+""" Km | """+carObject['location']+"""</p>
											<p><a href='"""+carObject['permalink']+"""' class='btn btn-primary' role='button'>Ver en el sitio</a></p>
										</div>
									</div>
								</div>
						</div>
					</div>
			        """
			        send_mail(
					    subject_email,
					    message_email,
					    from_email,
					    to_email,
					    html_message=html_email,
					    fail_silently=False,
					)

	context={
	"carros": carList,
	}
	return render(request, "alertas/alertas_catalog.html", context)