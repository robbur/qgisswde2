CREATE OR REPLACE FUNCTION public.__g5sp_dze_ins(IN ins_char character varying, IN idzd character varying)
  RETURNS TABLE(ins_g5id1 text, ins_g5npe text, udw_g5ud text, udw_g5rjdr text, jdr_g5ijr text, dze_g5id1 text, dze_g5idd text, dze_nr text, obr_nazwa text, jew_nazwa text, dze_geom geometry) AS
$BODY$
DECLARE
    	query_char text;
    	rec_ins record;
    	rec_udw record;
    	rec_dze record;
    	dze_nrobr text;
    	obr_teryt text;
    
BEGIN
	query_char = '%' || ins_char || '%';

	EXECUTE 'SELECT g5jew.g5naz from public.g5jew where g5jew.id_zd = $1'
					INTO jew_nazwa
					USING idzd;
    	for rec_ins in(
		SELECT g5ins.g5id1, g5ins.g5npe
		FROM public.g5ins where g5ins.id_zd = idzd and g5ins.g5npe LIKE (query_char) 
		)LOOP
			ins_g5id1 = rec_ins.g5id1; ins_g5npe = rec_ins.g5npe; 
			for rec_udw in(SELECT g5udw.g5ud, g5udw.g5rwld from public.g5udw
				where g5udw.id_zd = idzd and g5udw.g5rpod = ins_g5id1 )
				LOOP
					udw_g5ud = rec_udw.g5ud; udw_g5rjdr = rec_udw.g5rwld;
					EXECUTE 'SELECT g5jdr.g5ijr from public.g5jdr where g5jdr.id_zd = $1 and g5jdr.g5id1 = $2'
					INTO jdr_g5ijr
					USING idzd, udw_g5rjdr;
					for rec_dze in (Select g5dze.g5id1, g5dze.g5idd, g5dze.nr, g5dze.nrobr, g5dze.geom from public.g5dze
						where g5dze.id_zd = idzd and g5dze.g5rjdr = udw_g5rjdr)
						LOOP
							dze_g5id1=rec_dze.g5id1; dze_g5idd = rec_dze.g5idd; dze_geom = rec_dze.geom;
							dze_nr = rec_dze.nr; dze_nrobr = rec_dze.nrobr;
							obr_teryt = idzd || '.' || dze_nrobr;
							EXECUTE 'SELECT g5obr.g5naz from public.g5obr where g5obr.id_zd = $1 and g5obr.g5nro = $2'
							INTO obr_nazwa
							USING idzd, obr_teryt;
							RETURN NEXT;
						END LOOP;
				END LOOP;
			

			
		END LOOP;
END;
$BODY$
  LANGUAGE plpgsql VOLATILE