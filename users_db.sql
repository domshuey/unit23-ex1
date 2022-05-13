drop database if exists blogly;

create database blogly;

\c blogly;

create table users (
    id serial primary key,
    first_name text not null,
    last_name text not null,
    image_url text default 'https://www.pngitem.com/pimgs/m/504-5040528_empty-profile-picture-png-transparent-png.png'
)
