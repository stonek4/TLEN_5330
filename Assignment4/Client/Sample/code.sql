DROP FUNCTION recommend(varchar, integer) ;
CREATE OR REPLACE FUNCTION recommend(varchar, int) RETURNS varchar AS $$
  DECLARE
    mystr TEXT;
    myrow RECORD;
    myrow2 RECORD;
    bustotal NUMERIC(4,2);
    busminus NUMERIC(4,2);
  BEGIN
    CREATE TABLE relbus(name varchar, business_id varchar, city varchar);
    mystr = '';
    FOR myrow IN
    SELECT
      b.name,
      b.business_id,
      b.city
    FROM
      businesses b,
      business_categories bc,
      (SELECT
        bc2.category
      FROM
        business_categories bc,
        business_categories bc2
      WHERE
        bc.category = $1 and
        bc.business_id = bc2.business_id
      GROUP BY
        bc2.category
      HAVING
        count(bc2.business_id)>=5) m
    WHERE
      b.business_id = bc.business_id and
      bc.category = m.category
    GROUP BY
      b.business_id
    ORDER BY
      b.name
    LOOP
      INSERT INTO relbus VALUES(myrow.name, myrow.business_id, myrow.city);
    END LOOP;

    CREATE TABLE simusers(u1 varchar, u2 varchar, vote int, similarity numeric(10,8));
    CREATE TABLE simonly(u2 varchar, vote int, similarity numeric(10,8));
    FOR myrow IN SELECT * FROM favorites LOOP
      FOR myrow2 IN
      SELECT
        u.user_id,
        myrow.user_id,
        1-(avg(abs(r1.stars - r2.stars))/5) similarity
      FROM
        users u,
        reviews r1,
        reviews r2
      WHERE
        myrow.user_id = r1.user_id and
        u.user_id = r2.user_id and
        r1.business_id = r2.business_id
      GROUP BY
        u.user_id,
        myrow.user_id
      HAVING
        count(r2.business_id) >= 3 or
        myrow.user_id = u.user_id
      ORDER BY
        similarity DESC,
        u.user_id
      LIMIT
        $2+1
      LOOP
        INSERT INTO simusers VALUES(myrow.user_id, myrow2.user_id, myrow.vote, myrow2.similarity);
      END LOOP;
    END LOOP;
    FOR myrow IN SELECT s.u2,
                        s.vote,
                        s.similarity
                 FROM simusers s
                 EXCEPT
                 SELECT s.u2,
                        s.vote,
                        s.similarity
                 FROM simusers s,
                      simusers s2
                 WHERE
                      s.u1 <> s2.u1 and
                      s.u2 = s2.u2 and
                      s.vote <> s2.vote and
                      s.u1 <> s.u2
                 LOOP
      INSERT INTO simonly VALUES(myrow.u2, myrow.vote, myrow.similarity);
    END LOOP;

    CREATE TABLE finalout(name varchar, city varchar, score numeric(4,2));
    FOR myrow IN SELECT * FROM relbus LOOP
      bustotal = 00.00;
      busminus = 00.00;
      FOR myrow2 IN SELECT
                      sum(r.stars*s.similarity) as total
                    FROM
                      simonly s,
                      reviews r
                    WHERE
                      r.business_id = myrow.business_id and
                      r.user_id = s.u2 and
                      s.vote = 1
                    LOOP
          bustotal = myrow2.total;
      END LOOP;
      FOR myrow2 IN SELECT
                      0.1 * sum(r.stars*s.similarity) as totalm
                    FROM
                      simonly s,
                      reviews r
                    WHERE
                      r.business_id = myrow.business_id and
                      r.user_id = s.u2 and
                      s.vote = -1 and
                      r.stars >= 4
                    LOOP
          busminus = myrow2.totalm;
      END LOOP;
      IF busminus IS NULL THEN
        busminus = 00.00;
      ELSIF busminus < 00.00 THEN
        busminus = 00.00;
      END IF;
      IF bustotal IS NULL THEN
        bustotal = 00.00;
      ELSIF bustotal < 00.00 THEN
        bustotal = 00.00;
      END IF;
      bustotal = bustotal - busminus;
      IF bustotal <> 00.00 THEN
        INSERT INTO finalout VALUES(myrow.name, myrow.city, bustotal);
      END IF;
    END LOOP;
    FOR myrow in SELECT * FROM finalout ORDER BY score DESC, name LIMIT 10 LOOP
      mystr = mystr || rpad(myrow.name, 35) || ' ' || rpad(myrow.city,12) || ' ' || myrow.score || E'\n';
    END LOOP;
    DROP TABLE relbus;
    DROP TABLE simusers;
    DROP TABLE simonly;
    DROP TABLE finalout;
    return mystr;
  END;
$$ LANGUAGE plpgsql;
