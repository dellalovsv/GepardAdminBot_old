create table if not exists `bot_admins_telegram` (
    tid bigint not null unique,
    username varchar(30) unique,
    phone varchar(30) unique,
    disable int not null default 0,
    date_add datetime not null default current_timestamp,
    primary key (tid)
);

create table if not exists `bot_finance` (
    id bigint not null auto_increment,
    date_add date not null default current_date,
    type int(11) not null default 0 comment "Тип записи: 1 - Доход; 2 - Расход",
    summa double(15,2) not null default 0,
    dsc text,
    primary key(id)
);

create table if not exists `bot_districts` (
    id int(11) not null auto_increment,
    name varchar(30) not null,
    primary key (id)
);

create table if not exists `bot_streets` (
    id int(11) not null auto_increment,
    name varchar(30) not null,
    district_id int(11) not null default "0",
    primary key (id)
);

create table if not exists `bot_dillers` (
    id int(11) not null auto_increment,
    name varchar(30) not null,
    district int(11) not null default "0",
    street int(11) not null default "0",
    build varchar(5) not null default "0",
    phone text,
    primary key (id)
);
