INSERT INTO person (id_person,tx_first_name,tx_last_name_a,tx_last_name_b,tx_street,tx_city,tx_state,tx_zipcode,tx_telephone) VALUES
	 (2,'Miguel','Martinez','Rosas','3419 Terra Cotta Street','Campbell','Minnesota','29201','320-247-8904'),
	 (3,'Rodrigo','Perez','Palerma','2293 Burwell Heights Road','Beaumont','Texas','77701','409-351-8385'),
	 (4,'Luis','Banana','Suarez','3932 Northwest Boulevard','Union City','New Jersey','07087','201-277-5345'),
	 (5,'Tania','Gonzalez','Suarez','971 Frum Street','Nashville','Tennessee','37203','615-598-5684'),
	 (8,'UPDATE Name','Last Name','Second','UPDATE Street','City','State','Zip','Telephone'),
	 (1,'John','Doe','Ramirez','1014 Honeysuckle Lane','Redmond','Washington','98052','970-220-8436');
INSERT INTO users (id_user,tx_login,tx_password) VALUES
	 (2,'mmr@gmail.com','prueba123'),
	 (3,'palerma@gmail.com','prueba123'),
	 (4,'banana@gmail.com','prueba123'),
	 (5,'taglz@gmail.com','prueba123'),
	 (8,'email@gmail.com','prueba'),
	 (1,'johndoe@gmail.com','prueba123');
INSERT INTO access (id_access,nu_attempt,fh_failed,fh_lock) VALUES
	 (1,0,NULL,NULL),
	 (2,0,NULL,NULL),
	 (3,0,NULL,NULL),
	 (4,0,NULL,NULL),
	 (5,0,NULL,NULL),
	 (8,0,NULL,NULL);
INSERT INTO product (id_product,tx_name,tx_description,ft_price,nu_stock,ft_discount) VALUES
	 (1,'PlayStation 4 Slim','Incluye una consola PlayStation 4 Slim de 1 TB, un control inalámbrico DUALSHOCK 4, discos de Blu-ray de God of War, Horizon Zero Dawn Complete Edition, Shadow of the Colossus, y un cupón para PS Plus (suscripción de 3 meses).',6699.0,5,0.0),
	 (2,'Xbox One S','El paquete incluye: Consola Xbox One, descarga completa del juego Battlefield V Deluxe Edition, 1 mes de prueba de Xbox Game Pass con acceso a más de 100 juegos, y 14 días de prueba de Xbox Live Gold',5999.0,5,0.0),
	 (4,'HP Laptop 15-DA0001LA','Intel Celeron N4000, Ram 4 GB, Disco Duro 500GB, Windows 10 Home, 15.6", Sin Unidad Óptica. Garantía de 1 año.',5478.99,5,0.0),
	 (5,'Huawei Mate 20 Lite','64GB Libre de Fabrica 4G LTE SNE-LX3. SNE-LX3 Libre de Fabrica, Android 8.1 Oreo + EMUI 8.',5128.0,5,26.3),
	 (6,'Kingston Digital 32GB 100 G3 USB 3.0','DataTraveler (DT100G3/32GB). En acuerdo con las especificaciones de USB 3.0 Compatiblidad dual Conectividad USB 3.0 Retro compatibilidad con USB 2.0 Diseño elegante de negro sobre negro y tapa deslizable Dispositivo inicial de almacenaje USB 3.0.',119.95,5,20.31),
	 (7,'Nikon D7200 DX-format DSLR Body','La primera DSLR de Nikon con funciones integradas de Wi-Fi y Comunicación de Campo Cercano (NFC). Colof negro.',17118.98,5,50.0),
	 (8,'Kingston Digital 240GB Solid State Drive','SSDNow UV400 SATA 3 2.5" SUV400S37/240G. Storage Capacity: 240GB SSD. Form Factor: 2.5-inch. Interface: SATA Rev. 3.0 (6Gb/S), with backwards compatibility to SATA Rev. 2.0 (3Gb/S).',1814.27,5,33.33),
	 (9,'Appetite for Destruction (2LP)','Primer álbum Remaster de cintas analógicas originales Álbum original ampliado a 2 LP para reproducción de audio Corte de vinilo de 192 kHz 24 bits Remastered Audio de alta resolución Edición limitada Foil Art Slipcase Side 4 Bono extra: Holograma Hologroove de GNR Descargar etiqueta engomada de la tarjeta Álbum digital de 44 bits de 44.1kHz',631.01,5,40.2),
	 (10,'Marvel Guante Electrónico Avengers Infinity War','El Guante electrónico de Thanos, ¡que incluye luces y sonidos! ¡Presiona el botón central en el puño para iluminar la piedra central y activar el poderoso sonido! Este Guante del Infinito está inspirado en la película Avengers: Infinity War y está diseñado para adaptarse a la mayoría de los tamaños de mano.',226.82,5,50.3),
	 (12,'Funko, Figura Coleccionable Thanos','Funko Pop Vinyl Thanos. 5 pulgadas de alto. Figura coleccionable cabeza de Globo. Avengers Infinity War, Multicolor.',249.0,5,0.0),
	 (11,'Wicked Audio Endo Supraaural Audífonos','Los auriculares inalámbricos Bluetooth de Wicked Audio Endo están diseñados para ofrecer música rock para alimentar tu adrenalina y mantenerte en movimiento.',1682.28,5,10.3),
	 (3,'Eco Dot Bocina con Alexa','Echo Dot es una bocina inteligente que se controla con la voz. Se conecta a través de Wi-Fi a Alexa, un servicio de voz basado en la nube. Alexa puede reproducir música, responder a preguntas, narrar las noticias, consultar el pronóstico del clima, configurar alarmas, controlar dispositivos de Casa Inteligente compatibles y mucho más.',699.0,5,30.2);
INSERT INTO questions (id_question,question,answer,answer_date,id_product,id_user) VALUES
	 (1,'Viene en espaniol??','Si, es producto mexicano','2023-03-13 00:00:00',3,1),
	 (2,'Utiliza cargador o bateria?','Usa cargador, viene incluido.','2023-03-20 00:00:00',3,1),
	 (5,'testing','respuestaaaaaaaaaaaaaaaa','2023-03-21 23:52:08',3,1),
	 (6,'otra pregunta massssssssssssssssss','otra respuestaaaa','2023-03-21 23:52:19',3,1),
	 (7,'otra preguntitaaa',NULL,NULL,3,2);
INSERT INTO reviews (id_review,creation_date,country,stars,description,attachment,id_product,id_user) VALUES
	 (3,'2023-04-14 00:00:00','USA',2,'test',NULL,3,2),
	 (4,'2023-03-13 00:00:00','Colombia',5,'OTRA REVIEW',NULL,3,3),
	 (5,'2023-04-27 23:47:46','Mexico',4,'Prueba review desde front echo dot alexa',NULL,3,1),
	 (2,'2023-03-13 00:00:00','Mexico',3,'test review',NULL,3,4);
INSERT INTO wishlist (id_user,id_product) VALUES
	 (1,2),
	 (1,7);
