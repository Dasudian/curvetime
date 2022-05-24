--
-- PostgreSQL database dump
--

-- Dumped from database version 12.7 (Ubuntu 12.7-0ubuntu0.20.10.1)
-- Dumped by pg_dump version 12.7 (Ubuntu 12.7-0ubuntu0.20.10.1)

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
-- Name: auth_group; Type: TABLE; Schema: public; Owner: stockai
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO stockai;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: stockai
--

CREATE SEQUENCE public.auth_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO stockai;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: stockai
--

ALTER SEQUENCE public.auth_group_id_seq OWNED BY public.auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: stockai
--

CREATE TABLE public.auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO stockai;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: stockai
--

CREATE SEQUENCE public.auth_group_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO stockai;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: stockai
--

ALTER SEQUENCE public.auth_group_permissions_id_seq OWNED BY public.auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: stockai
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO stockai;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: stockai
--

CREATE SEQUENCE public.auth_permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO stockai;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: stockai
--

ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: stockai
--

CREATE TABLE public.auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(150) NOT NULL,
    last_name character varying(150) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE public.auth_user OWNER TO stockai;

--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: stockai
--

CREATE TABLE public.auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.auth_user_groups OWNER TO stockai;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: stockai
--

CREATE SEQUENCE public.auth_user_groups_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_groups_id_seq OWNER TO stockai;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: stockai
--

ALTER SEQUENCE public.auth_user_groups_id_seq OWNED BY public.auth_user_groups.id;


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: stockai
--

CREATE SEQUENCE public.auth_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_id_seq OWNER TO stockai;

--
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: stockai
--

ALTER SEQUENCE public.auth_user_id_seq OWNED BY public.auth_user.id;


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: stockai
--

CREATE TABLE public.auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_user_user_permissions OWNER TO stockai;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: stockai
--

CREATE SEQUENCE public.auth_user_user_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_user_permissions_id_seq OWNER TO stockai;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: stockai
--

ALTER SEQUENCE public.auth_user_user_permissions_id_seq OWNED BY public.auth_user_user_permissions.id;


--
-- Name: background_task; Type: TABLE; Schema: public; Owner: stockai
--

CREATE TABLE public.background_task (
    id integer NOT NULL,
    task_name character varying(190) NOT NULL,
    task_params text NOT NULL,
    task_hash character varying(40) NOT NULL,
    verbose_name character varying(255),
    priority integer NOT NULL,
    run_at timestamp with time zone NOT NULL,
    repeat bigint NOT NULL,
    repeat_until timestamp with time zone,
    queue character varying(190),
    attempts integer NOT NULL,
    failed_at timestamp with time zone,
    last_error text NOT NULL,
    locked_by character varying(64),
    locked_at timestamp with time zone,
    creator_object_id integer,
    creator_content_type_id integer,
    CONSTRAINT background_task_creator_object_id_check CHECK ((creator_object_id >= 0))
);


ALTER TABLE public.background_task OWNER TO stockai;

--
-- Name: background_task_completedtask; Type: TABLE; Schema: public; Owner: stockai
--

CREATE TABLE public.background_task_completedtask (
    id integer NOT NULL,
    task_name character varying(190) NOT NULL,
    task_params text NOT NULL,
    task_hash character varying(40) NOT NULL,
    verbose_name character varying(255),
    priority integer NOT NULL,
    run_at timestamp with time zone NOT NULL,
    repeat bigint NOT NULL,
    repeat_until timestamp with time zone,
    queue character varying(190),
    attempts integer NOT NULL,
    failed_at timestamp with time zone,
    last_error text NOT NULL,
    locked_by character varying(64),
    locked_at timestamp with time zone,
    creator_object_id integer,
    creator_content_type_id integer,
    CONSTRAINT background_task_completedtask_creator_object_id_check CHECK ((creator_object_id >= 0))
);


ALTER TABLE public.background_task_completedtask OWNER TO stockai;

--
-- Name: background_task_completedtask_id_seq; Type: SEQUENCE; Schema: public; Owner: stockai
--

CREATE SEQUENCE public.background_task_completedtask_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.background_task_completedtask_id_seq OWNER TO stockai;

--
-- Name: background_task_completedtask_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: stockai
--

ALTER SEQUENCE public.background_task_completedtask_id_seq OWNED BY public.background_task_completedtask.id;


--
-- Name: background_task_id_seq; Type: SEQUENCE; Schema: public; Owner: stockai
--

CREATE SEQUENCE public.background_task_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.background_task_id_seq OWNER TO stockai;

--
-- Name: background_task_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: stockai
--

ALTER SEQUENCE public.background_task_id_seq OWNED BY public.background_task.id;


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: stockai
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO stockai;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: stockai
--

CREATE SEQUENCE public.django_admin_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO stockai;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: stockai
--

ALTER SEQUENCE public.django_admin_log_id_seq OWNED BY public.django_admin_log.id;


