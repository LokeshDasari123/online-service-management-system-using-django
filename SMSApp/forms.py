from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User
from .models import *


class AusForm(UserCreationForm):
	password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control my-2","placeholder":"Password"}))
	password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control my-2","placeholder":"Password Again"}))
	class Meta:
		model = User
		fields = ["username","role_type","mble"]
		widgets = {
		"username":forms.TextInput(attrs={
			"class":"form-control my-2",
			"placeholder":"Username",
			}),
        "mble":forms.TextInput(attrs={
            "class":"form-control my-2",
			"placeholder":"Enter Mobile no",
            }),
	    "role_type":forms.Select(attrs={
			"class":"form-control my-2",
			}),
		}

class UsuserForm(UserCreationForm):
	password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control my-2","placeholder":"Password"}))
	password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control my-2 mt-3","placeholder":"Password Again"}))
	class Meta:
		model = User
		fields = ["username","role_type","email","mble"]
		widgets = {
		"username":forms.TextInput(attrs={
			"class":"form-control my-3",
			"placeholder":"Username",
			}),
		"role_type":forms.Select(attrs={
			"class":"form-control my-3",
			}),
        "email":forms.TextInput(attrs={
            "class":"form-control my-3",
			"placeholder":"Enter Mail",
            }),
		"mble":forms.TextInput(attrs={
            "class":"form-control my-3",
			"placeholder":"Enter Mobile no",
            }),		
		}

class UslistForm(UserCreationForm):
	password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control my-2","placeholder":"Password"}))
	password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control my-2","placeholder":"Password Again"}))
	class Meta:
		model = User
		fields = ["username","role_type","email","mble"]
		widgets = {
		"username":forms.TextInput(attrs={
			"class":"form-control my-3",
			"placeholder":"Username",
			}),
		"role_type":forms.Select(attrs={
			"class":"form-control my-3",
			}),
        "email":forms.TextInput(attrs={
            "class":"form-control my-3",
			"placeholder":"Enter Mail",
            }),
        "mble":forms.TextInput(attrs={
            "class":"form-control my-3",
			"placeholder":"Enter Mobile no",
            }),		
		}

class UdForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username","email","mble","role_type"]
        widgets = {
            "username":forms.TextInput(attrs={
                "class":"form-control my-2",
                "placeholder":"Username",
                    }),
            "email":forms.EmailInput(attrs={
                "class":"form-control my-2",
                "placeholder":"Email",
                }),
            "mble":forms.TextInput(attrs={
                "class":"form-control my-2",
                "placeholder":"Mobile No",
                }),
            "role_type":forms.Select(attrs={
                "class":"form-control my-2",
            }),
        }
        
from django import forms
from .models import Address

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['flat_address']
        widgets={
			"flat_address":forms.TextInput(attrs={
				 "class":"form-control my-2",
                 "placeholder":"Your Flat Number",
			}),
		}
        
from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'image', 'category_type']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control my-2',
                'placeholder': 'Enter Service name',
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control my-2',
                'placeholder': 'Enter price',
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control-file my-2',
            }),
            'category_type': forms.Select(attrs={
                'class': 'form-control my-2',
            }),
        }
class Serviceform(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['field_type','experience','form']
        widgets = {
            'field_type':forms.Select(attrs={
                'class': 'form-control my-2',
            }),
            'experience':forms.NumberInput(attrs={
                'class': 'form-control my-2',
                'placeholder':'Your Experience',
                }),
            'form':forms.ClearableFileInput(attrs={
                'class': 'form-control-file my-2'
            }),
        
        }
        



'''class AllocationForm(forms.Form):
    selected_provider = forms.ModelChoiceField(
        queryset=Service.objects.filter(is_approved=True),
        label='Select Service Provider',
        empty_label='Select a service provider',
    )'''
    
class AllocationForm(forms.Form):
    selected_providers = forms.ModelMultipleChoiceField(
        queryset=Service.objects.filter(is_approved=True),
        widget=forms.CheckboxSelectMultiple,
    )

class Updateprofile(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'mble']

class rarform(forms.ModelForm):
    class Meta:
        model = ReviewandRating
        fields = ['review','rating']
        widgets ={
            'review':forms.TextInput(attrs={
                'class': 'form-control my-2',
                'placeholder':'Enter your review',
            }),
            'rating':forms.NumberInput(attrs={
                'class': 'form-control my-2',
                'placeholder':'Rate us',
            })
        }
        
        