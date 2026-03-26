from datetime import datetime
from decimal import Decimal
import math
from django.http import JsonResponse , HttpResponse
from django.forms import formset_factory , modelformset_factory
from django.shortcuts import render , HttpResponseRedirect , get_object_or_404
import Software.models as md


#####################################################################################################################
##		SECONDARY Functions
#####################################################################################################################
def api(request , model=None , id=None):
	if (model == 'client') :
		try:
			obj = md.Client.objects.get(id=id)
			return JsonResponse({"name" : obj.name , "address" : obj.address , "mobile" : obj.mobile , "gstin" : obj.gstin , "state" : obj.state, "debit" : obj.debit_balance})
		except:
			return JsonResponse({"you get what you deserve" : "nothing"})
	elif (model == 'invoices') :
		try:
			obj = md.Bill.objects.get(id=id)
			obj.is_cleared = not obj.is_cleared
			obj.save()
			return JsonResponse({})
		except:
			pass
	elif (model == 'payments') :
		try:
			obj = md.Payment.objects.get(id=id)
			obj.is_cleared = not obj.is_cleared
			obj.save()
			return JsonResponse({})
		except:
			pass
	elif (model == 'product') :
		try:
			id = str(id)
			if md.Product.objects.filter(name=id).exists():
				product = md.Product.objects.get(name=id)
			else:
				product = md.Product(name=str(id),hsn_code='')
				product.save()
			return JsonResponse({"id" : product.id })
		except:
			return JsonResponse({"id":"0"})
	elif (model == 'size') :
		try:
			id = str(id)
			if md.Size.objects.filter(name=id).exists():
				size = md.Size.objects.get(name=id)
			else:
				size = md.Size(name=str(id))
				size.save()
			return JsonResponse({"id" : size.id })
		except:
			return JsonResponse({"id":"0"})
	return None

def get_invoice_number(tax):
	if tax : return" Tx"+ str(md.Bill.objects.filter(is_taxable=tax).count() + 1 ).zfill(3)
	else: return  "Nt" + str(md.Bill.objects.filter(is_taxable=tax).count() + 1 ).zfill(3)

def process_agent(agent):
	if agent == '' : return ''
	if agent.isdigit()  and md.Agent.objects.filter(id=int(agent)).exists() : return agent
	new_agent = md.Agent(name=agent , mobile='')
	new_agent.save()
	return str(new_agent.id)

#####################################################################################################################
##         SECTION PAGES      
#####################################################################################################################	
def homepage(request):
	return HttpResponseRedirect("/invoices")
	
	template="homepage.html"
	context = {}
	return render(request,template , context)

def agents(request):
	agents = md.Agent.objects.all()
	template="agents.html"
	context = {'agents' : agents}
	return render(request,template , context)

def clients(request):
	clients = md.Client.objects.all()
	template="clients.html"
	context = {'clients' : clients}
	return render(request,template , context)

def invoices(request):
	invoices = md.Bill.objects.all()
	template="invoices.html"
	context = {'invoices' : invoices}
	return render(request,template , context)

def payments(request):
	payments = md.Payment.objects.all()
	template="payments.html"
	context = {'payments' : payments}
	return render(request,template , context)

def products(request):
	products = md.Product.objects.all()
	template="products.html"
	context = {'products' : products}
	return render(request,template , context)

def sizes(request):
	if request.method == 'POST' :
		size_form = md.SizeForm(request.POST)
		if size_form.is_valid():
			size_form.save(commit=True)
			return HttpResponseRedirect('/sizes/')
	else:
		size_form = md.SizeForm()
	sizes = md.Size.objects.all()
	template = 'sizes.html'
	context = {'sizes' : sizes , 'form' : size_form}
	return render(request,template , context)	


#####################################################################################################################
##			ADD SOMETHING
#####################################################################################################################
def new_agent(request):
	if request.method == 'POST':
		temp_form = md.AgentForm(request.POST)
		if temp_form.is_valid():
			temp_agent = temp_form.save(commit=False)
			temp_agent.save()
			return HttpResponseRedirect("/agents")

	temp_form = md.AgentForm()
	template = "new_agent.html"
	context = {'form' : temp_form}
	return render(request , template, context)

def new_client(request):
	if request.method == 'POST' : 
		temp_form = md.ClientForm(request.POST)
		if temp_form.is_valid():
			temp_client = temp_form.save(commit=False)
			temp_client.debit_balance = 0.0
			temp_client.save()
			return HttpResponseRedirect("/invoices/new")
		else:
			temp_form = md.ClientForm(request.POST)
	else:
		temp_form = md.ClientForm()
	template="new_client.html"
	context = {"form" : temp_form , "states" : md.STATES}
	return render(request,template , context)