--
-- Name: django_celery_results_chordcounter; Type: TABLE; Schema: public; Owner: stockai
--

CREATE TABLE public.django_celery_results_chordcounter (
    id integer NOT NULL,
    group_id character varying(255) NOT NULL,
    sub_tasks text NOT NULL,
    count integer NOT NULL,
    CONSTRAINT django_celery_results_chordcounter_count_check CHECK ((count >= 0))
);


ALTER TABLE public.django_celery_results_chordcounter OWNER TO stockai;

--
-- Name: django_celery_results_chordcounter_id_seq; Type: SEQUENCE; Schema: public; Owner: stockai
--

CREATE SEQUENCE public.django_celery_results_chordcounter_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_celery_results_chordcounter_id_seq OWNER TO stockai;

--
-- Name: django_celery_results_chordcounter_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: stockai
--

ALTER SEQUENCE public.django_celery_results_chordcounter_id_seq OWNED BY public.django_celery_results_chordcounter.id;


--
-- Name: django_celery_results_groupresult; Type: TABLE; Schema: public; Owner: stockai
--

CREATE TABLE public.django_celery_results_groupresult (
    id integer NOT NULL,
    group_id character varying(255) NOT NULL,
    date_created timestamp with time zone NOT NULL,
    date_done timestamp with time zone NOT NULL,
    content_type character varying(128) NOT NULL,
    content_encoding character varying(64) NOT NULL,
    result text
);


ALTER TABLE public.django_celery_results_groupresult OWNER TO stockai;

--
-- Name: django_celery_results_groupresult_id_seq; Type: SEQUENCE; Schema: public; Owner: stockai
--

CREATE SEQUENCE public.django_celery_results_groupresult_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_celery_results_groupresult_id_seq OWNER TO stockai;

--
-- Name: django_celery_results_groupresult_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: stockai
--

ALTER SEQUENCE public.django_celery_results_groupresult_id_seq OWNED BY public.django_celery_results_groupresult.id;


--
-- Name: django_celery_results_taskresult; Type: TABLE; Schema: public; Owner: stockai
--

CREATE TABLE public.django_celery_results_taskresult (
    id integer NOT NULL,
    task_id character varying(255) NOT NULL,
    status character varying(50) NOT NULL,
    content_type character varying(128) NOT NULL,
    content_encoding character varying(64) NOT NULL,
    result text,
    date_done timestamp with time zone NOT NULL,
    traceback text,
    meta text,
    task_args text,
    task_kwargs text,
    task_name character varying(255),
    worker character varying(100),
    date_created timestamp with time zone NOT NULL
);


ALTER TABLE public.django_celery_results_taskresult OWNER TO stockai;

--
-- Name: django_celery_results_taskresult_id_seq; Type: SEQUENCE; Schema: public; Owner: stockai
--

CREATE SEQUENCE public.django_celery_results_taskresult_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_celery_results_taskresult_id_seq OWNER TO stockai;

--
-- Name: django_celery_results_taskresult_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: stockai
--

ALTER SEQUENCE public.django_celery_results_taskresult_id_seq OWNED BY public.django_celery_results_taskresult.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: stockai
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO stockai;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: stockai
--

CREATE SEQUENCE public.django_content_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO stockai;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: stockai
--

ALTER SEQUENCE public.django_content_type_id_seq OWNED BY public.django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: stockai
--

CREATE TABLE public.django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO stockai;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: stockai
--

CREATE SEQUENCE public.django_migrations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_migrations_id_seq OWNER TO stockai;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: stockai
--

ALTER SEQUENCE public.django_migrations_id_seq OWNED BY public.django_migrations.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: stockai
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO stockai;

--
-- Name: stockai_action; Type: TABLE; Schema: public; Owner: stockai
--

CREATE TABLE public.stockai_action (
    id integer NOT NULL,
    action integer NOT NULL,
    stock character varying(20),
    current_price double precision NOT NULL,
    last_price double precision NOT NULL,
    gain double precision NOT NULL,
    "time" character varying(24),
    onhold boolean NOT NULL
);


ALTER TABLE public.stockai_action OWNER TO stockai;

--
-- Name: stockai_action_id_seq; Type: SEQUENCE; Schema: public; Owner: stockai
--

CREATE SEQUENCE public.stockai_action_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.stockai_action_id_seq OWNER TO stockai;

--
-- Name: stockai_action_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: stockai
--

ALTER SEQUENCE public.stockai_action_id_seq OWNED BY public.stockai_action.id;


--
-- Name: stockai_action_user; Type: TABLE; Schema: public; Owner: stockai
--

CREATE TABLE public.stockai_action_user (
    id integer NOT NULL,
    openid character varying(40) NOT NULL,
    action integer NOT NULL,
    onhold boolean NOT NULL,
    stock character varying(20),
    current_price double precision NOT NULL,
    last_price double precision NOT NULL,
    gain double precision NOT NULL,
    "time" character varying(24),
    pay double precision NOT NULL
);


