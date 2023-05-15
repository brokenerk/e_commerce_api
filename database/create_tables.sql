
CREATE TABLE person (
	id_person serial4 NOT NULL,
	tx_first_name varchar(30) NOT NULL,
	tx_last_name_a varchar(30) NOT NULL,
	tx_last_name_b varchar(30) NOT NULL,
	tx_street varchar(100) NOT NULL,
	tx_city varchar(100) NOT NULL,
	tx_state varchar(100) NOT NULL,
	tx_zipcode varchar(5) NOT NULL,
	tx_telephone varchar(14) NOT NULL,
	CONSTRAINT person_pkey PRIMARY KEY (id_person)
);

CREATE TABLE product (
	id_product serial4 NOT NULL,
	tx_name varchar(50) NOT NULL,
	tx_description varchar(500) NOT NULL,
	ft_price float8 NOT NULL,
	nu_stock int4 NOT NULL,
	ft_discount float8 NULL,
	CONSTRAINT product_pkey PRIMARY KEY (id_product)
);

CREATE TABLE users (
	id_user int4 NOT NULL,
	tx_login varchar(30) NOT NULL,
	tx_password varchar(10) NOT NULL,
	CONSTRAINT users_pkey PRIMARY KEY (id_user),
	CONSTRAINT users_tx_login_key UNIQUE (tx_login),
	CONSTRAINT fkusers311802 FOREIGN KEY (id_user) REFERENCES person(id_person)
);


CREATE TABLE wishlist (
	id_user int4 NOT NULL,
	id_product int4 NOT NULL,
	CONSTRAINT wishlist_pkey PRIMARY KEY (id_product, id_user),
	CONSTRAINT fkwishlist118649 FOREIGN KEY (id_user) REFERENCES users(id_user),
	CONSTRAINT fkwishlist567841 FOREIGN KEY (id_product) REFERENCES product(id_product)
);


CREATE TABLE "access" (
	id_access int4 NOT NULL,
	nu_attempt int4 NOT NULL,
	fh_failed timestamp(0) NULL,
	fh_lock timestamp(0) NULL,
	CONSTRAINT access_pkey PRIMARY KEY (id_access),
	CONSTRAINT fkaccess801659 FOREIGN KEY (id_access) REFERENCES users(id_user)
);


CREATE TABLE order_c (
	id_order serial4 NOT NULL,
	fh_date timestamp(0) NOT NULL,
	st_purchased bool NOT NULL,
	ft_total float8 NOT NULL,
	id_user int4 NOT NULL,
	payment varchar NULL,
	CONSTRAINT order_c_pkey PRIMARY KEY (id_order),
	CONSTRAINT fkorder_c249289 FOREIGN KEY (id_user) REFERENCES users(id_user)
);


CREATE TABLE order_detail (
	id_product int4 NOT NULL,
	id_order int4 NOT NULL,
	nu_amount int4 NOT NULL,
	CONSTRAINT order_detail_pkey PRIMARY KEY (id_product, id_order),
	CONSTRAINT fkorder_detail713322 FOREIGN KEY (id_order) REFERENCES order_c(id_order),
	CONSTRAINT fkorder_detail999795 FOREIGN KEY (id_product) REFERENCES product(id_product)
);

CREATE TABLE questions (
	id_question serial4 NOT NULL,
	question varchar(50) NOT NULL,
	answer varchar(50) NULL,
	answer_date timestamp(0) NULL,
	id_product int4 NOT NULL,
	id_user int4 NULL,
	CONSTRAINT questions_pkey PRIMARY KEY (id_question),
	CONSTRAINT fkquestions846753 FOREIGN KEY (id_user) REFERENCES users(id_user),
	CONSTRAINT fkquestions885533 FOREIGN KEY (id_product) REFERENCES product(id_product)
);

CREATE TABLE reviews (
	id_review serial4 NOT NULL,
	creation_date timestamp(0) NOT NULL,
	country varchar(50) NOT NULL,
	stars int4 NOT NULL,
	description varchar(500) NOT NULL,
	attachment varchar(50) NULL,
	id_product int4 NOT NULL,
	id_user int4 NOT NULL,
	CONSTRAINT reviews_pkey PRIMARY KEY (id_review),
	CONSTRAINT fkreviews183490 FOREIGN KEY (id_product) REFERENCES product(id_product),
	CONSTRAINT fkreviews467382 FOREIGN KEY (id_user) REFERENCES users(id_user)
);