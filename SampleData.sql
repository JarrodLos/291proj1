PRAGMA foreign_keys = ON;

drop table if exists previews;
drop table if exists reviews;
drop table if exists bids;
drop table if exists sales;
drop table if exists products;
drop table if exists users;

create table users (
  email		char(20),
  name		char(16),
  pwd		char(4),
  city		char(15),
  gender	char(1),
  primary key (email)
);
create table products (
  pid		char(4),
  descr		char(20),
  primary key (pid)
);
create table sales (
  sid		char(4),
  lister	char(20) not null,
  pid		char(4),
  edate		date,
  descr		char(25),
  cond		char(10),
  rprice	int,
  primary key (sid),
  foreign key (lister) references users,
  foreign key (pid) references products
);
create table bids (
  bid		char(20),
  bidder	char(20) not null,
  sid		char(4) not null,
  bdate 	date,
  amount	float,
  primary key (bid),
  foreign key (bidder) references users,
  foreign key (sid) references sales
);
create table reviews (
  reviewer	char(20),
  reviewee	char(20),
  rating	float,
  rtext		char(20),
  rdate		date,
  primary key (reviewer, reviewee),
  foreign key (reviewer) references users,
  foreign key (reviewee) references users
);
create table previews (
  rid		int,
  pid		char(4),
  reviewer	char(20) not null,
  rating	float,
  rtext		char(20),
  rdate		date,
  primary key (rid),
  foreign key (pid) references products,
  foreign key (reviewer) references users
);

insert into users values ('mc@gmail.com','Michael Choi','abcd','Edmonton','M');
insert into users values ('tedwalsh@td.com','Ted Walsh','7632','Calgary','M');
insert into users values ('hm@mah.com','Harry Mah','1453','Waterloo, ON','M');
insert into users values ('ks@gmail.com','Kaitlyn Scott','pqwe','Toronto, ON','F');
insert into users values ('angels@gmail.com','Angel Silverman','anlo','Edmonton','F');
insert into users values ('mk@abc.com','Maximillion Kung','0931','Burnaby, BY','F');
insert into users values ('davood@gmail.com','Davood Rafiei','1234','Edmonton','M');
insert into users values ('amr@yahoo.ca','Amir Salimi','123445','Edmonton','O');
insert into users values ('amrv2@yahoo.ca','Amir Salimi','123445','Edmonton','O');
insert into users values ('chomsky@mit.edu','Noam chomsky','420420','MIT','N');
insert into users values ('chm@gmail.com','Angela Chomsky','1843','Toronto','F');
insert into users values ('j.chomsky.a@gmail.com','Janet','h7np','Calgary','F');
insert into users values ('johnChoMskY@gmail.com','John','7538','MIT','M');


insert into products values ('N01', 'Nikon F100');
insert into products values ('N02', 'Nikon D3500');
insert into products values ('B01', 'BMW M8');
insert into products values ('PS01', 'ps4xbox');
insert into products values ('PS02', 'ps4xbox');
insert into products values ('P01', 'Porsche 91');
insert into products values ('P02', 'Porsche 98');
insert into products values ('K01', 'kettle');
insert into products values ('K02', 'kettle2');
insert into products values ('K03', 'kettle sold as item only');


