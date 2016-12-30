/*
 Navicat Premium Data Transfer

 Source Server         : mysql
 Source Server Type    : MySQL
 Source Server Version : 50716
 Source Host           : localhost
 Source Database       : psms

 Target Server Type    : MySQL
 Target Server Version : 50716
 File Encoding         : utf-8

 Date: 12/30/2016 18:52:51 PM
*/

SET NAMES utf8;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `advertisers`
-- ----------------------------
DROP TABLE IF EXISTS `advertisers`;
CREATE TABLE `advertisers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `token` varchar(10000) DEFAULT NULL,
  `offer_id` int(11) DEFAULT NULL,
  `type` varchar(100) DEFAULT NULL,
  `advertise_series` varchar(100) NOT NULL,
  `advertise_groups` varchar(100) NOT NULL,
  `createdTime` varchar(100) NOT NULL,
  `updateTime` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `offer_id` (`offer_id`),
  CONSTRAINT `advertisers_ibfk_1` FOREIGN KEY (`offer_id`) REFERENCES `offer` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `advertisers`
-- ----------------------------
BEGIN;
INSERT INTO `advertisers` VALUES ('1', 'EAACvVZBcdZCr8BAFSLVOFo6HN8Vh36c5rIxV0uHrpwyDdZBgUVLDfonfMbdhe0IfaL48keNApjxZBjPGvmMK69j2aw5IhNZBfJl48zdeVCwS54CdPVyZCn7g0lIUPSvkFkoOYD3LmlF50R4hwljZC58lZAyzMAIEdDp7ZAjyQEW35OUzKBNyK30xu', '1', 'facebook', '12344555', '12334555', '2016-12-30 02:04:08', '2016-12-30 02:54:21'), ('2', 'EAACvVZBcdZCr8BAFSLVOFo6HN8Vh36c5rIxV0uHrpwyDdZBgUVLDfonfMbdhe0IfaL48keNApjxZBjPGvmMK69j2aw5IhNZBfJl48zdeVCwS54CdPVyZCn7g0lIUPSvkFkoOYD3LmlF50R4hwljZC58lZAyzMAIEdDp7ZAjyQEW35OUzKBNyK30xu', '1', 'facebook', '2112', '1221', '2016-12-30 02:04:35', '2016-12-30 02:04:35'), ('3', 'EAACvVZBcdZCr8BAFSLVOFo6HN8Vh36c5rIxV0uHrpwyDdZBgUVLDfonfMbdhe0IfaL48keNApjxZBjPGvmMK69j2aw5IhNZBfJl48zdeVCwS54CdPVyZCn7g0lIUPSvkFkoOYD3LmlF50R4hwljZC58lZAyzMAIEdDp7ZAjyQEW35OUzKBNyK30xu', '1', 'facebook', '12', '12', '2016-12-30 02:16:54', '2016-12-30 02:16:54');
COMMIT;

-- ----------------------------
--  Table structure for `alembic_version`
-- ----------------------------
DROP TABLE IF EXISTS `alembic_version`;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `country`
-- ----------------------------
DROP TABLE IF EXISTS `country`;
CREATE TABLE `country` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `shorthand` varchar(100) NOT NULL,
  `british` varchar(100) NOT NULL,
  `chinese` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=248 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `country`
-- ----------------------------
BEGIN;
INSERT INTO `country` VALUES ('1', 'AD', 'Andorra', '安道尔'), ('2', 'AE', 'United Arab Emirates', '阿联酋'), ('3', 'AF', 'Afghanistan', '阿富汗'), ('4', 'AG', 'Antigua & Barbuda', '安提瓜和巴布达'), ('5', 'AI', 'Anguilla', '安圭拉'), ('6', 'AL', 'Albania', '阿尔巴尼亚'), ('7', 'AM', 'Armenia', '亚美尼亚'), ('8', 'AO', 'Angola', '安哥拉'), ('9', 'AQ', 'Antarctica', '南极洲'), ('10', 'AR', 'Argentina', '阿根廷'), ('11', 'AS', 'American Samoa', '美属萨摩亚'), ('12', 'AT', 'Austria', '奥地利'), ('13', 'AU', 'Australia', '澳大利亚'), ('14', 'AW', 'Aruba', '阿鲁巴'), ('15', 'AX', '?aland Island', '奥兰群岛'), ('16', 'AZ', 'Azerbaijan', '阿塞拜疆'), ('17', 'BA', 'Bosnia & Herzegovina', '波黑'), ('18', 'BB', 'Barbados', '巴巴多斯'), ('19', 'BD', 'Bangladesh', '孟加拉'), ('20', 'BE', 'Belgium', '比利时'), ('21', 'BF', 'Burkina', '布基纳法索'), ('22', 'BG', 'Bulgaria', '保加利亚'), ('23', 'BH', 'Bahrain', '巴林'), ('24', 'BI', 'Burundi', '布隆迪'), ('25', 'BJ', 'Benin', '贝宁'), ('26', 'BL', 'Saint Barthélemy', '圣巴泰勒米岛'), ('27', 'BM', 'Bermuda', '百慕大'), ('28', 'BN', 'Brunei', '文莱'), ('29', 'BO', 'Bolivia', '玻利维亚'), ('30', 'BQ', 'Caribbean Netherlands', '荷兰加勒比区'), ('31', 'BR', 'Brazil', '巴西'), ('32', 'BS', 'The Bahamas', '巴哈马'), ('33', 'BT', 'Bhutan', '不丹'), ('34', 'BV', 'Bouvet Island', '布韦岛'), ('35', 'BW', 'Botswana', '博茨瓦纳'), ('36', 'BY', 'Belarus', '白俄罗斯'), ('37', 'BZ', 'Belize', '伯利兹'), ('38', 'CA', 'Canada', '加拿大'), ('39', 'CC', 'Cocos (Keeling) Islands', '科科斯群岛'), ('40', 'CF', 'Central African Republic', '中非'), ('41', 'CH', 'Switzerland', '瑞士'), ('42', 'CL', 'Chile', '智利'), ('43', 'CM', 'Cameroon', '喀麦隆'), ('44', 'CO', 'Colombia', '哥伦比亚'), ('45', 'CR', 'Costa Rica', '哥斯达黎加'), ('46', 'CU', 'Cuba', '古巴'), ('47', 'CV', 'Cape Verde', '佛得角'), ('48', 'CX', 'Christmas Island', '圣诞岛'), ('49', 'CY', 'Cyprus', '塞浦路斯'), ('50', 'CZ', 'Czech Republic', '捷克'), ('51', 'DE', 'Germany', '德国'), ('52', 'DJ', 'Djibouti', '吉布提'), ('53', 'DK', 'Denmark', '丹麦'), ('54', 'DM', 'Dominica', '多米尼克'), ('55', 'DO', 'Dominican Republic', '多米尼加'), ('56', 'DZ', 'Algeria', '阿尔及利亚'), ('57', 'EC', 'Ecuador', '厄瓜多尔'), ('58', 'EE', 'Estonia', '爱沙尼亚'), ('59', 'EG', 'Egypt', '埃及'), ('60', 'EH', 'Western Sahara', '西撒哈拉'), ('61', 'ER', 'Eritrea', '厄立特里亚'), ('62', 'ES', 'Spain', '西班牙'), ('63', 'FI', 'Finland', '芬兰'), ('64', 'FJ', 'Fiji', '斐济群岛'), ('65', 'FK', 'Falkland Islands', '马尔维纳斯群岛'), ('66', 'FM', 'Federated States of Micronesia', '密克罗尼西亚联邦'), ('67', 'FO', 'Faroe Islands', '法罗群岛'), ('68', 'FR', 'France', '法国'), ('69', 'GA', 'Gabon', '加蓬'), ('70', 'GD', 'Grenada', '格林纳达'), ('71', 'GE', 'Georgia', '格鲁吉亚'), ('72', 'GF', 'French Guiana', '法属圭亚那'), ('73', 'GH', 'Ghana', '加纳'), ('74', 'GI', 'Gibraltar', '直布罗陀'), ('75', 'GL', 'Greenland', '格陵兰'), ('76', 'GN', 'Guinea', '几内亚'), ('77', 'GP', 'Guadeloupe', '瓜德罗普'), ('78', 'GQ', 'Equatorial Guinea', '赤道几内亚'), ('79', 'GR', 'Greece', '希腊'), ('80', 'GS', 'South Georgia and the South Sandwich Islands', '南乔治亚岛和南桑威奇群岛'), ('81', 'GT', 'Guatemala', '危地马拉'), ('82', 'GU', 'Guam', '关岛'), ('83', 'GW', 'Guinea-Bissau', '几内亚比绍'), ('84', 'GY', 'Guyana', '圭亚那'), ('85', 'HK', 'Hong Kong', '香港'), ('86', 'HM', 'Heard Island and McDonald Islands', '赫德岛和麦克唐纳群岛'), ('87', 'HN', 'Honduras', '洪都拉斯'), ('88', 'HR', 'Croatia', '克罗地亚'), ('89', 'HT', 'Haiti', '海地'), ('90', 'HU', 'Hungary', '匈牙利'), ('91', 'ID', 'Indonesia', '印尼'), ('92', 'IE', 'Ireland', '爱尔兰'), ('93', 'IL', 'Israel', '以色列'), ('94', 'IM', 'Isle of Man', '马恩岛'), ('95', 'IN', 'India', '印度'), ('96', 'IO', 'British Indian Ocean Territory', '英属印度洋领地'), ('97', 'IQ', 'Iraq', '伊拉克'), ('98', 'IR', 'Iran', '伊朗'), ('99', 'IS', 'Iceland', '冰岛'), ('100', 'IT', 'Italy', '意大利'), ('101', 'JE', 'Jersey', '泽西岛'), ('102', 'JM', 'Jamaica', '牙买加'), ('103', 'JO', 'Jordan', '约旦'), ('104', 'JP', 'Japan', '日本'), ('105', 'KH', 'Cambodia', '柬埔寨'), ('106', 'KI', 'Kiribati', '基里巴斯'), ('107', 'KM', 'The Comoros', '科摩罗'), ('108', 'KW', 'Kuwait', '科威特'), ('109', 'KY', 'Cayman Islands', '开曼群岛'), ('110', 'LB', 'Lebanon', '黎巴嫩'), ('111', 'LI', 'Liechtenstein', '列支敦士登'), ('112', 'LK', 'Sri Lanka', '斯里兰卡'), ('113', 'LR', 'Liberia', '利比里亚'), ('114', 'LS', 'Lesotho', '莱索托'), ('115', 'LT', 'Lithuania', '立陶宛'), ('116', 'LU', 'Luxembourg', '卢森堡'), ('117', 'LV', 'Latvia', '拉脱维亚'), ('118', 'LY', 'Libya', '利比亚'), ('119', 'MA', 'Morocco', '摩洛哥'), ('120', 'MC', 'Monaco', '摩纳哥'), ('121', 'MD', 'Moldova', '摩尔多瓦'), ('122', 'ME', 'Montenegro', '黑山'), ('123', 'MF', 'Saint Martin (France)', '法属圣马丁'), ('124', 'MG', 'Madagascar', '马达加斯加'), ('125', 'MH', 'Marshall islands', '马绍尔群岛'), ('126', 'MK', 'Republic of Macedonia (FYROM)', '马其顿'), ('127', 'ML', 'Mali', '马里'), ('128', 'MM', 'Myanmar (Burma)', '缅甸'), ('129', 'MO', 'Macao', '澳门'), ('130', 'MQ', 'Martinique', '马提尼克'), ('131', 'MR', 'Mauritania', '毛里塔尼亚'), ('132', 'MS', 'Montserrat', '蒙塞拉特岛'), ('133', 'MT', 'Malta', '马耳他'), ('134', 'MV', 'Maldives', '马尔代夫'), ('135', 'MW', 'Malawi', '马拉维'), ('136', 'MX', 'Mexico', '墨西哥'), ('137', 'MY', 'Malaysia', '马来西亚'), ('138', 'NA', 'Namibia', '纳米比亚'), ('139', 'NE', 'Niger', '尼日尔'), ('140', 'NF', 'Norfolk Island', '诺福克岛'), ('141', 'NG', 'Nigeria', '尼日利亚'), ('142', 'NI', 'Nicaragua', '尼加拉瓜'), ('143', 'NL', 'Netherlands', '荷兰'), ('144', 'NO', 'Norway', '挪威'), ('145', 'NP', 'Nepal', '尼泊尔'), ('146', 'NR', 'Nauru', '瑙鲁'), ('147', 'OM', 'Oman', '阿曼'), ('148', 'PA', 'Panama', '巴拿马'), ('149', 'PE', 'Peru', '秘鲁'), ('150', 'PF', 'French polynesia', '法属波利尼西亚'), ('151', 'PG', 'Papua New Guinea', '巴布亚新几内亚'), ('152', 'PH', 'The Philippines', '菲律宾'), ('153', 'PK', 'Pakistan', '巴基斯坦'), ('154', 'PL', 'Poland', '波兰'), ('155', 'PN', 'Pitcairn Islands', '皮特凯恩群岛'), ('156', 'PR', 'Puerto Rico', '波多黎各'), ('157', 'PS', 'Palestinian territories', '巴勒斯坦'), ('158', 'PW', 'Palau', '帕劳'), ('159', 'PY', 'Paraguay', '巴拉圭'), ('160', 'QA', 'Qatar', '卡塔尔'), ('161', 'RE', 'Réunion', '留尼汪'), ('162', 'RO', 'Romania', '罗马尼亚'), ('163', 'RS', 'Serbia', '塞尔维亚'), ('164', 'RU', 'Russian Federation', '俄罗斯'), ('165', 'RW', 'Rwanda', '卢旺达'), ('166', 'SB', 'Solomon Islands', '所罗门群岛'), ('167', 'SC', 'Seychelles', '塞舌尔'), ('168', 'SD', 'Sudan', '苏丹'), ('169', 'SE', 'Sweden', '瑞典'), ('170', 'SG', 'Singapore', '新加坡'), ('171', 'SI', 'Slovenia', '斯洛文尼亚'), ('172', 'SJ', 'Template:Country data SJM Svalbard', '斯瓦尔巴群岛和扬马延岛'), ('173', 'SK', 'Slovakia', '斯洛伐克'), ('174', 'SL', 'Sierra Leone', '塞拉利昂'), ('175', 'SM', 'San Marino', '圣马力诺'), ('176', 'SN', 'Senegal', '塞内加尔'), ('177', 'SO', 'Somalia', '索马里'), ('178', 'SR', 'Suriname', '苏里南'), ('179', 'SS', 'South Sudan', '南苏丹'), ('180', 'ST', 'Sao Tome & Principe', '圣多美和普林西比'), ('181', 'SV', 'El Salvador', '萨尔瓦多'), ('182', 'SY', 'Syria', '叙利亚'), ('183', 'SZ', 'Swaziland', '斯威士兰'), ('184', 'TC', 'Turks & Caicos Islands', '特克斯和凯科斯群岛'), ('185', 'TD', 'Chad', '乍得'), ('186', 'TG', 'Togo', '多哥'), ('187', 'TH', 'Thailand', '泰国'), ('188', 'TK', 'Tokelau', '托克劳'), ('189', 'TL', 'Timor-Leste (East Timor)', '东帝汶'), ('190', 'TN', 'Tunisia', '突尼斯'), ('191', 'TO', 'Tonga', '汤加'), ('192', 'TR', 'Turkey', '土耳其'), ('193', 'TV', 'Tuvalu', '图瓦卢'), ('194', 'TZ', 'Tanzania', '坦桑尼亚'), ('195', 'UA', 'Ukraine', '乌克兰'), ('196', 'UG', 'Uganda', '乌干达'), ('197', 'US', 'United States of America (USA)', '美国'), ('198', 'UY', 'Uruguay', '乌拉圭'), ('199', 'VA', 'Vatican City (The Holy See)', '梵蒂冈'), ('200', 'VE', 'Venezuela', '委内瑞拉'), ('201', 'VG', 'British Virgin Islands', '英属维尔京群岛'), ('202', 'VI', 'United States Virgin Islands', '美属维尔京群岛'), ('203', 'VN', 'Vietnam', '越南'), ('204', 'WF', 'Wallis and Futuna', '瓦利斯和富图纳'), ('205', 'WS', 'Samoa', '萨摩亚'), ('206', 'YE', 'Yemen', '也门'), ('207', 'YT', 'Mayotte', '马约特'), ('208', 'ZA', 'South Africa', '南非'), ('209', 'ZM', 'Zambia', '赞比亚'), ('210', 'ZW', 'Zimbabwe', '津巴布韦'), ('211', 'CN', 'China', '中国'), ('212', 'CG', 'Republic of the Congo', '刚果（布）'), ('213', 'CD', 'Democratic Republic of the Congo', '刚果（金）'), ('214', 'MZ', 'Mozambique', '莫桑比克'), ('215', 'GG', 'Guernsey', '根西岛'), ('216', 'GM', 'Gambia', '冈比亚'), ('217', 'MP', 'Northern Mariana Islands', '北马里亚纳群岛'), ('218', 'ET', 'Ethiopia', '埃塞俄比亚'), ('219', 'NC', 'New Caledonia', '新喀里多尼亚'), ('220', 'VU', 'Vanuatu', '瓦努阿图'), ('221', 'TF', 'French Southern Territories', '法属南部领地'), ('222', 'NU', 'Niue', '纽埃'), ('223', 'UM', 'United States Minor Outlying Islands', '美国本土外小岛屿'), ('224', 'CK', 'Cook Islands', '库克群岛'), ('225', 'GB', 'Great Britain (United Kingdom; England)', '英国'), ('226', 'TT', 'Trinidad & Tobago', '特立尼达和多巴哥'), ('227', 'VC', 'St. Vincent & the Grenadines', '圣文森特和格林纳丁斯'), ('228', 'TW', 'Taiwan', '中华民国（台湾）'), ('229', 'NZ', 'New Zealand', '新西兰'), ('230', 'SA', 'Saudi Arabia', '沙特阿拉伯'), ('231', 'LA', 'Laos', '老挝'), ('232', 'KP', 'North Korea', '朝鲜'), ('233', 'KR', 'South Korea', '韩国'), ('234', 'PT', 'Portugal', '葡萄牙'), ('235', 'KG', 'Kyrgyzstan', '吉尔吉斯斯坦'), ('236', 'KZ', 'Kazakhstan', '哈萨克斯坦'), ('237', 'TJ', 'Tajikistan', '塔吉克斯坦'), ('238', 'TM', 'Turkmenistan', '土库曼斯坦'), ('239', 'UZ', 'Uzbekistan', '乌兹别克斯坦'), ('240', 'KN', 'St. Kitts & Nevis', '圣基茨和尼维斯'), ('241', 'PM', 'Saint-Pierre and Miquelon', '圣皮埃尔和密克隆'), ('242', 'SH', 'St. Helena & Dependencies', '圣赫勒拿'), ('243', 'LC', 'St. Lucia', '圣卢西亚'), ('244', 'MU', 'Mauritius', '毛里求斯'), ('245', 'CI', 'C?te d\'Ivoire', '科特迪瓦'), ('246', 'KE', 'Kenya', '肯尼亚'), ('247', 'MN', 'Mongolia', '蒙古国');
COMMIT;

-- ----------------------------
--  Table structure for `customers`
-- ----------------------------
DROP TABLE IF EXISTS `customers`;
CREATE TABLE `customers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `customer_code` varchar(100) NOT NULL,
  `company_name` varchar(100) NOT NULL,
  `company_address` varchar(100) NOT NULL,
  `comment` varchar(100) NOT NULL,
  `last_datetime` datetime DEFAULT NULL,
  `status` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `customer_code` (`customer_code`),
  UNIQUE KEY `company_name` (`company_name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `customers`
-- ----------------------------
BEGIN;
INSERT INTO `customers` VALUES ('1', '26AB5B9E', '12', '1212', '1221', '2016-12-28 10:54:23', 'Created');
COMMIT;

-- ----------------------------
--  Table structure for `history`
-- ----------------------------
DROP TABLE IF EXISTS `history`;
CREATE TABLE `history` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `offer_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `type` varchar(100) DEFAULT NULL,
  `status` varchar(100) NOT NULL,
  `createdTime` varchar(100) NOT NULL,
  `country` varchar(100) NOT NULL,
  `country_price` float NOT NULL,
  `price` float DEFAULT NULL,
  `daily_budget` float DEFAULT NULL,
  `daily_type` varchar(100) DEFAULT NULL,
  `total_budget` float DEFAULT NULL,
  `total_type` varchar(100) DEFAULT NULL,
  `KPI` varchar(100) NOT NULL,
  `contract_type` varchar(100) NOT NULL,
  `contract_scale` float DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `offer_id` (`offer_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `history_ibfk_1` FOREIGN KEY (`offer_id`) REFERENCES `offer` (`id`),
  CONSTRAINT `history_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `history`
-- ----------------------------
BEGIN;
INSERT INTO `history` VALUES ('1', '1', '1', 'default', 'active', '2016-12-28 21:55:43', 'AD', '124', '102', '12', 'install', '12', 'install', '12', '服务费', '112'), ('2', '1', '1', 'default', 'active', '2016-12-28 21:55:43', 'AF', '3', '102', '12', 'install', '12', 'install', '12', '服务费', '112');
COMMIT;

-- ----------------------------
--  Table structure for `offer`
-- ----------------------------
DROP TABLE IF EXISTS `offer`;
CREATE TABLE `offer` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `customer_id` int(11) DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  `contract_type` varchar(100) DEFAULT NULL,
  `contract_num` varchar(100) NOT NULL,
  `contract_scale` float DEFAULT NULL,
  `os` varchar(100) NOT NULL,
  `package_name` varchar(100) NOT NULL,
  `app_name` varchar(100) NOT NULL,
  `app_type` varchar(100) NOT NULL,
  `preview_link` varchar(100) NOT NULL,
  `track_link` varchar(100) NOT NULL,
  `material` varchar(100) DEFAULT NULL,
  `startTime` varchar(100) NOT NULL,
  `endTime` varchar(100) NOT NULL,
  `platform` varchar(100) NOT NULL,
  `country` varchar(100) NOT NULL,
  `price` float DEFAULT NULL,
  `daily_budget` float DEFAULT NULL,
  `daily_type` varchar(100) DEFAULT NULL,
  `total_budget` float DEFAULT NULL,
  `total_type` varchar(100) DEFAULT NULL,
  `distribution` varchar(100) NOT NULL,
  `authorized` varchar(100) NOT NULL,
  `named_rule` varchar(100) NOT NULL,
  `KPI` varchar(100) NOT NULL,
  `settlement` varchar(100) NOT NULL,
  `period` varchar(100) NOT NULL,
  `remark` varchar(100) NOT NULL,
  `email_time` float NOT NULL,
  `email_users` varchar(100) NOT NULL,
  `email_tempalte` int(11) NOT NULL,
  `createdTime` varchar(100) NOT NULL,
  `updateTime` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `customer_id` (`customer_id`),
  CONSTRAINT `offer_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `offer_ibfk_2` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `offer`
-- ----------------------------
BEGIN;
INSERT INTO `offer` VALUES ('1', '1', '1', 'active', '服务费', '123456', '112', 'ios', 'com.cqaicai.com', 'qwqqw', 'qwqw', 'qwqw', 'qwqw', 'no', '2016-12-06', '2016-12-30', '[u\'Facebook\', u\'Adwords\']', '[u\'AD\', u\'AF\']', '102', '12', 'install', '12', 'install', '12', '12', '12', '12', '12', '12', '12', '1482150000', 'aa@qq.com', '1', '2016-12-28 21:55:43', '2016-12-28 21:55:43');
COMMIT;

-- ----------------------------
--  Table structure for `permissions`
-- ----------------------------
DROP TABLE IF EXISTS `permissions`;
CREATE TABLE `permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `permissions`
-- ----------------------------
BEGIN;
INSERT INTO `permissions` VALUES ('11', 'dashboard_create'), ('12', 'dashboard_delete'), ('13', 'dashboard_edit'), ('14', 'dashboard_query'), ('15', 'report_create'), ('16', 'report_delete'), ('17', 'report_edit'), ('18', 'report_query'), ('19', 'offer_create'), ('20', 'offer_delete'), ('21', 'offer_edit'), ('22', 'offer_query'), ('23', 'advertiser_create'), ('24', 'advertiser_delete'), ('25', 'advertiser_edit'), ('26', 'advertiser_query');
COMMIT;

-- ----------------------------
--  Table structure for `role`
-- ----------------------------
DROP TABLE IF EXISTS `role`;
CREATE TABLE `role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `last_datetime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `role`
-- ----------------------------
BEGIN;
INSERT INTO `role` VALUES ('1', 'PM', '2016-12-27 17:16:25'), ('2', 'BD', '2016-12-27 17:16:25'), ('3', 'AD', '2016-12-27 17:16:25'), ('4', '8888', '2016-12-27 17:31:13'), ('5', '999', '2016-12-27 17:46:05'), ('6', '000', '2016-12-27 17:52:51'), ('7', '222', '2016-12-27 17:52:51'), ('8', 'ceshi', '2016-12-28 10:48:51');
COMMIT;

-- ----------------------------
--  Table structure for `role_permissions`
-- ----------------------------
DROP TABLE IF EXISTS `role_permissions`;
CREATE TABLE `role_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `role_id` int(11) DEFAULT NULL,
  `permissions_id` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `role_permissions`
-- ----------------------------
BEGIN;
INSERT INTO `role_permissions` VALUES ('1', '1', '11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26'), ('2', '2', '16,17,18,19,20,21,22,23,24,25,26'), ('3', '3', '16,17,18,19,20,21,22,23'), ('4', '4', '17,18,16,25,26,24,13,12,21,20'), ('5', '5', '17,16,25,24,13,12,21,20'), ('6', '6', '18,15,26,23,14,11,22,19'), ('7', '7', '18,26,14,22'), ('8', '8', '17,18,16,25,26,24,13,14,12,21,22,20');
COMMIT;

-- ----------------------------
--  Table structure for `timePrice`
-- ----------------------------
DROP TABLE IF EXISTS `timePrice`;
CREATE TABLE `timePrice` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `country_id` int(11) DEFAULT NULL,
  `date` varchar(100) NOT NULL,
  `price` float NOT NULL,
  PRIMARY KEY (`id`),
  KEY `country_id` (`country_id`),
  CONSTRAINT `timeprice_ibfk_1` FOREIGN KEY (`country_id`) REFERENCES `country` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `token`
-- ----------------------------
DROP TABLE IF EXISTS `token`;
CREATE TABLE `token` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `account` varchar(100) NOT NULL,
  `accessToken` varchar(1000) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `token`
-- ----------------------------
BEGIN;
INSERT INTO `token` VALUES ('1', '3426446735@qq.com', 'EAAHgEYXO0BABAO8dhDyFvLiFnIuBpaYDYp6bcSRtkJQg5cpFy7BCJiL9xyQrRkVpheDhP4EGZCgKzBqKeGh9y0Fdd7PPZBzHnT0Q7hvyEWxTpKgJXyB3EkZBZA01OC6wx7f9NdX9popYJksnTNT2ZCpiFHX8gqIncF9vvGGEQtAZDZD');
COMMIT;

-- ----------------------------
--  Table structure for `user`
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `passwd` varchar(100) NOT NULL,
  `phone` varchar(100) NOT NULL,
  `last_datetime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `user`
-- ----------------------------
BEGIN;
INSERT INTO `user` VALUES ('1', 'admin', 'admin@newborn-town.com', 'Y2hpemljaGVuZzUyMQ==\n', '8008208820', '2016-12-30 18:51:57'), ('2', 'chen', '924632889@qq.com', 'MTIzNA==\n', '8008208820', '2016-12-27 17:22:21'), ('3', 'aaa', 'aaa@aaa.com', 'MTIzNDU2\n', '123456', '2016-12-27 18:29:08'), ('4', 'ceshi1', 'ceshi@qq.com', 'MTIzNDU2\n', '123456', '2016-12-28 10:09:46');
COMMIT;

-- ----------------------------
--  Table structure for `user_permissions`
-- ----------------------------
DROP TABLE IF EXISTS `user_permissions`;
CREATE TABLE `user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `permissions_id` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `user_permissions`
-- ----------------------------
BEGIN;
INSERT INTO `user_permissions` VALUES ('1', '1', '18,26,14,22'), ('2', '2', '11,12,13,14,15,16'), ('3', '3', '17,18,15,25,26,23,13,14,11,21,22,19'), ('4', '4', '18,26,14,22');
COMMIT;

-- ----------------------------
--  Table structure for `user_role`
-- ----------------------------
DROP TABLE IF EXISTS `user_role`;
CREATE TABLE `user_role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `role_id` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `user_role`
-- ----------------------------
BEGIN;
INSERT INTO `user_role` VALUES ('1', '1', '1,2,3,7'), ('2', '2', '1,2'), ('3', '3', '1,2,6'), ('4', '4', '7');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
