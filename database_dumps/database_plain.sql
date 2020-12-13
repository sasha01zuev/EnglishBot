--
-- PostgreSQL database dump
--

-- Dumped from database version 12.5 (Ubuntu 12.5-1.pgdg20.04+1)
-- Dumped by pg_dump version 13.1 (Ubuntu 13.1-1.pgdg20.04+1)

-- Started on 2020-12-14 01:35:59 EET

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 207 (class 1259 OID 24694)
-- Name: current_dictionary; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.current_dictionary (
    user_id integer NOT NULL,
    dictionary_id integer NOT NULL
);


ALTER TABLE public.current_dictionary OWNER TO postgres;

--
-- TOC entry 204 (class 1259 OID 16466)
-- Name: dictionaries; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.dictionaries (
    id bigint NOT NULL,
    user_id integer NOT NULL,
    name text NOT NULL
);


ALTER TABLE public.dictionaries OWNER TO postgres;

--
-- TOC entry 203 (class 1259 OID 16464)
-- Name: dictionaries_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.dictionaries_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.dictionaries_id_seq OWNER TO postgres;

--
-- TOC entry 3099 (class 0 OID 0)
-- Dependencies: 203
-- Name: dictionaries_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.dictionaries_id_seq OWNED BY public.dictionaries.id;


--
-- TOC entry 218 (class 1259 OID 24831)
-- Name: fifth_repeat; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.fifth_repeat (
    dictionary_id bigint NOT NULL,
    translate_id bigint NOT NULL,
    approach_date timestamp without time zone NOT NULL
);


ALTER TABLE public.fifth_repeat OWNER TO postgres;

--
-- TOC entry 214 (class 1259 OID 24747)
-- Name: first_repeat; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.first_repeat (
    dictionary_id bigint NOT NULL,
    translate_id bigint NOT NULL,
    approach_date timestamp without time zone NOT NULL
);


ALTER TABLE public.first_repeat OWNER TO postgres;

--
-- TOC entry 213 (class 1259 OID 24745)
-- Name: first_repeat_translate_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.first_repeat_translate_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.first_repeat_translate_id_seq OWNER TO postgres;

--
-- TOC entry 3100 (class 0 OID 0)
-- Dependencies: 213
-- Name: first_repeat_translate_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.first_repeat_translate_id_seq OWNED BY public.first_repeat.translate_id;


--
-- TOC entry 217 (class 1259 OID 24818)
-- Name: fourth_repeat; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.fourth_repeat (
    dictionary_id bigint NOT NULL,
    translate_id bigint NOT NULL,
    approach_date timestamp without time zone NOT NULL
);


ALTER TABLE public.fourth_repeat OWNER TO postgres;

--
-- TOC entry 212 (class 1259 OID 24731)
-- Name: learn_translate; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.learn_translate (
    dictionary_id bigint NOT NULL,
    translate_id bigint NOT NULL,
    approach_date timestamp without time zone NOT NULL,
    times_repeat integer DEFAULT 0,
    CONSTRAINT learn_translate_times_repeat_check CHECK ((times_repeat < 5))
);


ALTER TABLE public.learn_translate OWNER TO postgres;

--
-- TOC entry 211 (class 1259 OID 24729)
-- Name: learn_translate_translate_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.learn_translate_translate_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.learn_translate_translate_id_seq OWNER TO postgres;

--
-- TOC entry 3101 (class 0 OID 0)
-- Dependencies: 211
-- Name: learn_translate_translate_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.learn_translate_translate_id_seq OWNED BY public.learn_translate.translate_id;


--
-- TOC entry 221 (class 1259 OID 24870)
-- Name: learned_translates; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.learned_translates (
    dictionary_id bigint NOT NULL,
    translate_id bigint NOT NULL
);


ALTER TABLE public.learned_translates OWNER TO postgres;

--
-- TOC entry 205 (class 1259 OID 24657)
-- Name: messages; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.messages (
    user_id integer NOT NULL,
    message text NOT NULL,
    date_time timestamp without time zone NOT NULL
);


ALTER TABLE public.messages OWNER TO postgres;

--
-- TOC entry 215 (class 1259 OID 24792)
-- Name: second_repeat; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.second_repeat (
    dictionary_id bigint NOT NULL,
    translate_id bigint NOT NULL,
    approach_date timestamp without time zone NOT NULL
);


ALTER TABLE public.second_repeat OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 24857)
-- Name: seventh_repeat; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.seventh_repeat (
    dictionary_id bigint NOT NULL,
    translate_id bigint NOT NULL,
    approach_date timestamp without time zone NOT NULL
);


ALTER TABLE public.seventh_repeat OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 24844)
-- Name: sixth_repeat; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sixth_repeat (
    dictionary_id bigint NOT NULL,
    translate_id bigint NOT NULL,
    approach_date timestamp without time zone NOT NULL
);