insert into sales values ('S01', 'mc@gmail.com', 'N01',  datetime('now','-365 days'), 'ticket ps4', 'Mint', 1400);
insert into sales values ('S02', 'mc@gmail.com', 'N02',  datetime('now','-730 days'), 'xbox Voucher', 'Used', 698);
insert into sales values ('S03', 'hm@mah.com', 'N02', datetime('now','+3 days'), ' xxboxx x', 'New', 10);
insert into sales values ('S04', 'ks@gmail.com', 'P01', datetime('now','-1 days'), 'tick ps4', 'ticket', 3000);
insert into sales values ('S042', 'ks@gmail.com', 'P01', datetime('now','-1 days'), 'vouch  xBoX', 'ticket', 3000);
insert into sales values ('S041', 'ks@gmail.com', 'P01', datetime('now','+4 days'), 'vouch', 'voucher', 3000);
insert into sales values ('S05', 'angels@gmail.com', 'N02', datetime('now'), 'ticket', 'very old', 30);
insert into sales values ('S051', 'angels@gmail.com', 'N02', datetime('now','+3 days','-10 minute'), 'ticket', 'very old', 30);
insert into sales values ('S052', 'angels@gmail.com', 'N02',datetime('now','+3 days','+10 minute'), 'ticket', 'very old', 30);
insert into sales values ('S06', 'davood@gmail.com', 'B01', datetime('now','+1 days','+6 hour','1 minute'), 'voucher', 'useful voucher', 424);
insert into sales values ('S07', 'davood@gmail.com', 'PS01', datetime('now','+100 days','-6 hour','-10 minute'), 'ps4 xbox', 'old console', 424);
insert into sales values ('S08', 'ks@gmail.com', 'PS01', datetime('now','-100 days'), 'PS4 xbox', 'mint', 10000);
insert into sales values ('S09', 'chomsky@mit.edu', 'K01', datetime('now','+100 days','-1 hour','-11 minute'), 'ok kettle', 'new', 1);
insert into sales values ('S091', 'chomsky@mit.edu', 'K01', datetime('now','-100 days', '+2 hour','+41 minute'), 'good kettle', 'new', 2);
insert into sales values ('S092', 'davood@gmail.com', 'N01', datetime('now','+100 days'), 'great camera', 'new', 3);
insert into sales values ('S093', 'davood@gmail.com', 'K02', datetime('now','+300 days'), 'a kettle', 'new', 100);
insert into sales values ('S094', 'ks@gmail.com', 'K02', datetime('now','+200 days'), 'a kettle', 'used', 100);
insert into sales values ('S010', 'amrv2@yahoo.ca', 'PS02', datetime('now','+300 days'), 'lorum ipsum', 'new', 100);
insert into sales values ('S011', 'hm@mah.com', 'B01', datetime('now','+300 days'), 'a device!', 'new', 600);
insert into sales values ('S012', 'hm@mah.com', 'P01', datetime('now','+300 days'), 'another device!', 'used', 223);
insert into sales values ('S081', 'ks@gmail.com', 'PS01', datetime('now','+100 days'), 'PS4 xbox xbox xxxboxxx', 'mint', 1000);


insert into bids values ('B01', 'hm@mah.com', 'S01', '2016-04-01', 1405.02);
insert into bids values ('B02', 'ks@gmail.com', 'S01', '2016-04-02', 1407.99);
insert into bids values ('B03', 'hm@mah.com', 'S02', '2018-09-11', 299);
insert into bids values ('B04', 'davood@gmail.com', 'S02', '2018-09-12', 999);
insert into bids values ('B05', 'angels@gmail.com', 'S03', '2016-01-03', 499);
insert into bids values ('B051', 'ks@gmail.com', 'S03', '2017-01-03', 523);
insert into bids values ('B052', 'angels@gmail.com', 'S03', '2017-01-05', 529);
insert into bids values ('B06', 'tedwalsh@td.com', 'S04', '2019-05-19', 3000);
insert into bids values ('B07', 'ks@gmail.com', 'S04', '2019-05-20', 4000);
insert into bids values ('B08', 'ks@gmail.com', 'S04', '2019-05-21', 100);
insert into bids values ('B09', 'tedwalsh@td.com', 'S04', '2019-06-22', 101);
insert into bids values ('B091', 'tedwalsh@td.com', 'S042', '2019-06-22', 8001);
insert into bids values ('B101', 'angels@gmail.com', 'S06', '2020-01-0', 421);
insert into bids values ('B102', 'angels@gmail.com', 'S06', '2020-01-07', 422);
insert into bids values ('B103', 'angels@gmail.com', 'S06', '2020-01-07', 424);
insert into bids values ('B11', 'amr@yahoo.ca', 'S07', '2018-09-12', 25);
insert into bids values ('B111', 'amr@yahoo.ca', 'S08', '2018-09-12', 50);


