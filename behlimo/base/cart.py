from ..cart.models import Cart


def get_cart_id(request):
    cart_id = request.session.session_key
    if not cart_id:
        cart_id = request.session.create()
        Cart.objects.create(cart_id=cart_id)
    return cart_id
