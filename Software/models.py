from decimal import Decimal
from datetime import datetime
from django.db import models
from django import forms

STATES = { '25': 'Daman and Diu', '13': 'Nagaland', '02': 'Himachal Pradesh', '17': 'Meghalaya', '06': 'Haryana', '15': 'Mizoram', '18': 'Assam', '32': 'Kerala', '26': 'Dadra and Nagar Haveli', '22': 'Chattisgarh', '28': 'Andhra Pradesh', '30': 'Goa', '31': 'Lakshadweep Islands', '21': 'Odisha', '20': 'Jharkhand', '11': 'Sikkim', '07': 'Delhi', '16': 'Tripura', '27': 'Maharashtra', '24': 'Gujarat', '09': 'Uttar Pradesh', '35': 'Andaman and Nicobar Islands', '33': 'Tamil Nadu', '10': 'Bihar', '37': 'New Andhra Pradesh (37)', '36': 'Telangana', '19': 'West Bengal', '03': 'Punjab', '12': 'Arunachal Pradesh', '08': 'Rajasthan', '14': 'Manipur', '29': 'Karnataka', '34': 'Pondicherry', '23': 'Madhya Pradesh', '01': 'Jammu and Kashmir', '05': 'Uttarakhand', '04': 'Chandigarh'}
SGST = 2.5
CGST = 2.5
IGST = 5.0

