--
-- PostgreSQL database dump
--

-- Dumped from database version 15.2
-- Dumped by pg_dump version 15.2

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
-- Name: account; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.account (
    id character varying(15) NOT NULL,
    credit integer NOT NULL,
    rating character varying(10) NOT NULL,
    role character varying(10) NOT NULL,
    CONSTRAINT account_credit_check CHECK ((credit >= 0)),
    CONSTRAINT account_role_check CHECK (((role)::text = ANY ((ARRAY['tutor'::character varying, 'tutee'::character varying])::text[])))
);


ALTER TABLE public.account OWNER TO postgres;

--
-- Name: charge_request; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.charge_request (
    id character varying(15) NOT NULL,
    money integer NOT NULL,
    CONSTRAINT charge_request_money_check CHECK ((money >= 0))
);


ALTER TABLE public.charge_request OWNER TO postgres;

--
-- Name: enrollment; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.enrollment (
    tutee character varying(15) NOT NULL,
    tutor character varying(15) NOT NULL,
    code character varying(2) NOT NULL,
    lecture_name character varying(20) NOT NULL,
    lecture_price integer,
    CONSTRAINT enrollment_lecture_price_check CHECK ((lecture_price >= 0))
);


ALTER TABLE public.enrollment OWNER TO postgres;

--
-- Name: lecture; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.lecture (
    code character varying(2) NOT NULL,
    name character varying(20) NOT NULL,
    price integer NOT NULL,
    tutor character varying(15) NOT NULL,
    CONSTRAINT lecture_price_check CHECK ((price >= 0))
);


ALTER TABLE public.lecture OWNER TO postgres;

--
-- Name: pass_enroll; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.pass_enroll (
    tutor character varying(15) NOT NULL,
    tutee character varying(15) NOT NULL
);


ALTER TABLE public.pass_enroll OWNER TO postgres;

--
-- Name: pass_info; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.pass_info (
    tutor character varying(15) NOT NULL,
    price integer NOT NULL,
    CONSTRAINT pass_info_price_check CHECK ((price >= 0))
);


ALTER TABLE public.pass_info OWNER TO postgres;

--
-- Name: rating_info; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rating_info (
    rating character varying(10) NOT NULL,
    condition integer NOT NULL,
    discount numeric(4,2) NOT NULL,
    CONSTRAINT rating_info_condition_check CHECK ((condition >= 0)),
    CONSTRAINT rating_info_discount_check CHECK ((((100)::numeric > discount) AND (discount >= (0)::numeric)))
);


ALTER TABLE public.rating_info OWNER TO postgres;

--
-- Name: subject; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.subject (
    code character varying(2) NOT NULL,
    subject_name character varying(20) NOT NULL
);


ALTER TABLE public.subject OWNER TO postgres;

--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id character varying(15) NOT NULL,
    password character varying(20) NOT NULL
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Data for Name: account; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.account (id, credit, rating, role) FROM stdin;
postgres	75000	bronze	tutee
Jo	8000	welcome	tutee
free	10000	welcome	tutor
jihoon	9000	welcome	tutee
admin	11030000	gold	tutor
mingyu809	1000	welcome	tutee
\.


--
-- Data for Name: charge_request; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.charge_request (id, money) FROM stdin;
\.


--
-- Data for Name: enrollment; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.enrollment (tutee, tutor, code, lecture_name, lecture_price) FROM stdin;
postgres	admin	00	korean history	1000
Jo	admin	00	korean history	1000
mingyu809	admin	00	korean history	0
mingyu809	admin	01	Geometry	0
mingyu809	admin	01	Calculus	0
jihoon	admin	01	Calculus	0
jihoon	admin	01	Geometry	0
\.


--
-- Data for Name: lecture; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.lecture (code, name, price, tutor) FROM stdin;
00	korean history	1000	admin
01	Geometry	1000	admin
01	Calculus	1000	admin
\.


--
-- Data for Name: pass_enroll; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.pass_enroll (tutor, tutee) FROM stdin;
free	mingyu809
admin	mingyu809
free	jihoon
\.


--
-- Data for Name: pass_info; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.pass_info (tutor, price) FROM stdin;
admin	1000000
free	0
\.


--
-- Data for Name: rating_info; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rating_info (rating, condition, discount) FROM stdin;
gold	500000	2.50
silver	100000	1.00
bronze	50000	0.50
welcome	0	0.00
\.


--
-- Data for Name: subject; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.subject (code, subject_name) FROM stdin;
00	history
01	mathematics
02	language
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, password) FROM stdin;
admin	0000
postgres	dbdb
Jo	qkqh123
mingyu809	whalsrb123
free	0000
jihoon	ehowl
\.


--
-- Name: account account_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account
    ADD CONSTRAINT account_pkey PRIMARY KEY (id);


--
-- Name: lecture lecture_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.lecture
    ADD CONSTRAINT lecture_pkey PRIMARY KEY (code, name, price, tutor);


--
-- Name: pass_enroll pass_enroll_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pass_enroll
    ADD CONSTRAINT pass_enroll_pkey PRIMARY KEY (tutor, tutee);


--
-- Name: pass_info pass_info_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pass_info
    ADD CONSTRAINT pass_info_pkey PRIMARY KEY (tutor);


--
-- Name: rating_info rating_info_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rating_info
    ADD CONSTRAINT rating_info_pkey PRIMARY KEY (rating);


--
-- Name: subject subject_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subject
    ADD CONSTRAINT subject_pkey PRIMARY KEY (code);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: account account_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account
    ADD CONSTRAINT account_id_fkey FOREIGN KEY (id) REFERENCES public.users(id);


--
-- Name: account account_rating_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account
    ADD CONSTRAINT account_rating_fkey FOREIGN KEY (rating) REFERENCES public.rating_info(rating);


--
-- Name: charge_request charge_request_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.charge_request
    ADD CONSTRAINT charge_request_id_fkey FOREIGN KEY (id) REFERENCES public.users(id);


--
-- Name: enrollment enrollment_code_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enrollment
    ADD CONSTRAINT enrollment_code_fkey FOREIGN KEY (code) REFERENCES public.subject(code);


--
-- Name: enrollment enrollment_tutee_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enrollment
    ADD CONSTRAINT enrollment_tutee_fkey FOREIGN KEY (tutee) REFERENCES public.users(id);


--
-- Name: enrollment enrollment_tutor_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enrollment
    ADD CONSTRAINT enrollment_tutor_fkey FOREIGN KEY (tutor) REFERENCES public.users(id);


--
-- Name: lecture lecture_code_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.lecture
    ADD CONSTRAINT lecture_code_fkey FOREIGN KEY (code) REFERENCES public.subject(code);


--
-- Name: lecture lecture_tutor_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.lecture
    ADD CONSTRAINT lecture_tutor_fkey FOREIGN KEY (tutor) REFERENCES public.users(id);


--
-- Name: pass_enroll pass_enroll_tutee_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pass_enroll
    ADD CONSTRAINT pass_enroll_tutee_fkey FOREIGN KEY (tutee) REFERENCES public.users(id);


--
-- Name: pass_enroll pass_enroll_tutor_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pass_enroll
    ADD CONSTRAINT pass_enroll_tutor_fkey FOREIGN KEY (tutor) REFERENCES public.users(id);


--
-- Name: pass_info pass_info_tutor_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pass_info
    ADD CONSTRAINT pass_info_tutor_fkey FOREIGN KEY (tutor) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

