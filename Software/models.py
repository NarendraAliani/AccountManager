from decimal import Decimal
from django.db import models
from django.db import transaction
from django.db.models import Sum
from django import forms
from django.conf import settings
from django.utils import timezone
from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder
import re
from django.templatetags.static import static

STATES = { '25': 'Daman and Diu', '13': 'Nagaland', '02': 'Himachal Pradesh', '17': 'Meghalaya', '06': 'Haryana', '15': 'Mizoram', '18': 'Assam', '32': 'Kerala', '26': 'Dadra and Nagar Haveli', '22': 'Chattisgarh', '28': 'Andhra Pradesh', '30': 'Goa', '31': 'Lakshadweep Islands', '21': 'Odisha', '20': 'Jharkhand', '11': 'Sikkim', '07': 'Delhi', '16': 'Tripura', '27': 'Maharashtra', '24': 'Gujarat', '09': 'Uttar Pradesh', '35': 'Andaman and Nicobar Islands', '33': 'Tamil Nadu', '10': 'Bihar', '37': 'New Andhra Pradesh (37)', '36': 'Telangana', '19': 'West Bengal', '03': 'Punjab', '12': 'Arunachal Pradesh', '08': 'Rajasthan', '14': 'Manipur', '29': 'Karnataka', '34': 'Pondicherry', '23': 'Madhya Pradesh', '01': 'Jammu and Kashmir', '05': 'Uttarakhand', '04': 'Chandigarh'}
DEFAULT_CGST_RATE = Decimal("2.50")
DEFAULT_SGST_RATE = Decimal("2.50")
DEFAULT_IGST_RATE = Decimal("5.00")
DEFAULT_HSN_CODE = "6205"

INVOICE_TYPE_TAXABLE = "TX"
INVOICE_TYPE_CHOICES = (
	(INVOICE_TYPE_TAXABLE, "Taxable"),
)

INVOICE_TEMPLATE_CLASSIC = "classic"
INVOICE_TEMPLATE_INVOICE1 = "invoice1"
INVOICE_TEMPLATE_CHOICES = (
	(INVOICE_TEMPLATE_CLASSIC, "Classic"),
	(INVOICE_TEMPLATE_INVOICE1, "Invoice 1"),
)
class AuditLog(models.Model):
	action = models.CharField(max_length=50)
	model_name = models.CharField(max_length=100)
	object_id = models.CharField(max_length=50, blank=True, null=True)
	object_repr = models.CharField(max_length=255, blank=True, null=True)
	before_data = models.JSONField(blank=True, null=True)
	after_data = models.JSONField(blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	actor = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		blank=True,
		null=True,
		on_delete=models.SET_NULL,
		related_name="audit_entries",
	)

	class Meta:
		ordering = ["-created_at"]

	def __str__(self):
		return "{0} {1}".format(self.action, self.model_name)


