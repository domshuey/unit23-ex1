drop database if exists blogly;

create database blogly;

\c blogly;

create table users (
    id serial primary key,
    first_name text not null,
    last_name text not null,
    image_url text default 'https://www.pngitem.com/pimgs/m/504-5040528_empty-profile-picture-png-transparent-png.png'
);

create table posts (
    id serial primary key,
    title text not null unique,
    content text not null,
    user_id integer references users on delete set null
);