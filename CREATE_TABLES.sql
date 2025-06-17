CREATE TABLE `cidades` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(255) DEFAULT NULL,
  `uf` char(2) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `clientes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(255) DEFAULT NULL,
  `cpf` char(11) DEFAULT NULL,
  `cidade_id` int DEFAULT NULL,
  `telefone` varchar(13) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `cidade_id` (`cidade_id`),
  CONSTRAINT `clientes_ibfk_1` FOREIGN KEY (`cidade_id`) REFERENCES `cidades` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `ordem_servico` (
  `id` int NOT NULL AUTO_INCREMENT,
  `cliente_id` int DEFAULT NULL,
  `data_cadastro` timestamp NULL DEFAULT NULL,
  `modelo` varchar(100) DEFAULT NULL,
  `descricao` varchar(1000) DEFAULT NULL,
  `observacao` blob,
  `ano` char(4) DEFAULT NULL,
  `valor_total` decimal(12,2) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `cliente_id` (`cliente_id`),
  CONSTRAINT `ordem_servico_ibfk_1` FOREIGN KEY (`cliente_id`) REFERENCES `clientes` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20250003 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `ordem_servico_produtos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `osv_id` int DEFAULT NULL,
  `produto_id` int DEFAULT NULL,
  `quantidade` int DEFAULT NULL,
  `valor_unitario` decimal(12,2) DEFAULT NULL,
  `sequencial` int DEFAULT NULL,
  `valor_total` decimal(12,2) DEFAULT NULL,
  `ano` char(4) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `osv_id` (`osv_id`),
  KEY `produto_id` (`produto_id`),
  CONSTRAINT `ordem_servico_produtos_ibfk_1` FOREIGN KEY (`osv_id`) REFERENCES `ordem_servico` (`id`),
  CONSTRAINT `ordem_servico_produtos_ibfk_2` FOREIGN KEY (`produto_id`) REFERENCES `produtos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=56 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `ordem_servico_servicos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `osv_id` int DEFAULT NULL,
  `servico_id` int DEFAULT NULL,
  `quantidade` int DEFAULT NULL,
  `valor_unitario` decimal(12,2) DEFAULT NULL,
  `sequencial` int DEFAULT NULL,
  `valor_total` decimal(12,2) DEFAULT NULL,
  `ano` char(4) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `osv_id` (`osv_id`),
  KEY `servico_id` (`servico_id`),
  CONSTRAINT `ordem_servico_servicos_ibfk_1` FOREIGN KEY (`osv_id`) REFERENCES `ordem_servico` (`id`),
  CONSTRAINT `ordem_servico_servicos_ibfk_2` FOREIGN KEY (`servico_id`) REFERENCES `produtos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `produtos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(1000) DEFAULT NULL,
  `custo_compra` decimal(12,2) DEFAULT NULL,
  `valor_venda` decimal(12,2) DEFAULT NULL,
  `quantidade_estoque` int DEFAULT NULL,
  `fl_servico` tinyint(1) NOT NULL DEFAULT '0',
  `FL_INATIVO` int DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `usuarios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `usuario` varchar(50) NOT NULL,
  `senha` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `usuario` (`usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO usuarios (usuario, senha)
VALUES ('admin', SHA2('123', 256));



