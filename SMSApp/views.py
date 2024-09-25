from typing import Any, Dict
from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.views.generic import View, TemplateView, CreateView, FormView, DetailView, ListView
from SMS import settings
from django.contrib.auth.models import User
import datetime
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import *
def home(self):
    return render(self,'html/home.html')
def register(request):
    if request.method == "POST":
        f = UsuserForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request,"User Created sucessfully")
        return redirect('/login')
    f = UsuserForm()
    return render(request,'html/signup.html',{'g':f})

def help(request):
    if request.method == "POST":
        sndr = request.POST['sn']
        sbj = request.POST['sb']
        m = request.POST['msg']
        t = settings.EMAIL_HOST_USER
        b = send_mail(sbj,m,t,[sndr])
        if b == 1:
            messages.success(request,"Mail has sent Successfully")
            return redirect('/helpdesk')
        else:
            messages.error(request,"Mail not sent")
            return redirect('/helpdesk')
    return render(request,'html/helpdesk.html')

def book(self):
    return render(self,'html/services.html')

def details(request):
    product = Product.objects.all()
    return render(request,'html/service_details.html',{'products':product})

def userlist(request): 
	c = User.objects.all()
	a = User.objects.all()
	n,m = {},{}
	if request.method == "POST":
		s = UslistForm(request.POST)
		if s.is_valid():
			s.save()
			messages.success(request,"User Created Successfully")
			return redirect('/usrlst')
		else:
			n[s] = s.errors
	for j in n.values():
		for v in j.items():
			m[v[0]] = v[1]
	s = UslistForm()
	return render(request,'html/userlist.html',{'w':s,'p':m.items(),'k':c})

def userdelete(request,d):
    n=User.objects.get(id=d)
    if request.method == "POST":
        n1=UdForm(request.POST,instance=n)
        n.delete()
        return redirect('/usrlst')
    n1=UdForm(instance=n)
    return render(request,'html/userdel.html',{'a':n1})

def profile(request):
    return render(request, "html/userprofile.html")


@login_required
def view_cart(request):
    cart = Cart.objects.get_or_create(user=request.user)[0]
    cart_items = cart.cartitem_set.all()
    cart_total = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'html/cart.html', {'cart_items': cart_items,'cart_total': cart_total})

@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('view_cart')

@login_required
def remove_from_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    cart = Cart.objects.get(user=request.user)
    cart_item = CartItem.objects.get(cart=cart, product=product)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('view_cart')   



def checkout(request):
    cart_items = CartItem.objects.filter(cart=request.user.cart)  # Get cart items for the user
    cart_total = sum(item.product.price * item.quantity for item in cart_items)
    if request.method == 'POST':
        address_form = AddressForm(request.POST)
        if address_form.is_valid():
            # Create the Address object
            address = address_form.save(commit=False)
            address.user = request.user
            address.save()

            # Create the Order object
            order = Order.objects.create(user=request.user, address=address, delivery_date=request.POST['delivery_date'])
            for item in cart_items:
                order.products.add(item.product)

            return redirect('order_confirmation',order_id=order.id)  # Redirect to order confirmation page
    else:
        address_form = AddressForm()

    context = {
        'address_form': address_form,
        'cart_items': cart_items,
        'cart_total': cart_total,
    }
    return render(request, 'html/checkout.html', context)
from decimal import Decimal
def order_confirmation(request,order_id):
    order = Order.objects.filter(user=request.user).latest('order_date')
    total_amount=Decimal(0.00)
    for item in order.products.all():
        total_amount+=item.price
    order.total_amount=total_amount
    order.save()
    
    return render(request, 'html/order_confirmation.html', {'order': order})
from django.db.models import Sum

from django.db.models import Sum

def order_history(request, user_id):
    user = get_object_or_404(User, id=user_id)
    orders = Order.objects.filter(user=user).order_by('-order_date')

    return render(request, 'html/userorders.html', {'user': user, 'orders': orders})

def cancel_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        # Add cancellation logic here (e.g., changing order status)
        order.status = 'Cancelled'
        order.delete()
        messages.success(request, 'Order has been cancelled.')
    except Order.DoesNotExist:
        messages.error(request, 'Order not found.')
    
    return redirect('services')
