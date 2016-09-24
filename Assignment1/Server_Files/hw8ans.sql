
select 'Q1: lowest rated in IMDB';

explain select
   m.id
   , m.name
   , m.movieyear
   , mr.rating as irating
   , mr.numvotes as ivotes
   , avg(tr.rating)::numeric(4,2) as trating
   , count(*) as tvotes
from
   movies m
   , imdbratings mr
   , twitterratings tr
where
   m.id = mr.movieid
   and m.name like 'Harry Potter%'
   and m.id = tr.movieid
group by
   m.id
   , m.name
   , m.movieyear
   , mr.rating
   , mr.numvotes
order by
  m.movieyear desc;

select 'Q2: lowest rated in IMDB';

explain
select
   m.id
   , m.name
   , r.rating
from
   movies m
   , imdbratings r
where
   m.id = r.movieid
   and r.rating = (select min(rating) from imdbratings);


select 'Q3: lowest rated on Twitter';

explain
select
   m.id
   , m.name
   , avg(tr.rating)::numeric(4,2)
from
   movies m
   , twitterratings tr
where
   m.id = tr.movieid
group by
   m.id
   , m.name
having
   avg(tr.rating) <= all
        (select  avg(rating)
	 from    twitterratings
	 group by movieid);



select 'Q4: actors with bad and good movies';

explain
select distinct
   a.id
   , a.name
   , a.surname
from
   actors a
   , movieroles mr1
   , imdbratings r1
   , movieroles mr2
   , imdbratings r2
where
   a.id = mr1.actorid
   and a.id = mr2.actorid
   and mr1.movieid = r1.movieid
   and mr2.movieid = r2.movieid
   and r1.rating < 2
   and r2.rating > 8;

select 'Q5: plot: destruction Earth, not Sci-Fi';

explain select
   m.id
   , m.name
from
   movies m
   join movieplots mp
   on (m.id = mp.movieid
      and mp.plot like '%destruction%'
      and mp.plot like '%Earth%')
   left join moviegenres mg
   on (mg.genre = 'Sci-Fi'
       and mg.movieid = m.id)
where
  mg.movieid is null ;


select 'Q6: hard to please/cranky Twitter users';


explain select
   u.id
   , 'https://twitter.com/intent/user?user_id='|| u.twitterid::varchar(12)
from
   twitterusers u
   , twitterratings tr
where
   u.id = tr.userid
   and tr.rating < 3
   and not exists
         (select 1
	  from twitterratings tr1
          where tr1.userid = tr.userid and tr1.rating>8)
group by
   u.id
   , u.twitterid
having
   count(*)>= 10;
