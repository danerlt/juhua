DROP DATABASE IF EXISTS `juhua`;
CREATE DATABASE `juhua`
/*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci */;

USE `juhua`;

DROP TABLE IF EXISTS `product`;
CREATE TABLE `product` (
  `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'id，主键，自增',
  `name` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '产品名',
  `link` text COLLATE utf8_unicode_ci COMMENT '产品链接',
  `shop_name` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '店铺名',
  `sales_num` int(10) unsigned DEFAULT NULL COMMENT '销售数量',
  `price` decimal(12,2) DEFAULT '0.00' COMMENT '价格',
  PRIMARY KEY (`id`),
  UNIQUE KEY (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


DROP TABLE IF EXISTS `product_info`;
CREATE TABLE `product_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键，自增',
   `name` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '产品名',
  `origin_price` decimal(12,2) DEFAULT NULL COMMENT '原价',
  `real_price` decimal(12,2) DEFAULT NULL COMMENT '实际卖价',
  `brand` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '品牌名',
  `address` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '产地,省份城市',
  `category` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '菊花茶种类',
  `weight` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '净含量',
  `quality_guarantee_period` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '保质期',
  `monthly_sales` int   DEFAULT 0 COMMENT '月销量,默认为0,只有天猫上的数据可以查看到',
  `pack_type` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '包装种类',
  `authentication` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '认证标准',
  `resource` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '来源,京东,淘宝,天猫',
  PRIMARY KEY (`id`),
  UNIQUE KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;