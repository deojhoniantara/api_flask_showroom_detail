-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jul 08, 2025 at 12:37 PM
-- Server version: 8.0.30
-- PHP Version: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_showroom`
--

-- --------------------------------------------------------

--
-- Table structure for table `admins`
--

CREATE TABLE `admins` (
  `id` int NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `admins`
--

INSERT INTO `admins` (`id`, `email`, `password`, `created_at`) VALUES
(1, 'admin@mail.com', '$2a$12$UonJRbmzNXz9wpY1dqTCe.rPvngI7oU3oVeUSbMHSAhnYrsldogpi', '2025-07-04 07:25:28');

-- --------------------------------------------------------

--
-- Table structure for table `articles`
--

CREATE TABLE `articles` (
  `id` int NOT NULL,
  `admin_id` int NOT NULL,
  `title` varchar(150) NOT NULL,
  `content` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `image` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `articles`
--

INSERT INTO `articles` (`id`, `admin_id`, `title`, `content`, `created_at`, `image`) VALUES
(3, 1, 'Manfaat Teknologi AI dalam Industri Otomotif', 'Teknologi kecerdasan buatan (AI) semakin banyak digunakan dalam industri otomotif untuk meningkatkan efisiensi, keselamatan, dan pengalaman pelanggan. AI diterapkan pada berbagai aspek mulai dari produksi hingga pengalaman pengguna di dalam kendaraan.\r\n\r\nSalah satu pemanfaatan AI yang signifikan adalah pada sistem kendaraan otonom. Dengan bantuan sensor, kamera, dan algoritma pembelajaran mesin, mobil mampu menginterpretasi lingkungan sekitar, mengenali rambu lalu lintas, dan mengambil keputusan secara otomatis. Hal ini tidak hanya membantu mengurangi kecelakaan, tetapi juga memudahkan mobilitas masyarakat.\r\n\r\nDi lini produksi, AI digunakan untuk mengotomatiskan proses perakitan, mengidentifikasi cacat produksi secara real-time, dan merencanakan rantai pasok dengan lebih akurat. Sementara itu, pada sisi pelanggan, AI membantu menciptakan pengalaman yang lebih personal melalui sistem infotainment pintar, navigasi berbasis prediksi, hingga layanan pelanggan otomatis.\r\n\r\nDengan terus berkembangnya teknologi, AI diharapkan semakin memperkuat inovasi di sektor otomotif dan membawa transformasi besar dalam cara manusia berkendara dan berinteraksi dengan kendaraan.', '2025-07-07 22:33:41', 'static/uploads/1751898821.670335_download_6.jpeg'),
(4, 1, 'Tren Mobil Listrik di Indonesia: Peluang dan Tantangan', 'Dalam beberapa tahun terakhir, tren mobil listrik (electric vehicle/EV) mulai menunjukkan peningkatan signifikan di Indonesia. Pemerintah Indonesia menunjukkan komitmen kuat untuk mendorong penggunaan kendaraan ramah lingkungan, salah satunya dengan memberikan berbagai insentif, seperti bebas pajak kendaraan, pembebasan bea masuk, hingga subsidi untuk pembelian mobil listrik tertentu.\r\n\r\nBeberapa pabrikan besar seperti Hyundai, Wuling, dan Toyota sudah merilis model mobil listrik yang cukup diminati masyarakat. Wuling Air EV misalnya, menjadi salah satu mobil listrik paling populer karena harganya yang relatif terjangkau dan cocok untuk kebutuhan perkotaan.\r\n\r\nNamun, tantangan besar masih mengadang. Salah satunya adalah infrastruktur pengisian daya yang belum merata. Di kota besar seperti Jakarta dan Surabaya, SPKLU (Stasiun Pengisian Kendaraan Listrik Umum) sudah mulai tersedia, tetapi di luar Pulau Jawa, fasilitas ini masih minim. Selain itu, harga mobil listrik secara umum masih lebih tinggi dibanding mobil konvensional, meskipun biaya operasionalnya lebih rendah.\r\n\r\nTantangan lainnya termasuk kesadaran masyarakat yang masih rendah, serta isu seputar daya tahan baterai dan limbahnya. Meski begitu, dengan regulasi yang mendukung dan adopsi teknologi yang semakin cepat, masa depan mobil listrik di Indonesia terlihat cerah.', '2025-07-07 22:38:46', 'static/uploads/1751899126.793609_download_7.jpeg'),
(5, 1, 'Perbedaan Mobil MPV, SUV, dan Sedan: Mana yang Cocok untuk Anda?', 'Memilih jenis mobil bukan hanya soal tampilan, tapi juga soal fungsi dan kebutuhan. Di Indonesia, tiga jenis mobil yang paling populer adalah MPV, SUV, dan Sedan. Masing-masing memiliki karakteristik yang berbeda, baik dari segi bentuk, fitur, hingga kenyamanan.\r\n\r\nMPV (Multi Purpose Vehicle) adalah pilihan ideal bagi keluarga. Mobil jenis ini dirancang untuk mengangkut banyak penumpang dengan nyaman, biasanya memiliki 7 kursi atau lebih. Kabin luas, konfigurasi tempat duduk fleksibel, dan fitur kenyamanan menjadikan MPV sangat cocok untuk perjalanan keluarga, baik jarak dekat maupun jauh. Contoh populer: Toyota Avanza, Mitsubishi Xpander.\r\n\r\nSUV (Sport Utility Vehicle) cocok bagi mereka yang senang bertualang. Didesain dengan ground clearance tinggi dan sistem penggerak empat roda (pada beberapa model), SUV mampu melewati medan sulit seperti jalan berbatu, berbukit, atau banjir ringan. SUV juga menawarkan ruang bagasi yang besar dan tampilan yang gagah. Contoh: Toyota Fortuner, Honda CR-V.\r\n\r\nSedan adalah pilihan klasik bagi pengguna perkotaan. Mobil jenis ini memiliki desain aerodinamis dan kenyamanan tinggi untuk penggunaan harian di jalan raya. Dengan handling yang baik dan konsumsi bahan bakar efisien, sedan cocok untuk eksekutif muda atau keluarga kecil. Contoh: Honda City, Toyota Vios.\r\n\r\nMemilih mobil yang tepat sangat tergantung pada gaya hidup, jumlah anggota keluarga, dan jenis medan yang sering dilalui.', '2025-07-07 22:39:54', 'static/uploads/1751899194.206747_download_8.jpeg'),
(6, 1, 'Cara Merawat Mobil agar Tetap Prima', 'Memiliki mobil bukan hanya tentang mengendarainya, tapi juga tentang merawatnya dengan baik. Perawatan rutin adalah kunci agar mobil tetap prima, aman dikendarai, dan memiliki usia pakai yang panjang. Sayangnya, banyak pemilik kendaraan yang menyepelekan hal ini dan hanya membawa mobil ke bengkel saat sudah mengalami kerusakan.\r\n\r\nBerikut beberapa langkah penting dalam merawat mobil:\r\n\r\nGanti Oli Secara Berkala\r\nOli mesin memiliki peran penting dalam melumasi dan mendinginkan mesin. Ganti oli sesuai rekomendasi, biasanya setiap 5.000–10.000 km tergantung jenis oli dan kondisi pemakaian.\r\n\r\nCek dan Rawat Sistem Rem\r\nRem adalah sistem keselamatan utama. Periksa kampas rem, minyak rem, dan cakram secara berkala agar selalu dalam kondisi optimal.\r\n\r\nPerhatikan Ban\r\nCek tekanan angin secara rutin. Tekanan ban yang tidak sesuai bisa mengurangi efisiensi bahan bakar dan meningkatkan risiko pecah ban. Periksa juga keausan tapak ban.\r\n\r\nService Berkala di Bengkel Resmi\r\nService berkala akan memeriksa seluruh sistem mobil, termasuk aki, AC, filter udara, dan suspensi. Gunakan bengkel resmi agar mendapat suku cadang asli dan teknisi terlatih.\r\n\r\nJaga Kebersihan Mobil\r\nMencuci mobil secara rutin tidak hanya membuatnya terlihat bersih, tapi juga mencegah karat, jamur pada kaca, dan kerusakan cat.\r\n\r\nDengarkan Suara-Suara Aneh\r\nSuara mencurigakan dari mesin, kaki-kaki, atau rem bisa jadi pertanda kerusakan awal. Jangan abaikan, segera periksakan.\r\n\r\nPerawatan yang baik akan membuat mobil lebih awet, nyaman digunakan, dan memiliki nilai jual kembali yang lebih tinggi.', '2025-07-07 22:43:49', 'static/uploads/1751899429.344383_images_1.jpeg'),
(7, 1, 'Modifikasi Mobil: Gaya atau Fungsi?', 'Modifikasi mobil telah menjadi bagian dari gaya hidup banyak penggemar otomotif. Beberapa melakukannya demi tampilan yang lebih keren, yang lain untuk meningkatkan performa atau kenyamanan. Apapun alasannya, modifikasi harus dilakukan dengan bijak dan tetap memperhatikan aspek keselamatan serta legalitas.\r\n\r\nJenis-jenis modifikasi umum yang populer antara lain:\r\n\r\nEksterior\r\nMulai dari mengganti velg, menambahkan body kit, hingga mengganti warna mobil dengan stiker atau cat khusus. Tujuannya biasanya untuk estetika.\r\n\r\nInterior\r\nModifikasi interior bisa meliputi penggantian jok, sistem audio, lampu ambient, hingga perangkat hiburan seperti monitor tambahan. Cocok untuk Anda yang ingin kenyamanan ekstra.\r\n\r\nMesin dan Performa\r\nModifikasi ini mencakup penggantian sistem intake, knalpot racing, turbocharger, atau rem performa tinggi. Namun, jenis modifikasi ini harus dilakukan oleh bengkel yang benar-benar berpengalaman karena menyangkut keselamatan.\r\n\r\nSuspensi dan Handling\r\nMengganti suspensi bisa memperbaiki kenyamanan atau menambah kesan sporty. Misalnya, lowering kit untuk tampilan lebih rendah atau suspensi udara yang bisa disetel.\r\n\r\nNamun perlu diingat: modifikasi ekstrem dapat membatalkan garansi, menyalahi aturan lalu lintas, atau bahkan membuat mobil tidak layak jalan. Beberapa modifikasi seperti lampu strobo, knalpot bising, atau ban terlalu besar juga bisa dikenai tilang.\r\n\r\nLakukan modifikasi dengan tujuan yang jelas dan sesuai dengan aturan hukum yang berlaku.', '2025-07-07 22:45:11', 'static/uploads/1751899511.897403_download_9.jpeg'),
(8, 1, 'Tips Membeli Mobil Bekas agar Tidak Tertipu', 'Membeli mobil bekas bisa menjadi solusi cerdas bagi Anda yang ingin memiliki kendaraan pribadi dengan budget terbatas. Namun, membeli mobil bekas juga memiliki risiko jika tidak dilakukan dengan hati-hati. Banyak kasus pembeli tertipu karena tergiur harga murah tanpa memeriksa kondisi mobil secara menyeluruh.\r\n\r\nBerikut adalah tips penting dalam membeli mobil bekas:\r\n\r\nBeli dari Sumber Terpercaya\r\nUsahakan membeli dari showroom resmi, dealer terpercaya, atau langsung dari pemilik asli. Hindari calo atau penjual tanpa identitas jelas.\r\n\r\nCek Riwayat Kendaraan\r\nMintalah bukti servis berkala, nota perbaikan, dan riwayat kepemilikan. Mobil yang dirawat rutin biasanya masih dalam kondisi baik.\r\n\r\nCek Fisik dan Mesin Mobil\r\nPeriksa bodi mobil dari goresan, bekas tabrakan, atau tanda-tanda pernah terkena banjir. Buka kap mesin, dengarkan suara mesin, dan periksa kebocoran oli.\r\n\r\nPeriksa Kelengkapan Dokumen\r\nPastikan STNK, BPKB, dan faktur pembelian lengkap dan asli. Hindari mobil yang surat-suratnya tidak jelas.\r\n\r\nLakukan Test Drive\r\nTest drive penting untuk merasakan kenyamanan, kinerja mesin, transmisi, dan sistem rem.\r\n\r\nGunakan Jasa Inspeksi Profesional\r\nJika Anda tidak paham mobil, sebaiknya gunakan layanan inspeksi mobil bekas agar bisa mendapat laporan objektif.\r\n\r\nDengan langkah-langkah di atas, Anda bisa menghindari risiko dan mendapatkan mobil bekas berkualitas.', '2025-07-07 22:46:03', 'static/uploads/1751899563.389769_download_10.jpeg'),
(9, 1, 'Kenapa Mobil Diesel Masih Jadi Pilihan Banyak Orang?', 'Di tengah gempuran tren mobil listrik dan hybrid, mobil bermesin diesel tetap punya tempat tersendiri di hati konsumen Indonesia, terutama mereka yang mencari efisiensi dan daya tahan dalam penggunaan jangka panjang. Mobil diesel terkenal dengan torsi besar di putaran rendah, yang membuatnya sangat andal untuk perjalanan jauh, kendaraan pengangkut, atau medan menantang seperti daerah pegunungan. Selain itu, konsumsi bahan bakar solar yang lebih irit dalam kondisi beban berat menjadikan mobil diesel sangat ekonomis, terutama bagi pelaku usaha atau pengguna kendaraan niaga. Banyak produsen juga telah menyematkan teknologi modern seperti turbo intercooler, common-rail, dan sistem injeksi elektronik yang membuat performa mesin diesel semakin halus, bertenaga, dan efisien. Meski begitu, tantangan terbesar mobil diesel saat ini adalah regulasi emisi yang makin ketat, terutama di kota-kota besar, karena emisinya mengandung partikulat halus dan nitrogen oksida (NOx) yang cukup tinggi. Namun dengan perawatan yang tepat dan penggunaan filter DPF serta urea (AdBlue), emisi ini bisa ditekan hingga setara mobil bensin. Untuk Anda yang mencari mobil tangguh, irit, dan mampu mengangkut beban besar dengan mudah, mobil diesel tetap menjadi pilihan rasional—dan sangat layak dipertimbangkan, bahkan di era elektrifikasi ini.', '2025-07-07 22:58:51', 'static/uploads/1751900331.59177_download_11.jpeg'),
(10, 1, 'Transmisi Manual vs Otomatis: Pilih yang Mana untuk Kebutuhan Harian?', 'Memilih antara transmisi manual dan otomatis bukan hanya soal kenyamanan, tapi juga menyangkut efisiensi bahan bakar, kendali berkendara, serta biaya jangka panjang. Transmisi manual menawarkan kontrol penuh terhadap perpindahan gigi, yang membuat pengemudi bisa menyesuaikan putaran mesin dengan kondisi jalan untuk efisiensi maksimal. Mobil manual juga cenderung lebih murah dari sisi harga awal, konsumsi bahan bakar, dan biaya perawatan karena sistemnya lebih sederhana dan tidak bergantung pada sensor elektronik kompleks. Di sisi lain, transmisi otomatis menjadi primadona di kota-kota besar karena sangat memudahkan saat menghadapi kemacetan panjang. Anda tak perlu sering menginjak kopling, cukup mainkan pedal gas dan rem. Teknologi transmisi otomatis pun semakin berkembang, dari torque converter konvensional, CVT, hingga dual-clutch transmission (DCT) yang memberikan perpindahan gigi super mulus dan responsif. Masing-masing punya keunggulan: manual cocok untuk mereka yang suka kontrol penuh dan irit bahan bakar, sementara otomatis cocok untuk kenyamanan dan kemudahan berkendara harian. Pada akhirnya, pilihan tergantung pada gaya hidup dan preferensi. Jika Anda banyak berkendara di dalam kota, otomatis bisa jadi pilihan ideal. Tapi kalau Anda senang merasakan sensasi berkendara yang lebih ‘aktif’ dan hemat bahan bakar, manual tetap tak tergantikan.', '2025-07-07 23:09:59', 'static/uploads/1751900999.472033_download_13.jpeg'),
(11, 1, 'Mengenal Teknologi ADAS pada Mobil Modern: Canggih, Aman, dan Nyaman', 'Teknologi ADAS (Advanced Driver Assistance System) adalah salah satu revolusi paling signifikan dalam dunia otomotif modern, yang dirancang untuk meningkatkan keselamatan berkendara sekaligus mengurangi beban kerja pengemudi. Sistem ini mencakup beragam fitur seperti lane departure warning (peringatan saat keluar jalur), lane keeping assist (mengoreksi setir secara otomatis), adaptive cruise control (menjaga jarak dan kecepatan dengan kendaraan di depan), blind spot monitoring (deteksi kendaraan di area tak terlihat spion), hingga automatic emergency braking (rem darurat otomatis saat mendeteksi potensi tabrakan). Bahkan beberapa mobil telah dilengkapi fitur parking assist hingga semi-autonomous driving. Dengan ADAS, pengemudi bisa lebih tenang saat berkendara jauh atau dalam kondisi lalu lintas padat karena sistem membantu mengoreksi kesalahan kecil yang sering terjadi. Fitur ini sangat berguna bagi pengemudi pemula atau lansia, dan secara umum membantu menurunkan angka kecelakaan di jalan raya. Namun, penting untuk diingat bahwa ADAS hanya asisten, bukan pengganti pengemudi. Tetap dibutuhkan kewaspadaan penuh saat berkendara. Kini, banyak pabrikan menyematkan ADAS bahkan pada mobil di bawah Rp400 jutaan, membuat teknologi ini makin terjangkau. Investasi pada mobil dengan ADAS adalah bentuk nyata kepedulian pada keselamatan Anda dan keluarga.', '2025-07-07 23:11:08', 'static/uploads/1751901068.713821_download_14.jpeg'),
(12, 1, 'Judul: Tips Praktis Hemat BBM untuk Mobil Harian Tanpa Ribet', 'Menghemat bahan bakar bukan hanya bergantung pada jenis mobil yang digunakan, tapi juga pada kebiasaan dan gaya mengemudi yang Anda terapkan setiap hari. Banyak pengemudi tidak menyadari bahwa cara mereka mengemudi sangat memengaruhi konsumsi bahan bakar. Salah satu tips paling efektif adalah menjaga akselerasi dan deselerasi tetap halus—hindari menekan pedal gas atau rem secara mendadak karena ini membuang energi secara tidak efisien. Selain itu, perhatikan kecepatan ideal saat berkendara. Untuk mobil bensin, kecepatan konstan antara 60–80 km/jam umumnya merupakan titik optimal efisiensi BBM. Tekanan ban juga sangat berpengaruh—ban yang kurang angin menciptakan hambatan gulir lebih tinggi sehingga mobil butuh tenaga lebih besar untuk bergerak. Jangan lupa servis rutin seperti mengganti filter udara, oli, dan mengecek sistem injeksi. Menjaga muatan mobil tetap ringan dan menghindari penggunaan AC secara berlebihan juga bisa menurunkan konsumsi BBM. Bila memungkinkan, manfaatkan aplikasi navigasi yang memberi info lalu lintas real-time agar Anda terhindar dari kemacetan panjang yang boros bahan bakar. Dengan sedikit perubahan gaya hidup dan pemeliharaan berkala, Anda bisa menghemat cukup banyak pengeluaran BBM tanpa harus beralih ke mobil baru.', '2025-07-07 23:19:04', 'static/uploads/1751901544.024094_download_15.jpeg'),
(13, 1, 'Panduan Memilih Mobil Keluarga Ideal: Nyaman, Aman, dan Serbaguna', 'Memilih mobil keluarga bukan sekadar soal harga atau jumlah kursi, melainkan soal bagaimana kendaraan tersebut bisa mengakomodasi kebutuhan seluruh anggota keluarga secara optimal. Mobil keluarga ideal seharusnya menawarkan ruang kabin lega, kapasitas bagasi yang fleksibel, kenyamanan berkendara dalam jangka panjang, dan fitur keselamatan lengkap. Mobil jenis MPV seperti Toyota Avanza, Mitsubishi Xpander, atau SUV seperti Hyundai Creta dan Honda BR-V menjadi pilihan favorit karena mampu menampung 7 penumpang dengan ruang kaki dan kepala yang cukup nyaman. Fitur ISOFIX untuk pemasangan car seat bayi, airbag ganda atau lebih, serta teknologi pengereman ABS dan kontrol traksi menjadi syarat penting untuk mobil keluarga modern. Tak kalah penting adalah kenyamanan selama perjalanan—AC double blower, port charger di baris belakang, dan sistem hiburan bisa membuat anak-anak lebih betah selama perjalanan jauh. Pilih mobil yang efisien bahan bakar agar perjalanan tidak membebani pengeluaran harian, dan pastikan jaringan servisnya luas agar tidak menyulitkan perawatan. Jika Anda sering bepergian jauh, pertimbangkan fitur cruise control dan suspensi empuk. Mobil keluarga bukan sekadar alat transportasi, tapi juga ruang aman dan nyaman untuk membangun momen kebersamaan bersama orang-orang tercinta.', '2025-07-07 23:19:55', 'static/uploads/1751901595.887524_download_16.jpeg');

-- --------------------------------------------------------

--
-- Table structure for table `article_comments`
--

CREATE TABLE `article_comments` (
  `id` int NOT NULL,
  `article_id` int NOT NULL,
  `user_id` int NOT NULL,
  `comment` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `bookings`
--

CREATE TABLE `bookings` (
  `id` int NOT NULL,
  `user_id` int NOT NULL,
  `car_id` int NOT NULL,
  `message` text,
  `booking_date` date DEFAULT NULL,
  `booking_time` time DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL,
  `status` enum('pending','approved','rejected') DEFAULT 'pending',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `cars`
--

CREATE TABLE `cars` (
  `id` int NOT NULL,
  `user_id` int NOT NULL,
  `name` varchar(100) NOT NULL,
  `brand` varchar(50) DEFAULT NULL,
  `transmission` varchar(20) DEFAULT NULL,
  `seats` int DEFAULT NULL,
  `year` year DEFAULT NULL,
  `color` varchar(30) DEFAULT NULL,
  `location` varchar(100) DEFAULT NULL,
  `fuel_type` varchar(20) DEFAULT NULL,
  `mileage` int DEFAULT NULL,
  `price` decimal(15,2) DEFAULT NULL,
  `description` text,
  `image` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `image_2` varchar(255) DEFAULT NULL,
  `image_3` varchar(255) DEFAULT NULL,
  `image_4` varchar(255) DEFAULT NULL,
  `image_5` varchar(255) DEFAULT NULL,
  `status` enum('tersedia','terjual') DEFAULT 'tersedia'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `cars`
--

INSERT INTO `cars` (`id`, `user_id`, `name`, `brand`, `transmission`, `seats`, `year`, `color`, `location`, `fuel_type`, `mileage`, `price`, `description`, `image`, `created_at`, `image_2`, `image_3`, `image_4`, `image_5`, `status`) VALUES
(1, 2, 'Avanza', 'Toyota', 'Manual', 5, 2021, 'Putih', 'Singaraja', 'Pertamax', 75000, '197000000.00', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum', 'static/uploads/1751702396_download.jpeg', '2025-07-04 07:35:50', 'static/uploads/1751702396_download_1.jpeg', 'static/uploads/1751702396_download_2.jpeg', 'static/uploads/1751702396_download_3.jpeg', 'static/uploads/1751702396_download_4.jpeg', 'tersedia'),
(8, 2, 'Jazz', 'Honda', 'Manual', 5, 2020, 'Putih', 'Dewi Sartika', 'Bensin', 85400, '200156000.00', '', 'static/uploads/1751959692_Evoluzione_di_stile_Scopri_la_nuova_honda_jazz_da_Sinauto_Per_info_contattaci_al_n030_2120132.jpeg', '2025-07-08 07:28:12', 'static/uploads/1751959692_Fit_15.jpeg', 'static/uploads/1751959692_FaiyzMohamed_8880_on_Instagram__accelera651sport_accelera651_sporttires_gtrwheels_gtrsuperdeepconcave_deepconcave_concavewheels_205_50_16_9_25jwheels....jpeg', 'static/uploads/1751959692_Back.jpeg', 'static/uploads/1751959692_White_Honda_Jazz_on_MUGEN_full_body_kit_-_ModifiedX.jpeg', 'tersedia'),
(9, 2, 'APV', 'Suzuki', 'Manual', 7, 2022, 'Hitam', 'Banyuasri', 'Bensin', 52300, '165200000.00', '', 'static/uploads/1751959839_Color_gris.jpeg', '2025-07-08 07:30:39', 'static/uploads/1751959839_0917e02a10ee68c0bbd7de094345fc64.jpg', 'static/uploads/1751959839_Jual_Suzuki_APV_bekas_-_Cari_mobil_bekas_murah___Cintamobil.jpeg', 'static/uploads/1751959839_Suzuki_APV.jpeg', 'static/uploads/1751959839_download_5.jpeg', 'terjual'),
(10, 5, 'Jazz', 'Honda', 'Manual', 5, 2023, 'Putih', 'Singaraja', 'Bensin', 58430, '203650000.00', '', 'static/uploads/1751961800_Back.jpeg', '2025-07-08 08:03:20', 'static/uploads/1751961800_White_Honda_Jazz_on_MUGEN_full_body_kit_-_ModifiedX.jpeg', 'static/uploads/1751961800_Evoluzione_di_stile_Scopri_la_nuova_honda_jazz_da_Sinauto_Per_info_contattaci_al_n030_2120132.jpeg', 'static/uploads/1751961800_FaiyzMohamed_8880_on_Instagram__accelera651sport_accelera651_sporttires_gtrwheels_gtrsuperdeepconcave_deepconcave_concavewheels_205_50_16_9_25jwheels....jpeg', 'static/uploads/1751961800_Fit_15.jpeg', 'tersedia'),
(11, 5, 'Avanza', 'Toyota', 'Manual', 7, 2024, 'Putih', 'Banjar Tegal', 'Bensin', 59640, '186543000.00', '', 'static/uploads/1751961893_download.jpeg', '2025-07-08 08:04:53', 'static/uploads/1751961893_images.jpeg', 'static/uploads/1751961893_download_2.jpeg', 'static/uploads/1751961893_download_4.jpeg', 'static/uploads/1751961893_download_3.jpeg', 'tersedia');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `password`, `phone`, `address`, `created_at`) VALUES
(2, 'Ucups', 'ucup@mail.com', '$2b$12$AfIsKG7GDK/9TIixAkxxgu/HjTYlC6d7ufZXUZV1/PC5O6c7n6D7a', '1234567890', 'test', '2025-07-04 07:17:23'),
(5, 'Aseps', 'asep@mail.com', '$2b$12$d70sm.hgX6q/wP9gXHo3be4m6Y5VvL61uq306CWW6OaWvnniJ0aCG', '39525486', 'Banyuning', '2025-07-08 07:45:05'),
(6, 'Adit', 'adit@mail.com', '$2b$12$9KzTJvuj2.DwftvlroFQB.nZjdib3r0/Kgwbf71R5a3TVaLqe/EMO', '89745621', 'test', '2025-07-08 07:46:22'),
(8, 'Anton', 'anton@mail.com', '$2b$12$sFTlYk4T/EwGof4Z78PHZurqo68uN7c11pghj9Aey9biJvVm/8kS6', '4569741', 'test', '2025-07-08 08:00:33');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admins`
--
ALTER TABLE `admins`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `articles`
--
ALTER TABLE `articles`
  ADD PRIMARY KEY (`id`),
  ADD KEY `admin_id` (`admin_id`);

--
-- Indexes for table `article_comments`
--
ALTER TABLE `article_comments`
  ADD PRIMARY KEY (`id`),
  ADD KEY `article_id` (`article_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `bookings`
--
ALTER TABLE `bookings`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `car_id` (`car_id`);

--
-- Indexes for table `cars`
--
ALTER TABLE `cars`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admins`
--
ALTER TABLE `admins`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `articles`
--
ALTER TABLE `articles`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `article_comments`
--
ALTER TABLE `article_comments`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `bookings`
--
ALTER TABLE `bookings`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `cars`
--
ALTER TABLE `cars`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `articles`
--
ALTER TABLE `articles`
  ADD CONSTRAINT `articles_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `admins` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `article_comments`
--
ALTER TABLE `article_comments`
  ADD CONSTRAINT `article_comments_ibfk_1` FOREIGN KEY (`article_id`) REFERENCES `articles` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `article_comments_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `bookings`
--
ALTER TABLE `bookings`
  ADD CONSTRAINT `bookings_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `bookings_ibfk_2` FOREIGN KEY (`car_id`) REFERENCES `cars` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `cars`
--
ALTER TABLE `cars`
  ADD CONSTRAINT `cars_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
