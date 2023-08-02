# from django.contrib.auth.decorators import login_required
# from django.core.exceptions import PermissionDenied

# def staff_required(view_func):
#     # 이 데코레이터는 로그인이 필요하므로, 먼저 login_required 데코레이터를 적용합니다.
#     @login_required
#     def _wrapped_view(request, *args, **kwargs):
#         # 로그인한 유저가 스태프인지 확인합니다.
#         if not request.user.is_staff:
#             raise PermissionDenied  # 스태프가 아닌 경우, PermissionDenied 예외를 발생시킵니다.
#         # 스태프인 경우, 원래의 뷰를 호출합니다.
#         return view_func(request, *args, **kwargs)
#     return _wrapped_view