def service_requests(request):
    service_requests=Order.objects.filter(status='Pending')
    return render(request,'html/service_requests.html',{'service_requests':service_requests})

from django.shortcuts import render
from .forms import ProductForm

def add_services(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = ProductForm()

    return render(request, 'html/addservices.html', {'form': form})
#Dividing services based on categories
def ac_services(request):
    product =Product.objects.filter(category_type="1")
    return render(request,"html/acservices.html",{'product':product})
def eletrical_service(request):
    product = Product.objects.filter(category_type="0")
    return render(request,'html/eletricalservice.html',{'product':product})
def carpenter_service(request):
    product = Product.objects.filter(category_type="3")
    return render(request,'html/Carpenterservice.html',{'product':product})

from django.shortcuts import render
from .forms import Serviceform

def service_form(request):
    if request.method == 'POST':
        g = Serviceform(request.POST, request.FILES)
        if g.is_valid():
            service=g.save(commit=False)
            service.user = request.user
            service.save()
    else:
        g = Serviceform()  
    
    return render(request, 'html/servicerapproval.html', {'form': g})

def pending_submissions(request):
    pending_services = Service.objects.filter(is_approved= False)
    return render(request,'html/pending_submissions.html',{'pending_services':pending_services})

def approve_service(request, service_id):
    service = get_object_or_404(Service, pk=service_id)

    if request.method == 'POST':
        if 'approve' in request.POST:
            service.is_approved=True
            service.save()
            Approvals.objects.create(service=service,is_approved=True)
            return redirect('pending_submissions')
        elif 'dont_approve' in request.POST:
            service.delete()
            user=service.user
            return redirect('pending_submissions')
    return render(request, 'html/approve_service.html', {'service': service})


def approved_service_providers(request,order_id):
    approved_service_providers = Service.objects.filter(is_approved=True)
    return render(request,'html/approvedusers.html',{'f':approved_service_providers})
    
    
from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, Service, AllocatedOrder
from .forms import AllocationForm

'''def bookings(request, user_id):
    service_provider = get_object_or_404(Service, user_id=user_id)
    bookings = AllocatedOrder.objects.filter(service_provider=service_provider)
    return render(request, 'html/bookings.html', {'bookings': bookings, 'service_provider': service_provider})'''

from django.shortcuts import render, get_object_or_404, redirect
from .models import AllocatedOrder, Service

from django.shortcuts import render, get_object_or_404
from .models import AllocatedOrder, Service

def bookings(request, user_id):
    try:
        service_provider = Service.objects.get(user_id=user_id,is_approved=True)
    except Service.DoesNotExist:
        service_provider = None

    # Check if the service provider is not approved
    if service_provider and not service_provider.is_approved:
        approval_message = "You need to get approved to start taking bookings."
        bookings = []  # No bookings to display
    else:
        approval_message = None
        bookings = AllocatedOrder.objects.filter(service_provider=service_provider)

    return render(request, 'html/bookings.html', {'bookings': bookings, 'service_provider': service_provider, 'approval_message': approval_message})
    





from django.core.mail import send_mail
from django.template.loader import render_to_string



from django.shortcuts import render, get_object_or_404, redirect
from .models import Order, Service, AllocatedOrder
from .forms import AllocationForm
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib import messages
@login_required  # Make sure the user is logged in to access this view
def update_profile(request):
    if request.method == 'POST':
        form = Updateprofile(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('pf')  
    else:
        form = Updateprofile(instance=request.user)  

    return render(request, 'html/userupd.html', {'s': form})

def review_rating(request):
    if request.method =='POST':
        form=rarform(request.POST)
        if form.is_valid():
            
            form.save()
            return redirect('order_history')
    else:
        form = rarform()
    return render(request,'html/reviewandrating.html',{'form': form})





    



from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.shortcuts import render, redirect, get_object_or_404
# Import your AllocationForm

'''def allocate_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    approved_service_providers = Service.objects.filter(is_approved=True)

    if request.method == "POST":
        form = AllocationForm(request.POST)
        if form.is_valid():
            try:
                selected_provider_id = form.cleaned_data['selected_provider'].id
                selected_provider = get_object_or_404(Service, pk=selected_provider_id)
            except ObjectDoesNotExist:
                messages.error(request, 'Invalid service provider selected.')
                return redirect('service_requests')

            # Create or update AllocatedOrder entry
            allocated_order, created = AllocatedOrder.objects.get_or_create(
                order=order,
                defaults={'service_provider_id': selected_provider_id}
            )

            if not created:
                allocated_order.service_provider_id = selected_provider_id
                allocated_order.save()

            # Send email to the user (customer)
            subject = 'Your Service Request Allocation Notification'
            message = f'Your service request has been allocated to {selected_provider.user.username}'
            from_email = 'your_email@example.com'  # Update with your email
            recipient_list = [order.user.email]  # The customer's email

            # Render the email content from the template
            context = {'user': order.user, 'service_provider': selected_provider, 'order': order}
            html_message = render_to_string('html/allocation_email.html', context)

            # Send the email
            send_mail(subject, message, from_email, recipient_list, fail_silently=False, html_message=html_message)

            # Render the updated allocated service providers
            allocated_providers = AllocatedOrder.objects.filter(order=order).select_related('service_provider')

            return render(request, 'html/allocate_order.html', {
                'order': order,
                'approved_service_providers': approved_service_providers,
                'form': form,
                'allocated_providers': allocated_providers,
            })
    else:
        form = AllocationForm()

    allocated_providers = AllocatedOrder.objects.filter(order=order).select_related('service_provider')

    return render(request, 'html/allocate_order.html', {
        'order': order,
        'approved_service_providers': approved_service_providers,
        'form': form,
        'allocated_providers': allocated_providers,
    })'''

def allocate_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    approved_service_providers = Service.objects.filter(is_approved=True)

    if request.method == "POST":
        form = AllocationForm(request.POST)
        if form.is_valid():
            selected_provider_ids = form.cleaned_data['selected_providers']
            
            for selected_provider_id in selected_provider_ids:
                try:
                    selected_provider = get_object_or_404(Service, pk=selected_provider_id.id)
                except ObjectDoesNotExist:
                    messages.error(request, 'Invalid service provider selected.')
                    return redirect('service_requests')

                # Create or update AllocatedOrder entry
                allocated_order, created = AllocatedOrder.objects.get_or_create(
                    order=order,
                    service_provider=selected_provider,
                )

                if not created:
                    allocated_order.service_provider = selected_provider
                    allocated_order.save()

                # Send email to the user (customer)
                subject = 'Your Service Request Allocation Notification'
                message = f'Your service request has been allocated to {selected_provider.user.username}'
                from_email = 'your_email@example.com'  # Update with your email
                recipient_list = [order.user.email]  # The customer's email

                # Render the email content from the template
                context = {'user': order.user, 'service_provider': selected_provider, 'order': order}
                html_message = render_to_string('html/allocation_email.html', context)

                # Send the email
                send_mail(subject, message, from_email, recipient_list, fail_silently=False, html_message=html_message)

            # Render the updated allocated service providers
            allocated_providers = AllocatedOrder.objects.filter(order=order).select_related('service_provider')

            return render(request, 'html/allocate_order.html', {
                'order': order,
                'approved_service_providers': approved_service_providers,
                'form': form,
                'allocated_providers': allocated_providers,
            })
    else:
        form = AllocationForm()

    allocated_providers = AllocatedOrder.objects.filter(order=order).select_related('service_provider')

    return render(request, 'html/allocate_order.html', {
        'order': order,
        'approved_service_providers': approved_service_providers,
        'form': form,
        'allocated_providers': allocated_providers,
    })
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string

@login_required
def unallocate_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    try:
        allocated_order = AllocatedOrder.objects.get(order=order)
        allocated_order.delete()
        messages.success(request, 'Order unallocated successfully!')
    except AllocatedOrder.DoesNotExist:
        messages.error(request, 'Order is not currently allocated.')
    
    return redirect('service_requests')