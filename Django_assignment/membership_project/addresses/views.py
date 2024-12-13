from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.authentication import TokenAuthentication # 어떤 유저인지 식별, 사용자 인증
from rest_framework.permissions import IsAuthenticated # 인증된 유저만 볼 수 있게 권한 부여
from .models import AddressesModel
from .serializers import AddressSerializer


# Create your views here.
class AddressesList(APIView):
	# authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request): # address테이블의 모든 정보 조회
		addresses = AddressesModel.objects.all()
		# 직렬화
		serializer = AddressSerializer(addresses, many=True)
		return Response(serializer.data)

class BaseAddressView(APIView):
	# 함수기반 view, as_view()를 사용하지 않아도 됨, as_view()는 클래스 기반 view
	def get_object(self, pk): # 오브젝트 재활용
		try:
			return AddressesModel.objects.get(pk=pk)
		except AddressesModel.DoesNotExist:
			raise NotFound

class AddressDetail(BaseAddressView):
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, pk):
		address = self.get_object(pk=pk)
		serializer = AddressSerializer(address)
		return Response(serializer.data)

class CreateUserAddress(APIView):
	def post(self, request, user_id):
		serializer = AddressSerializer(data=request.data)
		if serializer.is_valid():  # 데이터가 유효한지 확인
			serializer.save(user_id=user_id)
			return Response(serializer.data)
		else:
			raise ParseError(serializer.errors)

class UpdateAddress(BaseAddressView):
	# 일부만 수정할수도 있으니까 PATCH 사용
	def patch(self, request, pk):
		address = self.get_object(pk) # 기존 정보가 있어야 수정 가능
		serializer = AddressSerializer(address, data=request.data, partial=True)
		# partial은 false가 기본값, True는 serializer를 사용하여 데이터를 검증할 때, 요청 데이터에 포함되지 않은 필드는 검증에서 제외
		# false면 필드가 누락된 게 있으면 검증에서 오류 발생, 모든 필드가 요청데이터에 포함돼야함
		# PATCH로 부분수정하기 위해 사용한다고 봐도 무방
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		else:
			raise ParseError(serializer.errors)

class DeleteAddress(BaseAddressView):
	def delete(self, request, pk):
		address = self.get_object(pk) # 어떤 내용을 지울지 가져와야함
		address.delete()
		return Response("delete complete")


