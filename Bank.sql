-- Drop the existing Transferencia table if it exists
DROP TABLE IF EXISTS Transferencia;

-- Drop the existing Cliente table if it exists
DROP TABLE IF EXISTS Cliente;

-- Create the Cliente table
CREATE TABLE Cliente (
    NumeroConta INTEGER PRIMARY KEY NOT NULL,
    cpf NVARCHAR(11) NOT NULL,
    Nome NVARCHAR(255) NOT NULL,
    Endereco NVARCHAR(255) NOT NULL,
    CartaoEnviado INTEGER NOT NULL,
    CodigoRastreio NVARCHAR(8) -- Updated data type and length
);

-- Insert sample data into the Cliente table
INSERT INTO Cliente (NumeroConta, cpf, Nome, Endereco, CartaoEnviado, CodigoRastreio) 
VALUES
    (1, '48142742039', 'Daniel', 'Rua das Flores, 123, Itajubá, Minas Gerais', 1, 'H7E9K2D4'),
    (2, '98884236061', 'Matheus', 'Avenida Principal, 456, Itajubá, Minas Gerais', 0, NULL),
    (3, '20358962072', 'Ryan', 'Rua da Praça, 789, Itajubá, Minas Gerais', 1, 'P2R6T5Q8'),
    (4, '20071006060', 'Gabriela', 'Rua dos Sonhos, 567, Itajubá, Minas Gerais', 0, NULL),
    (5, '98577323056', 'Amanda', 'Avenida das Estrelas, 789, Itajubá, Minas Gerais', 1, 'A3B8F1G7');


-- Create the Transferencia table
CREATE TABLE Transferencia (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    NumeroContaOrigem INTEGER NOT NULL,
    NumeroContaDestino INTEGER NOT NULL,
    Valor NUMERIC NOT NULL,
    DataTransferencia DATETIME NOT NULL,
    FOREIGN KEY (NumeroContaOrigem) REFERENCES Cliente (NumeroConta),
    FOREIGN KEY (NumeroContaDestino) REFERENCES Cliente (NumeroConta)
);

-- Insert sample transfer data into the Transferencia table with date and time
INSERT INTO Transferencia (NumeroContaOrigem, NumeroContaDestino, Valor, DataTransferencia)
VALUES
    (1, 2, 1000.00, DATETIME('now', '-2 days')),
    (3, 4, 500.00, DATETIME('now', '-1 day')),
    (4, 2, 700.00, DATETIME('now', '-1 hour')),
    (5, 3, 300.00, DATETIME('now', '-3 hours')),
    (2, 1, 200.00, DATETIME('now', '-4 hours')),
    (1, 3, 1500.00, DATETIME('now', '-5 hours'));

-- Display the updated Cliente records
SELECT * FROM Cliente;
