from .models import Cart

def cart_count(request):
    try:
        if request.session.session_key:
            cart = Cart.objects.filter(session_key=request.session.session_key).first()
            if cart:
                return {'cart_count': cart.total_items}
    except Exception:
        pass
    return {'cart_count': 0}
