-- #QUERY
-- List of rooms and number of students in each of them
select r.name, count(s.id) as number_of_student
from rooms r 
join students s on s.room = r.id 
group by r.name, r.id
order by r.name;

-- #QUERY
-- 5 rooms where the average age of students is the smallest
select r.name, floor(avg(extract(year from age(current_date, s.birthday)))) as average_age
from rooms r 
join students s on s.room = r.id 
group by r.name, r.id
order by average_age
limit 5;

-- #QUERY
-- 5 rooms with the biggest age difference between students
select r.name, floor(max(extract(year from age(current_date, s.birthday)))) - floor(min(extract(year from age(current_date, s.birthday)))) as age_difference
from rooms r 
join students s on s.room = r.id 
group by r.name, r.id
order by age_difference desc
limit 5;

-- #QUERY
-- List of rooms where mixed-sex students live
select r.name
from rooms r 
join students s on s.room = r.id 
group by r.name, r.id
having count(distinct sex) > 1;

