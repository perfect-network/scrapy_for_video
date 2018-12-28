-- phpMyAdmin SQL Dump
-- version phpStudy 2014
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Dec 28, 2018 at 11:47 AM
-- Server version: 5.5.53
-- PHP Version: 5.4.45

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `tv`
--

-- --------------------------------------------------------

--
-- Table structure for table `classify`
--

CREATE TABLE IF NOT EXISTS `classify` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `value` varchar(64) NOT NULL,
  `pid` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1865 ;

-- --------------------------------------------------------

--
-- Table structure for table `link`
--

CREATE TABLE IF NOT EXISTS `link` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL COMMENT '本集名字',
  `pid` int(11) NOT NULL COMMENT '视频id',
  `member` tinyint(1) NOT NULL COMMENT '是否会员',
  `site` varchar(64) NOT NULL COMMENT '所属站点',
  `link` varchar(128) NOT NULL COMMENT '视频链接',
  `episode` text NOT NULL COMMENT '视频集数',
  `image` text NOT NULL,
  `start` int(11) NOT NULL,
  `end` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=33569 ;

-- --------------------------------------------------------

--
-- Table structure for table `performer`
--

CREATE TABLE IF NOT EXISTS `performer` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pid` int(11) NOT NULL,
  `name` varchar(32) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=4363 ;

-- --------------------------------------------------------

--
-- Table structure for table `play`
--

CREATE TABLE IF NOT EXISTS `play` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `chinese` varchar(128) NOT NULL COMMENT '中文名字',
  `finish` tinyint(1) NOT NULL COMMENT '是否完结',
  `year` varchar(4) NOT NULL COMMENT '所属年份',
  `picture` varchar(256) NOT NULL COMMENT '竖屏图片',
  `picture_hor` varchar(256) NOT NULL COMMENT '横屏图片',
  `description` text NOT NULL COMMENT '视频简介',
  `director` varchar(128) NOT NULL COMMENT '参演演员',
  `current_num` int(11) NOT NULL COMMENT '当前集数',
  `total` int(11) NOT NULL COMMENT '总共集数',
  `region` varchar(32) NOT NULL COMMENT '所属区域',
  `score` double NOT NULL COMMENT '视频评分',
  `addtime` int(11) NOT NULL COMMENT '入库时间',
  `tid` int(11) NOT NULL COMMENT '分类名称',
  `site` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2413 ;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