ALTER TABLE public.sixth_repeat OWNER TO postgres;

--
-- TOC entry 216 (class 1259 OID 24805)
-- Name: third_repeat; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.third_repeat (
    dictionary_id bigint NOT NULL,
    translate_id bigint NOT NULL,
    approach_date timestamp without time zone NOT NULL
);


ALTER TABLE public.third_repeat OWNER TO postgres;

--
-- TOC entry 210 (class 1259 OID 24713)
-- Name: translates; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.translates (
    id bigint NOT NULL,
    english_word text,
    russian_word text,
    dictionary_id bigint NOT NULL,
    repetition_number integer DEFAULT 0 NOT NULL
);


ALTER TABLE public.translates OWNER TO postgres;

--
-- TOC entry 209 (class 1259 OID 24711)
-- Name: translates_dictionary_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.translates_dictionary_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.translates_dictionary_id_seq OWNER TO postgres;

--
-- TOC entry 3102 (class 0 OID 0)
-- Dependencies: 209
-- Name: translates_dictionary_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.translates_dictionary_id_seq OWNED BY public.translates.dictionary_id;


--
-- TOC entry 208 (class 1259 OID 24709)
-- Name: translates_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.translates_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.translates_id_seq OWNER TO postgres;

--
-- TOC entry 3103 (class 0 OID 0)
-- Dependencies: 208
-- Name: translates_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.translates_id_seq OWNED BY public.translates.id;


--
-- TOC entry 206 (class 1259 OID 24681)
-- Name: user_parameters; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_parameters (
    user_id integer NOT NULL,
    registration_date date NOT NULL,
    last_action timestamp without time zone NOT NULL,
    reverse_translate boolean NOT NULL,
    user_language text NOT NULL,
    last_learning_translate bigint
);


ALTER TABLE public.user_parameters OWNER TO postgres;

--
-- TOC entry 202 (class 1259 OID 16418)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    tg_id integer NOT NULL,
    name text NOT NULL,
    full_name text NOT NULL,
    username text NOT NULL
);


ALTER TABLE public.users OWNER TO postgres;

--
-- TOC entry 2903 (class 2604 OID 16469)
-- Name: dictionaries id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dictionaries ALTER COLUMN id SET DEFAULT nextval('public.dictionaries_id_seq'::regclass);


--
-- TOC entry 2910 (class 2604 OID 24750)
-- Name: first_repeat translate_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.first_repeat ALTER COLUMN translate_id SET DEFAULT nextval('public.first_repeat_translate_id_seq'::regclass);


--
-- TOC entry 2907 (class 2604 OID 24734)
-- Name: learn_translate translate_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.learn_translate ALTER COLUMN translate_id SET DEFAULT nextval('public.learn_translate_translate_id_seq'::regclass);


--
-- TOC entry 2904 (class 2604 OID 24716)
-- Name: translates id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.translates ALTER COLUMN id SET DEFAULT nextval('public.translates_id_seq'::regclass);


--
-- TOC entry 2905 (class 2604 OID 24717)
-- Name: translates dictionary_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.translates ALTER COLUMN dictionary_id SET DEFAULT nextval('public.translates_dictionary_id_seq'::regclass);


--
-- TOC entry 3079 (class 0 OID 24694)
-- Dependencies: 207
-- Data for Name: current_dictionary; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3076 (class 0 OID 16466)
-- Dependencies: 204
-- Data for Name: dictionaries; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3090 (class 0 OID 24831)
-- Dependencies: 218
-- Data for Name: fifth_repeat; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3086 (class 0 OID 24747)
-- Dependencies: 214
-- Data for Name: first_repeat; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3089 (class 0 OID 24818)
-- Dependencies: 217
-- Data for Name: fourth_repeat; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3084 (class 0 OID 24731)
-- Dependencies: 212
-- Data for Name: learn_translate; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3093 (class 0 OID 24870)
-- Dependencies: 221
-- Data for Name: learned_translates; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3077 (class 0 OID 24657)
-- Dependencies: 205
-- Data for Name: messages; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3087 (class 0 OID 24792)
-- Dependencies: 215
-- Data for Name: second_repeat; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3092 (class 0 OID 24857)
-- Dependencies: 220
-- Data for Name: seventh_repeat; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3091 (class 0 OID 24844)
-- Dependencies: 219
-- Data for Name: sixth_repeat; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3088 (class 0 OID 24805)
-- Dependencies: 216
-- Data for Name: third_repeat; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3082 (class 0 OID 24713)
-- Dependencies: 210
-- Data for Name: translates; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3078 (class 0 OID 24681)
-- Dependencies: 206
-- Data for Name: user_parameters; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3074 (class 0 OID 16418)
-- Dependencies: 202
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3104 (class 0 OID 0)
-- Dependencies: 203
-- Name: dictionaries_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.dictionaries_id_seq', 1, false);