class FirmSettings(models.Model):
	firm_name = models.CharField(max_length=200, default="Gurukrupa Enterprise")
	address_line1 = models.CharField(max_length=255, blank=True, null=True)
	address_line2 = models.CharField(max_length=255, blank=True, null=True)
	city = models.CharField(max_length=100, blank=True, null=True)
	state = models.CharField(max_length=100, blank=True, null=True)
	pincode = models.CharField(max_length=12, blank=True, null=True)
	gstin = models.CharField(max_length=30, blank=True, null=True)
	contact_number = models.CharField(max_length=20, blank=True, null=True)
	alternate_contact_number = models.CharField(max_length=20, blank=True, null=True)
	third_contact_number = models.CharField(max_length=20, blank=True, null=True)
	email = models.EmailField(blank=True, null=True)
	logo = models.ImageField(upload_to="firm/", blank=True, null=True)
	bank_name = models.CharField(max_length=120, blank=True, null=True)
	account_name = models.CharField(max_length=120, blank=True, null=True)
	account_number = models.CharField(max_length=50, blank=True, null=True)
	ifsc_code = models.CharField(max_length=20, blank=True, null=True)
	rtgs_code = models.CharField(max_length=30, blank=True, null=True)
	upi_id = models.CharField(max_length=120, blank=True, null=True)
	invoice_footer = models.TextField(blank=True, null=True)
	invoice_terms = models.TextField(blank=True, null=True)
	cgst_rate = models.DecimalField(max_digits=6, decimal_places=2, default=DEFAULT_CGST_RATE)
	sgst_rate = models.DecimalField(max_digits=6, decimal_places=2, default=DEFAULT_SGST_RATE)
	igst_rate = models.DecimalField(max_digits=6, decimal_places=2, default=DEFAULT_IGST_RATE)
	show_invoice_delete_button = models.BooleanField(default=True)
	show_payment_delete_button = models.BooleanField(default=True)
	show_client_delete_button = models.BooleanField(default=True)
	show_size_delete_button = models.BooleanField(default=True)
	show_product_delete_button = models.BooleanField(default=True)
	show_agent_delete_button = models.BooleanField(default=True)
	invoice_template = models.CharField(max_length=30, choices=INVOICE_TEMPLATE_CHOICES, default=INVOICE_TEMPLATE_CLASSIC)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.firm_name

	def logo_url(self):
		if self.logo:
			return self.logo.url
		return static("logo/logo.jpg")

	@classmethod
	def current(cls):
		obj = cls.objects.first()
		if obj is None:
			obj = cls.objects.create(
				firm_name="Gurukrupa Enterprise",
				cgst_rate=DEFAULT_CGST_RATE,
				sgst_rate=DEFAULT_SGST_RATE,
				igst_rate=DEFAULT_IGST_RATE,
				third_contact_number="",
				show_invoice_delete_button=True,
				show_payment_delete_button=True,
				show_client_delete_button=True,
				show_size_delete_button=True,
				show_product_delete_button=True,
				show_agent_delete_button=True,
				invoice_template=INVOICE_TEMPLATE_CLASSIC,
			)
		else:
			updates = {}
			if obj.cgst_rate is None:
				updates["cgst_rate"] = DEFAULT_CGST_RATE
			if obj.sgst_rate is None:
				updates["sgst_rate"] = DEFAULT_SGST_RATE
			if obj.igst_rate is None:
				updates["igst_rate"] = DEFAULT_IGST_RATE
			if obj.show_invoice_delete_button is None:
				updates["show_invoice_delete_button"] = True
			if obj.show_payment_delete_button is None:
				updates["show_payment_delete_button"] = True
			if obj.show_client_delete_button is None:
				updates["show_client_delete_button"] = True
			if obj.show_size_delete_button is None:
				updates["show_size_delete_button"] = True
			if obj.show_product_delete_button is None:
				updates["show_product_delete_button"] = True
			if obj.show_agent_delete_button is None:
				updates["show_agent_delete_button"] = True
			if obj.third_contact_number is None:
				updates["third_contact_number"] = ""
			if not obj.invoice_template:
				updates["invoice_template"] = INVOICE_TEMPLATE_CLASSIC
			if updates:
				for field, value in updates.items():
					setattr(obj, field, value)
				obj.save(update_fields=list(updates.keys()))
		return obj

	def full_address(self):
		parts = [self.address_line1, self.address_line2, self.city, self.state, self.pincode]
		return ", ".join([part for part in parts if part])


def _json_safe(value):
	if isinstance(value, Decimal):
		return str(value)
	if hasattr(value, "name") and not isinstance(value, (str, bytes)):
		return value.name or str(value)
	if hasattr(value, "isoformat"):
		try:
			return value.isoformat()
		except TypeError:
			pass
	if isinstance(value, dict):
		return {key: _json_safe(item) for key, item in value.items()}
	if isinstance(value, (list, tuple, set)):
		return [_json_safe(item) for item in value]
	return value


def audit_snapshot(instance, include_related=False):
	if instance is None:
		return None
	data = _json_safe(model_to_dict(instance))
	data["__model__"] = instance.__class__.__name__
	data["__repr__"] = str(instance)
	if include_related and hasattr(instance, "item_set"):
		data["items"] = [_json_safe(model_to_dict(item)) for item in instance.item_set.all()]
	return data


def log_audit_entry(action, instance, actor=None, before_data=None, after_data=None):
	AuditLog.objects.create(
		action=action,
		model_name=instance.__class__.__name__ if instance is not None else "Unknown",
		object_id=str(getattr(instance, "pk", "")) if instance is not None else None,
		object_repr=str(instance) if instance is not None else None,
		before_data=_json_safe(before_data),
		after_data=_json_safe(after_data),
		actor=actor if getattr(actor, "is_authenticated", False) else None,
	)

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

	def current_debit_balance(self):
		invoice_total = sum((bill.total_after_tax for bill in self.bill_set.filter(is_deleted=False)), Decimal("0.00"))
		payment_total = sum((payment.paid_amount for payment in self.payment_set.filter(is_deleted=False)), Decimal("0.00"))
		return invoice_total - payment_total

	def refresh_debit_balance(self):
		self.debit_balance = self.current_debit_balance()
		self.save(update_fields=["debit_balance"])
		return self.debit_balance

	def active_bills(self):
		return self.bill_set.filter(is_deleted=False)

	def active_payments(self):
		return self.payment_set.filter(is_deleted=False)

	def active_bill_count(self):
		return self.active_bills().count()
		
