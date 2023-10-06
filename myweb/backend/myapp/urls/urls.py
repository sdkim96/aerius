from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..views.views import *
from ..views.store_views import *

router = DefaultRouter()
router.register(r'messages', MessageViewSet)
# router.register(r'store', StoreViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('checkuser/', CheckUserViewSet.as_view(), name='checkuser'),
    path('login/', LoginViewSet.as_view(), name='login'),  # Add this line
    path('logout/', LogoutViewSet.as_view(), name='logout'),  # Add this line
    path('authorize/', AuthorizedViewSet.as_view(), name='authorize'),
    path('store_products/', StoreViewSet.as_view(), name='store_products'),
    path('store_products/<int:pk>', EachStoreViewSet.as_view(), name='each_store_product'),
    path('carts/', CartListCreateView.as_view(), name='cart-list-create'),
    path('cart_view/', CartRetrieveView.as_view(), name='cart-retrieve'),
    path('cart_items/remove_one/product/<int:product_id>/size/<str:size>/', CartItemRemoveOneView.as_view(), name='cart-item-remove-one'),
    path('cart_items/remove_all/product/<int:product_id>/size/<str:size>/', CartItemRemoveAllView.as_view(), name='cart-item-remove-all'),
    path('search_item/', SearchItemViewSet.as_view(), name='search_item')
]

# get 메서드는 클라이언트가 장바구니의 내용을 요청할 때 호출됩니다.
# 먼저, 요청을 한 사용자의 장바구니(Cart)를 데이터베이스에서 찾습니다.
# 해당 장바구니에 담긴 아이템들(CartItem)을 데이터베이스에서 찾습니다.
# 각 CartItem에 대한 정보를 리스트로 만들어서 응답(Response)에 담습니다.
# 장바구니가 없는 경우에는 404 상태 코드와 함께 에러 메시지를 반환합니다

# post 메서드는 클라이언트가 장바구니에 새로운 아이템을 추가하려고 할 때 호출됩니다.
# 요청에서 product_id를 추출하여 해당 상품을 데이터베이스에서 찾습니다.
# 사용자의 장바구니를 찾거나 없다면 새로 만듭니다.
# 새 CartItem을 만들거나, 이미 같은 상품이 장바구니에 있다면 수량을 증가시킵니다.
# 상품이 성공적으로 추가되면, 201 Created 상태 코드와 함께 성공 메시지를 반환합니다.

# delete 메서드는 클라이언트가 장바구니에서 특정 아이템을 제거하려고 할 때 호출됩니다.
# 요청에서 cart_item_id를 이용하여 해당 CartItem을 데이터베이스에서 찾습니다.
# 찾은 CartItem을 데이터베이스에서 제거합니다.
# 아이템이 성공적으로 제거되면, 204 No Content 상태 코드와 함께 성공 메시지를 반환합니다.