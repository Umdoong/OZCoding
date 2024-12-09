from django.contrib import admin
from .models import Board

@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
	list_display = ('title', 'writer', 'date', 'likes', 'content', 'updated_at', 'created_at')
	list_filter = ('date', 'writer')
	search_fields = ('title', 'content') # 검색창에서 검색fields설정
	ordering = ('-date', ) # -date -> 최신순, date -> 과거순
	readonly_fields = ('writer', ) # 읽기만 가능
	fieldsets = (
		(None, {'fields': ('title', 'content')}), # 바로 보이는 부분
		('추가 옵션', {'fields': ('writer', 'likes', 'reviews'), 'classes': ('collapse', )})
		# 아래로 확장해서 볼 수 있는 목록
	)
	list_per_page = 1

	actions = ('increment_likes', ) # 체크한 게시물에 대해 action가능
	def increment_likes(self, request, queryset):
		for board in queryset:
			board.likes += 1
			board.save()
	increment_likes.short_description = "선택된 게시글의 좋아요 수 증가"