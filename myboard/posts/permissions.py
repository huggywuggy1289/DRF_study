from rest_framework import permissions

# 게시글 조회는 누구나 가능하지만 게시글 생성/삭제/수정은 인증된 유저만 가능해야함.
class CustomReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET': # 게시글 조회(GET요청)은 누구나 True 반환
            return True
        # 그외 요청:  사용자가 인증된 경우에만 요청을 허용(is_authenticated)
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
        # 데이터에 영향을 미치지않는 메소드라면 true로 반환시킨다.
            return True
        # 객체에 대한 작업을 요청한 사용자가 객체의 소유자일 경우에만 허용
        return obj.user == request.user