const totalPages = 3; // 총 페이지 수
let currentPage = 1;  // 현재 페이지 (초기 페이지를 1로 설정)

// 페이지 버튼 클릭 이벤트 처리
document.querySelectorAll('.page-link').forEach(link => {
link.addEventListener('click', function(e) {
  e.preventDefault();

  const selectedPage = parseInt(this.getAttribute('data-page'));

  if (!isNaN(selectedPage)) {
	currentPage = selectedPage;
	updatePagination();
  }
});
});

// 페이지네이션 상태 업데이트
function updatePagination() {
// 이전 버튼 비활성화 처리
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');

if (currentPage === 1) {
  prevBtn.classList.add('disabled');
} else {
  prevBtn.classList.remove('disabled');
}

// 다음 버튼 비활성화 처리
if (currentPage === totalPages) {
  nextBtn.classList.add('disabled');
} else {
  nextBtn.classList.remove('disabled');
}

// 페이지 버튼 업데이트 (선택된 페이지 강조)
document.querySelectorAll('.page-item').forEach(item => {
  item.classList.remove('active');
});

document.querySelector(`.page-link[data-page="${currentPage}"]`).parentElement.classList.add('active');
}

// 페이지 로드 시 초기화
updatePagination();

//시계
function setClock(){
  var dateInfo = new Date();
  var hour =
  modifyNumber(dateInfo.getHours());
  var min =
  modifyNumber(dateInfo.getMinutes());
  var sec =
  modifyNumber(dateInfo.getSeconds());
  var year = dateInfo.getFullYear();
  var month = dateInfo.getMonth();
  var date = dateInfo.getDate();
  document.getElementById("time").innerHTML = hour + ":" + min + ":" + sec;
  document.getElementById("date").innerHTML = year + "년 " + (month+1) + "월 " + date + "일";
}

function modifyNumber(time){
  if(parseInt(time)<10){
	return "0" + time;
  } else {
	return time;
  }
}

window.onload = function(){
	setClock();
	setInterval(setClock,1000); // 1초마다 setClock 함수 실행
}