class Agent(models.Model):
	name = models.CharField(max_length=150 , blank=False, null=False , unique=False)
	mobile = models.CharField(max_length=50,blank=True,null=True)
	def __str__(self): return self.name

	def active_bills(self):
		return self.bill_set.filter(is_deleted=False)

	def active_bill_count(self):
		return self.active_bills().count()

class Bill(models.Model):
	is_taxable = models.BooleanField(default=True)

	invoice_date = models.DateField(default=timezone.localdate)
	invoice_number = models.CharField(max_length=20 , blank=False , null=False,  unique=True)
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
	
	is_cleared = models.BooleanField(default=False)
	is_deleted = models.BooleanField(default=False)

	qty_total = models.IntegerField(default=0)
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
	
	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
	
	def display_invoice_number(self):
		parts = [part for part in (self.invoice_number or "").split("/") if part]
		if len(parts) >= 3 and re.fullmatch(r"\d{2,4}-\d{2,4}", parts[1]):
			parts.pop(1)
		return "/".join(parts) or (self.invoice_number or "")

	def __str__(self):
		return "{0} {1}".format(self.display_invoice_number(), self.client.name)

class Product(models.Model):
	name = models.CharField(max_length=150,blank=False,null=False)
	hsn_code = models.CharField(max_length=20,blank=True,null=True, default=DEFAULT_HSN_CODE)
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
	is_deleted = models.BooleanField(default=False)

	def __str__(self): 
		return "{0} {1}".format(self.client.name, self.payment_date)

	def printable_date(self):
		return self.payment_date.strftime('%d %B, %Y')

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)


class InvoiceSequence(models.Model):
	invoice_type = models.CharField(max_length=2, choices=INVOICE_TYPE_CHOICES, unique=True)
	prefix = models.CharField(max_length=2)
	last_number = models.PositiveIntegerField(default=0)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return "{0}".format(self.invoice_type)

	@transaction.atomic
	def next_number(self):
		self.last_number += 1
		self.save(update_fields=["last_number", "updated_at"])
		return self.last_number

## ============================================================================================================= ##
## ============================================================================================================= ##
## 										MODEL-FORMS 															 ##
## ============================================================================================================= ##
## ============================================================================================================= ##

