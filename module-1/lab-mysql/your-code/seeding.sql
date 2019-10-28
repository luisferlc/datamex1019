use lab_mysql;

insert into cars values(0,'3K096I98581DHSNUP', 'Volkswagen', 'Tiguan', 2019, 'Blue');
insert into cars values(1,'ZM8G7BEUQZ97IH46V','Peugeot','Rifter',2019,'Red');
insert into cars values(2, 'RKXVNNIHLVVZOUB4M', 'Ford', 'Fusion', 2018,'White');
insert into cars values(3,'HKNDGS7CU31E9Z7JW','Toyota','RAV4',2018,'Silver');
insert into cars values(4, 'DAM41UDN3CHU2WVF6','Volvo','V60',2019,'Gray');
insert into cars values(5,'DAM41UDN3CHU2WVF6','Volvo','V60 Cross Country',2019,'Gray');

select * from cars;

######################################################################################################
insert into customers values(0, 10001, 'Pablo Picasso','+34 636 17 63 82','-','Paseo de la Chopera, 14','Madrid','Madrid','Spain',28045);
insert into customers values(1, 20001,'Abraham Lincoln','+1 305 907 7086','-','120 SW 8th St','Miami','Florida','United States',33130);
insert into customers values(2,30001,'Napoléon Bonaparte','+33 1 79 75 40 00','-','40 Rue du Colisée','Paris','Île-de-France','France' ,75008);

select * from customers;

######################################################################################################
insert into salespersons values(0,00001,'Petey Cruiser','Madrid');
insert into salespersons values(1,00002,'Anna Sthesia','Barcelona');
insert into salespersons values(2,00003,'Paul Molive','Berlin');
insert into salespersons values(3,00004,'Gail Forcewind','Paris');
insert into salespersons values(4,00005,'Paige Turner','Mimia');
insert into salespersons values(5,00006,'Bob Frapples','Mexico City');
insert into salespersons values(6,00007,'Walter Melon','Amsterdam');
insert into salespersons values(7,00008,'Shonda Leer','São Paulo');

select * from salespersons

######################################################################################################
insert into invoices values(0,852399038, '20180822',1,3);
insert into invoices values(1,731166526, 20181231,0,5);
insert into invoices values(2,271135104, 20190122,2,7);

select * from invoices;













