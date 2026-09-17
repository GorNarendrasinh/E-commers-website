import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .models import User, PurchaseOrder


def home(request):
    username = request.session.get("username")

    return render(request, "index.html", {
        "username": username
    })


def clothingproduct(request):
    return render(request, "clothingproduct.html")


def electronics(request):
    return render(request, "electronics.html")


def Gaming(request):
    return render(request, "gaming.html")


def kidsproduct(request):
    return render(request, "kidsproduct.html")


def toys(request):
    return render(request, "toys.html")

def Stationery(request):
    return render(request, "stationery.html")


def addtocart(request):
    username = request.session.get("username")
    user_logged_in = "user_id" in request.session

    return render(request, "addtocart.html", {
        "username": username,
        "user_logged_in": user_logged_in
    })


def account(request):

    if request.method == "POST":

        username = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        mobile = request.POST.get("mobile", "").strip()
        password = request.POST.get("password", "")

        if not username or not email or not mobile or not password:
            messages.error(request, "All fields are required.")
            return render(request, "account.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, "account.html")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return render(request, "account.html")

        if User.objects.filter(mobile=mobile).exists():
            messages.error(request, "Mobile number already exists.")
            return render(request, "account.html")

        user = User(
            username=username,
            email=email,
            mobile=mobile
        )

        user.set_password(password)
        user.save()

        messages.success(
            request,
            "Account created successfully. Please login."
        )

        return redirect("login")

    return render(request, "account.html")


def login(request):

    if request.method == "POST":

        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "Username does not exist.")
            return render(request, "login.html")

        if user.check_password(password):

            request.session["user_id"] = user.id
            request.session["username"] = user.username

            return redirect("home")

        messages.error(request, "Wrong password.")

    return render(request, "login.html")


def logout_view(request):
    request.session.flush()
    return redirect("home")


import json



def order(request):
    user_id = request.session.get("user_id")

    if not user_id:
        return redirect("login")

    user = get_object_or_404(User, id=user_id)

    return render(request, "order.html", {
        "logged_user": user
    })


def save_purchase(request):

    if request.method != "POST":
        return redirect("order")

    user_id = request.session.get("user_id")

    if not user_id:
        return redirect("login")

    user = get_object_or_404(User, id=user_id)

    products_text = request.POST.get("products", "[]")

    try:
        products = json.loads(products_text)
    except (json.JSONDecodeError, TypeError):
        products = []

    if not isinstance(products, list):
        products = []

    if not products:
        return redirect("order")

    purchase = PurchaseOrder.objects.create(
        user=user,
        full_name=request.POST.get("full_name", user.username),
        mobile=request.POST.get("mobile", user.mobile),
        email=request.POST.get("email", user.email),
        address=request.POST.get("address", ""),
        city=request.POST.get("city", ""),
        state=request.POST.get("state", ""),
        pincode=request.POST.get("pincode", ""),
        payment_method=request.POST.get(
            "payment_method",
            "Cash on Delivery"
        ),
        products=products,
        subtotal=request.POST.get("subtotal", "0"),
        shipping=request.POST.get("shipping", "0"),
        total=request.POST.get("total", "0"),
        status="Order Placed"
    )

    request.session["last_order_id"] = purchase.id

    return redirect("result")





def result(request):

    user_id = request.session.get("user_id")

    if not user_id:
        return redirect("login")

    user = get_object_or_404(User, id=user_id)

    orders = PurchaseOrder.objects.filter(
        user=user
    ).order_by("-created_at")

    purchase_items = []

    for order in orders:

        products = order.products

        if isinstance(products, str):
            try:
                products = json.loads(products)
            except (json.JSONDecodeError, TypeError):
                products = []

        if isinstance(products, dict):
            products = [products]

        if not isinstance(products, list):
            products = []

        for product in products:

            if not isinstance(product, dict):
                continue

            name = (
                product.get("name")
                or product.get("product_name")
                or product.get("title")
                or product.get("product")
                or "Product"
            )

            image = (
                product.get("image")
                or product.get("image_url")
                or product.get("img")
                or product.get("thumbnail")
                or ""
            )

            price = (
                product.get("price")
                or product.get("selling_price")
                or product.get("amount")
                or 0
            )

            original_price = (
                product.get("original_price")
                or product.get("originalPrice")
                or product.get("old_price")
                or price
            )

            quantity = (
                product.get("quantity")
                or product.get("qty")
                or 1
            )

            try:
                price = float(price)
            except (ValueError, TypeError):
                price = 0

            try:
                original_price = float(original_price)
            except (ValueError, TypeError):
                original_price = price

            try:
                quantity = int(quantity)
            except (ValueError, TypeError):
                quantity = 1

            total = product.get("total")

            if total is None:
                total = price * quantity

            try:
                total = float(total)
            except (ValueError, TypeError):
                total = price * quantity

            purchase_items.append({
                "name": name,
                "image": image,
                "price": price,
                "original_price": original_price,
                "quantity": quantity,
                "total": total,

                "order_id": order.id,
                "payment_method": order.payment_method,
                "status": order.status,
                "created_at": order.created_at,
            })


    product_chart_data = {}

    for item in purchase_items:

        product_name = item["name"]
        product_total = float(item["total"])

        if product_name in product_chart_data:
            product_chart_data[product_name] += product_total
        else:
            product_chart_data[product_name] = product_total


    total_orders = orders.count()

    total_spent = sum(
        float(order.total or 0)
        for order in orders
    )

    total_products = sum(
        item["quantity"]
        for item in purchase_items
    )


    now = timezone.localtime()

    monthly_spent = sum(
        float(order.total or 0)
        for order in orders
        if order.created_at.year == now.year
        and order.created_at.month == now.month
    )


    monthly_data = []

    for month in range(1, 13):

        month_total = sum(
            float(order.total or 0)
            for order in orders
            if order.created_at.year == now.year
            and order.created_at.month == month
        )

        monthly_data.append(month_total)


    status_data = {}

    for order in orders:

        status = order.status or "Order Placed"

        if status in status_data:
            status_data[status] += 1
        else:
            status_data[status] = 1


    return render(
        request,
        "result.html",
        {
            "username": user.username,
            "emailid": user.email,
            "mobile": user.mobile,

            "orders": orders,
            "purchase_items": purchase_items,

            "total_orders": total_orders,
            "total_spent": total_spent,
            "total_products": total_products,

            "monthly_spent": monthly_spent,
            "monthly_data": monthly_data,

            "product_chart_data": product_chart_data,
            "status_data": status_data,

            "cart_count": 0,
        }
    )
    