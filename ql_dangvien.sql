-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 18, 2023 at 06:20 AM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.0.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ql_dangvien`
--

-- --------------------------------------------------------

--
-- Table structure for table `chibo`
--

CREATE TABLE `chibo` (
  `MaChiBo` varchar(255) NOT NULL,
  `TenChiBo` varchar(255) NOT NULL,
  `NgayThanhLap` date NOT NULL,
  `TongSo` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `chibo`
--

INSERT INTO `chibo` (`MaChiBo`, `TenChiBo`, `NgayThanhLap`, `TongSo`) VALUES
('CB01', 'Chi bộ 01', '2023-09-15', 12),
('CB02', 'Chi bộ 02', '2023-09-15', 15);

-- --------------------------------------------------------

--
-- Table structure for table `chucvuchinhquyen`
--

CREATE TABLE `chucvuchinhquyen` (
  `MaChucVu` varchar(255) NOT NULL,
  `ChucVuChinhQuyen` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `chucvuchinhquyen`
--

INSERT INTO `chucvuchinhquyen` (`MaChucVu`, `ChucVuChinhQuyen`) VALUES
('CTX', 'Chủ tịch xã'),
('TCAH', 'Trưởng công an huyện');

-- --------------------------------------------------------

--
-- Table structure for table `chucvudang`
--

CREATE TABLE `chucvudang` (
  `MaChucVu` varchar(255) NOT NULL,
  `ChucVuDang` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `chucvudang`
--

INSERT INTO `chucvudang` (`MaChucVu`, `ChucVuDang`) VALUES
('PBT', 'Phó bí thư'),
('TBT', 'Tổng bí thư');

-- --------------------------------------------------------

--
-- Table structure for table `dangvien`
--

CREATE TABLE `dangvien` (
  `id` int(11) NOT NULL,
  `MaDangVien` varchar(255) NOT NULL,
  `SoTheDang` varchar(25) NOT NULL,
  `MaChiBo` varchar(255) NOT NULL,
  `HoTen` varchar(255) NOT NULL,
  `GioiTinh` varchar(25) NOT NULL,
  `MaDanToc` varchar(255) NOT NULL,
  `MaTonGiao` varchar(255) NOT NULL,
  `NgaySinh` date NOT NULL,
  `NoiSinh` varchar(255) NOT NULL,
  `QueQuan` varchar(255) NOT NULL,
  `HoKhauThuongTru` varchar(500) NOT NULL,
  `DiaChiHienTai` varchar(500) NOT NULL,
  `MaChucVuChinhQuyen` varchar(255) NOT NULL,
  `MaChucVuDang` varchar(255) NOT NULL,
  `NgayVaoDang` date NOT NULL,
  `NgayChinhThuc` date NOT NULL,
  `SoCCCD` varchar(25) NOT NULL,
  `SoDienThoai` varchar(25) NOT NULL,
  `Email` varchar(255) NOT NULL,
  `MaTrinhDoLyLuanChinhTri` varchar(255) NOT NULL,
  `MaTrinhDoChuyenMon` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `dangvien`
--

INSERT INTO `dangvien` (`id`, `MaDangVien`, `SoTheDang`, `MaChiBo`, `HoTen`, `GioiTinh`, `MaDanToc`, `MaTonGiao`, `NgaySinh`, `NoiSinh`, `QueQuan`, `HoKhauThuongTru`, `DiaChiHienTai`, `MaChucVuChinhQuyen`, `MaChucVuDang`, `NgayVaoDang`, `NgayChinhThuc`, `SoCCCD`, `SoDienThoai`, `Email`, `MaTrinhDoLyLuanChinhTri`, `MaTrinhDoChuyenMon`) VALUES
(1, 'ĐV01', '070220021111', 'CB01', 'Đào Ngọc Diễm', 'Nữ', 'KINH', 'DPhat', '1993-08-16', 'Hà Nội', 'Trần Bình, Mai Dịch, Hà Nội', 'Trần Bình, Mai Dịch, Hà Nội', '15A/Ngách 52, Phố Trần Bình, Mai Dịch, Hà Nội', 'CTX', 'PBT', '2023-09-08', '2023-09-09', '001102020205', '0999888999', 'daongocdiem@gmail.com', 'SC', 'TS');

-- --------------------------------------------------------

--
-- Table structure for table `dantoc`
--

CREATE TABLE `dantoc` (
  `MaDanToc` varchar(255) NOT NULL,
  `TenDanToc` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `dantoc`
--

INSERT INTO `dantoc` (`MaDanToc`, `TenDanToc`) VALUES
('KINH', 'Kinh'),
('MUONG', 'Mường'),
('TAY', 'Tày');

-- --------------------------------------------------------

--
-- Table structure for table `lyluanchinhtri`
--

CREATE TABLE `lyluanchinhtri` (
  `MaTrinhDo` varchar(255) NOT NULL,
  `TrinhDoChinhTri` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `lyluanchinhtri`
--

INSERT INTO `lyluanchinhtri` (`MaTrinhDo`, `TrinhDoChinhTri`) VALUES
('CC', 'Cao cấp'),
('SC', 'Sơ cấp');

-- --------------------------------------------------------

--
-- Table structure for table `taikhoan`
--

CREATE TABLE `taikhoan` (
  `MaTaiKhoan` varchar(255) NOT NULL,
  `HoTen` varchar(255) NOT NULL,
  `NgaySinh` date NOT NULL,
  `SoDienThoai` varchar(11) NOT NULL,
  `TaiKhoan` varchar(255) NOT NULL,
  `MatKhau` varchar(255) NOT NULL,
  `DiaChi` varchar(500) NOT NULL,
  `PhanQuyen` int(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `taikhoan`
--

INSERT INTO `taikhoan` (`MaTaiKhoan`, `HoTen`, `NgaySinh`, `SoDienThoai`, `TaiKhoan`, `MatKhau`, `DiaChi`, `PhanQuyen`) VALUES
('TK1', 'Admin', '2023-09-12', '0999888999', 'admin', '21232f297a57a5a743894a0e4a801fc3', 'Hà Nội', 1);

-- --------------------------------------------------------

--
-- Table structure for table `tongiao`
--

CREATE TABLE `tongiao` (
  `MaTonGiao` varchar(255) NOT NULL,
  `TenTonGiao` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `tongiao`
--

INSERT INTO `tongiao` (`MaTonGiao`, `TenTonGiao`) VALUES
('DPhat', 'Đạo phật'),
('HGiao', 'Hồi giáo'),
('KHONG', 'Không'),
('TChua', 'Thiên chúa');

-- --------------------------------------------------------

--
-- Table structure for table `trinhdo`
--

CREATE TABLE `trinhdo` (
  `MaTrinhDo` varchar(255) NOT NULL,
  `ChuyenMon` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `trinhdo`
--

INSERT INTO `trinhdo` (`MaTrinhDo`, `ChuyenMon`) VALUES
('KS', 'Kỹ sư'),
('ThS', 'Thạc sĩ'),
('TS', 'Tiến sĩ');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `chibo`
--
ALTER TABLE `chibo`
  ADD PRIMARY KEY (`MaChiBo`);

--
-- Indexes for table `chucvuchinhquyen`
--
ALTER TABLE `chucvuchinhquyen`
  ADD PRIMARY KEY (`MaChucVu`);

--
-- Indexes for table `chucvudang`
--
ALTER TABLE `chucvudang`
  ADD PRIMARY KEY (`MaChucVu`);

--
-- Indexes for table `dangvien`
--
ALTER TABLE `dangvien`
  ADD PRIMARY KEY (`id`,`MaDangVien`);

--
-- Indexes for table `dantoc`
--
ALTER TABLE `dantoc`
  ADD PRIMARY KEY (`MaDanToc`);

--
-- Indexes for table `lyluanchinhtri`
--
ALTER TABLE `lyluanchinhtri`
  ADD PRIMARY KEY (`MaTrinhDo`);

--
-- Indexes for table `taikhoan`
--
ALTER TABLE `taikhoan`
  ADD PRIMARY KEY (`MaTaiKhoan`);

--
-- Indexes for table `tongiao`
--
ALTER TABLE `tongiao`
  ADD PRIMARY KEY (`MaTonGiao`);

--
-- Indexes for table `trinhdo`
--
ALTER TABLE `trinhdo`
  ADD PRIMARY KEY (`MaTrinhDo`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `dangvien`
--
ALTER TABLE `dangvien`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