--
-- TOC entry 3105 (class 0 OID 0)
-- Dependencies: 213
-- Name: first_repeat_translate_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.first_repeat_translate_id_seq', 1, false);


--
-- TOC entry 3106 (class 0 OID 0)
-- Dependencies: 211
-- Name: learn_translate_translate_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.learn_translate_translate_id_seq', 1, false);


--
-- TOC entry 3107 (class 0 OID 0)
-- Dependencies: 209
-- Name: translates_dictionary_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.translates_dictionary_id_seq', 1, false);


--
-- TOC entry 3108 (class 0 OID 0)
-- Dependencies: 208
-- Name: translates_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.translates_id_seq', 1, false);


--
-- TOC entry 2918 (class 2606 OID 24698)
-- Name: current_dictionary current_dictionary_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.current_dictionary
    ADD CONSTRAINT current_dictionary_user_id_key UNIQUE (user_id);


--
-- TOC entry 2914 (class 2606 OID 16474)
-- Name: dictionaries dictionaries_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dictionaries
    ADD CONSTRAINT dictionaries_pkey PRIMARY KEY (id);


--
-- TOC entry 2922 (class 2606 OID 24767)
-- Name: learn_translate translate_id_unique; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.learn_translate
    ADD CONSTRAINT translate_id_unique UNIQUE (translate_id);


--
-- TOC entry 2920 (class 2606 OID 24722)
-- Name: translates translates_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.translates
    ADD CONSTRAINT translates_pkey PRIMARY KEY (id);


--
-- TOC entry 2916 (class 2606 OID 24688)
-- Name: user_parameters user_parameters_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_parameters
    ADD CONSTRAINT user_parameters_user_id_key UNIQUE (user_id);


--
-- TOC entry 2912 (class 2606 OID 16422)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (tg_id);


--
-- TOC entry 2928 (class 2606 OID 24704)
-- Name: current_dictionary current_dictionary_dictionary_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.current_dictionary
    ADD CONSTRAINT current_dictionary_dictionary_id_fkey FOREIGN KEY (dictionary_id) REFERENCES public.dictionaries(id) ON DELETE CASCADE;


--
-- TOC entry 2927 (class 2606 OID 24699)
-- Name: current_dictionary current_dictionary_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.current_dictionary
    ADD CONSTRAINT current_dictionary_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(tg_id) ON DELETE CASCADE;


--
-- TOC entry 2923 (class 2606 OID 24652)
-- Name: dictionaries dictionaries_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dictionaries
    ADD CONSTRAINT dictionaries_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(tg_id) ON DELETE CASCADE;


--
-- TOC entry 2940 (class 2606 OID 24834)
-- Name: fifth_repeat fifth_repeat_dictionary_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fifth_repeat
    ADD CONSTRAINT fifth_repeat_dictionary_id_fkey FOREIGN KEY (dictionary_id) REFERENCES public.dictionaries(id) ON DELETE CASCADE;


--
-- TOC entry 2941 (class 2606 OID 24839)
-- Name: fifth_repeat fifth_repeat_translate_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fifth_repeat
    ADD CONSTRAINT fifth_repeat_translate_id_fkey FOREIGN KEY (translate_id) REFERENCES public.translates(id) ON DELETE CASCADE;


--
-- TOC entry 2932 (class 2606 OID 24751)
-- Name: first_repeat first_repeat_dictionary_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.first_repeat
    ADD CONSTRAINT first_repeat_dictionary_id_fkey FOREIGN KEY (dictionary_id) REFERENCES public.dictionaries(id) ON DELETE CASCADE;


--
-- TOC entry 2933 (class 2606 OID 24756)
-- Name: first_repeat first_repeat_translate_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.first_repeat
    ADD CONSTRAINT first_repeat_translate_id_fkey FOREIGN KEY (translate_id) REFERENCES public.translates(id) ON DELETE CASCADE;


--
-- TOC entry 2938 (class 2606 OID 24821)
-- Name: fourth_repeat fourth_repeat_dictionary_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fourth_repeat
    ADD CONSTRAINT fourth_repeat_dictionary_id_fkey FOREIGN KEY (dictionary_id) REFERENCES public.dictionaries(id) ON DELETE CASCADE;


--
-- TOC entry 2939 (class 2606 OID 24826)
-- Name: fourth_repeat fourth_repeat_translate_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fourth_repeat
    ADD CONSTRAINT fourth_repeat_translate_id_fkey FOREIGN KEY (translate_id) REFERENCES public.translates(id) ON DELETE CASCADE;


