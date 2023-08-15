create table if not exists `bot_admins_telegram` (
    tid bigint not null unique,
    username varchar(30) unique,
    phone varchar(30) unique,
    disable int not null default 0,
    date_add datetime not null default current_timestamp,
    primary key (tid)
);
