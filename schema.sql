
CREATE TABLE CSRF_Token (
	csrf_token CHAR(64) PRIMARY KEY
);


CREATE TABLE UserAccount (
	account_id    INT NOT NULL;
	creation_time Datetime NOT NULL;
	status        TINYINT NOT NULL;
	email         VARCHAR(40) NOT NULL;
	username      VARCHAR(24) NOT NULL;
	nombre        VARCHAR(24) NOT NULL;
	apellido_p    VARCHAR(24);
	apellido_m    VARCHAR(24);

	CONSTRAINT PRIMARY KEY(account_id);
);

CREATE TABLE UserLogin (
	account_id INT NOT NULL;
	passwd_hash BINARY() NOT NULL;
	passwd_salt BINARY() NOT NULL;
	CONSTRAINT PRIMARY KEY(account_id);
	CONSTRAINT FK_UserLogin_User FOREIGN KEY (account_id)
	REFERENCES UserAccount(account_id);
);


CREATE TABLE UserSession (
	session_id CHAR(44) PRIMARY KEY;
	account_id INT NOT NULL;

	CONSTRAINT FK_UserSession_UserAccount FOREIGN KEY (user_account)
	REFERENCES UserAccount(user_account_id)
	ON DELETE CASCADE;
);

