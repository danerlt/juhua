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
  `shop_addr` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '店铺地址',
  `price` decimal(15,2) DEFAULT '0.00' COMMENT '价格',
  `sales_num` int(10) unsigned DEFAULT NULL COMMENT '销售数量',
  PRIMARY KEY (`id`),
  UNIQUE KEY (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=4420 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


DROP TABLE IF EXISTS `product_info`;
CREATE TABLE `product_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键，自增',
  `pid` int(11) UNSIGNED DEFAULT NULL COMMENT '外键，来自product的id',
  `brand` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '品牌名',
  `province` varchar(8) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '产地省份',
  `city` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '产地城市',
  `catagory` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '菊花茶种类',
  `weight` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '净含量',
  `origin_price` decimal(12,2) DEFAULT NULL COMMENT '原价',
  `real_price` decimal(12,2) DEFAULT NULL COMMENT '实际卖价',
  `quality_guarantee_period` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '保质期',
  `monthly_sales` int(10) unsigned zerofill DEFAULT NULL COMMENT '月销量',
  `authentication` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '认证标准',
  `pack_type` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '包装种类',
  `image` text COLLATE utf8_unicode_ci COMMENT '图片路径',
  `resource` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '来源',
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_product_id` FOREIGN KEY (`pid`) REFERENCES `product`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;