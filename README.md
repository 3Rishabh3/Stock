This is a project created using python which connects to a mysql database server locally.

!!!!!!!!!!!! I M P O R T A N T !!!!!!!!!!!!

As this project is locally hosted so you have to run these commands in mysql.
1. create database stock_business;
2. create table stock(id varchar(5) primary key,cereal varchar(15),quantity int default 0,cost_price float default 0);
3. create table finance(id varchar(5) primary key,cost_price float default 0,profit_loss float default 0,status varchar(1) default 'N');
