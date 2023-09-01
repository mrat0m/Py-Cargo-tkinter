#Creating Cargo database
import mysql.connector as mc
c=mc.connect(host="localhost",user="root",password="root")
cur=c.cursor()
try:
    cur.execute("Drop database cargo_database")#if other cargo_databse exist
except:
    pass
cur.execute("CREATE DATABASE cargo_database")
cur.execute("USE cargo_database")
#Table structure for table `bookings`
cur.execute("CREATE TABLE bookings(booking_id int(50) primary key AUTO_INCREMENT,customer_id int(50) DEFAULT NULL,booking_date varchar(50) DEFAULT NULL,from_loc varchar(50) DEFAULT NULL,toloc varchar(50) DEFAULT NULL,weight varchar(50) DEFAULT NULL,length varchar(50) DEFAULT NULL,width varchar(50) DEFAULT NULL,amount varchar(50) DEFAULT NULL,booking_status varchar(50) DEFAULT NULL,pack_id int(50) DEFAULT NULL)AUTO_INCREMENT=1000")
#Data for the table `bookings`
cur.execute("insert  into bookings values(1000,100,'2023-07-21','Kochi','Thevara','10','100','100','20000','collected',3000)")
#Table structure for table `cargo_status`
cur.execute("CREATE TABLE cargo_status(status_id int(50) primary key AUTO_INCREMENT,booking_id int(50) DEFAULT NULL,place_name varchar(50) DEFAULT NULL,status_date_time varchar(50) DEFAULT NULL)AUTO_INCREMENT=2000")
#Data for the table `cargo_status`
cur.execute("insert  into cargo_status values (2000,1000,'Kochi','2023-07-21 18:00:48')")
#Table structure for table `customers`
cur.execute("CREATE TABLE customers(customer_id int(50) primary key AUTO_INCREMENT,username varchar(50) DEFAULT NULL,first_name varchar(50) DEFAULT NULL,last_name varchar(50) DEFAULT NULL,phone varchar(50) DEFAULT NULL,email varchar(50) DEFAULT NULL)AUTO_INCREMENT=100")
#Data for the table `customers`
cur.execute("insert  into customers values(100,'tonystark','Tony','Stark','9876543210','tony@stark.com')")
#Table structure for table `login`
cur.execute("CREATE TABLE login(username varchar(50) primary key,password varchar(50) DEFAULT NULL,user_type varchar(50) DEFAULT NULL)")
#Data for the table `login` *
cur.execute("insert  into login values('admin','admin','admin')")
cur.execute("insert  into login values('tonystark','tonyst@rk123','customer')")
#Table structure for table `payment` 
cur.execute("CREATE TABLE payment(payment_id int(50) primary key AUTO_INCREMENT,booking_id int(50) DEFAULT NULL,amount_paid varchar(50) DEFAULT NULL,payment_date varchar(50) DEFAULT NULL)AUTO_INCREMENT=5000")
#Data for the table `payment`
cur.execute("insert  into payment values(5000,1000,'20000','2022-03-21 17:54:37')")
#Table structure for table `packages` 
cur.execute("CREATE TABLE packages(pack_id int(50) PRIMARY KEY AUTO_INCREMENT,packname varchar(50) DEFAULT NULL,maximum_weight varchar(50) DEFAULT NULL,maximum_height varchar(50) DEFAULT NULL,maximum_width varchar(50) DEFAULT NULL,minimum_price varchar(50) DEFAULT NULL,pstatus varchar(50) DEFAULT NULL)AUTO_INCREMENT=3000")
#Data for the table `packages`
cur.execute("insert  into packages values(3000,'Premium','25','100','100','20000','active')")
print("********DATABASE for cargo_service_management created in your system********")
c.commit()
cur.close()
c.close()
