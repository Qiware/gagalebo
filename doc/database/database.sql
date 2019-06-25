SET SESSION FOREIGN_KEY_CHECKS=0;

/* Drop Tables */

DROP TABLE IF EXISTS account;
/*DROP TABLE IF EXISTS video;
DROP TABLE IF EXISTS word;
DROP TABLE IF EXISTS statistic;*/


/* Create Tables */

-- 账号信息表
CREATE TABLE account
(
	id bigint unsigned NOT NULL AUTO_INCREMENT COMMENT 'id : 用户ID',
	nickname varchar(64) COMMENT '用户昵称',
	gender tinyint COMMENT '性别',
	avatar varchar(1024) COMMENT '头像URL',
	country varchar(32) COMMENT '国家',
	province varchar(512) COMMENT '省份',
	city varchar(512) COMMENT '城市',
	wx_openid varchar(64) COMMENT '微信OPEN ID',
	child_age tinyint COMMENT '孩子年龄',
	child_gender tinyint COMMENT '孩子性别',
	time_setting int COMMENT '学习时间设置',
	create_time timestamp NOT NULL COMMENT '创建时间',
	update_time timestamp DEFAULT NOW() NOT NULL COMMENT '修改时间',
	PRIMARY KEY (id),
	UNIQUE (wx_openid)
) AUTO_INCREMENT = 10000 COMMENT = '账号信息表';


-- 视频信息表
CREATE TABLE video
(
	id bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '视频ID',
	name_en varchar(512) DEFAULT '' NOT NULL COMMENT '视频名称(EN)',
	name_ch varchar(512) DEFAULT '' NOT NULL COMMENT '视频名称(CH)',
	poster varchar(1024) DEFAULT '' NOT NULL COMMENT '缩略图URL',
	duration bigint unsigned DEFAULT 0 NOT NULL COMMENT '视频时长(秒)',
	url varchar(1024) DEFAULT '' NOT NULL COMMENT '视频播放地址',
	words_script longtext NOT NULL COMMENT '字幕',
	words longtext NOT NULL COMMENT '各单词统计数(JSON格式)',
	definition varchar(16) DEFAULT '' NOT NULL COMMENT '视频清晰度',
	description varchar(1024) DEFAULT '' COMMENT '描述信息',
	PRIMARY KEY (id),
	UNIQUE (name_en),
	UNIQUE (name_ch)
) AUTO_INCREMENT = 0 COMMENT = '视频信息表';


-- 单词信息表
CREATE TABLE word
(
	id bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '单词ID',
	word varchar(64) NOT NULL COMMENT '单词',
	description varchar(1024) DEFAULT '' COMMENT '拼音/词性/例句等',
	level int DEFAULT 1 COMMENT '难度级(1,2,3,4...)',
	PRIMARY KEY (id),
	UNIQUE (word)
) AUTO_INCREMENT = 0 COMMENT = '单词信息表';


-- 统计信息表
CREATE TABLE statistic
(
	id bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '主键ID',
	uid bigint unsigned DEFAULT 0 NOT NULL COMMENT '用户ID',
	time bigint unsigned DEFAULT 0 NOT NULL COMMENT '累计学习时长',
	videos bigint unsigned DEFAULT 0 NOT NULL COMMENT '累计学习视频数',
	words bigint unsigned DEFAULT 0 NOT NULL COMMENT '累计学习单词数',
	score int unsigned DEFAULT 0 NOT NULL COMMENT '综合评分(整数)',
	PRIMARY KEY (id),
	UNIQUE (uid)
) AUTO_INCREMENT = 0 COMMENT = '统计信息表';


/* Create Foreign Keys */

ALTER TABLE statistic
	ADD FOREIGN KEY (uid)
	REFERENCES account (id)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;

/* Create Indexes */

CREATE INDEX account_id ON account (id ASC);
CREATE UNIQUE INDEX account_wx_union_id ON account (wx_union_id ASC);
