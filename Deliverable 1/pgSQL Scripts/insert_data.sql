INSERT INTO dim_customer
(customer_id, customer_name, gender, city, state, customer_segment)
VALUES
('C001','Uday Pisharody','Male','Bangalore','Karnataka','Premium'),
('C002','Alice Thomas','Female','Kochi','Kerala','Premium'),
('C003','Bob Kumar','Male','Bangalore','Karnataka','Standard'),
('C004','John Mathew','Male','Chennai','Tamil Nadu','Standard'),
('C005','Sara Joseph','Female','Trivandrum','Kerala','Premium'),
('C006','Rahul Sharma','Male','Mumbai','Maharashtra','Standard'),
('C007','Priya Nair','Female','Kochi','Kerala','Premium'),
('C008','Arjun Menon','Male','Calicut','Kerala','Standard'),
('C009','Neha Gupta','Female','Delhi','Delhi','Premium'),
('C010','Vikram Singh','Male','Pune','Maharashtra','Standard'),
('C011','Anu Krishnan','Female','Thrissur','Kerala','Standard'),
('C012','Rohit Das','Male','Hyderabad','Telangana','Premium'),
('C013','Kiran Patel','Male','Ahmedabad','Gujarat','Standard'),
('C014','Sneha Roy','Female','Kolkata','West Bengal','Premium'),
('C015','Deepak Rao','Male','Mysore','Karnataka','Standard'),
('C016','Asha Pillai','Female','Kochi','Kerala','Premium'),
('C017','Nitin Verma','Male','Noida','UP','Standard'),
('C018','Meera Iyer','Female','Chennai','Tamil Nadu','Premium'),
('C019','Harish Nair','Male','Kannur','Kerala','Standard'),
('C020','Divya Menon','Female','Bangalore','Karnataka','Premium');

INSERT INTO dim_product
(product_id, product_name, category, sub_category, brand)
VALUES
('P001','MacBook Air','Electronics','Laptop','Apple'),
('P002','ThinkPad X1','Electronics','Laptop','Lenovo'),
('P003','iPhone 15','Electronics','Mobile','Apple'),
('P004','Galaxy S25','Electronics','Mobile','Samsung'),
('P005','iPad Air','Electronics','Tablet','Apple'),
('P006','Mechanical Keyboard','Accessories','Keyboard','Logitech'),
('P007','Gaming Mouse','Accessories','Mouse','Razer'),
('P008','27 Inch Monitor','Electronics','Monitor','LG'),
('P009','Smart Watch','Wearables','Watch','Apple'),
('P010','Noise Buds','Audio','Earbuds','Noise'),
('P011','Sony Headphones','Audio','Headphones','Sony'),
('P012','External SSD','Storage','SSD','Samsung'),
('P013','Webcam','Accessories','Camera','Logitech'),
('P014','USB Hub','Accessories','Hub','Anker'),
('P015','Power Bank','Accessories','Battery','Mi'),
('P016','Router','Networking','Router','TP-Link'),
('P017','Printer','Office','Printer','HP'),
('P018','Graphics Tablet','Electronics','Tablet','Wacom'),
('P019','Desk Lamp','Furniture','Lighting','Philips'),
('P020','Office Chair','Furniture','Chair','Ikea');

INSERT INTO dim_date
VALUES
(20260601,'2026-06-01','Monday','June',2,2026),
(20260602,'2026-06-02','Tuesday','June',2,2026),
(20260603,'2026-06-03','Wednesday','June',2,2026),
(20260604,'2026-06-04','Thursday','June',2,2026),
(20260605,'2026-06-05','Friday','June',2,2026),
(20260606,'2026-06-06','Saturday','June',2,2026),
(20260607,'2026-06-07','Sunday','June',2,2026),
(20260608,'2026-06-08','Monday','June',2,2026),
(20260609,'2026-06-09','Tuesday','June',2,2026),
(20260610,'2026-06-10','Wednesday','June',2,2026),
(20260611,'2026-06-11','Thursday','June',2,2026),
(20260612,'2026-06-12','Friday','June',2,2026),
(20260613,'2026-06-13','Saturday','June',2,2026),
(20260614,'2026-06-14','Sunday','June',2,2026),
(20260615,'2026-06-15','Monday','June',2,2026),
(20260616,'2026-06-16','Tuesday','June',2,2026),
(20260617,'2026-06-17','Wednesday','June',2,2026),
(20260618,'2026-06-18','Thursday','June',2,2026),
(20260619,'2026-06-19','Friday','June',2,2026),
(20260620,'2026-06-20','Saturday','June',2,2026);

INSERT INTO fact_sales
(customer_key,product_key,date_key,quantity,unit_price,discount_amount,sales_amount)
VALUES
(1,1,20260601,1,95000,5000,90000),
(2,3,20260601,1,80000,2000,78000),
(3,8,20260602,2,18000,1000,35000),
(4,6,20260602,3,3500,500,10000),
(5,9,20260603,1,30000,1500,28500),
(6,10,20260603,2,2500,200,4800),
(7,4,20260604,1,85000,3000,82000),
(8,12,20260604,1,9000,0,9000),
(9,20,20260605,1,15000,1000,14000),
(10,15,20260605,2,2000,0,4000),
(11,14,20260606,3,1000,0,3000),
(12,11,20260606,1,12000,500,11500),
(13,16,20260607,1,6000,500,5500),
(14,17,20260607,1,11000,1000,10000),
(15,18,20260608,1,25000,1500,23500),
(16,7,20260608,2,4000,500,7500),
(17,5,20260609,1,60000,2000,58000),
(18,2,20260609,1,105000,5000,100000),
(19,13,20260610,1,4500,0,4500),
(20,19,20260610,2,1500,100,2900);