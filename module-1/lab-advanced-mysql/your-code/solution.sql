######## Lab | Advanced MySQL #############
use publications;

############### Challenge 1 - Most Profiting Authors #########################

# Step 1: Calculate the royalties of each sales for each author
-- Write a SELECT query to obtain the following output:
--    Title ID
--    Author ID
--    Royalty of each sale for each author
--        The formular is:
--        sales_royalty = titles.price * sales.qty * titles.royalty / 100 * titleauthor.royaltyper / 100

#select * from titles;
#select * from roysched;
#select * from sales;
#select * from titleauthor;

select t.title_id as Title_ID, au.au_id as Author_ID, (t.price * s.qty * (t.royalty / 100) * (a.royaltyper / 100)) as Sales_Royalty
from authors au
right join titleauthor a
on a.au_id=au.	au_id
join titles t
on t.title_id=a.title_id
join sales s
on s.title_id=t.title_id
order by Sales_Royalty desc
;

# Step 2: Aggregate the total royalties for each title for each author
-- Using the output from Step 1, write a query to obtain the following output:
--    Title ID
--    Author ID
--    Aggregated royalties of each title for each author
--        Hint: use the SUM subquery and group by both au_id and title_id

#Sumas Sales_Royalty y agrupas por autor y titulos
select t.title_id as Title_ID, au.au_id as Author_ID, sum((t.price * s.qty * (t.royalty / 100) * (a.royaltyper / 100))) as Sales_Royalty
from authors au
right join titleauthor a
on a.au_id=au.	au_id
join titles t
on t.title_id=a.title_id
join sales s
on s.title_id=t.title_id
group by Author_ID, Title_ID
order by Sales_Royalty desc
;

# Step 3: Calculate the total profits of each author
-- Now that each title has exactly one row for each author where the advance and royalties are available, we are ready to obtain the eventual output. Using the output from Step 2, write a query to obtain the following output:
--    Author ID
--    Profits of each author by aggregating the advance and total royalties of each title
-- sort the output based on a total profits from high to low, and limit the number of rows to 3.

#Ahora solo agrupas por autor
select au.au_id as Author_ID, sum((t.price * s.qty * (t.royalty / 100) * (a.royaltyper / 100))) as Sales_Royalty
from authors au
right join titleauthor a
on a.au_id=au.	au_id
join titles t
on t.title_id=a.title_id
join sales s
on s.title_id=t.title_id
group by Author_ID
order by Sales_Royalty desc
;

############## Challenge 2 - Alternative Solution  ####################

## Creando tabla temporal del step 2 del challenge 1, para luego aplicar a esta temporal el step 3 del challenge 1:

create temporary table most_profiting_authors 
select t.title_id as Title_ID, au.au_id as Author_ID, sum((t.price * s.qty * (t.royalty / 100) * (a.royaltyper / 100))) as Sales_Royalty
from authors au
right join titleauthor a
on a.au_id=au.	au_id
join titles t
on t.title_id=a.title_id
join sales s
on s.title_id=t.title_id
group by Author_ID, Title_ID
order by Sales_Royalty desc
;

select Author_ID, Sales_Royalty from most_profiting_authors group by Author_ID

############## Challenge 3 ##############

create table most_profiting_authors_real as
select Author_ID as au_id, Sales_Royalty as profits
from most_profiting_authors
;

select * from most_profiting_authors_real;