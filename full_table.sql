/*rename to table from abc to full_table*/
alter table abc
rename to full_table;
/* drop the index column*/
alter table full_table
drop index;
/* add column matches*/
alter table full_table
add column matches text
/* create the table agg with the columns subtasks names per id*/
create table agg as select STRING_AGG(a,',') as matches,subtasks,id from (select array_to_string(regexp_matches(subtasks,'name([^}]*)status','g'),',') as a,subtasks,id from full_table where subtasks!='[]') as foe group by id,subtasks;

/*update the full_table.maches column with the column from agg*/
update full_table 
set matches=agg.matches 
from agg
where full_table.id=agg.id;

alter table full_table 
drop subtasks;

alter table full_table
rename matches to subtasks;

alter table full_table 
rename organiazation to dao;

/*clean table to remove quotations, blankets, question mark*/
update full_table
set comments=lower(trim(replace(translate(comments,'[]','**'),'*',''))),
tags=LOWER(trim(replace(translate(tags,'[]','**'),'*',''))),
subtasks=LOWER(trim(replace(subtasks,', , ',','))),
review=LOWER(trim(replace(translate(substring(review,'message(.*)rating'),''':,)','|||||'),'|','')));

select  regexp_matches(audit_log,'createdAt..([^,]*)','g') as time_stamp,
regexp_matches(audit_log,'path..([^,]*)','g') as path,
regexp_matches(audit_log,'rhs..([^,]*)','g') as activity,
regexp_matches(audit_log,'username..([^,]*)','g') as users,
id into time_activity_users from full_table;


create table new_full as 
select full_table.*,time_stamp,path,activity,users from full_table left join time_activity_users on full_table.id=time_activity_users.id;



alter table new_full 
add column duration interval;


update new_full 
set duration=to_timestamp(done,'YYYY-MM-DD HH24:MI:SS')-to_timestamp(creat,'YYYY-MM-DD HH24:MI:SS')
where done!='None';


alter table new_full 
alter column time_stamp type text,
alter column activity type text, 
alter column users type text,
alter column path type text,
drop column audit_log;




update new_full
set time_stamp=replace(translate(time_stamp,'{}""''','%%%%%%'),'%',''),
path=trim(replace(translate(path,'{}[]''""','%%%%%%%%'),'%','')),
users=trim(replace(translate(users,'{}[]''""','%%%%%%%%'),'%','')),
priority=lower(trim(priority)),
status=lower(trim(status)),
comments=lower(trim(comments)),
description=regexp_replace(lower(description),'[^a-z^0-9 ]','','g'),
activity=lower(substring(activity,'[A-Z]{2,9}_*[A-Z]{2,9}')),
name=regexp_replace(lower(name),'[^a-z^0-9 ]','','g'),
assignees=replace(assignees,'|',',');

alter table new_full
add column year int,
add column month int,
add column day_of_week int,
add column hours_of_day int;


update new_full 
set year=extract(YEAR from time_stamp),
month=extract(MONTH from time_stamp),
day_of_week=extract(DOW from time_stamp),
hours_of_day=extract(HOUR from time_stamp);


/*create four seperate tables todo, done,inprogess,inreview*/
select * into todo from new_full where status='todo';
select * into done from new_full where status='done';
select * into inprogress from new_full where status='inprogress';
select * into inreview from new_full where status='inreview';

/* answer the question that what percenatge of the tasks are applied to out of all available tasks*/
DO $$
DECLARE
Total_to_do int;
Total_done  int;
Total_in_progress int;
Total_in_review int;
Total int;
Begin
select count(distinct id) into Total_done from done;
select count(distinct id) into Total_in_progress from inprogress;
select count(distinct id) into Total_to_do from todo;
select count(distinct id) into Total_in_review from inreview;
select count(distinct id) into Total from new_full;
raise notice 'percenatge of tasks applied to: %',div((Total_done+Total_in_progress+Total_in_review+Total_to_do)*100,Total);
END $$

/* what percentage of tasks are completed*/
DO $$
DECLARE
Total_to_do int;
Total_done  int;
Total_in_progress int;
Total_in_review int;
Begin
select count(distinct id) into Total_done from done;
select count(distinct id) into Total_in_progress from inprogress;
select count(distinct id) into Total_to_do from todo;
select count(distinct id) into Total_in_review from inreview;
raise notice 'percetage of tasks completed: %',div(Total_done*100,Total_to_do+Total_done+Total_in_progress+Total_in_review);
END $$


alter table new_full 
add column counts int;

update new_full 
set counts=subquery.counts
from (select count(time_stamp) as counts, id 
from new_full group by id) as subquery
where new_full.id=subquery.id;

alter table new_full 
rename counts to activity_counts;

alter table new_full 
alter column creat type timestamp USING creat::timestamp without time zone;

update new_full
set time_stamp=case 
when activity_counts=0 then creat
else time_stamp
end;

delete from new_full 
where time_stamp is null;



/* finding out the count of customer participation each bin*/

/* What is the count of customer participation of tasks by month*/
select year,month,id,name,case when activity_counts<=1 then '<=1' 
when 2<=activity_counts and activity_counts<=5 then '2-5' when 6<=activity_counts and activity_counts<=10 then '6-10' when activity_counts>10 then '>10'  
end As bins from new_full  group by year, month,id,name,activity_counts order by year,month, activity_counts;

/* find out the count of DAOs that created a task by month*/
select year,month, dao, case when count(id)<=1 then '<=1' when 2<=count(activity) and count(activity)<=5 then '2-5' when 6<=count(activity) and count(activity)<=10 then '6-10' when count(activity)>10 then '>10'  
end As bins from clean  group by year, month, dao order by year,month;

/* count the task by priority level*/
select count(distinct id),priority from new_full group by priority;






/*avg length of time for all completed tasks by month*/
select avg(duration),year,month from done group by year,month order by year,month ;

/*median length of time for all compled tasks by month*/
select PERCENTILE_CONT(0.5) within group (order by duration) as median ,month from done  group by year,month order by year,month ;
/*avg num of times the top 3 task were completed by month*/
 select avg(count),year,month from (
select rank() over(partition by year,month order by count DESC) as rank_name,year,month,name,count from(
select year,month,name,count(name) from done where done!='None' group by year,month,name) as b) as c where rank_name<=3 group by year,month;


/*top three DAO  with most completed tasks by month */
select year,month,dao,rank_name from (

select rank() over(partition by year,month order by count DESC ) as rank_name,year,month,dao from(
select count(distinct id),dao,year,month from done where done!='None' group by year,month,dao) AS F) as p where rank_name<=3;


/* top three users*/
select year,month,users ,rank_name from (

select rank() over(partition by year,month order by count DESC ) as rank_name,year,month,users from(
select count(activity),users,year,month from done where activity='done' group by year,month,users order by year,month) as m where users is not null) as b where rank_name<=3;


/* most completed task*/
select count(distinct id),name from done where name!='' group by name order by count Desc limit 1;

/*num of tasks with 2 or more assignees*/
select count(distinct id) from (
select cardinality(string_to_array(assignees,',')),* from new_full ) as f where cardinality>=2;
/* month to month customer retention of active doe*/
create table idd as select year, month,row_number() OVER () as ind from (
select distinct year, month from new_full order by year, month) as a;

DROP TABLE retention;
create table retention(
 year int,
 month int,
 percentage float
);

DO $$
DECLARE M int;
i int;
Y int;
lead_m int;
lead_y int;
c int;
c_1 int;
BEGIN 
FOR i in select ind from idd order by year,month
    LOOP
	raise notice 'month:%',M;
	select month into M from idd where ind=i;
	select year into Y from idd where ind=i;
	select month into lead_m from idd where ind=i+1;
	select year into lead_y from idd where ind=i+1;
	select count(distinct dao) into c_1 from new_full where month=lead_m and year=lead_y and dao in (
	select distinct dao  from new_full where month=M and year=Y
	);
	select count(distinct dao) into c from new_full where month=M and year=Y;
	insert into retention(year,month,percentage)
    values(lead_y,lead_m, c_1*100/c);
	END LOOP;
END$$;

select * from retention order by year, month;

/* month to month customer retention of active users*/
drop table user_retention;
create table user_retention(
year int,
month int,
percentage float
);

DO $$
DECLARE M int;
i int;
Y int;
lead_m int;
lead_y int;
c int;
c_1 int;
BEGIN 
FOR i in select ind from idd order by year,month
    LOOP
	select month into M from idd where ind=i;
	select year into Y from idd where ind=i;
	select month into lead_m from idd where ind=i+1;
	select year into lead_y from idd where ind=i+1;
	select count(distinct users) into c_1 from new_full where month=lead_m and year=lead_y and users in (
	select distinct users  from new_full where month=M and year=Y
	);
	select count(distinct users) into c from new_full where month=M and year=Y;
	raise notice 'how many users:%',c;
	insert into user_retention(year,month,percentage)
    values(lead_y,lead_m, c_1*100/(c+0.01));
	END LOOP;
END$$;


select * from user_retention;


/*ad-hoc analysis*/
select count(distinct id) from new_full where rewards is not null;
select avg(float(rewards)) from new_full where rewards is not null;

select rewards from new_full;