class BillForm(forms.ModelForm):
	client = forms.ModelChoiceField(queryset=Client.objects.all() ,  empty_label=None , widget=forms.Select(attrs={'class' : 'form-control' , 'required' : '', 'oninvalid':"this.setCustomValidity('Bill cannot be made without a client.')"}))
	invoice_date = forms.DateField(
		help_text="Defaults to today and can be changed.",
		input_formats=["%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y"],
		widget=forms.DateInput(
			format="%Y-%m-%d",
			attrs={
				'class': 'form-control border-input',
				'type': 'date',
				'required': '',
				'oninvalid':"this.setCustomValidity('Enter proper invoice date')",
				'min': '2017-01-01',
			},
		),
	)
	date_of_supply = forms.DateField(
		help_text="Use the calendar picker or enter a date like 2026-03-26.",
		input_formats=["%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y"],
		widget=forms.DateInput(
			format="%Y-%m-%d",
			attrs={
				'class': 'form-control border-input',
				'type': 'date',
				'required': '',
				'oninvalid':"this.setCustomValidity('Enter proper date of supply')",
				'min': '2017-01-01',
			},
		),
	)
	agent = forms.ModelChoiceField(queryset=Agent.objects.all(), empty_label='' , required=False, widget=forms.Select(attrs={'class' : 'form-control'}))

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if not self.is_bound and not self.initial.get("invoice_date"):
			self.fields["invoice_date"].initial = timezone.localdate()
		if not self.is_bound and not self.initial.get("date_of_supply"):
			self.fields["date_of_supply"].initial = timezone.localdate()

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
		exclude =  ("invoice_number" , "total_before_tax" , "cgst" , "sgst" , "igst" , "total_after_tax" , "is_cleared" , "is_deleted" , "qty_total", "is_taxable")
		widgets = {
			'place_of_supply' : forms.TextInput(attrs={'class' : 'form-control border-input'}),
			'transport_mode' :  forms.TextInput(attrs={'class' : 'form-control border-input'}),
			'vehicle_number' : forms.TextInput(attrs={'class' : 'form-control border-input'}),
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
		try:
			product = Product.objects.get(name=product)
			if not product.hsn_code:
				product.hsn_code = DEFAULT_HSN_CODE
				product.save(update_fields=["hsn_code"])
		except:
			product = Product(name=product , hsn_code=DEFAULT_HSN_CODE)
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
		exclude = ("payment_date", "is_cleared", "is_deleted",)
		widgets = {
			'paid_amount' : forms.TextInput(attrs={'class' : 'form-control border-input' , 'required' : '' , 'type' : 'number', "min": "0" , "step" : "0.01"}),
			'method_of_payment' : forms.TextInput(attrs={'class' : 'form-control border-input' , 'required' : ''}),
			'description' : forms.Textarea(attrs={'class' : 'form-control border-input', 'rows' : 3  }),
		}

class ProductForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if not self.is_bound:
			self.fields["hsn_code"].initial = self.instance.hsn_code or self.initial.get("hsn_code") or DEFAULT_HSN_CODE

	class Meta:
		model=Product
		exclude = "",
		widgets = {
			'name' : forms.TextInput(attrs={'class' : 'form-control border-input' , 'required' : ''}),
			'hsn_code' : forms.TextInput(attrs={'class' : 'form-control border-input', 'placeholder': DEFAULT_HSN_CODE}),
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


class FirmSettingsForm(forms.ModelForm):
	class Meta:
		model = FirmSettings
		fields = "__all__"
		widgets = {
			'firm_name': forms.TextInput(attrs={'class': 'form-control border-input', 'required': ''}),
			'address_line1': forms.TextInput(attrs={'class': 'form-control border-input'}),
			'address_line2': forms.TextInput(attrs={'class': 'form-control border-input'}),
			'city': forms.TextInput(attrs={'class': 'form-control border-input'}),
			'state': forms.TextInput(attrs={'class': 'form-control border-input'}),
			'pincode': forms.TextInput(attrs={'class': 'form-control border-input'}),
			'gstin': forms.TextInput(attrs={'class': 'form-control border-input'}),
			'contact_number': forms.TextInput(attrs={'class': 'form-control border-input'}),
			'alternate_contact_number': forms.TextInput(attrs={'class': 'form-control border-input'}),
			'third_contact_number': forms.TextInput(attrs={'class': 'form-control border-input'}),
			'email': forms.EmailInput(attrs={'class': 'form-control border-input'}),
			'bank_name': forms.TextInput(attrs={'class': 'form-control border-input'}),
			'account_name': forms.TextInput(attrs={'class': 'form-control border-input'}),
			'account_number': forms.TextInput(attrs={'class': 'form-control border-input'}),
			'ifsc_code': forms.TextInput(attrs={'class': 'form-control border-input'}),
			'rtgs_code': forms.TextInput(attrs={'class': 'form-control border-input'}),
			'upi_id': forms.TextInput(attrs={'class': 'form-control border-input'}),
			'cgst_rate': forms.TextInput(attrs={'class': 'form-control border-input', 'type': 'number', 'step': '0.01', 'min': '0'}),
			'sgst_rate': forms.TextInput(attrs={'class': 'form-control border-input', 'type': 'number', 'step': '0.01', 'min': '0'}),
			'igst_rate': forms.TextInput(attrs={'class': 'form-control border-input', 'type': 'number', 'step': '0.01', 'min': '0'}),
			'invoice_template': forms.Select(attrs={'class': 'form-control border-input'}),
			'show_invoice_delete_button': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
			'show_payment_delete_button': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
			'show_client_delete_button': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
			'show_size_delete_button': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
			'show_product_delete_button': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
			'show_agent_delete_button': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
			'invoice_footer': forms.Textarea(attrs={'class': 'form-control border-input', 'rows': 3}),
			'invoice_terms': forms.Textarea(attrs={'class': 'form-control border-input', 'rows': 4}),
			'logo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
		}


def get_invoice_sequence():
	prefix = INVOICE_TYPE_TAXABLE
	sequence, _ = InvoiceSequence.objects.get_or_create(
		invoice_type=INVOICE_TYPE_TAXABLE,
		defaults={"prefix": prefix, "last_number": 0},
	)
	if not sequence.prefix:
		sequence.prefix = prefix
		sequence.save(update_fields=["prefix"])
	return sequence


def next_invoice_number(parcel_digits=None):
	sequence = get_invoice_sequence()
	next_number = sequence.next_number()
	base_number = "{0}/{1}".format(sequence.prefix, str(next_number).zfill(4))
	if parcel_digits and str(parcel_digits).strip():
		parcel_digits = str(parcel_digits).strip()
		if parcel_digits.isalnum():
			return "{0}/{1}".format(base_number, parcel_digits)
	return base_number
