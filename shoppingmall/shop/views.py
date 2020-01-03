from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Count, F,Sum #WHERE, OR 조건 등 복잡한 SQL 쿼리문을 사용하기 위해 Q 객체를 import
from datetime import date, datetime

# from .forms import ProductForm
from .models import Product, Bid, Shoppinglist, Wish, Review
from accounts.models import Buyer, Seller

#home page
def home(request):
    products = Product.objects
    sort = request.GET.get('sort','')
    #Sorting
    if sort == "new":
        products = products.order_by('-pub_date')
    elif sort == "expen":
        products = products.order_by('-price')
    elif sort == "cheap":
        products = products.order_by('price')
    return render(request, 'home.html', {'products': products})

#Product detail
def detail(request, product_id):
    product_detail = get_object_or_404(Product, pk=product_id)
    reviews = Review.objects.filter(pid=product_id)
    return render(request, 'detail.html', {'product':product_detail, 'reviews':reviews})

#Filtering with category / brand
def filter(request, f, select):
    sort = request.GET.get('sort','')
    if f=="category":
        products = Product.objects.filter(type=select)
        #Ordering by
        if sort == "new":
            products = products.order_by('-pub_date')
        elif sort == "expen":
            products = products.order_by('-price')
        elif sort == "cheap":
            products = products.order_by('price')
    elif f == "status":
        products = Product.objects.filter(status=select)
        if sort == "new":
            products = products.order_by('-pub_date')
        elif sort == "expen":
            products = products.order_by('-price')
        elif sort == "cheap":
            products = products.order_by('price')
    else:
        if select == "10000":
            products = Product.objects.filter(price__lt = 10) #field__lt(less than)
            if sort == "new":
                products = products.order_by('-pub_date')
            elif sort == "expen":
                products = products.order_by('-price')
            elif sort == "cheap":
                products = products.order_by('price')
        elif select =="50000":
            products = Product.objects.filter(price__gte = 10, price__lt = 50) #gte(greater than or equal)
            if sort == "new":
                products = products.order_by('-pub_date')
            elif sort == "expen":
                products = products.order_by('-price')
            elif sort == "cheap":
                products = products.order_by('price')
        elif select =="100000":
            products = Product.objects.filter(price__gte = 50, price__lt = 100)
            if sort == "new":
                products = products.order_by('-pub_date')
            elif sort == "expen":
                products = products.order_by('-price')
            elif sort == "cheap":
                products = products.order_by('price')
        else:
            products = Product.objects.filter(price__gte = 100)
            if sort == "new":
                products = products.order_by('-pub_date')
            elif sort == "expen":
                products = products.order_by('-price')
            elif sort == "cheap":
                products = products.order_by('price')
    return render(request, 'home.html', {'products':products})

#Search product
def searchitem(request):   
    try:
        word = request.GET.get('searching')
    except:
        word = None
    #field__icontains: 대소문자 구분하지 않고 해당 문자열 포함한 경우 return 
    if word is not None and len(word) != 0:
        products = Product.objects.filter(Q(pname__icontains = word) | Q(sellid__username__icontains = word)) 
        return render(request, 'search.html', {'word':word, 'products':products})
   
#Buy product
def buy(request, product_id):
    product = Product.objects.get(pid=product_id)
    reviews = Review.objects.filter(pid=product_id)         
    if Buyer.objects.filter(user = request.user):
        buyer = Buyer.objects.get(user=request.user)
        if product.stock <=0:
            messages.add_message(request, messages.ERROR, 'This product is sold out !!!!!!')
            return render(request, 'detail.html', {'product':product, 'reviews':reviews})
        elif product.stock ==1:
            product.status = 'PUR'
        buyer.pids.add(Product.objects.get(pid=product_id))
        product.stock -= 1
        product.save()
        shoppinglist = Shoppinglist()
        shoppinglist.uid = request.user
        shoppinglist.pid = Product.objects.get(pid=product_id)
        shoppinglist.save()
        messages.add_message(request, messages.SUCCESS, 'Successfully purchased')
    else:
        messages.add_message(request, messages.ERROR, "Only 'BUYERS' are allowed to buy")
    return render(request, 'detail.html', {'product':product, 'reviews':reviews})

#Mypage
def mypage(request):
    if Buyer.objects.filter(user=request.user):
        buyer = Buyer.objects.filter(user=request.user)
        bids = Bid.objects.filter(uid=request.user)
        return render(request, 'mypage.html', {'buyer':buyer, 'bids':bids})
    elif Seller.objects.filter(user=request.user):
        seller = Seller.objects.filter(user=request.user)
        return render(request,'mypage.html', {'seller':seller})

#Bidding
def bid(request, product_id):
    product = Product.objects.get(pid=product_id)
    reviews = Review.objects.filter(pid=product_id)
    if request.method == "POST":
        if Buyer.objects.filter(user = request.user):
            # Can't bid if auction endtime is over
            if product.endtime < date.today():
                messages.add_message(request, messages.ERROR, 'Bid failed. Auction is over!')
                return render(request, 'detail.html', {'product':product, 'reviews':reviews})
            bidprice = request.POST['bidprice']
            if int(bidprice) > product.price:
                #update the product price
                product.price = bidprice
                product.save()
                #make the instance of Bid
                bid = Bid()
                bid.uid = request.user
                bid.price = bidprice
                bid.pid = Product.objects.get(pid=product_id)
                bid.save()
                messages.add_message(request, messages.SUCCESS, 'Bid successfully registered')
            else:
                messages.add_message(request, messages.ERROR, 'Bid failed. Please enter the price higher than the current price.')
        else:
            messages.add_message(request, messages.ERROR, "Only 'BUYERS' are allowed to bid")
    return render(request, 'detail.html', {'product':product, 'reviews':reviews})