--
-- TOC entry 2930 (class 2606 OID 24735)
-- Name: learn_translate learn_translate_dictionary_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.learn_translate
    ADD CONSTRAINT learn_translate_dictionary_id_fkey FOREIGN KEY (dictionary_id) REFERENCES public.dictionaries(id) ON DELETE CASCADE;


--
-- TOC entry 2931 (class 2606 OID 24740)
-- Name: learn_translate learn_translate_translate_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.learn_translate
    ADD CONSTRAINT learn_translate_translate_id_fkey FOREIGN KEY (translate_id) REFERENCES public.translates(id) ON DELETE CASCADE;


--
-- TOC entry 2946 (class 2606 OID 24873)
-- Name: learned_translates learned_translates_dictionary_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.learned_translates
    ADD CONSTRAINT learned_translates_dictionary_id_fkey FOREIGN KEY (dictionary_id) REFERENCES public.dictionaries(id) ON DELETE CASCADE;


--
-- TOC entry 2947 (class 2606 OID 24878)
-- Name: learned_translates learned_translates_translate_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.learned_translates
    ADD CONSTRAINT learned_translates_translate_id_fkey FOREIGN KEY (translate_id) REFERENCES public.translates(id) ON DELETE CASCADE;


--
-- TOC entry 2924 (class 2606 OID 24663)
-- Name: messages messages_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(tg_id) ON DELETE CASCADE;


--
-- TOC entry 2934 (class 2606 OID 24795)
-- Name: second_repeat second_repeat_dictionary_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.second_repeat
    ADD CONSTRAINT second_repeat_dictionary_id_fkey FOREIGN KEY (dictionary_id) REFERENCES public.dictionaries(id) ON DELETE CASCADE;


--
-- TOC entry 2935 (class 2606 OID 24800)
-- Name: second_repeat second_repeat_translate_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.second_repeat
    ADD CONSTRAINT second_repeat_translate_id_fkey FOREIGN KEY (translate_id) REFERENCES public.translates(id) ON DELETE CASCADE;


--
-- TOC entry 2944 (class 2606 OID 24860)
-- Name: seventh_repeat seventh_repeat_dictionary_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.seventh_repeat
    ADD CONSTRAINT seventh_repeat_dictionary_id_fkey FOREIGN KEY (dictionary_id) REFERENCES public.dictionaries(id) ON DELETE CASCADE;


--
-- TOC entry 2945 (class 2606 OID 24865)
-- Name: seventh_repeat seventh_repeat_translate_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.seventh_repeat
    ADD CONSTRAINT seventh_repeat_translate_id_fkey FOREIGN KEY (translate_id) REFERENCES public.translates(id) ON DELETE CASCADE;


--
-- TOC entry 2942 (class 2606 OID 24847)
-- Name: sixth_repeat sixth_repeat_dictionary_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sixth_repeat
    ADD CONSTRAINT sixth_repeat_dictionary_id_fkey FOREIGN KEY (dictionary_id) REFERENCES public.dictionaries(id) ON DELETE CASCADE;


--
-- TOC entry 2943 (class 2606 OID 24852)
-- Name: sixth_repeat sixth_repeat_translate_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sixth_repeat
    ADD CONSTRAINT sixth_repeat_translate_id_fkey FOREIGN KEY (translate_id) REFERENCES public.translates(id) ON DELETE CASCADE;


--
-- TOC entry 2936 (class 2606 OID 24808)
-- Name: third_repeat third_repeat_dictionary_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.third_repeat
    ADD CONSTRAINT third_repeat_dictionary_id_fkey FOREIGN KEY (dictionary_id) REFERENCES public.dictionaries(id) ON DELETE CASCADE;


--
-- TOC entry 2937 (class 2606 OID 24813)
-- Name: third_repeat third_repeat_translate_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.third_repeat
    ADD CONSTRAINT third_repeat_translate_id_fkey FOREIGN KEY (translate_id) REFERENCES public.translates(id) ON DELETE CASCADE;


--
-- TOC entry 2929 (class 2606 OID 24723)
-- Name: translates translates_dictionary_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.translates
    ADD CONSTRAINT translates_dictionary_id_fkey FOREIGN KEY (dictionary_id) REFERENCES public.dictionaries(id) ON DELETE CASCADE;


--
-- TOC entry 2926 (class 2606 OID 24779)
-- Name: user_parameters user_parameters_last_learning_translate_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_parameters
    ADD CONSTRAINT user_parameters_last_learning_translate_fkey FOREIGN KEY (last_learning_translate) REFERENCES public.translates(id) ON DELETE CASCADE;


--
-- TOC entry 2925 (class 2606 OID 24689)
-- Name: user_parameters user_parameters_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_parameters
    ADD CONSTRAINT user_parameters_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(tg_id) ON DELETE CASCADE;


-- Completed on 2020-12-14 01:35:59 EET

--
-- PostgreSQL database dump complete
--

