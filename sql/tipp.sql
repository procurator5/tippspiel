-- Function: iswin(integer)

-- DROP FUNCTION iswin(integer);

CREATE OR REPLACE FUNCTION iswin(p_tipp_id integer)
  RETURNS boolean AS
$BODY$
DECLARE
 v_bet_proc text;
 v_match_id int;
 v_res boolean;
BEGIN
 SELECT match_id, handler
 INTO v_match_id, v_bet_proc
	FROM tippspiel_tipp t
	JOIN tippspiel_bettype b ON t.bet_id = b.id
	WHERE t.id = p_tipp_id;
 IF v_match_id IS NOT NULL AND v_bet_proc IS NOT NULL THEN
	EXECUTE 'SELECT '|| v_bet_proc ||'($1);'
	   INTO v_res
	   USING v_match_id;
 END IF;
 RETURN FALSE;
END;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION iswin(integer)
  OWNER TO postgres;