ALTER TABLE public.stockai_action_user OWNER TO stockai;

--
-- Name: stockai_action_user_id_seq; Type: SEQUENCE; Schema: public; Owner: stockai
--

CREATE SEQUENCE public.stockai_action_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.stockai_action_user_id_seq OWNER TO stockai;

--
-- Name: stockai_action_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: stockai
--

ALTER SEQUENCE public.stockai_action_user_id_seq OWNED BY public.stockai_action_user.id;


--
-- Name: stockai_feature; Type: TABLE; Schema: public; Owner: stockai
--

CREATE TABLE public.stockai_feature (
    id integer NOT NULL,
    "time" character varying(40),
    frame jsonb
);


ALTER TABLE public.stockai_feature OWNER TO stockai;

--
-- Name: stockai_feature2; Type: TABLE; Schema: public; Owner: stockai
--

CREATE TABLE public.stockai_feature2 (
    id integer NOT NULL,
    "time" character varying(40),
    frame jsonb
);


ALTER TABLE public.stockai_feature2 OWNER TO stockai;

--
-- Name: stockai_feature2_id_seq; Type: SEQUENCE; Schema: public; Owner: stockai
--

CREATE SEQUENCE public.stockai_feature2_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.stockai_feature2_id_seq OWNER TO stockai;

--
-- Name: stockai_feature2_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: stockai
--

ALTER SEQUENCE public.stockai_feature2_id_seq OWNED BY public.stockai_feature2.id;


--
-- Name: stockai_feature_id_seq; Type: SEQUENCE; Schema: public; Owner: stockai
--

CREATE SEQUENCE public.stockai_feature_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.stockai_feature_id_seq OWNER TO stockai;

--
-- Name: stockai_feature_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: stockai
--

ALTER SEQUENCE public.stockai_feature_id_seq OWNED BY public.stockai_feature.id;


--
-- Name: stockai_logs; Type: TABLE; Schema: public; Owner: stockai
--

CREATE TABLE public.stockai_logs (
    id integer NOT NULL,
    operation character varying(20),
    operator character varying(20),
    "time" character varying(50),
    module character varying(20),
    ip character varying(15),
    operand character varying(50),
    result boolean,
    detailed character varying(50),
    type character varying(20)
);


ALTER TABLE public.stockai_logs OWNER TO stockai;

--
-- Name: stockai_logs_id_seq; Type: SEQUENCE; Schema: public; Owner: stockai
--

CREATE SEQUENCE public.stockai_logs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.stockai_logs_id_seq OWNER TO stockai;

--
-- Name: stockai_logs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: stockai
--

ALTER SEQUENCE public.stockai_logs_id_seq OWNED BY public.stockai_logs.id;


--
-- Name: stockai_payhistory; Type: TABLE; Schema: public; Owner: stockai
--

CREATE TABLE public.stockai_payhistory (
    id integer NOT NULL,
    openid character varying(40) NOT NULL,
    "time" character varying(24),
    expire character varying(24),
    amount double precision NOT NULL,
    schema integer NOT NULL,
    payid character varying(64),
    trade_no character varying(22)
);


ALTER TABLE public.stockai_payhistory OWNER TO stockai;

--
-- Name: stockai_payhistory_id_seq; Type: SEQUENCE; Schema: public; Owner: stockai
--

CREATE SEQUENCE public.stockai_payhistory_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.stockai_payhistory_id_seq OWNER TO stockai;

--
-- Name: stockai_payhistory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: stockai
--

ALTER SEQUENCE public.stockai_payhistory_id_seq OWNED BY public.stockai_payhistory.id;


--
-- Name: stockai_price; Type: TABLE; Schema: public; Owner: stockai
--

CREATE TABLE public.stockai_price (
    id integer NOT NULL,
    code character varying(20),
    "time" character varying(40),
    open double precision,
    close double precision,
    price double precision,
    high double precision,
    low double precision,
    ask double precision,
    bid double precision,
    volume double precision,
    amount double precision,
    ask_v1 double precision,
    ask1 double precision,
    ask_v2 double precision,
    ask2 double precision,
    ask_v3 double precision,
    ask3 double precision,
    ask_v4 double precision,
    ask4 double precision,
    ask_v5 double precision,
    ask5 double precision,
    bid_v1 double precision,
    bid1 double precision,
    bid_v2 double precision,
    bid2 double precision,
    bid_v3 double precision,
    bid3 double precision,
    bid_v4 double precision,
    bid4 double precision,
    bid_v5 double precision,
    bid5 double precision
);


ALTER TABLE public.stockai_price OWNER TO stockai;

--
-- Name: stockai_price_id_seq; Type: SEQUENCE; Schema: public; Owner: stockai
--

CREATE SEQUENCE public.stockai_price_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.stockai_price_id_seq OWNER TO stockai;

--
-- Name: stockai_price_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: stockai
--

