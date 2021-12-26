create database swprj;
create table teacher(tid int,fname varchar(20),lname varchar(20),primary key(tid));
create table teacher(sid int,fname varchar(20),lname varchar(20),primary key(sid));
create table lesson(lid int,title varchar(20),weight int,primary key(lid));
create table class(lid int,cday set('satur','sun','mon','tues','wednes'),chour int,cminute int,tid int,
primary key(lid,cday,chour,cminute),foreign key(tid) references teacher(tid));
create table section(lid int,sid int,term1 float,fianl1 float,term2 float,final2 float,primary key(lid,sid));