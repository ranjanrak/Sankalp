# Nsekite
Flow of built application:

1> When any new client register, he will be allotted virtual margin of 1lakh.

2>Dashboard donut chart for free margin and holdings amount. 

3>In market watch 1 and 2, there is list of 10-10 stocks based highest gainer and loser of the day.

4>On market watch 3, any script can be added (using ajax to add script on marketwatch with ltp), enabled auto search for all stock.

5>Buy and sell button , when hover over the script.

6>When buy button is pressed, required client name, script name, timing, trade type(buy/sell), latest LTP(it's the buy price), quantity is saved in our database.

7>Orderbook will show all these orders detail. 

8>If entered order is Limit order, then it keep on compairing every second with the latest LTP and once the LTP matches(greater than or less than as per order type),
order is completed and changed for pending to completed.

9>Holdings will have above detail,and will be comparing buy price with latest ltp to get p&l.

10>Donut chart on home page,will change accordingly, for holdings amount and free cash.

![login](https://user-images.githubusercontent.com/29432131/29319252-0375b584-81f1-11e7-9426-667bbb1dfb23.PNG)

Dashboard page

![dashboard](https://user-images.githubusercontent.com/29432131/29319346-57d39984-81f1-11e7-8fb0-e887fac89353.PNG)

Order type

![order](https://user-images.githubusercontent.com/29432131/29319435-b313c896-81f1-11e7-8901-dcb48ad589cf.PNG)

Order Book

![ordermain](https://user-images.githubusercontent.com/29432131/29319598-266cafce-81f2-11e7-8002-2fc54b656c02.PNG)
