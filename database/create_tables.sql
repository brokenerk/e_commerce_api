---------------------------------------------------------
--Create database:
--$ sudo su
--$ su - postgres
--$ createdb e_commerce
--$ psql e_commerce

---------------------------------------------------------
--Tables:
create table users (
	id_user int4 not null, 
	tx_login varchar(30) not null unique, 
	tx_password varchar(10) not null, 
	primary key (id_user));

create table person (
	id_person serial not null, 
	tx_first_name varchar(30) not null, 
	tx_last_name_a varchar(30) not null, 
	tx_last_name_b varchar(30) not null, 
	tx_street varchar(100) not null, 
	tx_city varchar(100) not null, 
	tx_state varchar(100) not null,
	tx_zipcode varchar(5) not null,
	tx_telephone varchar(14) not null, 
	primary key (id_person));

create table access (
	id_access int4 not null, 
	nu_attempt int4 not null, 
	fh_failed timestamp(0), 
	fh_lock timestamp(0), 
	primary key (id_access));

create table product (
	id_product serial not null, 
	tx_name varchar(50) not null, 
	tx_description varchar(500) not null, 
	ft_price float not null,
	nu_stock int4 not null,
	ft_discount float,
	primary key (id_product));

create table order_detail (
	id_product int4 not null, 
	id_order int4 not null,
	nu_amount int4 not null, 
	primary key (id_product, id_order));

create table order_c (
	id_order serial not null,
	fh_date timestamp(0) not null,
	st_purchased bool not null,
	ft_total float not null,
	payment varchar(-1),
	id_user int4 not null,
	primary key (id_order));

create table wishlist (
	id_user int4 not null,
	id_product int4 not null,
	primary key (id_product, id_user));

create table questions (
	id_question serial not null, 
	question varchar(50) not null,
	answer varchar(50),
	answer_date timestamp(0),
	id_product int4 not null,
	id_user int4,
	primary key (id_question));

create table reviews (
	id_review serial not null, 
	creation_date timestamp(0) not null,
	country varchar(50) not null,
	stars int4 not null,
	description varchar(500) not null,
	attachment varchar(50) not null,
	id_product int4 not null,
	id_user int4 not null,
	primary key (id_review));

alter table access add constraint FKaccess801659 foreign key (id_access) references users;
alter table users add constraint FKusers311802 foreign key (id_user) references person;
alter table order_detail add constraint FKorder_detail999795 foreign key (id_product) references product;
alter table order_detail add constraint FKorder_detail713322 foreign key (id_order) references order_c;
alter table order_c add constraint FKorder_c249289 foreign key (id_user) references users;

alter table wishlist add constraint FKwishlist567841 foreign key (id_product) references product;
alter table wishlist add constraint FKwishlist118649 foreign key (id_user) references users;

alter table questions add constraint FKquestions885533 foreign key (id_product) references product;
alter table questions add constraint FKquestions846753 foreign key (id_user) references users;

alter table reviews add constraint FKreviews183490 foreign key (id_product) references product;
alter table reviews add constraint FKreviews467382 foreign key (id_user) references users;