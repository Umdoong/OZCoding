//제출 이벤트를 받는다(이벤트 핸들링)
//제출된 입력 값들을 참조한다
// 입력값에 문제가 있는 경우 이를 감지한다
//가입 환영 인사를 제공한다

const form = document.getElementById("form")

form.addEventListener("submit", function(event){
	event.preventDefault() // 새로고침 차단

	let userId = event.target.id.value
	let userPw1 = event.target.pw1.value
	let userPw2 = event.target.pw2.value
	let userName = event.target.name.value
	let userPhone = event.target.phone.value
	let userGender = event.target.gender.value
	let userEmail = event.target.email.value

	//아이디 정규식 검사
	let idReg = /^[a-zA-Z]+[a-z0-9]{5,11}$/g;
	if( !idReg.test(userId) ) {
		alert("아이디는 영문자로 시작하는 6~12자 영문자 또는 숫자이어야 합니다.");
		return;
	}

	//비밀번호 정규식 검사
	let passwordReg = /^(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[!@#$%^&*?_]).{7,29}$/;
	if (passwordReg.test(userPw1)) {
		if (userPw1 !== userPw2) {
			alert('비밀번호가 서로 일치하지 않습니다.')
			return
		}
	}else{
		alert('비밀번호는 최소 8자에서 30자까지, 영문자, 숫자 및 특수 문자를 포함해야 합니다.')
		return
	}

	//폰 정규식 검사
	let phoneReg = /^01([0|1|6|7|8|9])-?([0-9]{3,4})-?([0-9]{4})$/g;
	if(!phoneReg.test(userPhone)){
		alert("올바른 형식의 휴대전화 번호가 아닙니다")
		return
	}

	//알림창 띄우기, 나중에 데이터 보낼 때 phone의 hyphen을 제거 후 보내기
	let info=
		`${userId}님 환영합니다.
		회원 가입 시 입력하신 내역은 다음과 같습니다.
		아이디 : ${userId}
		이름 : ${userName}
		전화번호 : ${userPhone.replace(/-/g, '')}
		성별 : ${userGender}
		이메일 : ${userEmail}`;
	
	alert(info.replace(/\t/g, ''))

	//가입이 잘 되었다!
	location.href = "index.html"
})

//폰 자동 하이픈
const autoHyphen = (phone) => {
    phone.value = phone.value
    .replace(/[^0-9]/g, '')
    .replace(/^(\d{0,3})(\d{0,4})(\d{0,4})$/g, "$1-$2-$3").replace(/(\-{1,2})$/g, "");
}