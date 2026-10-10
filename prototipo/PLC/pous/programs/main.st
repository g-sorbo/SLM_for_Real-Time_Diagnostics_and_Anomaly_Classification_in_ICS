PROGRAM main
  VAR
    START : BOOL AT %IX0.0; (* Pulsante avvio ciclo continuo *)
    STOP : BOOL AT %IX0.1; (* Richiesta di arresto (evasa a fine passo corrente) *)
    LSL : BOOL AT %IX0.2; (* Sensore di livello minimo (Low Level Switch) *)
    LSH : BOOL AT %IX0.3; (* Sensore di livello massimo (High Level Switch) *)
    RESET : BOOL AT %IX0.4; (* Reset manuale condizione di allarme *)
    VA : BOOL AT %QX0.0; (* Elettrovalvola alimentazione liquido A *)
    VB : BOOL AT %QX0.1; (* Elettrovalvola alimentazione liquido B *)
    VSCARICO : BOOL AT %QX0.2; (* Elettrovalvola di scarico verso utenza *)
    ALLARME : BOOL AT %QX0.3; (* Segnalazione allarme (spia/cicalino) *)
    RUN : BOOL AT %QX0.4; (* Segnalazione ciclo in corso *)
    stato : INT := 0; (* 0: IDLE, 1: RIEMPIMENTO, 2: SCARICO, 9: ALLARME *)
    STOP_REQ : BOOL := FALSE; (* Memoria della richiesta di arresto *)
    timer_watchdog : TON; (* Timer sorveglianza riempimento (20s) *)
  END_VAR

(* -------------------------------------------------------------
   1. GESTIONE MEMORIA RICHIESTA DI ARRESTO (STOP)
   Se premuto durante il ciclo attivo, viene memorizzato ed evaso
   soltanto al completamento del passo in corso.
   ------------------------------------------------------------- *)
IF STOP AND (stato <> 0) AND (stato <> 9) THEN
    STOP_REQ := TRUE;
END_IF;

(* -------------------------------------------------------------
   2. TIMER DI SORVEGLIANZA WATCHDOG (20 SECONDI)
   Esegue il conteggio solo nello Stato 1 (RIEMPIMENTO).
   ------------------------------------------------------------- *)
timer_watchdog(IN := (stato = 1), PT := T#20s);

(* -------------------------------------------------------------
   3. MACCHINA A STATI FINITI (FSM)
   ------------------------------------------------------------- *)
CASE stato OF
    0: (* STATO IDLE *)
        VA := FALSE;
        VB := FALSE;
        VSCARICO := FALSE;
        ALLARME := FALSE;
        RUN := FALSE;

        IF START THEN
            STOP_REQ := FALSE;
            stato := 1;
        END_IF;

    1: (* STATO RIEMPIMENTO *)
        VA := TRUE;
        VB := TRUE;
        VSCARICO := FALSE;
        ALLARME := FALSE;
        RUN := TRUE;

        IF LSH THEN
            stato := 2;
        ELSIF timer_watchdog.Q THEN
            stato := 9;
        END_IF;

    2: (* STATO SCARICO *)
        VA := FALSE;
        VB := FALSE;
        VSCARICO := TRUE;
        ALLARME := FALSE;
        RUN := TRUE;

        IF LSL THEN
            IF STOP_REQ THEN
                STOP_REQ := FALSE;
                stato := 0;
            ELSE
                stato := 1;
            END_IF;
        END_IF;

    9: (* STATO ALLARME *)
        VA := FALSE;
        VB := FALSE;
        VSCARICO := FALSE;
        ALLARME := TRUE;
        RUN := FALSE;

        IF RESET THEN
            stato := 0;
        END_IF;

ELSE
    stato := 0;
END_CASE;

END_PROGRAM
