CREATE DATABASE Sehpora_Database;
use SephoraDataImport;

DROP TABLE IF EXISTS Customer_Review;
DROP TABLE IF EXISTS Products;
DROP TABLE IF EXISTS Brand;

create table Brand(
	brand_id varchar(200) primary key,
    brand_name varchar(200)
);


CREATE TABLE Products(
	product_id varchar(200) primary key,
    brand_id varchar(200),
    product_name varchar(100),
    size varchar(100),
    price decimal(10,2),
    sale_price decimal(10,2),
    out_of_stock boolean,
    sephora_exclusive boolean,
    online_only boolean,
    foreign key (brand_id) references Brand(brand_id)
);

create table Customer_Review(
	product_id varchar(200),
	loves int,
    rating decimal(10,1),
    reviews int,
    foreign key (product_id) references Products(product_id)
);



