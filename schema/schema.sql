CREATE TABLE "shows" (
	"showid" serial NOT NULL,
	"name" varchar(255) NOT NULL UNIQUE,
	"showtype" varchar(255) NOT NULL DEFAULT 'tv',
	"showlength" integer,
	"plexname" varchar(255) DEFAULT NULL,
	CONSTRAINT "shows_pk" PRIMARY KEY ("showid")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "links" (
	"linkid" serial NOT NULL,
	"show" integer NOT NULL,
	"linktype" varchar(255) NOT NULL,
	"uri" varchar(255) NOT NULL UNIQUE,
	CONSTRAINT "links_pk" PRIMARY KEY ("linkid")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "lastshown" (
	"show" integer NOT NULL UNIQUE,
	"lastid" integer NOT NULL
) WITH (
  OIDS=FALSE
);


ALTER TABLE "links" ADD CONSTRAINT "links_fk0" FOREIGN KEY ("show") REFERENCES "shows"("showid");

ALTER TABLE "lastshown" ADD CONSTRAINT "lastshown_fk0" FOREIGN KEY ("show") REFERENCES "shows"("showid");


