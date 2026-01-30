USE WNTRADE;

SELECT * FROM wntrade.제품;
-- 제품정보 - 제품명, 단가, 구매가능수량
select 제품명, format(단가,0) as 단가, 재고 as 구매가능수량 # 띄어쓰기하려면 따옴표 필요
from 제품;

SELECT 제품번호
, 단가
, 주문수량
, 할인율
, FORMAT(단가*주문수량*할인율,0) AS 할인금액
, FORMAT(단가*주문수량*(1-할인율),0) AS 주문금액
FROM 주문세부;