ALTER SEQUENCE public.stockai_price_id_seq OWNED BY public.stockai_price.id;


--
-- Name: stockai_reward; Type: TABLE; Schema: public; Owner: stockai
--

CREATE TABLE public.stockai_reward (
    id integer NOT NULL,
    openid character varying(40) NOT NULL,
    reward double precision NOT NULL,
    "time" character varying(24),
    tier integer NOT NULL,
    pay_history_id integer NOT NULL
);


ALTER TABLE public.stockai_reward OWNER TO stockai;

--
-- Name: stockai_reward_id_seq; Type: SEQUENCE; Schema: public; Owner: stockai
--

CREATE SEQUENCE public.stockai_reward_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.stockai_reward_id_seq OWNER TO stockai;

--
-- Name: stockai_reward_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: stockai
--

ALTER SEQUENCE public.stockai_reward_id_seq OWNED BY public.stockai_reward.id;


--
-- Name: stockai_stocks; Type: TABLE; Schema: public; Owner: stockai
--

CREATE TABLE public.stockai_stocks (
    id integer NOT NULL,
    code character varying(20),
    name character varying(40),
    pe double precision,
    capital double precision
);


ALTER TABLE public.stockai_stocks OWNER TO stockai;

--
-- Name: stockai_stocks_id_seq; Type: SEQUENCE; Schema: public; Owner: stockai
--

CREATE SEQUENCE public.stockai_stocks_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.stockai_stocks_id_seq OWNER TO stockai;

--
-- Name: stockai_stocks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: stockai
--

ALTER SEQUENCE public.stockai_stocks_id_seq OWNED BY public.stockai_stocks.id;


--
-- Name: stockai_user; Type: TABLE; Schema: public; Owner: stockai
--

CREATE TABLE public.stockai_user (
    id integer NOT NULL,
    username character varying(20),
    password character varying(80),
    "imgUrl" character varying(200),
    nick character varying(40),
    openid character varying(40),
    phone character varying(20),
    role character varying(1) NOT NULL,
    session_key character varying(100),
    sex integer NOT NULL,
    referer integer NOT NULL,
    create_time character varying(24),
    state integer NOT NULL,
    schema integer NOT NULL
);


ALTER TABLE public.stockai_user OWNER TO stockai;

--
-- Name: stockai_user_id_seq; Type: SEQUENCE; Schema: public; Owner: stockai
--

CREATE SEQUENCE public.stockai_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.stockai_user_id_seq OWNER TO stockai;

--
-- Name: stockai_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: stockai
--

ALTER SEQUENCE public.stockai_user_id_seq OWNED BY public.stockai_user.id;


--
-- Name: stockai_withdraw; Type: TABLE; Schema: public; Owner: stockai
--

CREATE TABLE public.stockai_withdraw (
    id integer NOT NULL,
    openid character varying(40) NOT NULL,
    "time" character varying(24),
    amount double precision NOT NULL,
    state integer NOT NULL
);


ALTER TABLE public.stockai_withdraw OWNER TO stockai;

--
-- Name: stockai_withdraw_id_seq; Type: SEQUENCE; Schema: public; Owner: stockai
--

CREATE SEQUENCE public.stockai_withdraw_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.stockai_withdraw_id_seq OWNER TO stockai;

--
-- Name: stockai_withdraw_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: stockai
--

ALTER SEQUENCE public.stockai_withdraw_id_seq OWNED BY public.stockai_withdraw.id;


--
-- Name: auth_group id; Type: DEFAULT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.auth_group ALTER COLUMN id SET DEFAULT nextval('public.auth_group_id_seq'::regclass);


--
-- Name: auth_group_permissions id; Type: DEFAULT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_group_permissions_id_seq'::regclass);


--
-- Name: auth_permission id; Type: DEFAULT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.auth_permission ALTER COLUMN id SET DEFAULT nextval('public.auth_permission_id_seq'::regclass);


--
-- Name: auth_user id; Type: DEFAULT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.auth_user ALTER COLUMN id SET DEFAULT nextval('public.auth_user_id_seq'::regclass);


--
-- Name: auth_user_groups id; Type: DEFAULT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.auth_user_groups ALTER COLUMN id SET DEFAULT nextval('public.auth_user_groups_id_seq'::regclass);


--
-- Name: auth_user_user_permissions id; Type: DEFAULT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_user_user_permissions_id_seq'::regclass);


--
-- Name: background_task id; Type: DEFAULT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.background_task ALTER COLUMN id SET DEFAULT nextval('public.background_task_id_seq'::regclass);


--
-- Name: background_task_completedtask id; Type: DEFAULT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.background_task_completedtask ALTER COLUMN id SET DEFAULT nextval('public.background_task_completedtask_id_seq'::regclass);


--
-- Name: django_admin_log id; Type: DEFAULT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.django_admin_log ALTER COLUMN id SET DEFAULT nextval('public.django_admin_log_id_seq'::regclass);