# End the auction by seller
def endauction(request, product_id):
    allbid = Bid.objects.filter(pid = product_id)
    auctionitem = Product.objects.get(pid=product_id)
    if allbid.count() <= 0:
        messages.add_message(request, messages.SUCCESS, 'Nobody bidded. Auction successfully ended')
    else:
        # Get the winner of the auction
        winbid = Bid.objects.filter(pid=product_id).order_by('-bidtime')[0]
        winner = Buyer.objects.get(user_id = winbid.uid)
        winner.pids.add(Product.objects.get(pid=product_id))

        # Purchased by the winner
        shoppinglist = Shoppinglist()
        user = User.objects.get(username=winbid.uid)
        shoppinglist.uid = user
        shoppinglist.pid = Product.objects.get(pid=product_id)
        shoppinglist.save()
        messages.add_message(request, messages.SUCCESS, 'Auction successfully ended. The product is purchased by user')
    # Stock and status change
    if auctionitem.stock == 1:
        auctionitem.status = 'PUR'            
    auctionitem.stock -= 1
    auctionitem.status = 'PUR'
    auctionitem.save()
    return redirect('home')

# Add items to wish list 
def addwish(request, product_id):
    product = Product.objects.get(pid=product_id)
    reviews = Review.objects.filter(pid=product_id)
    if Buyer.objects.filter(user = request.user):
        wishitem = Wish()
        wishitem.uid = request.user
        wishitem.pid = product
        wishitem.save()
        messages.add_message(request, messages.SUCCESS, 'Successfully added to WISH LIST')
    else:
        messages.add_message(request, messages.ERROR, "Only 'BUYERS' are allowed to add items to wish list")
    return render(request, 'detail.html', {'product':product, 'reviews':reviews})

#View wish list 
def viewwish(request):
    wishlist = Wish.objects.filter(uid=request.user)
    return render(request, 'wish.html', {'wishlist': wishlist})

# View Shopping list(What buyers bought) for buyers
def cart(request):
    sumprice = 0
    product = Shoppinglist.objects.filter(uid=request.user)
    for x in product:
        sumprice += x.pid.price    
    return render(request, 'cart.html', {'product':product, 'sumprice':sumprice})

# Product list for sellers
def productlist(request):
    user = Seller.objects.filter(user=request.user)
    product = Product.objects.filter(sellid=request.user)
    return render(request, 'productlist.html',{'products':product})

# Product registration for sellers
def productregister(request):
    product = Product.objects.filter(sellid=request.user)
    if request.method == "POST":
        try:
            product.endtime = request.POST['endtime']
        except:
            pass
        if request.user.is_authenticated:
            product = Product()
            product.pname = request.POST['productName']
            product.price = request.POST['productPrice']
            product.stock = request.POST['productStock']
            product.tradeplace = request.POST['tradingPlace']
            product.pimg = request.FILES['photo']
            marketType = request.POST.get('dropdown')
            if marketType == 'AC':
                product.status = 'AUC'
            product.type = marketType
            product.category = request.POST['category']
            product.sellid = request.user
            product.save()
            messages.add_message(request, messages.SUCCESS, 'Successfully registered product')
            return redirect('home')
        else:
            messages.add_message(request, messages.ERROR, 'Registering product failed')
    return render(request, 'productregister.html')
        

# Add Review
def review(request, product_id):
    product = Product.objects.get(pid=product_id)
    reviews = Review.objects.filter(pid=product_id)
    if request.method == "POST":
        if request.user.is_authenticated:
            review = Review()
            review.content = request.POST['content']
            review.uid = request.user
            review.pid = Product.objects.get(pid=product_id)
            review.save()
            messages.add_message(request, messages.SUCCESS, 'Successfully added comment')
        else:
            messages.add_message(request, messages.ERROR, 'Only users are allowed to review')
    return render(request, 'detail.html',{'product':product,  'reviews':reviews})

def deleteProduct(request, product_id):
    user = Seller.objects.filter(user=request.user)
    product = get_object_or_404(Product, pid=product_id)
    product.delete()
    messages.add_message(request, messages.SUCCESS, 'Successfully deleted item')    
    return redirect('home')

def modifyProduct(request,product_id):
    item = get_object_or_404(Product, pid=product_id)
    if request.method == "POST":
        try:
            item.endtime = request.POST['endtime']
        except:
            pass
        item.pname = request.POST['productName']
        item.price = request.POST['productPrice']
        item.stock = request.POST['productStock']
        item.tradeplace = request.POST['tradingPlace']
        item.pimg = request.FILES['photo']
        marketType = request.POST.get('dropdown')
        if marketType == 'AC':
            item.status = 'AUC'
        item.type = marketType
        item.category = request.POST['category']
        item.sellid = request.user
        item.save()
        messages.add_message(request, messages.SUCCESS, 'Successfully modified product')
        return redirect('home')
    return render(request, 'productmodify.html', {'product':item})


def history(request,product_id):
    product = get_object_or_404(Product, pid=product_id)
    # Bid history
    bid = Bid.objects.filter(pid=product_id)
    bid = bid.order_by('bidtime')
    # Count users who wish to buy this product
    wishlist = Wish.objects.filter(pid=product_id)
    howmanyuser = 0
    for x in wishlist:
        howmanyuser += 1
    return render(request, 'productsellerdetail.html', {'product':product, 'bid':bid, 'wishlist':wishlist, 'howmanyuser': howmanyuser})