CREATE FUNCTION "total-less-0.5"(p_match_id integer) RETURNS boolean
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
 IF (v_score_home + v_score_visitor) < 0.5 THEN
	RETURN TRUE;
 END IF;
 RETURN FALSE;
END;
$$;


--
-- TOC entry 244 (class 1255 OID 1501655)
-- Name: total-less-1.5(integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION "total-less-1.5"(p_match_id integer) RETURNS boolean
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
 IF (v_score_home + v_score_visitor) < 1.5 THEN
	RETURN TRUE;
 END IF;
 RETURN FALSE;
END;
$$;


--
-- TOC entry 245 (class 1255 OID 1501656)
-- Name: total-less-2.5(integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION "total-less-2.5"(p_match_id integer) RETURNS boolean
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


--
-- TOC entry 246 (class 1255 OID 1501657)
-- Name: total-less-3.5(integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION "total-less-3.5"(p_match_id integer) RETURNS boolean
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
 IF (v_score_home + v_score_visitor) < 3.5 THEN
	RETURN TRUE;
 END IF;
 RETURN FALSE;
END;
$$;


--
-- TOC entry 247 (class 1255 OID 1501658)
-- Name: total-less-4.5(integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION "total-less-4.5"(p_match_id integer) RETURNS boolean
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
 IF (v_score_home + v_score_visitor) < 4.5 THEN
	RETURN TRUE;
 END IF;
 RETURN FALSE;
END;
$$;


--
-- TOC entry 260 (class 1255 OID 1501659)
-- Name: total-less-5.5(integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION "total-less-5.5"(p_match_id integer) RETURNS boolean
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
 IF (v_score_home + v_score_visitor) < 5.5 THEN
	RETURN TRUE;
 END IF;
 RETURN FALSE;
END;
$$;


--
-- TOC entry 261 (class 1255 OID 1501660)
-- Name: total-less-6.5(integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION "total-less-6.5"(p_match_id integer) RETURNS boolean
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
 IF (v_score_home + v_score_visitor) < 6.5 THEN
	RETURN TRUE;
 END IF;
 RETURN FALSE;
END;
$$;


--
-- TOC entry 268 (class 1255 OID 1501667)
-- Name: total-more-0.5(integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION "total-more-0.5"(p_match_id integer) RETURNS boolean
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
 IF (v_score_home + v_score_visitor) > 0.5 THEN
	RETURN TRUE;
 END IF;
 RETURN FALSE;
END;
$$;


--
-- TOC entry 267 (class 1255 OID 1501666)
-- Name: total-more-1.5(integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION "total-more-1.5"(p_match_id integer) RETURNS boolean
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
 IF (v_score_home + v_score_visitor) > 1.5 THEN
	RETURN TRUE;
 END IF;
 RETURN FALSE;
END;
$$;


--
-- TOC entry 266 (class 1255 OID 1501665)
-- Name: total-more-2.5(integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION "total-more-2.5"(p_match_id integer) RETURNS boolean
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


--
-- TOC entry 265 (class 1255 OID 1501664)
-- Name: total-more-3.5(integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION "total-more-3.5"(p_match_id integer) RETURNS boolean
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
 IF (v_score_home + v_score_visitor) > 3.5 THEN
	RETURN TRUE;
 END IF;
 RETURN FALSE;
END;
$$;


--
-- TOC entry 264 (class 1255 OID 1501663)
-- Name: total-more-4.5(integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION "total-more-4.5"(p_match_id integer) RETURNS boolean
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
 IF (v_score_home + v_score_visitor) > 4.5 THEN
	RETURN TRUE;
 END IF;
 RETURN FALSE;
END;
$$;


--
-- TOC entry 263 (class 1255 OID 1501662)
-- Name: total-more-5.5(integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION "total-more-5.5"(p_match_id integer) RETURNS boolean
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
 IF (v_score_home + v_score_visitor) > 5.5 THEN
	RETURN TRUE;
 END IF;
 RETURN FALSE;
END;
$$;


--
-- TOC entry 262 (class 1255 OID 1501661)
-- Name: total-more-6.5(integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION "total-more-6.5"(p_match_id integer) RETURNS boolean
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
 IF (v_score_home + v_score_visitor) > 6.5 THEN
	RETURN TRUE;
 END IF;
 RETURN FALSE;
END;
$$;


--
-- TOC entry 240 (class 1255 OID 1501651)
-- Name: win-1x2-1(integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION "win-1x2-1"(p_match_id integer) RETURNS boolean
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

CREATE FUNCTION "win-1x2-2"(p_match_id integer) RETURNS boolean
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

CREATE FUNCTION "win-1x2-x"(p_match_id integer) RETURNS boolean
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

