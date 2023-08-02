create table Product(
    id int primary key,
    name varchar(200),
    type varchar(200),
    price int,
    size varchar(200),
)

create table Type(
    id int primary key,
    name varchar(20)
)

create table Size(
    id int primary key,
    name varchar(20)
)

create table Discount(
    id int primary key,
    percent int
)

create table Each_Product(
    id int primary key,
    product varchar(20),
    user 
    review
    discount
    final_price int

    foreign key (user) references user
    foreign key (review) references Review
    foreign key (discount) references Discount
    

)

create table Cart(
    id int primary key,
    each_product,
    quantity int

    foreign key (each_product) references Each_Product 
)