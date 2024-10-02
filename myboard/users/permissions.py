from rest_framework import permissions

class CustomReadOnly(permissions.BasePermission):
# GET(조회)요청은 누구나, PUT/PATCH(수정 및 삭제 등)은 해당유저만
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            # 데이터에 영향을 미치지않는 메소드라면 true로 반환시킨다.
            return True
        # 객체의 유저와 들어온(request) 유저와 같은지 비교시킨 후 통과시킨다.
        return obj.user == request.user