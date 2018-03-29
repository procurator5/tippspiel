CREATE  OR REPLACE FUNCTION "total-less-2.5"(p_match_id integer) RETURNS boolean
    LANGUAGE plpgsql
    AS $$
DECLARE
 v_score_home int;
 v_score_visitor int;
BEGIN
 SELECT score_home, score_visitor
 INTO v_score_home, v_score_visitor
	FROM tippspiel_match
	WHERE id = p_match_id;
 IF (v_score_home + v_score_visitor) < 2.5 THEN
	RETURN TRUE;
 END IF;
 RETURN FALSE;
END;
$$;

CREATE  OR REPLACE FUNCTION "total-more-2.5"(p_match_id integer) RETURNS boolean
    LANGUAGE plpgsql
    AS $$
DECLARE
 v_score_home int;
 v_score_visitor int;
BEGIN
 SELECT score_home, score_visitor
 INTO v_score_home, v_score_visitor
	FROM tippspiel_match
	WHERE id = p_match_id;
 IF (v_score_home + v_score_visitor) > 2.5 THEN
	RETURN TRUE;
 END IF;
 RETURN FALSE;
END;
$$;

CREATE  OR REPLACE FUNCTION "win-1x2-1"(p_match_id integer) RETURNS boolean
    LANGUAGE plpgsql
    AS $$
DECLARE
 v_score_home int;
 v_score_visitor int;
BEGIN
 SELECT score_home, score_visitor
 INTO v_score_home, v_score_visitor
	FROM tippspiel_match
	WHERE id = p_match_id;
 IF v_score_home > v_score_visitor THEN
	RETURN TRUE;
 END IF;
 RETURN FALSE;
END;
$$;


--
-- TOC entry 242 (class 1255 OID 1501653)
-- Name: win-1x2-2(integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE  OR REPLACE FUNCTION "win-1x2-2"(p_match_id integer) RETURNS boolean
    LANGUAGE plpgsql
    AS $$
DECLARE
 v_score_home int;
 v_score_visitor int;
BEGIN
 SELECT score_home, score_visitor
 INTO v_score_home, v_score_visitor
	FROM tippspiel_match
	WHERE id = p_match_id;
 IF v_score_home < v_score_visitor THEN
	RETURN TRUE;
 END IF;
 RETURN FALSE;
END;
$$;


--
-- TOC entry 241 (class 1255 OID 1501652)
-- Name: win-1x2-x(integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE  OR REPLACE FUNCTION "win-1x2-x"(p_match_id integer) RETURNS boolean
    LANGUAGE plpgsql
    AS $$
DECLARE
 v_score_home int;
 v_score_visitor int;
BEGIN
 SELECT score_home, score_visitor
 INTO v_score_home, v_score_visitor
	FROM tippspiel_match
	WHERE id = p_match_id;
 IF v_score_home = v_score_visitor THEN
	RETURN TRUE;
 END IF;
 RETURN FALSE;
END;
$$;

CREATE OR REPLACE FUNCTION "dchance-12"(p_match_id integer)
  RETURNS boolean AS
$BODY$
DECLARE
 v_score_home int;
 v_score_visitor int;
BEGIN
 SELECT score_home, score_visitor
 INTO v_score_home, v_score_visitor
	FROM tippspiel_match
	WHERE id = p_match_id;
 IF v_score_home <> v_score_visitor THEN
	RETURN TRUE;
 END IF;
 RETURN FALSE;
END;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;

CREATE OR REPLACE FUNCTION "dchance-1X"(p_match_id integer)
  RETURNS boolean AS
$BODY$
DECLARE
 v_score_home int;
 v_score_visitor int;
BEGIN
 SELECT score_home, score_visitor
 INTO v_score_home, v_score_visitor
	FROM tippspiel_match
	WHERE id = p_match_id;
 IF v_score_home >= v_score_visitor THEN
	RETURN TRUE;
 END IF;
 RETURN FALSE;
END;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
  
CREATE OR REPLACE FUNCTION "dchance-2X"(p_match_id integer)
  RETURNS boolean AS
$BODY$
DECLARE
 v_score_home int;
 v_score_visitor int;
BEGIN
 SELECT score_home, score_visitor
 INTO v_score_home, v_score_visitor
	FROM tippspiel_match
	WHERE id = p_match_id;
 IF v_score_home <= v_score_visitor THEN
	RETURN TRUE;
 END IF;
 RETURN FALSE;
END;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;  