def new_invoice(request):
	errors = None
	formset = formset_factory(md.ItemForm , extra=1)
	if request.method == 'POST' :
		## Add a dynamic Agent name if it doesn't exists
		request.POST._mutable=True
		request.POST['agent'] = process_agent(request.POST.get('agent', ''))
		request.POST._mutable=False
		
		form = md.BillForm(request.POST)
		Itemformset = formset(request.POST)
		if form.is_valid() and Itemformset.is_valid():
			bill = form.save(commit=False)
			if 'is_taxable' in request.POST : bill.is_taxable = True
			
			parcel_digits = request.POST.get("parcel_digits" , "")
			if parcel_digits and parcel_digits.strip().isalnum() :
				bill.invoice_number = get_invoice_number(bill.is_taxable) + "/{0}".format(parcel_digits)
			else:
				bill.invoice_number = get_invoice_number(bill.is_taxable)
			bill.qty_total = 0
			bill.save()
			
			bill.total_before_tax = Decimal(0)
			for Itemform in Itemformset:
				item = Itemform.save(commit=False)
				item.bill= bill
				item.save()
				bill.total_before_tax += item.rate*item.qty

			bill.total_before_tax *= (100-bill.discount)*Decimal(0.01) 
			if bill.is_taxable:
				if bill.client.state_code == '24':
					bill.cgst = 2.5
					bill.sgst = 2.5
					bill.igst = 0.0
				else:
					bill.cgst = 0
					bill.sgst = 0
					bill.igst = 5.0
				bill.total_after_tax = Decimal(math.ceil(float(bill.total_before_tax)*1.05))
			else:
				bill.cgst = 0
				bill.sgst = 0
				bill.igst = 0
				bill.total_after_tax = Decimal(math.ceil(float(bill.total_before_tax)))

			bill.qty_total_set()
			bill.save()
			bill.client.debit_balance += bill.total_after_tax
			bill.client.save()
			return HttpResponseRedirect("/invoices/{0}".format(bill.id))
		else:
			print(form.errors)
			print(Itemformset.errors)
	else:	
		form = md.BillForm()
	template="new_invoice.html"
	context = {
		"form" : form,
		"formset" : formset(),
		"errors" : errors,
		"size_choices" : [x.name for x in md.Size.objects.all()],
		"product_choices" : [x.name for x in md.Product.objects.all()],
		"add" : True,
		"name" : "New Invoice",
	}
	return render(request,template , context)

def new_payment(request):
	if request.method == 'POST' : 
		temp_form = md.PaymentForm(request.POST)
		if temp_form.is_valid():
			temp_payment = temp_form.save(commit=False)
			temp_payment.save()
			temp_payment.client.debit_balance -= temp_payment.paid_amount
			temp_payment.client.save()
			return HttpResponseRedirect("/payments")
		else:
			return HttpResponse(str(temp_form.errors))
	temp_form = md.PaymentForm()
	template="new_payment.html"
	context = {"form" : temp_form , "add" : True}
	return render(request,template , context)

def new_product(request):
	if request.method == 'POST' : 
		temp_form = md.ProductForm(request.POST)
		if temp_form.is_valid():
			temp_product = temp_form.save(commit=False)
			temp_product.save()
			return HttpResponseRedirect("/products")
		else:
			temp_form = md.ProductForm(request.POST)
	else:
		temp_form = md.ProductForm()
	template="new_product.html"
	context = {'form' : temp_form}
	return render(request,template , context)	


#####################################################################################################################
##			Individual Page and Edit
#####################################################################################################################
def single_invoice(request , id):
	try:
		invoice = md.Bill.objects.get(id=id)
	except:
		return HttpResponseRedirect("/invoices")

	if invoice.is_taxable: maximum_bills = 16
	else: maximum_bills=20
	context={'invoice': invoice}
	items = invoice.item_set.all()
	count = len(items)
	blank_rows = maximum_bills - (count%maximum_bills)
	context["blank"] = ([x+count+1 for x in range(blank_rows)])
	
	#template="bill_format.html"
	template="single_invoice.html"
	return render(request,template , context)

def single_product(request,id):
	try:
		product = md.Product.objects.get(id=id)
	except:
		return HttpResponseRedirect("/products")
	
	template = 'single_product.html'
	context = {'product' : product}
	return render(request,template , context)

def single_agent(request,id):
	try:
		agent = md.Agent.objects.get(id=id)
	except:
		return HttpResponseRedirect("/agents")
	
	template = 'single_agent.html'
	context = {'agent' : agent}
	return render(request,template , context)

def single_client(request,id):
	try: client = md.Client.objects.get(id=id)
	except: return HttpResponseRedirect("/clients")
	
	client.debit_balance = sum( [bill.total_after_tax for bill in client.bill_set.all()] ) - sum( [payment.paid_amount for payment in client.payment_set.all()] )
	client.save()
	
	template = 'single_client.html'
	context = {'client' : client}
	return render(request,template , context)