--
-- Name: django_celery_results_chordcounter id; Type: DEFAULT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.django_celery_results_chordcounter ALTER COLUMN id SET DEFAULT nextval('public.django_celery_results_chordcounter_id_seq'::regclass);


--
-- Name: django_celery_results_groupresult id; Type: DEFAULT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.django_celery_results_groupresult ALTER COLUMN id SET DEFAULT nextval('public.django_celery_results_groupresult_id_seq'::regclass);


--
-- Name: django_celery_results_taskresult id; Type: DEFAULT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.django_celery_results_taskresult ALTER COLUMN id SET DEFAULT nextval('public.django_celery_results_taskresult_id_seq'::regclass);


--
-- Name: django_content_type id; Type: DEFAULT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.django_content_type ALTER COLUMN id SET DEFAULT nextval('public.django_content_type_id_seq'::regclass);


--
-- Name: django_migrations id; Type: DEFAULT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.django_migrations ALTER COLUMN id SET DEFAULT nextval('public.django_migrations_id_seq'::regclass);


--
-- Name: stockai_action id; Type: DEFAULT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.stockai_action ALTER COLUMN id SET DEFAULT nextval('public.stockai_action_id_seq'::regclass);


--
-- Name: stockai_action_user id; Type: DEFAULT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.stockai_action_user ALTER COLUMN id SET DEFAULT nextval('public.stockai_action_user_id_seq'::regclass);


--
-- Name: stockai_feature id; Type: DEFAULT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.stockai_feature ALTER COLUMN id SET DEFAULT nextval('public.stockai_feature_id_seq'::regclass);


--
-- Name: stockai_feature2 id; Type: DEFAULT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.stockai_feature2 ALTER COLUMN id SET DEFAULT nextval('public.stockai_feature2_id_seq'::regclass);


--
-- Name: stockai_logs id; Type: DEFAULT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.stockai_logs ALTER COLUMN id SET DEFAULT nextval('public.stockai_logs_id_seq'::regclass);


--
-- Name: stockai_payhistory id; Type: DEFAULT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.stockai_payhistory ALTER COLUMN id SET DEFAULT nextval('public.stockai_payhistory_id_seq'::regclass);


--
-- Name: stockai_price id; Type: DEFAULT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.stockai_price ALTER COLUMN id SET DEFAULT nextval('public.stockai_price_id_seq'::regclass);


--
-- Name: stockai_reward id; Type: DEFAULT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.stockai_reward ALTER COLUMN id SET DEFAULT nextval('public.stockai_reward_id_seq'::regclass);


--
-- Name: stockai_stocks id; Type: DEFAULT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.stockai_stocks ALTER COLUMN id SET DEFAULT nextval('public.stockai_stocks_id_seq'::regclass);


--
-- Name: stockai_user id; Type: DEFAULT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.stockai_user ALTER COLUMN id SET DEFAULT nextval('public.stockai_user_id_seq'::regclass);


--
-- Name: stockai_withdraw id; Type: DEFAULT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.stockai_withdraw ALTER COLUMN id SET DEFAULT nextval('public.stockai_withdraw_id_seq'::regclass);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_user_id_group_id_94350c0c_uniq; Type: CONSTRAINT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq UNIQUE (user_id, group_id);


--
-- Name: auth_user auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_permission_id_14a6b632_uniq; Type: CONSTRAINT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq UNIQUE (user_id, permission_id);


--
-- Name: auth_user auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: background_task_completedtask background_task_completedtask_pkey; Type: CONSTRAINT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.background_task_completedtask
    ADD CONSTRAINT background_task_completedtask_pkey PRIMARY KEY (id);


--
-- Name: background_task background_task_pkey; Type: CONSTRAINT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.background_task
    ADD CONSTRAINT background_task_pkey PRIMARY KEY (id);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_celery_results_chordcounter django_celery_results_chordcounter_group_id_key; Type: CONSTRAINT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.django_celery_results_chordcounter
    ADD CONSTRAINT django_celery_results_chordcounter_group_id_key UNIQUE (group_id);


--
-- Name: django_celery_results_chordcounter django_celery_results_chordcounter_pkey; Type: CONSTRAINT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.django_celery_results_chordcounter
    ADD CONSTRAINT django_celery_results_chordcounter_pkey PRIMARY KEY (id);


--
-- Name: django_celery_results_groupresult django_celery_results_groupresult_group_id_key; Type: CONSTRAINT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.django_celery_results_groupresult
    ADD CONSTRAINT django_celery_results_groupresult_group_id_key UNIQUE (group_id);


--
-- Name: django_celery_results_groupresult django_celery_results_groupresult_pkey; Type: CONSTRAINT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.django_celery_results_groupresult
    ADD CONSTRAINT django_celery_results_groupresult_pkey PRIMARY KEY (id);


--
-- Name: django_celery_results_taskresult django_celery_results_taskresult_pkey; Type: CONSTRAINT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.django_celery_results_taskresult
    ADD CONSTRAINT django_celery_results_taskresult_pkey PRIMARY KEY (id);