def int_to_en(num):
	if type(num) == float:
		rs = int(num)
		paise = int((num%1.0)*100)
		if paise > 0 :
			return "{0} rupees and {1} paise".format( int_to_en(rs) , int_to_en(paise))
		else:
			return "{0} rupees".format( int_to_en(rs))

	d = { 0 : 'Zero', 1 : 'One', 2 : 'Two', 3 : 'Three', 4 : 'Four', 5 : 'Five', 6 : 'Six', 7 : 'Seven', 8 : 'Eight', 9 : 'Nine', 10 : 'Ten', 11 : 'Eleven', 12 :  'Twelve', 13 :  'Thirteen', 14 :  'Fourteen', 15 :  'Fifteen', 16 :  'Sixteen', 17 :  'Seventeen', 18 :  'Eighteen', 19 :  'Nineteen', 20 :  'Twenty', 30 :  'Thirty', 40 :  'Forty', 50 :  'Fifty', 60 :  'Sixty', 70 :  'Seventy', 80 :  'Eighty', 90 :  'Ninety' }
	k = 1000
	m = k * 1000
	b = m * 100
	t = b * 100
	assert(0 <= num)
	if (num < 20): return d[num]
	if (num < 100):
		if num % 10 == 0: return d[num]
		else: return d[num // 10 * 10] + '-' + d[num % 10]
	if (num < k):
		if num % 100 == 0: return d[num // 100] + ' Hundred'
		else: return d[num // 100] + ' Hundred and ' + int_to_en(num % 100)
	if (num < m):
		if num % k == 0: return int_to_en(num // k) + ' Thousand'
		else: return int_to_en(num // k) + ' Thousand, ' + int_to_en(num % k)
	if (num < b):
		if (num % m) == 0: return int_to_en(num // m) + ' Lac'
		else: return int_to_en(num // m) + ' Lac, ' + int_to_en(num % m)
	if (num < t):
		if (num % m) == 0: return int_to_en(num // t) + ' Crores'
		else: return int_to_en(num // t) + ' Crores, ' + int_to_en(num % t)
	
	else: return ''
	
class Size(models.Model):
	name = models.CharField(max_length=100,blank=False,unique=False)
	def __str__(self): return self.name
	
class Client(models.Model):
	def _get_state(self): return STATES[ self.state_code ]
	def __str__(self): return self.name

	name = models.CharField(max_length=120 , blank=False, null=False , unique=False)
	address = models.CharField(max_length=300,blank=True , null = True , default = None)
	mobile = models.CharField(max_length=50,blank=True,null=True)
	gstin = models.CharField(max_length=30,blank=True, null=True, unique=False)
	debit_balance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0.0)
	state = property(_get_state)
	state_code = models.CharField(max_length=2,blank=True, null=False, unique=False)
		
class Agent(models.Model):
	name = models.CharField(max_length=150 , blank=False, null=False , unique=False)
	mobile = models.CharField(max_length=50,blank=True,null=True)
	def __str__(self): return self.name

class Bill(models.Model):
	is_taxable = models.BooleanField(default=False)

	invoice_date = models.DateField(auto_now_add=True , auto_now=False)
	invoice_number = models.CharField(max_length=10 , blank=False , null=False,  unique=True)
	client = models.ForeignKey(Client, on_delete=models.CASCADE)
	date_of_supply = models.DateField()
	place_of_supply = models.CharField(max_length=50 , blank=True, null=True , unique=False)
	transport_mode = models.CharField(max_length=200 , blank=True, null=True , unique=False)
	vehicle_number = models.CharField(max_length=100 , blank=True, null=True , unique=False)
	agent = models.ForeignKey(Agent ,blank=True, null=True, on_delete=models.SET_NULL)
	total_before_tax = models.DecimalField(max_digits=12, decimal_places=2, blank=False, default=0)
	cgst = models.DecimalField(max_digits=10, decimal_places=2, blank=False, default=0)
	sgst = models.DecimalField(max_digits=10, decimal_places=2, blank=False, default=0)
	igst = models.DecimalField(max_digits=10, decimal_places=2, blank=False, default=0)
	total_after_tax = models.DecimalField(max_digits=12, decimal_places=2, blank=False, default=0)
	description = models.CharField(max_length=500 ,blank=True,null=True)
	
	is_cleared = models.BooleanField(default=False)
	is_deleted = models.BooleanField(default=False)

	qty_total = models.IntegerField()
	discount = models.DecimalField(max_digits=10 , decimal_places=2, blank=False, default=0)

	def qty_total_set(self):
		self.qty_total = sum([x.qty for x in self.item_set.all()])
	
	def before_discount(self):
		return round( (self.total_before_tax*100) / (100-self.discount) , 2)
	
	def discount_value (self):
		return self.total_before_tax - self.before_discount()

	def cgst_value(self): 
		if self.cgst>0 :return round((self.total_after_tax-self.total_before_tax)/2 ,2)
		else: return 0.0
	
	def sgst_value(self): 
		if self.sgst>0: return round( (self.total_after_tax-self.total_before_tax)/2 ,2)
		else: return 0.0
	
	def igst_value(self): 
		if self.igst>0: return round(self.total_after_tax-self.total_before_tax ,2)
		else: return 0.0
	
	def total_tax(self): return float(self.total_after_tax - self.total_before_tax)
	def printable_date(self): return self.invoice_date.strftime('%d %B, %Y')
	def printable_date_of_supply(self): return self.date_of_supply.strftime('%d %B, %Y')
	def total_before_tax_words(self): return int_to_en(float(self.total_before_tax))
	def total_after_tax_words(self): return int_to_en(float(self.total_after_tax))
	def total_tax_words(self): return int_to_en(float(self.total_tax()))
	
	def __str__(self): return "{0} {1}".format(self.invoice_number , self.client.name)

class Product(models.Model):
	name = models.CharField(max_length=150,blank=False,null=False)
	hsn_code = models.CharField(max_length=20,blank=True,null=True)
	def __str__(self): return self.name

class Item(models.Model):
	def __get_amount(self): return self.rate * self.qty
	def __str__(self): return "{0}-{1}".format(self.bill.id , self.id)
	bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	size = models.ForeignKey(Size, on_delete=models.CASCADE)
	rate = models.DecimalField(max_digits=10, decimal_places=2, blank=False, default=0.0)
	qty = models.DecimalField(max_digits=10, decimal_places=0, blank=False, default=0)
	amount = property(__get_amount)

class Payment(models.Model):
	client = models.ForeignKey(Client, on_delete=models.CASCADE)
	paid_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=False, default=0)
	payment_date = models.DateField(auto_now_add=True , auto_now=False)
	method_of_payment = models.CharField(max_length=100,null=False, blank=False,unique=False)
	description = models.CharField(max_length=200,null=True, blank=True,unique=False)
	is_cleared = models.BooleanField(default=False)

	def __str__(self): 
		return "{0} {1}".format(self.client.name, self.payment_date)

## ============================================================================================================= ##
## ============================================================================================================= ##
## 										MODEL-FORMS 															 ##
## ============================================================================================================= ##
## ============================================================================================================= ##

class BillForm(forms.ModelForm):
	client = forms.ModelChoiceField(queryset=Client.objects.all() ,  empty_label=None , widget=forms.Select(attrs={'class' : 'form-control' , 'required' : '', 'oninvalid':"this.setCustomValidity('Bill cannot be made without a client.')"}))
	date_of_supply = forms.DateField(widget= forms.TextInput(attrs={'class' : 'form-control border-input' , 'type':'date' , 'required' : '', 'oninvalid':"this.setCustomValidity('Enter proper date of supply')", 'min':'2017-01-01'}))
	agent = forms.ModelChoiceField(queryset=Agent.objects.all(), empty_label='' , required=False, widget=forms.Select(attrs={'class' : 'form-control'}))

	def clean_agent(self):
		agent = self.cleaned_data.get("agent" , None)
		if agent==None: return 
		try:
			agent = Agent.objects.get(name=agent)
		except:
			agent = Agent(name=agent , mobile='')
			agent.save()
		return agent

	class Meta:
		model = Bill
		exclude =  ("invoice_date", "invoice_number" , "total_before_tax" , "cgst" , "sgst" , "igst" , "total_after_tax" , "is_cleared" , "is_deleted" , "qty_total")
		widgets = {
			'is_taxable' : forms.TextInput(attrs={'type' : 'checkbox', 'class':'onoffswitch-checkbox' , 'id' :"myonoffswitch" , 'checked' : ''}),
			'place_of_supply' : forms.TextInput(attrs={'class' : 'form-control border-input'}),
			'transport_mode' :  forms.TextInput(attrs={'class' : 'form-control border-input'}),
			'vehicle_number' : forms.TextInput(attrs={'class' : 'form-control border-input'}),
			'description' : forms.Textarea(attrs={'class' : 'form-control border-input', 'rows' : 3 }),
			'discount' : forms.TextInput(attrs={'class' : 'form-control border-input' , 'type' : 'number' , 'placeholder' : '0.0',  'required' : '', 'step' : '0.01', 'oninvalid':"this.setCustomValidity('Enter valid discount')" }),
		}

class ClientForm(forms.ModelForm):
	state_code = forms.ChoiceField(choices=STATES.items() , widget=forms.Select(attrs={'class' : 'form-control'}))
	class Meta:
		model=Client
		exclude = "debit_balance",
		widgets = {
			'name' : forms.TextInput(attrs={'class' : 'form-control border-input' , 'required' : '', 'oninvalid':"this.setCustomValidity('Client Name should be entered')"}),
			'address' : forms.Textarea(attrs={'class' : 'form-control border-input', 'rows' : 3 }),
			'mobile' : forms.TextInput(attrs={'class' : 'form-control border-input'}),
			'gstin':forms.TextInput(attrs={'class':'form-control border-input', "pattern":r"\d{2}[a-zA-Z]{5}\d{4}[a-zA-Z]{1}\d[zZ]{1}[a-zA-Z\d]{1}", 'oninvalid':"this.setCustomValidity('Enter a valid GSTIN eg. 24ABCDE1234A1ZV')"})
		}

class ItemForm(forms.ModelForm):
	product = forms.ModelChoiceField(empty_label=None, queryset=Product.objects.all(), widget=forms.Select(attrs={'class': 'form-control product', 'required' : ''}) )
	size = forms.ModelChoiceField(empty_label=None, queryset=Size.objects.all(), widget=forms.Select(attrs={'class': 'form-control size', 'required' : '' }))

	def clean_product(self):
		product = self.cleaned_data.get("product" , None)
		try: product = Product.objects.get(name=product)
		except:
			product = Product(name=product , hsn_code='')
			product.save()
		return product

	def clean_size(self):
		size = self.cleaned_data.get("size" , None)
		try: size = Size.objects.get(name=size)
		except:
			size = Size(name=size)
			size.save()
		return size

	class Meta:
		model=Item
		exclude="bill",
		widgets = { 
			'rate' : forms.TextInput(
				attrs={
					'class':'form-control border-input rate',
					'type' :'number',
					'placeholder':'0.0',
					'required':'',
					'step':'0.01',
					'oninvalid':"this.setCustomValidity('Enter valid rate')",
					'min':'0.0',
				}),
			'qty' : forms.TextInput(
				attrs={
					'class':'form-control border-input quantity',
					'type':'text',
					'placeholder':'0',
					'required':'',
					'pattern':r"\d+",
					'oninvalid':"this.setCustomValidity('Enter valid quantity')",
					'min':'0',
				}),
		}

class PaymentForm(forms.ModelForm):
	client = forms.ModelChoiceField(queryset=Client.objects.all() ,  empty_label=None , widget=forms.Select(attrs={'class' : 'form-control' , 'required' : ''}))
	class Meta:
		model = Payment
		exclude = ("payment_date", "is_cleared",)
		widgets = {
			'paid_amount' : forms.TextInput(attrs={'class' : 'form-control border-input' , 'required' : '' , 'type' : 'number', "min": "0" , "step" : "0.01"}),
			'method_of_payment' : forms.TextInput(attrs={'class' : 'form-control border-input' , 'required' : ''}),
			'description' : forms.Textarea(attrs={'class' : 'form-control border-input', 'rows' : 3  }),
		}

class ProductForm(forms.ModelForm):
	class Meta:
		model=Product
		exclude = "",
		widgets = {
			'name' : forms.TextInput(attrs={'class' : 'form-control border-input' , 'required' : ''}),
			'hsn_code' : forms.TextInput(attrs={'class' : 'form-control border-input'}),
		}

class SizeForm(forms.ModelForm):
	class Meta:
		model=Size
		exclude="",
		widgets = {
			'name' : forms.TextInput(attrs={'class' : 'form-control border-input' , 'required' : ''}),
		}

class AgentForm(forms.ModelForm):
	class Meta:
		model=Agent
		exclude="",
		widgets = {
			'name' : forms.TextInput(attrs={'class' : 'form-control border-input' , 'required' : ''}),
			'mobile' : forms.TextInput(attrs={'class' : 'form-control border-input'}),
		}