def single_payment(request,id):
	try: payment = md.Payment.objects.get(id=id)
	except: return HttpResponseRedirect("/payments")
	
	template = 'single_payment.html'
	context = {'payment' : payment}
	return render(request,template , context)	

def edit_payment(request,id):
	try : 
		payment = md.Payment.objects.get(id=id)
		old_client = payment.client
		old_amount = payment.paid_amount
	except: return HttpResponseRedirect("/payments/")
	if request.method == 'POST' : 
		temp_form = md.PaymentForm(request.POST , instance=payment)
		if temp_form.is_valid():
			temp_payment = temp_form.save(commit=False)
			temp_payment.save()
			if (old_client == temp_payment.client):
				temp_payment.client.debit_balance -= temp_payment.paid_amount - old_amount
			else:
				old_client.debit_balance += old_amount
				old_client.save()
				temp_payment.client.debit_balance -= temp_payment.paid_amount
			temp_payment.client.save()
			return HttpResponseRedirect("/payments/{0}".format(temp_payment.id))
		else:
			return HttpResponse(str(temp_form.errors))
	temp_form = md.PaymentForm(instance=payment)
	template="new_payment.html"
	context = {"form" : temp_form}
	return render(request,template , context)

def edit_client(request,id):
	try: client = md.Client.objects.get(id=id)
	except: return HttpResponseRedirect("/clients")
	if request.method == 'POST' :
		temp_form = md.ClientForm(request.POST , instance=client)
		if temp_form.is_valid():
			temp_client = temp_form.save(commit=False)
			temp_client.save()
			return HttpResponseRedirect("/clients/{0}".format(client.id))
		else:
			temp_form = md.ClientForm(request.POST)
	
	temp_form = md.ClientForm(instance=client)
	template="new_client.html"
	context={"form" : temp_form}
	return render(request,template , context)

def edit_invoice(request,id):
	error = None
	try:
		old_bill = md.Bill.objects.get(id=id)
		old_bill_taxable = old_bill.is_taxable
		old_items = md.Item.objects.filter(bill=old_bill)
		old_items_id = [item.id for item in old_items]
		old_bill_value = old_bill.total_after_tax
		old_bill_client = old_bill.client
	except:
		return HttpResponseRedirect("/invoices")
	formset = modelformset_factory(md.Item, form=md.ItemForm, extra=0, can_delete=True, max_num=100 )
	if (request.method == 'POST'):
		## Add a dynamic Agent name if it doesn't exists
		request.POST._mutable=True
		request.POST['agent'] = process_agent(request.POST.get('agent', ''))
		request.POST._mutable=False

		form = md.BillForm(request.POST, instance=old_bill)
		Itemformset = formset(request.POST , queryset=old_items)
		if form.is_valid() and Itemformset.is_valid():
			bill = form.save(commit=False)
			bill.is_taxable = old_bill_taxable
			parcel_digits = request.POST.get("parcel_digits" , "")
			if parcel_digits and parcel_digits.strip().isalnum():
				bill.invoice_number = old_bill.invoice_number.split('/')[0] + "/{0}".format(parcel_digits)
			else:
				bill.invoice_number = old_bill.invoice_number
			bill.invoice_date = old_bill.invoice_date
			bill.qty_total = 0
			bill.save()
			
			bill.total_before_tax = Decimal(0)
			for Itemform in Itemformset:
				item = Itemform.save(commit=False)
				if item.id in old_items_id: old_items_id.remove(item.id)
				item.bill= bill
				item.save()
				bill.total_before_tax += item.rate*item.qty
			for item in old_items.filter(id__in=old_items_id):
				item.delete()
			
			bill.qty_total_set()
			bill.total_before_tax *= (100-bill.discount)*Decimal(0.01) 
			if bill.is_taxable:
				if bill.client.state_code == '24':
					bill.cgst = 2.5
					bill.sgst = 2.5
					bill.igst = 0.0
				else:
					bill.cgst = 0
					bill.sgst = 0
					bill.igst = 5.0
				bill.total_after_tax = Decimal(math.ceil(float(bill.total_before_tax)*1.05))
			else:
				bill.cgst = 0
				bill.sgst = 0
				bill.igst = 0
				bill.total_after_tax = Decimal(math.ceil(float(bill.total_before_tax)))
			bill.save()

			old_bill.client.debit_balance -= old_bill_value
			old_bill.client.save()
			bill.client.debit_balance += bill.total_after_tax
			bill.client.save()
			return HttpResponseRedirect("/invoices/{0}".format(bill.id))
		else: 
			print(form.errors)
			fm = formset()
			print(fm.non_form_errors() )
	else:	
		form = md.BillForm(instance=old_bill)
	template="new_invoice.html"
	context = {
		"form" : form,
		"formset" : formset(queryset = old_items),
		"name" : "Edit Invoice",
		"size_choices" : [x.name for x in md.Size.objects.all()],
		"product_choices" : [x.name for x in md.Product.objects.all()],
	}
	return render(request,template , context)