--
-- Name: django_celery_results_taskresult django_celery_results_taskresult_task_id_key; Type: CONSTRAINT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.django_celery_results_taskresult
    ADD CONSTRAINT django_celery_results_taskresult_task_id_key UNIQUE (task_id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: stockai_action stockai_action_pkey; Type: CONSTRAINT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.stockai_action
    ADD CONSTRAINT stockai_action_pkey PRIMARY KEY (id);


--
-- Name: stockai_action_user stockai_action_user_pkey; Type: CONSTRAINT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.stockai_action_user
    ADD CONSTRAINT stockai_action_user_pkey PRIMARY KEY (id);


--
-- Name: stockai_feature2 stockai_feature2_pkey; Type: CONSTRAINT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.stockai_feature2
    ADD CONSTRAINT stockai_feature2_pkey PRIMARY KEY (id);


--
-- Name: stockai_feature stockai_feature_pkey; Type: CONSTRAINT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.stockai_feature
    ADD CONSTRAINT stockai_feature_pkey PRIMARY KEY (id);


--
-- Name: stockai_feature stockai_feature_time_9558d08b_uniq; Type: CONSTRAINT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.stockai_feature
    ADD CONSTRAINT stockai_feature_time_9558d08b_uniq UNIQUE ("time");


--
-- Name: stockai_logs stockai_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.stockai_logs
    ADD CONSTRAINT stockai_logs_pkey PRIMARY KEY (id);


--
-- Name: stockai_payhistory stockai_payhistory_pkey; Type: CONSTRAINT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.stockai_payhistory
    ADD CONSTRAINT stockai_payhistory_pkey PRIMARY KEY (id);


--
-- Name: stockai_price stockai_price_pkey; Type: CONSTRAINT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.stockai_price
    ADD CONSTRAINT stockai_price_pkey PRIMARY KEY (id);


--
-- Name: stockai_reward stockai_reward_pkey; Type: CONSTRAINT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.stockai_reward
    ADD CONSTRAINT stockai_reward_pkey PRIMARY KEY (id);


--
-- Name: stockai_stocks stockai_stocks_pkey; Type: CONSTRAINT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.stockai_stocks
    ADD CONSTRAINT stockai_stocks_pkey PRIMARY KEY (id);


--
-- Name: stockai_user stockai_user_pkey; Type: CONSTRAINT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.stockai_user
    ADD CONSTRAINT stockai_user_pkey PRIMARY KEY (id);


--
-- Name: stockai_withdraw stockai_withdraw_pkey; Type: CONSTRAINT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.stockai_withdraw
    ADD CONSTRAINT stockai_withdraw_pkey PRIMARY KEY (id);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: stockai
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: stockai
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: stockai
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: stockai
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_group_id_97559544; Type: INDEX; Schema: public; Owner: stockai
--

CREATE INDEX auth_user_groups_group_id_97559544 ON public.auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_user_id_6a12ed8b; Type: INDEX; Schema: public; Owner: stockai
--

CREATE INDEX auth_user_groups_user_id_6a12ed8b ON public.auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_permission_id_1fbb5f2c; Type: INDEX; Schema: public; Owner: stockai
--

CREATE INDEX auth_user_user_permissions_permission_id_1fbb5f2c ON public.auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_user_id_a95ead1b; Type: INDEX; Schema: public; Owner: stockai
--

CREATE INDEX auth_user_user_permissions_user_id_a95ead1b ON public.auth_user_user_permissions USING btree (user_id);


--
-- Name: auth_user_username_6821ab7c_like; Type: INDEX; Schema: public; Owner: stockai
--

CREATE INDEX auth_user_username_6821ab7c_like ON public.auth_user USING btree (username varchar_pattern_ops);


--
-- Name: background_task_attempts_a9ade23d; Type: INDEX; Schema: public; Owner: stockai
--

CREATE INDEX background_task_attempts_a9ade23d ON public.background_task USING btree (attempts);


--
-- Name: background_task_completedtask_attempts_772a6783; Type: INDEX; Schema: public; Owner: stockai
--

CREATE INDEX background_task_completedtask_attempts_772a6783 ON public.background_task_completedtask USING btree (attempts);


--
-- Name: background_task_completedtask_creator_content_type_id_21d6a741; Type: INDEX; Schema: public; Owner: stockai
--

CREATE INDEX background_task_completedtask_creator_content_type_id_21d6a741 ON public.background_task_completedtask USING btree (creator_content_type_id);


--
-- Name: background_task_completedtask_failed_at_3de56618; Type: INDEX; Schema: public; Owner: stockai
--

CREATE INDEX background_task_completedtask_failed_at_3de56618 ON public.background_task_completedtask USING btree (failed_at);


--
-- Name: background_task_completedtask_locked_at_29c62708; Type: INDEX; Schema: public; Owner: stockai
--

CREATE INDEX background_task_completedtask_locked_at_29c62708 ON public.background_task_completedtask USING btree (locked_at);


--
-- Name: background_task_completedtask_locked_by_edc8a213; Type: INDEX; Schema: public; Owner: stockai
--

CREATE INDEX background_task_completedtask_locked_by_edc8a213 ON public.background_task_completedtask USING btree (locked_by);


--
-- Name: background_task_completedtask_locked_by_edc8a213_like; Type: INDEX; Schema: public; Owner: stockai
--

CREATE INDEX background_task_completedtask_locked_by_edc8a213_like ON public.background_task_completedtask USING btree (locked_by varchar_pattern_ops);


--
-- Name: background_task_completedtask_priority_9080692e; Type: INDEX; Schema: public; Owner: stockai
--

CREATE INDEX background_task_completedtask_priority_9080692e ON public.background_task_completedtask USING btree (priority);


--
-- Name: background_task_completedtask_queue_61fb0415; Type: INDEX; Schema: public; Owner: stockai
--

CREATE INDEX background_task_completedtask_queue_61fb0415 ON public.background_task_completedtask USING btree (queue);


--
-- Name: background_task_completedtask_queue_61fb0415_like; Type: INDEX; Schema: public; Owner: stockai
--

CREATE INDEX background_task_completedtask_queue_61fb0415_like ON public.background_task_completedtask USING btree (queue varchar_pattern_ops);


--
-- Name: background_task_completedtask_run_at_77c80f34; Type: INDEX; Schema: public; Owner: stockai
--

CREATE INDEX background_task_completedtask_run_at_77c80f34 ON public.background_task_completedtask USING btree (run_at);


--
-- Name: background_task_completedtask_task_hash_91187576; Type: INDEX; Schema: public; Owner: stockai
--

CREATE INDEX background_task_completedtask_task_hash_91187576 ON public.background_task_completedtask USING btree (task_hash);


--
-- Name: background_task_completedtask_task_hash_91187576_like; Type: INDEX; Schema: public; Owner: stockai
--

CREATE INDEX background_task_completedtask_task_hash_91187576_like ON public.background_task_completedtask USING btree (task_hash varchar_pattern_ops);


--
-- Name: background_task_completedtask_task_name_388dabc2; Type: INDEX; Schema: public; Owner: stockai
--

CREATE INDEX background_task_completedtask_task_name_388dabc2 ON public.background_task_completedtask USING btree (task_name);


--
-- Name: background_task_completedtask_task_name_388dabc2_like; Type: INDEX; Schema: public; Owner: stockai
--

CREATE INDEX background_task_completedtask_task_name_388dabc2_like ON public.background_task_completedtask USING btree (task_name varchar_pattern_ops);


--
-- Name: background_task_creator_content_type_id_61cc9af3; Type: INDEX; Schema: public; Owner: stockai
--

CREATE INDEX background_task_creator_content_type_id_61cc9af3 ON public.background_task USING btree (creator_content_type_id);


--
-- Name: background_task_failed_at_b81bba14; Type: INDEX; Schema: public; Owner: stockai
--

CREATE INDEX background_task_failed_at_b81bba14 ON public.background_task USING btree (failed_at);


--
-- Name: background_task_locked_at_0fb0f225; Type: INDEX; Schema: public; Owner: stockai
--

CREATE INDEX background_task_locked_at_0fb0f225 ON public.background_task USING btree (locked_at);


--
-- Name: background_task_locked_by_db7779e3; Type: INDEX; Schema: public; Owner: stockai
--

CREATE INDEX background_task_locked_by_db7779e3 ON public.background_task USING btree (locked_by);


--
-- Name: background_task_locked_by_db7779e3_like; Type: INDEX; Schema: public; Owner: stockai
--

CREATE INDEX background_task_locked_by_db7779e3_like ON public.background_task USING btree (locked_by varchar_pattern_ops);


--
-- Name: background_task_priority_88bdbce9; Type: INDEX; Schema: public; Owner: stockai
--

CREATE INDEX background_task_priority_88bdbce9 ON public.background_task USING btree (priority);


--
-- Name: background_task_queue_1d5f3a40; Type: INDEX; Schema: public; Owner: stockai
--

CREATE INDEX background_task_queue_1d5f3a40 ON public.background_task USING btree (queue);


--
-- Name: background_task_queue_1d5f3a40_like; Type: INDEX; Schema: public; Owner: stockai
--

CREATE INDEX background_task_queue_1d5f3a40_like ON public.background_task USING btree (queue varchar_pattern_ops);


--
-- Name: background_task_run_at_7baca3aa; Type: INDEX; Schema: public; Owner: stockai
--

CREATE INDEX background_task_run_at_7baca3aa ON public.background_task USING btree (run_at);


--
-- Name: background_task_task_hash_d8f233bd; Type: INDEX; Schema: public; Owner: stockai
--

CREATE INDEX background_task_task_hash_d8f233bd ON public.background_task USING btree (task_hash);


--
-- Name: background_task_task_hash_d8f233bd_like; Type: INDEX; Schema: public; Owner: stockai
--

CREATE INDEX background_task_task_hash_d8f233bd_like ON public.background_task USING btree (task_hash varchar_pattern_ops);


--
-- Name: background_task_task_name_4562d56a; Type: INDEX; Schema: public; Owner: stockai
--

CREATE INDEX background_task_task_name_4562d56a ON public.background_task USING btree (task_name);


--
-- Name: background_task_task_name_4562d56a_like; Type: INDEX; Schema: public; Owner: stockai
--

CREATE INDEX background_task_task_name_4562d56a_like ON public.background_task USING btree (task_name varchar_pattern_ops);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: stockai
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: stockai
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_cele_date_cr_bd6c1d_idx; Type: INDEX; Schema: public; Owner: stockai
--

CREATE INDEX django_cele_date_cr_bd6c1d_idx ON public.django_celery_results_groupresult USING btree (date_created);


--
-- Name: django_cele_date_cr_f04a50_idx; Type: INDEX; Schema: public; Owner: stockai
--

CREATE INDEX django_cele_date_cr_f04a50_idx ON public.django_celery_results_taskresult USING btree (date_created);


--
-- Name: django_cele_date_do_caae0e_idx; Type: INDEX; Schema: public; Owner: stockai
--

CREATE INDEX django_cele_date_do_caae0e_idx ON public.django_celery_results_groupresult USING btree (date_done);


--
-- Name: django_cele_date_do_f59aad_idx; Type: INDEX; Schema: public; Owner: stockai
--

CREATE INDEX django_cele_date_do_f59aad_idx ON public.django_celery_results_taskresult USING btree (date_done);


--
-- Name: django_cele_status_9b6201_idx; Type: INDEX; Schema: public; Owner: stockai
--

CREATE INDEX django_cele_status_9b6201_idx ON public.django_celery_results_taskresult USING btree (status);


--
-- Name: django_cele_task_na_08aec9_idx; Type: INDEX; Schema: public; Owner: stockai
--

CREATE INDEX django_cele_task_na_08aec9_idx ON public.django_celery_results_taskresult USING btree (task_name);


--
-- Name: django_cele_worker_d54dd8_idx; Type: INDEX; Schema: public; Owner: stockai
--

CREATE INDEX django_cele_worker_d54dd8_idx ON public.django_celery_results_taskresult USING btree (worker);


--
-- Name: django_celery_results_chordcounter_group_id_1f70858c_like; Type: INDEX; Schema: public; Owner: stockai
--

CREATE INDEX django_celery_results_chordcounter_group_id_1f70858c_like ON public.django_celery_results_chordcounter USING btree (group_id varchar_pattern_ops);


--
-- Name: django_celery_results_groupresult_group_id_a085f1a9_like; Type: INDEX; Schema: public; Owner: stockai
--

CREATE INDEX django_celery_results_groupresult_group_id_a085f1a9_like ON public.django_celery_results_groupresult USING btree (group_id varchar_pattern_ops);


--
-- Name: django_celery_results_taskresult_task_id_de0d95bf_like; Type: INDEX; Schema: public; Owner: stockai
--

CREATE INDEX django_celery_results_taskresult_task_id_de0d95bf_like ON public.django_celery_results_taskresult USING btree (task_id varchar_pattern_ops);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: stockai
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: stockai
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: stockai_feature_time_9558d08b_like; Type: INDEX; Schema: public; Owner: stockai
--

CREATE INDEX stockai_feature_time_9558d08b_like ON public.stockai_feature USING btree ("time" varchar_pattern_ops);


--
-- Name: stockai_reward_pay_history_id_2ac9abdd; Type: INDEX; Schema: public; Owner: stockai
--

CREATE INDEX stockai_reward_pay_history_id_2ac9abdd ON public.stockai_reward USING btree (pay_history_id);


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_group_id_97559544_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_user_id_6a12ed8b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: background_task_completedtask background_task_comp_creator_content_type_21d6a741_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.background_task_completedtask
    ADD CONSTRAINT background_task_comp_creator_content_type_21d6a741_fk_django_co FOREIGN KEY (creator_content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: background_task background_task_creator_content_type_61cc9af3_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.background_task
    ADD CONSTRAINT background_task_creator_content_type_61cc9af3_fk_django_co FOREIGN KEY (creator_content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: stockai_reward stockai_reward_pay_history_id_2ac9abdd_fk_stockai_payhistory_id; Type: FK CONSTRAINT; Schema: public; Owner: stockai
--

ALTER TABLE ONLY public.stockai_reward
    ADD CONSTRAINT stockai_reward_pay_history_id_2ac9abdd_fk_stockai_payhistory_id FOREIGN KEY (pay_history_id) REFERENCES public.stockai_payhistory(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

