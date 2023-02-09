

## 쿠폰 생성 및 조회 API

* 기능 : 쿠폰 생성 및 조회 기능
  * POST
    * 관리자만 접근 가능
    * 요청값 : 쿠폰이름, 쿠폰종류(정률/정액), 할인율/할인금액, 최소주문금액
    * Reosponse:
      * 201 CREATED: 쿠폰 생성에 성공한 경우, 생성된 쿠폰 정보가 담긴 JSON data
      * 400 BAD REQUEST: 쿠폰 생성에 실패한 경우, 오류 메세지가 담긴 JSON data
  * GET
    * 관리자만 접근 가능
    * 쿠폰 종류에 따라 할인율 또는 할인금액 노출
    * Response:
        * 200 OK: 쿠폰 목록 조회에 성공한 경우, 페이지 당 5개의 쿠폰 정보가 담긴 JSON data
        * 400 BAD REQUEST: 쿠폰 목록 조회에 실패한 경우, 오류 메세지가 담긴 JSON data

## 쿠폰 삭제 API

*기능 : 쿠폰 조회 및 삭제 기능
  *GET
    * 관리자만 접근 가능
    * 현재 잔여 쿠폰 노출
    * Response:
      * 200 OK: 쿠폰 목록 조회에 성공한 경우, 페이지 당 5개의 쿠폰 정보가 담긴 JSON data
      * 400 BAD REQUEST: 쿠폰 목록 조회에 실패한 경우, 오류 메세지가 담긴 JSON data
      
## 쿠폰 발행 API

* 기능 : 쿠폰을 발행하고 발행된 쿠폰을 보여줌
* POST
    * 관리자만 접근 가능
    * 요청값 : user_id, coupon_id
    * Reosponse:
      * 201 CREATED: 쿠폰 발행에 성공한 경우, 생성된 쿠폰 정보가 담긴 JSON data
      * 400 BAD REQUEST: 쿠폰 생성에 실패한 경우, 오류 메세지가 담긴 JSON data
  * GET
    * 관리자만 접근 가능
    * coupon_id와 user_id 노출
    * Response:
        * 200 OK: 쿠폰 목록 조회에 성공한 경우, JSON data
        * 400 BAD REQUEST: 쿠폰 목록 조회에 실패한 경우, 오류 메세지가 담긴 JSON data
        
## 쿠폰 사용 API

*기능 : client가 쿠폰을 사용
  * 로그인 후 접근 가능
  * POST
    * 요청값 : coupon_id
    * Responses:
      * 201 CREATED: "쿠폰이 사용되었습니다"
      * 400 BAD REQUEST: "쿠폰을 사용할 수 없는 유저입니다.
  * GET
    * 로그인 후 접근 가능
    * 사용한 쿠폰 목록 조회
   
## 회원가입 API
    
  * 기능 : 회원가입
  * 로그인 없어도 사용 가능
  * POST
    * 요청값 : username, password, email
    * Responses:
      * 201 CREATED : 가입된 사용자 정보
      * 400 BAD REQUEST : 데이터 오류 메시지
      
## 서버 빌드 방법
 * 로컬에서 돌림
