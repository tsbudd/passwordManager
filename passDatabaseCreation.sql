/*
file name: passDatabaseCreation.py
version: 1.00.01
author: Tyler S. Budd
author GitHub: https://github.com/tsbudd
date created: 07/23/2022
last updated: 07/23/2022
description: MariaDB MySQL script for creating the database for passwordsMain.py
*/

create table accounts(
    acc_name varchar(30) primary key,
    acc_pass text not null,
    acc_lastUpdated datetime not null);
    
delimiter //

drop procedure newPass;
create procedure newPass(aName varchar(30), pass text)
begin
	insert into accounts (acc_name, acc_pass, acc_lastUpdated) values
		(aName, pass, now());
end //

create procedure updatePass(aName varchar(30), pass text)
begin
	update accounts
    set acc_pass = pass,
		acc_lastUpdated = now()
    where acc_name = aName;
end //

create procedure deletePass(aName varchar(30))
begin
	delete from accounts
    where acc_name = aName;
end//

delimiter ;