INSERT INTO "reviews" VALUES ('mc@gmail.com', 'tedwalsh@td.com', 3.9, 'great guy!', '2016-05-02');
INSERT INTO "reviews" VALUES ('ks@gmail.com', 'tedwalsh@td.com', 4.0, 'great guy!', '2016-05-02');
INSERT INTO "reviews" VALUES ('davood@gmail.com', 'tedwalsh@td.com', 4.0, 'great guy!', '2016-05-02');
INSERT INTO "reviews" VALUES ('mk@abc.com', 'tedwalsh@td.com', 4.1, 'great guy!', '2016-05-02');
INSERT INTO "reviews" VALUES ('tedwalsh@td.com', 'ks@gmail.com', 4.0, 'great guy!', '2016-05-02');
INSERT INTO "reviews" VALUES ('mc@gmail.com', 'ks@gmail.com', 4.0, 'great guy!', '2016-05-02');
INSERT INTO "reviews" VALUES ('angels@gmail.com', 'ks@gmail.com', 4.2, 'great guy!', '2016-05-02');
INSERT INTO "reviews" VALUES ('hm@mah.com', 'mc@gmail.com', 5.0, '', '2016-03-16 17:51:30');
INSERT INTO "reviews" VALUES ('angels@gmail.com', 'mc@gmail.com', 5.0, '', '2017-03-16 17:51:30');
INSERT INTO "reviews" VALUES ('mc@gmail.com', 'davood@gmail.com', 3.9, 'great guy!', '2016-05-02');
INSERT INTO "reviews" VALUES ('hm@mah.com', 'davood@gmail.com', 5.0, '', '2016-03-16 17:51:30');
INSERT INTO "reviews" VALUES ('angels@gmail.com', 'davood@gmail.com', 5.0, '', '2017-03-16 17:51:30');
INSERT INTO "reviews" VALUES ('tedwalsh@td.com', 'davood@gmail.com', 5.0, 'great prof!', '2016-05-02');
INSERT INTO "reviews" VALUES ('mc@gmail.com', 'amr@yahoo.ca', 1.0, 'bad', '2016-05-02');
INSERT INTO "reviews" VALUES ('hm@mah.com', 'amr@yahoo.ca', 1.0, 'slow', '2016-03-16 17:51:30');
INSERT INTO "reviews" VALUES ('angels@gmail.com', 'amr@yahoo.ca', 1.0, 'tired', '2017-03-16 17:51:30');
INSERT INTO "reviews" VALUES ('mc@gmail.com', 'amrv2@yahoo.ca', 5.0, 'bad', '2016-05-02');
INSERT INTO "reviews" VALUES ('hm@mah.com', 'amrv2@yahoo.ca', 5.0, 'slow', '2016-03-16 17:51:30');
INSERT INTO "reviews" VALUES ('angels@gmail.com', 'amrv2@yahoo.ca', 5.0, 'tired', '2017-03-16 17:51:30');
INSERT INTO "reviews" VALUES ('mc@gmail.com', 'hm@mah.com', 2.0, 'bad', '2016-05-02');
INSERT INTO "reviews" VALUES ('hm@mah.com', 'hm@mah.com', 2.0, 'slow', '2016-03-16 17:51:30');
INSERT INTO "reviews" VALUES ('angels@gmail.com', 'hm@mah.com', 2.0, 'tired', '2017-03-16 17:51:30');
INSERT INTO "reviews" VALUES ('tedwalsh@td.com', 'chomsky@mit.edu', 1.0, '!', '2016-05-02');
INSERT INTO "reviews" VALUES ('angels@gmail.com', 'chomsky@mit.edu', 1.0, 'ok!', '2016-05-02');

INSERT INTO "previews" VALUES (1, 'N01', 'hm@mah.com', 1.0, 'definitly used', '2019-09-01 21:47:25');
INSERT INTO "previews" VALUES (2, 'N01', 'hm@mah.com', 1.0, 'unused', '2019-11-01 21:47:25');
INSERT INTO "previews" VALUES (3, 'N02', 'ks@gmail.com', 3.0, 'great quality', '2019-10-01 21:47:25');
INSERT INTO "previews" VALUES (4, 'N02', 'ks@gmail.com', 5.0, 'great quality', '2019-10-01 21:47:25');
INSERT INTO "previews" VALUES (5, 'P02', 'mk@abc.com', 4.1, 'amazing car', '2019-09-01 21:47:25');
INSERT INTO "previews" VALUES (6, 'P02', 'mk@abc.com', 3.8, 'amazing car', '2019-10-01 21:47:25');
INSERT INTO "previews" VALUES (61, 'P02', 'mk@abc.com', 4.2, 'amazing car', '2019-10-01 21:47:25');
INSERT INTO "previews" VALUES (7, 'PS01', 'mk@abc.com', 5.0, 'a console', '2019-03-01 21:47:25');
INSERT INTO "previews" VALUES (8, 'PS01', 'mk@abc.com', 5.0, 'xbox+ps4?', '2019-03-01 21:47:25');
INSERT INTO "previews" VALUES (9, 'PS01', 'mk@abc.com', 4.0, '3rd time buying', '2020-02-01 21:47:25');
INSERT INTO "previews" VALUES (10, 'PS01', 'mk@abc.com', 3.9, 'addicted', '2020-02-01 21:47:25');
INSERT INTO "previews" VALUES (11, 'K01', 'mk@abc.com', 5.0, 'addicted', '2020-02-01 21:47:25');
INSERT INTO "previews" VALUES (12, 'K01', 'hm@mah.com', 5.0, 'addicted', '2020-01-01 21:47:25');
INSERT INTO "previews" VALUES (13, 'K01', 'chomsky@mit.edu', 5.0, 'addicted', '2019-12-01 21:47:25');
