####### lab-mysql-select #########
use publications;
#################### Challenge 1
-- what titles each author has published at which publishers. Your output should have at least the following columns:
--    AUTHOR ID - the ID of the author
--    LAST NAME - author last name
--    FIRST NAME - author first name
--    TITLE - name of the published title
--    PUBLISHER - name of the publisher where the title was published

select * from titleauthor

select a.au_id as Author_ID, au.au_lname as Last_Name, au.au_fname as First_Name,
t.title as Title, p.pub_name as Publisher
from authors au
right join titleauthor a
on a.au_id=au.	au_id
join titles t
on t.title_id=a.title_id
join publishers p
on p.pub_id=t.pub_id
;


################### Challenge 2 - Who Have Published How Many At Where?
-- Elevating from your solution in Challenge 1, query how many titles each author has published at each publisher. 
-- Your output should look something like below:


create temporary table Count_Titles_Authors
select Author_ID, Last_Name, First_Name, Publisher, count(Title) as Count_Titles from 
(select a.au_id as Author_ID, au.au_lname as Last_Name, au.au_fname as First_Name,
t.title as Title, p.pub_name as Publisher
from authors au
right join titleauthor a
on a.au_id=au.	au_id
join titles t
on t.title_id=a.title_id
join publishers p
on p.pub_id=t.pub_id
) as titles_per_author
group by Author_ID
;

select sum(Count_Titles) from Count_Titles_Authors;

################### Challenge 3 - Best Selling Authors
-- Who are the top 3 authors who have sold the highest number of titles? Write a query to find out.
-- Requirements:

--    Your output should have the following columns:
--       AUTHOR ID - the ID of the author
--       LAST NAME - author last name
--       FIRST NAME - author first name
--       TOTAL - total number of titles sold from this author
--    Your output should be ordered based on TOTAL from high to low.
--    Only output the top 3 best selling authors.

-- Hint: In order to calculate the total of profits of an author, you need to use the MySQL SUM function. Refer to the reference and learn how to use it.
select * from sales;
select * from titleauthor;

select a.au_id as Author_ID, au.au_lname as Last_Name, au.au_fname as First_Name, sum(s.qty) as Total_Titles_Sold
from authors au
right join titleauthor a
on a.au_id=au.	au_id
join titles t
on t.title_id=a.title_id
join sales s
on s.title_id=t.title_id
group by Author_ID
order by Total_Titles_Sold desc
limit 3
;

###################  Challenge 4 - Best Selling Authors Ranking
select a.au_id as Author_ID, au.au_lname as Last_Name, au.au_fname as First_Name, sum(s.qty) as Total_Titles_Sold
from authors au
right join titleauthor a
on a.au_id=au.	au_id
join titles t
on t.title_id=a.title_id
join sales s
on s.title_id=t.title_id
group by Author_ID
order by Total_Titles_Sold desc
;

############### BONUS
select a.au_id as Author_ID, au.au_lname as Last_Name, au.au_fname as First_Name, sum(a.royaltyper) as Profit
from authors au
right join titleauthor a
on a.au_id=au.au_id
join titles t
on t.title_id=a.title_id
group by Author_ID
order by Profit desc
limit 3
;

